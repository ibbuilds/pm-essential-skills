"""Synthetic policy and read/usage scenarios; no measured live savings claims."""

from contextlib import redirect_stderr
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


READ = load("read_source", "skills/pm-essential-skills-source-selection/scripts/read_source.py")
POLICY = load("cost_policy", "skills/pm-essential-skills-context-management/scripts/assess_context.py")
USAGE = load("evaluate_usage", "scripts/evaluate_usage.py")


class BoundedReaderTests(unittest.TestCase):
    def setUp(self):
        work = ROOT / "work"
        work.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=work)
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "source.txt"
        self.path.write_text("First line\nSecond line\nThird line\n", encoding="utf-8", newline="")

    def read(self, **extra):
        return READ.read_source({"path": str(self.path), **extra})

    def known(self, result):
        return {"loaded_source_id": result["source_id"], "loaded_revision": result["revision"],
                "loaded_spans": result["coverage_spans"], "content_available": True}

    def test_directory_is_not_a_regular_source(self):
        with self.assertRaisesRegex(ValueError, "requires a regular file"):
            READ.read_source({"path": str(self.path.parent)})

    @unittest.skipUnless(hasattr(os, "mkfifo"), "POSIX named pipe")
    def test_named_pipe_is_rejected_without_waiting_for_a_writer(self):
        pipe = self.path.parent / "source.pipe"
        os.mkfifo(pipe)
        result = subprocess.run([sys.executable, str(Path(READ.__file__))],
                                input=json.dumps({"path": str(pipe)}), text=True,
                                capture_output=True, timeout=3)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("requires a regular file", result.stderr)

    def test_path_resolution_runtime_errors_use_cli_error_envelope(self):
        for operation, diagnostic in (("expanduser", "Could not determine home directory."),
                                      ("resolve", "Symlink loop from fixture source")):
            with self.subTest(operation=operation):
                stderr = io.StringIO()
                with mock.patch.object(Path, operation, side_effect=RuntimeError(diagnostic)), \
                     mock.patch.object(sys, "argv", ["read_source.py"]), \
                     mock.patch.object(sys, "stdin", io.StringIO(json.dumps({"path": str(self.path)}))), \
                     redirect_stderr(stderr):
                    self.assertEqual(READ.main(), 2)
                self.assertEqual(json.loads(stderr.getvalue()), {"error": diagnostic})
        self.assertEqual(self.read()["action"], "read")

    def test_symlink_loop_errors_but_regular_alias_reads_canonical_source(self):
        alias = self.path.parent / "alias.txt"
        loop = self.path.parent / "loop.txt"
        try:
            alias.symlink_to(self.path.name)
            loop.symlink_to(loop.name)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"Symlink creation unavailable: {exc}")
        for path, code in ((loop, 2), (alias, 0), (self.path.parent / "missing.txt", 2)):
            with self.subTest(path=path):
                result = subprocess.run([sys.executable, str(Path(READ.__file__))],
                                        input=json.dumps({"path": str(path)}), text=True,
                                        capture_output=True, timeout=3)
                self.assertEqual(result.returncode, code)
                if code:
                    self.assertEqual(result.stdout, "")
                    self.assertIn("error", json.loads(result.stderr))
                    self.assertNotIn("Traceback", result.stderr)
                else:
                    value = json.loads(result.stdout)
                    self.assertEqual(value["source_id"], self.path.resolve().as_uri())
                    self.assertEqual(value["content"][0]["text"], self.path.read_text())

    def test_unchanged_available_source_returns_no_duplicate_content(self):
        first = self.read()
        second = self.read(**self.known(first))
        self.assertEqual(second["action"], "reuse")
        self.assertEqual(second["content"], [])
        self.assertTrue(second["full_read_complete"])

    def test_overlap_reads_only_missing_task_coverage(self):
        first = self.read(start_line=1, end_line=2)
        second = self.read(start_line=2, end_line=3, **self.known(first))
        self.assertEqual("".join(item["text"] for item in second["content"]), "Third line\n")
        self.assertTrue(second["coverage_sufficient"])

    def test_changed_source_invalidates_available_old_content(self):
        first = self.read()
        self.path.write_text("Updated source\n", encoding="utf-8", newline="")
        second = self.read(**self.known(first))
        self.assertNotEqual(first["revision"], second["revision"])
        self.assertEqual(second["action"], "read")
        self.assertEqual(second["content"][0]["text"], "Updated source\n")

    def test_cursor_requires_revision_and_cannot_skip_unread_content(self):
        for extra in ({"cursor": 1}, {"cursor": 1, "expected_revision": self.read()["revision"]}):
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                self.read(**extra)

    def test_full_read_paginates_long_lines_without_losing_characters(self):
        text = "A" * 31 + "é\n" + "Z" * 20
        self.path.write_text(text, encoding="utf-8", newline="")
        options = {"max_chars": 7, "required_full_read": True, "start_line": 2, "end_line": 2}
        chunks = []
        for _ in range(20):
            result = self.read(**options)
            pieces = result["content"]
            self.assertLessEqual(sum(len(item["text"]) for item in pieces), 7)
            chunks.extend(item["text"] for item in pieces)
            if result["coverage_sufficient"]:
                break
            self.assertFalse(result["full_read_complete"])
            options.update(self.known(result), cursor=result["next_cursor"], expected_revision=result["revision"])
        self.assertEqual("".join(chunks), text)
        self.assertTrue(result["full_read_complete"])

    def test_pagination_source_change_requires_restart(self):
        first = self.read(max_chars=5)
        self.path.write_text("Different\n", encoding="utf-8")
        result = self.read(cursor=first["next_cursor"], expected_revision=first["revision"])
        self.assertEqual(result["action"], "restart")
        self.assertFalse(result["full_read_complete"])
        self.assertEqual(result["content"], [])

    def test_explicit_reread_and_lost_context_prevent_reuse(self):
        first = self.read()
        for extra in ({"force_read": True}, {"content_available": False}, {"loaded_source_id": "another-source"}):
            with self.subTest(extra=extra):
                self.assertEqual(self.read(**(self.known(first) | extra))["action"], "read")

    def test_forced_full_reread_does_not_claim_completion_from_old_coverage(self):
        first = self.read()
        options = self.known(first) | {"required_full_read": True, "force_read": True, "max_chars": 5}
        reread = []
        for _ in range(20):
            result = self.read(**options)
            reread.extend(item["text"] for item in result["content"])
            if result["coverage_sufficient"]:
                break
            self.assertFalse(result["full_read_complete"])
            options.update(self.known(result), cursor=result["next_cursor"], expected_revision=result["revision"],
                           reread_spans=result["reread_spans"])
        self.assertEqual("".join(reread), self.path.read_text(encoding="utf-8"))
        self.assertTrue(result["full_read_complete"])

    def test_forced_cursor_cannot_use_old_coverage_or_skip_unread_prefix(self):
        first = self.read()
        for cursor in (1, first["total_chars"]):
            for available in (True, False):
                with self.subTest(cursor=cursor, available=available), self.assertRaises(ValueError):
                    self.read(**(self.known(first) | {
                        "required_full_read": True, "force_read": True,
                        "cursor": cursor, "expected_revision": first["revision"],
                        "content_available": available}))

    def test_forced_pass_coverage_is_distinct_from_old_full_coverage(self):
        old = self.read()
        first = self.read(**self.known(old), force_read=True, max_chars=5)
        self.assertEqual(first["coverage_spans"], old["coverage_spans"])
        self.assertEqual(first["reread_spans"], [[0, 5]])
        self.assertFalse(first["coverage_sufficient"])
        with self.assertRaises(ValueError):
            self.read(**self.known(first), force_read=True, cursor=first["total_chars"],
                      expected_revision=first["revision"], reread_spans=first["reread_spans"])
        with self.assertRaises(ValueError):
            self.read(**(self.known(first) | {"content_available": False}), force_read=True,
                      cursor=5, expected_revision=first["revision"], reread_spans=first["reread_spans"])

    def test_reread_spans_are_validated_and_reset_for_new_pass(self):
        old = self.read()
        for spans in (None, [[-1, 3]], [[0, True]], [[0, old["total_chars"] + 1]]):
            with self.subTest(spans=spans), self.assertRaises(ValueError):
                self.read(**self.known(old), force_read=True, reread_spans=spans)
        result = self.read(**self.known(old), force_read=True, max_chars=5,
                           reread_spans=old["coverage_spans"])
        self.assertEqual(result["reread_spans"], [[0, 5]])
        self.assertFalse(result["full_read_complete"])

    def test_line_navigation_uses_physical_lf_lines_and_preserves_offsets(self):
        for separator in ("\n", "\r\n"):
            for embedded in ("\u2028", "\f", "\r"):
                with self.subTest(separator=separator, embedded=embedded):
                    prefix = 'x = "first' + embedded + 'still first"' + separator
                    suffix = "print(x)" + separator
                    self.path.write_bytes((prefix + suffix).encode("utf-8"))
                    result = self.read(start_line=2, end_line=2)
                    self.assertEqual(result["total_lines"], 2)
                    self.assertEqual(result["content"], [{"start": len(prefix),
                                     "end": len(prefix + suffix), "text": suffix}])
                    full = self.read()
                    self.assertEqual(full["content"][0]["text"], prefix + suffix)
                    self.assertEqual(result["revision"], full["revision"])

    def test_empty_source_is_a_complete_read(self):
        self.path.write_text("", encoding="utf-8")
        result = self.read()
        self.assertEqual(result["action"], "read")
        self.assertTrue(result["full_read_complete"])

    def test_reader_writes_no_state_and_rejects_binary_or_invalid_requests(self):
        before = list(self.path.parent.iterdir())
        self.read()
        self.assertEqual(list(self.path.parent.iterdir()), before)
        for extra in ({"max_chars": True}, {"max_chars": 0}, {"max_chars": 100001},
                      {"start_line": 9}, {"loaded_spans": [[1, -1]]}, {"unexpected": True}):
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                self.read(**extra)
        self.path.write_bytes(b"\0binary")
        with self.assertRaises(ValueError):
            self.read()

    def test_reader_cli_keeps_metadata_and_returns_only_requested_lines(self):
        result = subprocess.run([sys.executable, str(ROOT / "skills/pm-essential-skills-source-selection/scripts/read_source.py")],
                                input=json.dumps({"path": str(self.path), "start_line": 2, "end_line": 2}),
                                text=True, capture_output=True, check=True)
        parsed = json.loads(result.stdout)
        self.assertEqual(parsed["content"][0]["text"], "Second line\n")
        self.assertFalse(parsed["full_read_complete"])


