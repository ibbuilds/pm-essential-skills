"""Decision tests using synthetic observations; no live chats or model calls."""

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/context-management/scripts/assess_context.py"
SPEC = importlib.util.spec_from_file_location("context_policy", SCRIPT)
POLICY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(POLICY)


def context(used=85000, fresh=True, **overrides):
    values = dict(kind="current_context", used_tokens=used, window_tokens=100000,
                  source="synthetic test observation", fresh=fresh)
    values.update(overrides)
    return values


class RoutingTests(unittest.TestCase):
    def test_unknown_context_does_not_force_a_transfer(self):
        result = POLICY.assess({})
        self.assertEqual(result["action"], "continue")
        self.assertIsNone(result["context_ratio"])
        self.assertEqual(result["measurement"], "unavailable")

    def test_boundaries(self):
        for used, expected in [(0, "continue"), (74999, "continue"), (75000, "review"),
                               (84999, "review"), (85000, "rollover"), (100000, "rollover")]:
            with self.subTest(used=used):
                self.assertEqual(POLICY.assess({"context": context(used),
                                               "safe_checkpoint": True})["action"], expected)

    def test_unsafe_and_unknown_checkpoints_defer(self):
        for extra in [{}, {"safe_checkpoint": False}]:
            with self.subTest(extra=extra):
                result = POLICY.assess({"context": context(), **extra})
                self.assertEqual(result["action"], "defer")
                self.assertTrue(result["requires_transfer_checks"])

    def test_completed_work_does_not_spawn_empty_successor(self):
        self.assertEqual(POLICY.assess({"completed": True, "context": context()})["action"],
                         "complete")

    def test_distinct_requested_outcome_at_safe_boundary(self):
        result = POLICY.assess({"completed": True, "new_outcome": True,
                                "safe_checkpoint": True})
        self.assertEqual(result["action"], "rollover")
        self.assertEqual(result["reason"], "distinct_requested_outcome")

    def test_new_outcome_does_not_interrupt_unsafe_work(self):
        self.assertEqual(POLICY.assess({"new_outcome": True})["action"], "defer")

    def test_user_preference_overrides_pressure_and_new_outcome(self):
        result = POLICY.assess({"user_keep_thread": True, "new_outcome": True,
                                "safe_checkpoint": True, "context": context()})
        self.assertEqual(result["action"], "continue")
        self.assertEqual(result["reason"], "user_prefers_current_thread")

    def test_counters_alone_only_request_review(self):
        for field, value in [("substantive_turns", 20), ("large_outputs", 6), ("compactions", 2)]:
            with self.subTest(field=field):
                self.assertEqual(POLICY.assess({field: value, "safe_checkpoint": True})["action"],
                                 "review")
                self.assertEqual(POLICY.assess({field: value - 1})["action"], "continue")

    def test_proxy_and_concrete_evidence_can_prepare_transfer(self):
        result = POLICY.assess({"large_outputs": 6, "safe_checkpoint": True,
                                "obsolete_context_evidence": [
                                    "Earlier campaign plan superseded by approved brief",
                                    "Logs from a resolved source import issue"]})
        self.assertEqual(result["action"], "rollover")
        self.assertEqual(result["measurement"], "heuristic")

    def test_duplicate_evidence_is_not_two_signals(self):
        result = POLICY.assess({"substantive_turns": 30, "safe_checkpoint": True,
                                "obsolete_context_evidence": ["Old plan", " OLD   PLAN "]})
        self.assertEqual(result["action"], "review")
        self.assertEqual(result["obsolete_evidence_count"], 1)

    def test_fresh_low_context_overrides_historical_proxy_counts(self):
        result = POLICY.assess({"context": context(10000), "compactions": 5,
                                "obsolete_context_evidence": ["Resolved logs", "Replaced plan"],
                                "safe_checkpoint": True})
        self.assertEqual(result["action"], "continue")
        self.assertEqual(result["measurement"], "measured")

    def test_stale_telemetry_is_ignored(self):
        result = POLICY.assess({"context": context(99000, fresh=False), "safe_checkpoint": True})
        self.assertEqual(result["action"], "continue")
        self.assertIsNone(result["context_ratio"])

    def test_stale_telemetry_allows_proxy_fallback(self):
        result = POLICY.assess({"context": context(1000, fresh=False), "large_outputs": 6})
        self.assertEqual(result["action"], "review")
        self.assertEqual(result["measurement"], "heuristic")

    def test_null_unknown_counters_are_supported(self):
        result = POLICY.assess({"context": None, "substantive_turns": None,
                                "large_outputs": None, "compactions": None})
        self.assertEqual(result["measurement"], "unavailable")

    def test_assessment_does_not_mutate_observations(self):
        observation = {"context": context(), "safe_checkpoint": True}
        before = json.dumps(observation, sort_keys=True)
        POLICY.assess(observation)
        self.assertEqual(json.dumps(observation, sort_keys=True), before)

    def test_pressure_is_monotonic_for_same_outcome_at_safe_checkpoint(self):
        rank = {"continue": 0, "review": 1, "rollover": 2}
        previous = -1
        for used in range(0, 100001, 1000):
            result = POLICY.assess({"context": context(used), "safe_checkpoint": True})
            self.assertGreaterEqual(rank[result["action"]], previous)
            previous = rank[result["action"]]

    def test_user_stays_for_all_measured_pressures(self):
        for used in range(0, 100001, 1000):
            result = POLICY.assess({"context": context(used), "safe_checkpoint": True,
                                    "user_keep_thread": True})
            self.assertEqual(result["action"], "continue")
            self.assertFalse(result["requires_transfer_checks"])

    def test_no_rollover_without_safe_checkpoint_across_signal_types(self):
        scenarios = [{"new_outcome": True}, {"context": context()},
                     {"large_outputs": 6, "obsolete_context_evidence": ["Old plan", "Resolved logs"]}]
        for observation in scenarios:
            with self.subTest(observation=observation):
                self.assertEqual(POLICY.assess(observation)["action"], "defer")


