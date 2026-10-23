"""Transfer storage, capability, and source-reuse tests. No live accounts or chats."""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


STATE = load("transfer_state", "skills/pm-essential-skills-context-management/scripts/transfer_state.py")
PREFLIGHT = load("preflight", "skills/pm-essential-skills-context-management/scripts/preflight.py")
SOURCE = load("assess_source", "skills/pm-essential-skills-source-selection/scripts/assess_source.py")


class TransferTests(unittest.TestCase):
    def setUp(self):
        work = (ROOT / "work").resolve()
        work.mkdir(exist_ok=True)
        self.directory = tempfile.TemporaryDirectory(dir=work)
        assert Path(self.directory.name).resolve().is_relative_to(work)
        self.addCleanup(self.directory.cleanup)
        root = Path(self.directory.name)
        self.path = root / "journal.json"
        self.brief = root / "brief.md"
        self.brief.write_text("Source thread: source-a\nConfirmed goal, constraints, evidence and next action.\n", encoding="utf-8")
        self.data = dict(handoff_id="task-001", project_id="project-a", source_thread_id="source-a",
                         brief_path=str(self.brief))
        self.gates = {key: True for key in STATE.GATES}
        self.confirmation = dict(destination_thread_id="destination-b", destination_ready=True,
                                 project_id="project-a", handoff_id="task-001")
        self.state = STATE.update(self.path, "prepare", self.data)

    def change(self, event, data=None):
        self.state = STATE.update(self.path, event, data or {}, self.state["revision"])
        return self.state

    def test_complete_transfer_preserves_one_writer(self):
        self.assertEqual(STATE.summary(self.state)["active_writer"], "source-a")
        self.change("request", self.gates)
        self.assertIsNone(STATE.summary(self.state)["active_writer"])
        self.change("confirm", self.confirmation)
        self.assertEqual(STATE.summary(self.state)["active_writer"], "destination-b")
        self.change("supersede", {"routing_saved": True})
        self.assertTrue(STATE.summary(self.state)["must_pause_source"])
        self.assertEqual(self.state["phase"], "superseded")

    def test_lost_response_recovers_existing_destination_without_second_create(self):
        self.change("request", self.gates)
        # Simulated host created a destination but its response was lost.
        host_destinations = {"task-001": "destination-b"}
        self.change("unknown")
        restored = STATE.update(self.path, "status", {})
        self.assertEqual(restored["phase"], "uncertain")
        with self.assertRaises(ValueError):
            self.change("request", self.gates)
        self.assertIsNone(STATE.summary(restored)["active_writer"])
        self.change("confirm", dict(self.confirmation, destination_thread_id=host_destinations["task-001"]))
        self.assertEqual(self.state["attempts"], 1)

    def test_stale_writer_cannot_overwrite_newer_state(self):
        old_revision = self.state["revision"]
        self.change("request", self.gates)
        with self.assertRaises(ValueError):
            STATE.update(self.path, "unknown", {}, old_revision)
        self.assertEqual(STATE.update(self.path, "status", {})["phase"], "requesting")

    def test_creation_requires_every_gate(self):
        for key in STATE.GATES:
            with self.subTest(key=key):
                with self.assertRaises(ValueError):
                    self.change("request", self.gates | {key: False})
        self.assertEqual(STATE.update(self.path, "status", {})["attempts"], 0)

    def test_unknown_fields_report_only_fixed_schema_without_mutating_state(self):
        original = self.path.read_bytes()
        snapshot = json.dumps(self.state, sort_keys=True)
        fields = {
            "request": STATE.GATES | {"failure_resolved"}, "unknown": set(),
            "failed": {"definite_failure"}, "absent": {"definitive_absence"},
            "confirm": {"destination_thread_id", "destination_ready", "project_id", "handoff_id"},
            "supersede": {"routing_saved"}, "cancel": set(),
        }
        hostile = "PRIVATE-KEY\n" + "x" * 10000
        for event, allowed in fields.items():
            expected = (f"Unknown event-data field. Allowed fields for {event}: "
                        + (", ".join(sorted(allowed)) or "(none; use an empty object)"))
            with self.subTest(event=event):
                for change in (lambda: STATE.transition(self.state, event, {hostile: "PRIVATE-VALUE"}),
                               lambda: STATE.update(self.path, event, {hostile: "PRIVATE-VALUE"}, 0)):
                    with self.assertRaises(ValueError) as error:
                        change()
                    self.assertEqual(str(error.exception), expected)
                    self.assertLess(len(str(error.exception)), 400)
                self.assertEqual(json.dumps(self.state, sort_keys=True), snapshot)
                self.assertEqual(self.path.read_bytes(), original)
                self.assertFalse(self.path.with_name(self.path.name + ".lock").exists())

    def test_unknown_events_report_only_fixed_supported_events(self):
        original = self.path.read_bytes()
        snapshot = json.dumps(self.state, sort_keys=True)
        hostile = "PRIVATE-EVENT\n" + "x" * 10000
        cases = (
            (lambda: STATE.transition(self.state, hostile, {}), "transition", STATE.EVENTS - {"prepare", "status"}),
            (lambda: STATE.update(self.path, hostile, {}, 0), "transfer", STATE.EVENTS),
        )
        for change, kind, events in cases:
            with self.subTest(kind=kind), self.assertRaises(ValueError) as error:
                change()
            self.assertEqual(str(error.exception),
                             f"Unknown {kind} event. Supported events: " + ", ".join(sorted(events)))
            self.assertLess(len(str(error.exception)), 200)
        self.assertEqual(json.dumps(self.state, sort_keys=True), snapshot)
        self.assertEqual(self.path.read_bytes(), original)
        self.assertFalse(self.path.with_name(self.path.name + ".lock").exists())

    def test_unknown_request_fields_cli_preserves_envelope_and_safe_correction(self):
        original = self.path.read_bytes()
        payload = self.gates | {"PRIVATE-KEY" + "x" * 10000: "PRIVATE-VALUE"}
        command = [sys.executable, str(Path(STATE.__file__)), "--state", str(self.path),
                   "--event", "request", "--expected-revision", "0"]
        run = subprocess.run(command, input=json.dumps(payload), text=True,
                             capture_output=True, timeout=3, check=False)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(run.stdout, "")
        self.assertEqual(json.loads(run.stderr), {"error":
                         "Unknown event-data field. Allowed fields for request: "
                         + ", ".join(sorted(STATE.GATES | {"failure_resolved"}))})
        self.assertLess(len(run.stderr), 450)
        self.assertEqual(self.path.read_bytes(), original)
        self.assertFalse(self.path.with_name(self.path.name + ".lock").exists())
        corrected = self.change("request", self.gates)
        self.assertEqual((corrected["phase"], corrected["revision"], corrected["attempts"]),
                         ("requesting", 1, 1))

    def test_brief_without_exact_source_reference_cannot_be_prepared(self):
        for content in ("Goal and next step only", "Source title only", "Source ID: source-aa"):
            with self.subTest(content=content):
                self.brief.write_text(content, encoding="utf-8")
                new_path = self.path.with_name("missing-source.json")
                with self.assertRaisesRegex(ValueError, "source_thread_id"):
                    STATE.update(new_path, "prepare", self.data)
                self.assertFalse(new_path.exists())

    def test_source_reference_without_recovery_gate_cannot_dispatch(self):
        gates = {key: value for key, value in self.gates.items() if key != "source_recovery_ready"}
        with self.assertRaises(ValueError):
            self.change("request", gates)
        unchanged = STATE.update(self.path, "status", {})
        self.assertEqual(unchanged["phase"], "prepared")
        self.assertEqual(unchanged["attempts"], 0)

    def test_brief_changes_block_dispatch(self):
        self.brief.write_text("Different constraints\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.change("request", self.gates)
        self.assertEqual(STATE.update(self.path, "status", {})["phase"], "prepared")

    @unittest.skipUnless(hasattr(os, "mkfifo"), "POSIX named pipes")
    def test_durable_fifo_inputs_fail_without_blocking_or_retaining_lock(self):
        original = self.path.read_bytes()
        original_brief = self.brief.read_bytes()
        for case in ("status_journal", "request_journal", "prepare_brief", "request_brief"):
            self.path.unlink(missing_ok=True)
            self.brief.unlink(missing_ok=True)
            self.path.write_bytes(original)
            self.brief.write_bytes(original_brief)
            target = self.path if case.endswith("journal") else self.brief
            target.unlink()
            os.mkfifo(target)
            event = case.split("_")[0]
            if event == "prepare":
                self.path.unlink()
            data = self.data if event == "prepare" else self.gates if event == "request" else {}
            command = [sys.executable, str(Path(STATE.__file__)), "--state", str(self.path),
                       "--event", event, "--expected-revision", "0"]
            with self.subTest(case=case):
                run = subprocess.run(command, input=json.dumps(data), text=True,
                                     capture_output=True, timeout=3, check=False)
                self.assertEqual(run.returncode, 2)
                self.assertEqual(run.stdout, "")
                self.assertIn("regular file", json.loads(run.stderr)["error"])
                self.assertFalse(self.path.with_name(self.path.name + ".lock").exists())
                if case == "request_brief":
                    self.assertEqual(self.path.read_bytes(), original)
                elif case == "prepare_brief":
                    self.assertFalse(self.path.exists())

    def test_symlinked_regular_brief_is_resolved_and_remains_usable(self):
        link = self.brief.with_name("brief-link.md")
        try:
            link.symlink_to(self.brief)
        except (OSError, NotImplementedError):
            self.skipTest("Symbolic links unavailable")
        journal = self.path.with_name("linked-brief-state.json")
        state = STATE.update(journal, "prepare", self.data | {"brief_path": str(link)})
        self.assertEqual(state["brief_path"], str(self.brief.resolve()))
        self.assertEqual(state["brief_sha256"], self.state["brief_sha256"])
        self.assertEqual(STATE.update(journal, "request", self.gates, 0)["phase"], "requesting")
        journal_link = self.path.with_name("journal-link.json")
        journal_link.symlink_to(journal)
        with self.assertRaisesRegex(ValueError, "symbolic link"):
            STATE.update(journal_link, "status", {})

    @unittest.skipUnless(Path("/dev/stdin").exists(), "stdin descriptor path unavailable")
    def test_event_input_path_can_still_read_a_pipe(self):
        run = subprocess.run([sys.executable, str(Path(STATE.__file__)),
                              "--state", str(self.path), "--event", "request",
                              "--expected-revision", "0", "--input", "/dev/stdin"],
                             input=json.dumps(self.gates), text=True, capture_output=True,
                             timeout=3, check=False)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)["phase"], "requesting")

    def test_uncertain_result_cannot_resume_source_or_retry_blindly(self):
        self.change("request", self.gates)
        self.change("unknown")
        for event, payload in [("cancel", {}), ("request", self.gates),
                               ("absent", {"definitive_absence": False})]:
            with self.subTest(event=event):
                with self.assertRaises(ValueError):
                    self.change(event, payload)

    def test_definite_failure_allows_one_resolved_retry_then_stops(self):
        self.change("request", self.gates)
        self.change("failed", {"definite_failure": True})
        self.assertEqual(STATE.summary(self.state)["active_writer"], "source-a")
        with self.assertRaises(ValueError):
            self.change("request", self.gates)
        self.change("request", self.gates | {"failure_resolved": True})
        self.change("failed", {"definite_failure": True})
        self.assertEqual(self.state["phase"], "failed")
        with self.assertRaises(ValueError):
            self.change("request", self.gates | {"failure_resolved": True})

    def test_confirmation_is_idempotent_and_cannot_redirect(self):
        self.change("request", self.gates)
        self.change("confirm", self.confirmation)
        revision = self.state["revision"]
        self.change("confirm", self.confirmation)
        self.assertEqual(self.state["revision"], revision)
        with self.assertRaises(ValueError):
            self.change("confirm", self.confirmation | {"destination_thread_id": "another"})

    def test_wrong_project_handoff_or_source_as_destination_is_rejected(self):
        self.change("request", self.gates)
        for override in [{"project_id": "other"}, {"handoff_id": "other"},
                         {"destination_thread_id": "source-a"}, {"destination_ready": False}]:
            with self.subTest(override=override):
                with self.assertRaises(ValueError):
                    self.change("confirm", self.confirmation | override)

    def test_bookkeeping_failure_cannot_restore_source_or_create_again(self):
        self.change("request", self.gates)
        self.change("confirm", self.confirmation)
        with self.assertRaises(ValueError):
            self.change("supersede", {"routing_saved": False})
        for event, data in [("cancel", {}), ("request", self.gates)]:
            with self.assertRaises(ValueError):
                self.change(event, data)
        self.assertEqual(STATE.summary(STATE.update(self.path, "status", {}))["active_writer"], "destination-b")

    def test_duplicate_preparation_does_not_overwrite_state(self):
        original = self.path.read_bytes()
        with self.assertRaises(ValueError):
            STATE.update(self.path, "prepare", self.data)
        self.assertEqual(self.path.read_bytes(), original)

    def test_existing_lock_fails_closed_and_is_preserved(self):
        lock = self.path.with_name(self.path.name + ".lock")
        lock.write_text("other writer", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            self.change("request", self.gates)
        self.assertEqual(lock.read_text(), "other writer")

    def test_invalid_or_corrupt_journal_is_not_silently_reset(self):
        self.path.write_text('{"phase":"confirmed"}', encoding="utf-8")
        with self.assertRaises(ValueError):
            STATE.update(self.path, "status", {})
        self.assertEqual(self.path.read_text(), '{"phase":"confirmed"}')

    def test_corrupt_attempt_count_cannot_bypass_resolved_retry_gate(self):
        self.change("request", self.gates)
        self.change("failed", {"definite_failure": True})
        corrupt = self.state | {"attempts": 0}
        self.path.write_text(json.dumps(corrupt), encoding="utf-8")
        original = self.path.read_bytes()
        for event, data in [("status", {}), ("request", self.gates)]:
            with self.subTest(event=event), self.assertRaisesRegex(ValueError, "attempts disagree"):
                STATE.update(self.path, event, data, self.state["revision"])
            self.assertEqual(self.path.read_bytes(), original)
            self.assertFalse(self.path.with_name(self.path.name + ".lock").exists())

    def test_internally_inconsistent_history_fails_closed(self):
        self.change("request", self.gates)
        self.change("unknown")
        for case in ("missing_prepare", "invalid_transition", "false_source_owner"):
            corrupt = json.loads(json.dumps(self.state))
            if case == "missing_prepare":
                corrupt["events"][0]["event"] = "cancel"
            elif case == "invalid_transition":
                corrupt["events"][1]["event"] = "confirm"
            else:
                # A matching final snapshot/history phase is not enough to
                # resume the source after an unresolved host outcome.
                corrupt["phase"] = corrupt["events"][-1]["phase"] = "prepared"
            self.path.write_text(json.dumps(corrupt), encoding="utf-8")
            original = self.path.read_bytes()
            with self.subTest(case=case), self.assertRaises(ValueError):
                STATE.update(self.path, "status", {})
            self.assertEqual(self.path.read_bytes(), original)

    def test_corrupt_history_cli_returns_error_without_owner(self):
        self.state["events"][0]["event"] = "cancel"
        self.path.write_text(json.dumps(self.state), encoding="utf-8")
        original = self.path.read_bytes()
        run = subprocess.run([sys.executable, str(Path(STATE.__file__)),
                              "--state", str(self.path), "--event", "status"],
                             capture_output=True, text=True, check=False)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(run.stdout, "")
        self.assertIn("history must start", json.loads(run.stderr)["error"])
        self.assertEqual(self.path.read_bytes(), original)

    def test_absence_reconciliation_and_terminal_cancel_histories_remain_valid(self):
        self.change("request", self.gates)
        self.change("unknown")
        self.change("absent", {"definitive_absence": True})
        self.change("request", self.gates | {"failure_resolved": True})
        self.change("unknown")
        self.change("absent", {"definitive_absence": True})
        self.assertEqual(self.state["phase"], "failed")
        self.change("cancel")
        revision = self.state["revision"]
        self.change("cancel")
        restored = STATE.update(self.path, "status", {})
        self.assertEqual(restored["revision"], revision)
        self.assertEqual(restored["attempts"], 2)
        self.assertEqual(STATE.summary(restored)["active_writer"], "source-a")

    def test_status_cli_works_after_process_restart(self):
        self.change("request", self.gates)
        run = subprocess.run([sys.executable, str(ROOT / "skills/pm-essential-skills-context-management/scripts/transfer_state.py"),
                              "--state", str(self.path), "--event", "status"],
                             capture_output=True, text=True, check=False)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(json.loads(run.stdout)["must_pause_source"])

    def test_storage_failure_preserves_prior_journal_and_releases_own_lock(self):
        original = self.path.read_bytes()
        with patch.object(STATE.os, "replace", side_effect=PermissionError("simulated blocked rename")):
            with self.assertRaises(PermissionError):
                self.change("request", self.gates)
        self.assertEqual(self.path.read_bytes(), original)
        self.assertFalse(self.path.with_name(self.path.name + ".lock").exists())
        self.assertEqual(list(self.path.parent.glob("journal.json.*.tmp")), [])

    def test_audit_is_small_and_records_recovery_without_private_content(self):
        self.change("request", self.gates)
        self.change("unknown")
        self.change("confirm", self.confirmation)
        self.assertEqual([entry["event"] for entry in self.state["events"]],
                         ["prepare", "request", "unknown", "confirm"])
        self.assertLessEqual(len(self.state["events"]), 12)
        self.assertNotIn("Confirmed goal", self.path.read_text())

    def test_missing_revision_is_rejected_for_mutations(self):
        with self.assertRaises(ValueError):
            STATE.update(self.path, "request", self.gates)


class PreflightTests(unittest.TestCase):
    def test_complete_transfer_requirements(self):
        value = {key: True for key in PREFLIGHT.FLAGS}
        value.update(membership="project", project_id="project-a", source_thread_id="source-a")
        self.assertTrue(PREFLIGHT.assess(value)["transfer_ready"])
        for key in ["destination_skill_available", "settings_preserved", "authorization_verified"]:
            with self.subTest(key=key):
                result = PREFLIGHT.assess(value | {key: False})
                self.assertFalse(result["transfer_ready"])
                self.assertIn(key, result["transfer_missing"])

    def test_unknown_capabilities_are_not_success(self):
        result = PREFLIGHT.assess({})
        self.assertFalse(result["transfer_ready"])
        self.assertEqual(result["status"], "unavailable")

    def test_known_source_identity_does_not_establish_recoverable_context(self):
        value = {key: True for key in PREFLIGHT.FLAGS}
        value.update(membership="project", project_id="project-a", source_thread_id="source-a")
        for state in ({}, {"source_recovery_ready": False}, {"source_recovery_ready": None}):
            observed = {key: item for key, item in value.items() if key != "source_recovery_ready"} | state
            result = PREFLIGHT.assess(observed)
            self.assertFalse(result["transfer_ready"])
            self.assertIn("source_recovery_ready", result["transfer_missing"])

    def test_project_setup_needs_real_tools_consent_and_name(self):
        value = dict(membership="standalone", source_thread_id="source-a", safe_checkpoint=True)
        self.assertEqual(PREFLIGHT.assess(value)["project_setup"], "unsupported")
        value.update(create_project_available=True, move_chat_available=True, verify_membership_available=True)
        self.assertEqual(PREFLIGHT.assess(value)["project_setup"], "needs_consent")
        value["setup_consent_verified"] = True
        self.assertEqual(PREFLIGHT.assess(value)["project_setup"], "needs_name")
        value["chosen_project_name"] = "Research"
        self.assertEqual(PREFLIGHT.assess(value)["project_setup"], "ready")

    def test_invalid_boolean_is_rejected(self):
        with self.assertRaises(ValueError):
            PREFLIGHT.assess({"create_thread_available": "yes"})

    def test_explicit_verified_target_can_accept_unaffiliated_source(self):
        value = {key: True for key in PREFLIGHT.FLAGS}
        value.update(membership="unknown", project_id="project-a", source_thread_id="source-a")
        result = PREFLIGHT.assess(value)
        self.assertTrue(result["transfer_ready"])
        self.assertEqual(result["source_membership"], "unknown")
        for key in ["target_project_verified", "project_selection_authorized"]:
            with self.subTest(key=key):
                result = PREFLIGHT.assess(value | {key: False})
                self.assertFalse(result["transfer_ready"])
                self.assertIn("verified_project_membership", result["transfer_missing"])


class SourceReuseTests(unittest.TestCase):
    def setUp(self):
        self.value = dict(source_id="document-a", loaded_source_id="document-a", content_available=True,
                          coverage_sufficient=True, freshness_required=True,
                          loaded_revision="v1", current_revision="v1", revision_verified=True)

    def test_unchanged_sufficient_source_is_reused(self):
        self.assertEqual(SOURCE.assess(self.value)["action"], "reuse")

    def test_changed_revision_fetches(self):
        self.assertEqual(SOURCE.assess(self.value | {"current_revision": "v2"})["action"], "fetch")

    def test_unknown_freshness_uses_lightweight_verification(self):
        for extra in [{"revision_verified": False}, {"current_revision": None}, {"loaded_revision": None}]:
            with self.subTest(extra=extra):
                self.assertEqual(SOURCE.assess(self.value | extra)["action"], "verify")

    def test_equal_revisions_from_different_sources_do_not_reuse(self):
        self.assertEqual(SOURCE.assess(self.value | {"loaded_source_id": "other"})["action"], "fetch")

    def test_metadata_cannot_replace_missing_content(self):
        self.assertEqual(SOURCE.assess(self.value | {"content_available": False})["action"], "fetch")

    def test_full_read_requirement_cannot_be_optimized_away(self):
        result = SOURCE.assess(self.value | {"needed": False, "required_full_read": True})
        self.assertEqual(result["reason"], "required_full_read_incomplete")

    def test_immutable_content_can_be_reused_without_current_metadata(self):
        result = SOURCE.assess(self.value | {"known_immutable": True, "current_revision": None})
        self.assertEqual(result["action"], "reuse")

    def test_coverage_and_access_are_respected(self):
        self.assertEqual(SOURCE.assess(self.value | {"coverage_sufficient": False})["action"], "fetch")
        self.assertEqual(SOURCE.assess(self.value | {"access": "denied"})["action"], "blocked")
        self.assertEqual(SOURCE.assess(self.value | {"needed": False})["action"], "skip")

    def test_invalid_observations_are_not_reused(self):
        for value in [{}, {"source_id": "a", "content_available": "yes"},
                      {"source_id": "a", "access": []}]:
            with self.assertRaises(ValueError):
                SOURCE.assess(value)

    def test_source_cli(self):
        run = subprocess.run([sys.executable, str(ROOT / "skills/pm-essential-skills-source-selection/scripts/assess_source.py")],
                             input=json.dumps(self.value), capture_output=True, text=True, check=False)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)["action"], "reuse")