class TransferCostTests(unittest.TestCase):
    def setUp(self):
        self.observation = {"new_outcome": True, "safe_checkpoint": True}
        self.cost = {"basis": "estimated", "source": "Synthetic remaining-work comparison",
                     "unit": "tokens", "scope": "remaining_requested_work", "fresh": True,
                     "continue": 100, "handoff": 40, "startup": 40, "reconstruction": 40}

    def test_expensive_transfer_stays_without_notice_or_extra_checks(self):
        result = POLICY.assess(self.observation | {"transfer_cost": self.cost})
        self.assertEqual(result["action"], "continue")
        self.assertEqual(result["notice"], "none")
        self.assertFalse(result["requires_transfer_checks"])
        self.assertEqual(result["transfer_cost"]["basis"], "estimated")

    def test_beneficial_or_unknown_cost_does_not_block_normal_gates(self):
        for cost in (None, self.cost | {"reconstruction": 0}, self.cost | {"fresh": False}):
            with self.subTest(cost=cost):
                result = POLICY.assess(self.observation | {"transfer_cost": cost})
                self.assertEqual(result["action"], "rollover")
                self.assertTrue(result["requires_transfer_checks"])

    def test_context_loss_and_repeated_investigation_avoid_automatic_transfer(self):
        self.assertEqual(POLICY.assess(self.observation | {"transfer_context_ready": False})["reason"],
                         "transfer_context_unavailable")
        result = POLICY.assess(self.observation | {"reconstruction_repeats_work": True})
        self.assertEqual(result["action"], "checkpoint")
        self.assertFalse(result["requires_transfer_checks"])

    def test_user_requested_thread_bypasses_cost_but_preserves_access_gate(self):
        value = self.observation | {"user_requested_new_thread": True, "transfer_cost": self.cost}
        self.assertEqual(POLICY.assess(value)["action"], "rollover")
        self.assertEqual(POLICY.assess(value | {"transfer_context_ready": False})["action"], "blocked_transfer")
        self.assertEqual(POLICY.assess(value | {"completed": True, "new_outcome": False})["action"], "rollover")
        self.assertEqual(POLICY.assess(value | {"safe_checkpoint": False})["action"], "defer")

    def test_incomparable_cost_is_rejected(self):
        for extra in ({"unit": "money"}, {"scope": "one_request_only"}, {"fresh": 1},
                      {"handoff": -1}, {"startup": True}, {"basis": "guess"}):
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                POLICY.assess(self.observation | {"transfer_cost": self.cost | extra})