class ValidationTests(unittest.TestCase):
    def test_invalid_observations_fail_instead_of_becoming_rollovers(self):
        invalid = [[], {"weekly_limit": 95}, {"safe_checkpoint": "true"},
                   {"completed": None}, {"compactions": True}, {"large_outputs": -1},
                   {"substantive_turns": 2.5}, {"obsolete_context_evidence": "old logs"},
                   {"obsolete_context_evidence": [""]},
                   {"context": context(kind="cumulative_usage")},
                   {"context": context(window_tokens=0)},
                   {"context": context(used_tokens=100001)},
                   {"context": context(used_tokens=True)},
                   {"context": context(source=" ")}, {"context": context(fresh="yes")},
                   {"context": context(extra="unsupported")}, {"context": {}},
                   {"project_mode": "folder"}, {"project_mode": []},
                   {"project_mode": None}, {"project_offer_dismissed": "no"},
                   {"admission_check": "yes"}, {"last_notice_level": []},
                   {"last_notice_level": "warning"}]
        for observation in invalid:
            with self.subTest(observation=observation):
                with self.assertRaises(ValueError):
                    POLICY.assess(observation)


class ExistingChatTests(unittest.TestCase):
    def test_existing_project_chat_is_assessed_without_future_turns(self):
        result = POLICY.assess({"project_mode": "project", "admission_check": True,
                                "context": context(90000), "safe_checkpoint": True})
        self.assertEqual(result["action"], "rollover")
        self.assertEqual(result["notice"], "rollover")

    def test_unknown_old_counts_with_concrete_evidence_trigger_review(self):
        result = POLICY.assess({"project_mode": "project", "admission_check": True,
                                "safe_checkpoint": True, "obsolete_context_evidence": [
                                    "Superseded launch plan", "Output from resolved import issue"]})
        self.assertEqual(result["action"], "review")
        self.assertEqual(result["reason"], "existing_history_review")
        self.assertEqual(result["measurement"], "heuristic")
        self.assertIsNone(result["context_ratio"])
        self.assertEqual(result["notice"], "review")

    def test_unsubstantiated_first_use_does_not_invent_pressure(self):
        result = POLICY.assess({"admission_check": True, "safe_checkpoint": True})
        self.assertEqual(result["action"], "continue")
        self.assertEqual(result["notice"], "none")

    def test_low_fresh_occupancy_overrides_catchup_evidence(self):
        result = POLICY.assess({"admission_check": True, "safe_checkpoint": True,
                                "context": context(10000), "obsolete_context_evidence": [
                                    "Replaced draft", "Resolved investigation logs"]})
        self.assertEqual(result["action"], "continue")
        self.assertEqual(result["notice"], "none")

    def test_notice_deduplication_does_not_cancel_transfer_decision(self):
        result = POLICY.assess({"context": context(), "safe_checkpoint": True,
                                "last_notice_level": "rollover"})
        self.assertEqual(result["action"], "rollover")
        self.assertEqual(result["notice"], "none")

    def test_pressure_escalation_can_notify_once(self):
        observation = {"context": context(), "safe_checkpoint": True,
                       "last_notice_level": "review"}
        self.assertEqual(POLICY.assess(observation)["notice"], "rollover")
        observation["last_notice_level"] = "rollover"
        self.assertEqual(POLICY.assess(observation)["notice"], "none")

    def test_no_notice_for_unsafe_or_user_overridden_pressure(self):
        for extra in [{"safe_checkpoint": False},
                      {"safe_checkpoint": True, "user_keep_thread": True},
                      {"safe_checkpoint": True, "completed": True}]:
            with self.subTest(extra=extra):
                self.assertEqual(POLICY.assess({"context": context(), **extra})["notice"], "none")

    def test_task_boundary_is_not_mislabeled_as_context_warning(self):
        result = POLICY.assess({"new_outcome": True, "safe_checkpoint": True})
        self.assertEqual(result["action"], "rollover")
        self.assertEqual(result["notice"], "none")

    def test_standalone_catchup_uses_one_project_offer(self):
        result = POLICY.assess({"project_mode": "standalone", "admission_check": True,
                                "safe_checkpoint": True, "obsolete_context_evidence": [
                                    "Replaced draft", "Resolved investigation logs"]})
        self.assertEqual(result["action"], "offer_project")
        self.assertEqual(result["notice"], "none")


class StandaloneTests(unittest.TestCase):
    def test_standalone_pressure_offers_instead_of_creating_or_rolling_over(self):
        result = POLICY.assess({"project_mode": "standalone", "context": context(),
                                "safe_checkpoint": True})
        self.assertEqual(result["action"], "offer_project")
        self.assertFalse(result["requires_transfer_checks"])

    def test_standalone_review_threshold_can_offer_organization(self):
        result = POLICY.assess({"project_mode": "standalone", "context": context(75000),
                                "safe_checkpoint": True})
        self.assertEqual(result["action"], "offer_project")

    def test_standalone_proxy_signal_is_honestly_labeled(self):
        result = POLICY.assess({"project_mode": "standalone", "substantive_turns": 20,
                                "safe_checkpoint": True})
        self.assertEqual(result["action"], "offer_project")
        self.assertEqual(result["measurement"], "heuristic")

    def test_dismissal_does_not_keep_prompting_or_disable_context_review(self):
        result = POLICY.assess({"project_mode": "standalone", "context": context(),
                                "safe_checkpoint": True, "project_offer_dismissed": True})
        self.assertEqual(result["action"], "review")
        self.assertEqual(result["reason"], "standalone_offer_dismissed")

    def test_standalone_offer_waits_for_safe_checkpoint(self):
        result = POLICY.assess({"project_mode": "standalone", "context": context()})
        self.assertEqual(result["action"], "defer")

    def test_no_offer_for_small_finished_or_user_overridden_chat(self):
        cases = [{"context": context(10000)}, {"completed": True, "context": context()},
                 {"user_keep_thread": True, "context": context()}]
        for extra in cases:
            with self.subTest(extra=extra):
                result = POLICY.assess({"project_mode": "standalone", "safe_checkpoint": True,
                                        **extra})
                self.assertNotEqual(result["action"], "offer_project")

    def test_unknown_membership_is_not_assumed_standalone(self):
        for mode in ["unknown", "project"]:
            with self.subTest(mode=mode):
                result = POLICY.assess({"project_mode": mode, "safe_checkpoint": True,
                                        "context": context()})
                self.assertEqual(result["action"], "rollover")
                self.assertTrue(result["requires_transfer_checks"])

    def test_successful_compaction_does_not_provoke_a_project_offer(self):
        result = POLICY.assess({"project_mode": "standalone", "context": context(10000),
                                "safe_checkpoint": True, "substantive_turns": 40, "compactions": 3})
        self.assertEqual(result["action"], "continue")


class CliTests(unittest.TestCase):
    def test_file_fixture(self):
        run = subprocess.run([sys.executable, str(SCRIPT), "--input",
                              str(ROOT / "tests/fixtures/high-context.json")],
                             capture_output=True, text=True, check=False)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)["action"], "rollover")

    def test_stdin(self):
        run = subprocess.run([sys.executable, str(SCRIPT)], input='{"completed":true}',
                             capture_output=True, text=True, check=False)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)["action"], "complete")

    def test_malformed_input_has_nonzero_exit_and_no_candidate(self):
        run = subprocess.run([sys.executable, str(SCRIPT)], input="{broken",
                             capture_output=True, text=True, check=False)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(run.stdout, "")
        self.assertIn("error", json.loads(run.stderr))

    def test_duplicate_fields_are_rejected(self):
        for raw in ['{"safe_checkpoint":false,"safe_checkpoint":true}',
                    '{"context":{"kind":"current_context","kind":"cumulative_usage"}}']:
            with self.subTest(raw=raw):
                run = subprocess.run([sys.executable, str(SCRIPT)], input=raw,
                                     capture_output=True, text=True, check=False)
                self.assertEqual(run.returncode, 2)
                self.assertEqual(run.stdout, "")
                self.assertIn("Duplicate JSON field", json.loads(run.stderr)["error"])

    def test_pretty_and_compact_formats_have_identical_decisions(self):
        values = []
        for args in [[], ["--pretty"]]:
            run = subprocess.run([sys.executable, str(SCRIPT), *args], input='{"completed":true}',
                                 capture_output=True, text=True, check=False)
            self.assertEqual(run.returncode, 0, run.stderr)
            values.append(json.loads(run.stdout))
            if not args:
                self.assertEqual(len(run.stdout.splitlines()), 1)
        self.assertEqual(*values)


if __name__ == "__main__":
    unittest.main()