class UsageEvaluationTests(unittest.TestCase):
    def record(self, task, variant, tokens):
        return {"task_id": task, "variant": variant, "conditions_id": "synthetic-matched-task",
                "model": "synthetic-model", "effort": "synthetic-effort",
                "quality": dict.fromkeys(USAGE.QUALITY, True),
                "usage": {"source": "Synthetic test export", "scope": "complete_task", "complete": True,
                          "requests": [{"request_id": f"{task}-{variant}-{index}", "total_tokens": total}
                                       for index, total in enumerate(tokens)]}}

    def pair(self):
        return [self.record("a", "baseline", [100, 100]), self.record("a", "suite", [70, 70])]

    def test_complete_task_counts_all_startup_retries_and_handoff_requests(self):
        runs = self.pair()
        runs[1]["usage"]["requests"].extend([
            {"request_id": "retry", "total_tokens": 50}, {"request_id": "handoff", "total_tokens": 30}])
        result = USAGE.compare({"runs": runs})
        self.assertEqual(result["total_token_delta"], 20)
        self.assertFalse(result["observed_improvement"])

    def test_smaller_complete_accepted_run_reports_observed_change(self):
        result = USAGE.compare({"runs": self.pair()})
        self.assertEqual(result["total_token_delta"], -60)
        self.assertTrue(result["observed_improvement"])

    def test_failed_or_unknown_quality_cannot_be_called_improvement(self):
        for quality in ({}, dict.fromkeys(USAGE.QUALITY, False)):
            runs = self.pair()
            runs[1]["quality"] = quality
            result = USAGE.compare({"runs": runs})
            self.assertFalse(result["all_quality_passed"])
            self.assertFalse(result["observed_improvement"])

    def test_missing_telemetry_stays_unknown(self):
        for usage in (None, {"source": "Synthetic", "scope": "complete_task", "complete": False, "requests": []}):
            runs = self.pair()
            runs[1]["usage"] = usage
            result = USAGE.compare({"runs": runs})
            self.assertIsNone(result["total_token_delta"])
            self.assertFalse(result["observed_improvement"])

    def test_unknown_request_total_is_not_silently_zero(self):
        runs = self.pair()
        runs[1]["usage"]["requests"][0]["total_tokens"] = None
        result = USAGE.compare({"runs": runs})
        self.assertFalse(result["all_pairs_measured"])
        self.assertIsNone(result["pairs"][0]["token_delta"])

    def test_different_conditions_are_not_compared(self):
        for field in ("model", "effort", "conditions_id"):
            runs = self.pair()
            runs[1][field] = "different"
            self.assertIsNone(USAGE.compare({"runs": runs})["total_token_delta"])

    def test_incomplete_pair_does_not_allow_cherry_picked_aggregate(self):
        runs = self.pair() + [self.record("b", "baseline", [10])]
        result = USAGE.compare({"runs": runs})
        self.assertIsNone(result["total_token_delta"])
        self.assertFalse(result["observed_improvement"])

    def test_unpaired_quality_preserves_failure_without_claiming_pair_success(self):
        for variant in ("baseline", "suite"):
            for flags, expected in (({"completed": False}, "failed"), ({}, "unknown"),
                                    (dict.fromkeys(USAGE.QUALITY, True), "unknown")):
                with self.subTest(variant=variant, quality=flags):
                    record = self.record("unpaired", variant, [10])
                    record["quality"] = flags
                    result = USAGE.compare({"runs": [record]})
                    self.assertEqual(result["pairs"][0]["status"], "unpaired")
                    self.assertEqual(result["pairs"][0]["quality"], expected)
                    self.assertFalse(result["all_quality_passed"])
                    self.assertFalse(result["observed_improvement"])
                    self.assertIsNone(result["total_token_delta"])

    def test_ratio_overflow_preserves_exact_totals_with_unknown_ratio(self):
        runs = [self.record("large", "baseline", [1]),
                self.record("large", "suite", [10 ** 400])]
        result = subprocess.run([sys.executable, str(ROOT / "scripts/evaluate_usage.py")],
                                input=json.dumps({"runs": runs}), text=True,
                                capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        for report in (json.loads(result.stdout), USAGE.compare({"runs": runs})):
            self.assertTrue(report["all_pairs_measured"])
            self.assertEqual(report["total_token_delta"], 10 ** 400 - 1)
            self.assertIsNone(report["relative_token_change"])
            pair = report["pairs"][0]
            self.assertEqual(pair["baseline_tokens"], 1)
            self.assertEqual(pair["suite_tokens"], 10 ** 400)
            self.assertEqual(pair["token_delta"], 10 ** 400 - 1)
            self.assertIsNone(pair["relative_token_change"])
        # Large exact totals remain supported when their relative change is representable.
        runs[0]["usage"]["requests"][0]["total_tokens"] = 10 ** 400
        result = USAGE.compare({"runs": runs})
        self.assertEqual(result["total_token_delta"], 0)
        self.assertEqual(result["relative_token_change"], 0)
        self.assertFalse(result["observed_improvement"])

    def test_large_finite_ratio_and_nonzero_underflow(self):
        huge = 10 ** 400
        for delta, ratio in ((huge, 1.0), (-1, None), (1, None), (0, 0.0)):
            with self.subTest(delta_sign=(delta > 0) - (delta < 0), ratio=ratio):
                runs = [self.record("large", "baseline", [huge]),
                        self.record("large", "suite", [huge + delta])]
                result = USAGE.compare({"runs": runs})
                self.assertEqual(result["total_token_delta"], delta)
                self.assertEqual(result["pairs"][0]["token_delta"], delta)
                for report in (result, result["pairs"][0]):
                    if ratio is None:
                        self.assertIsNone(report["relative_token_change"])
                    else:
                        self.assertEqual(report["relative_token_change"], ratio)
                self.assertEqual(result["observed_improvement"], delta < 0)

    def test_summed_integer_serialization_failure_is_structured(self):
        limit = getattr(sys, "get_int_max_str_digits", lambda: 0)()
        if not limit:
            self.skipTest("Interpreter integer-string conversion limit disabled")
        largest = int("9" * limit)
        runs = [self.record("large", variant, [largest, largest])
                for variant in ("baseline", "suite")]
        report = USAGE.compare({"runs": runs})
        self.assertEqual(report["pairs"][0]["baseline_tokens"], 2 * largest)
        self.assertEqual(report["total_token_delta"], 0)
        result = subprocess.run([sys.executable, str(ROOT / "scripts/evaluate_usage.py")],
                                input=json.dumps({"runs": runs}), text=True,
                                capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        error = json.loads(result.stderr)
        self.assertEqual(set(error), {"error"})
        self.assertTrue(error["error"])
        self.assertNotIn("Traceback", result.stderr)

    def test_duplicate_requests_and_token_subtotals_are_rejected(self):
        runs = self.pair()
        runs[1]["usage"]["requests"][0]["request_id"] = runs[0]["usage"]["requests"][0]["request_id"]
        with self.assertRaises(ValueError):
            USAGE.compare({"runs": runs})
        runs = self.pair()
        runs[0]["usage"]["requests"][0]["reasoning_tokens"] = 50
        with self.assertRaises(ValueError):
            USAGE.compare({"runs": runs})

    def test_observable_counts_remain_useful_without_token_telemetry(self):
        runs = self.pair()
        for record in runs:
            record["usage"] = None
        runs[0]["observations"] = {"repeated_reads": 3}
        runs[1]["observations"] = {"repeated_reads": 1}
        result = USAGE.compare({"runs": runs})
        self.assertEqual(result["pairs"][0]["observation_deltas"]["repeated_reads"], -2)
        self.assertIsNone(result["total_token_delta"])

    def test_cli_accepts_supplied_exports_without_writing_logs(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/evaluate_usage.py")],
                                input=json.dumps({"runs": self.pair()}), text=True,
                                capture_output=True, check=True)
        self.assertEqual(json.loads(result.stdout)["total_token_delta"], -60)


if __name__ == "__main__":
    unittest.main()
