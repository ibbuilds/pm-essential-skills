"""Exercise archive lifecycle guards with synthetic observations, no app mutations."""

import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/ibbuilds-pm-context-management/scripts/assess_archive.py"
SPEC = importlib.util.spec_from_file_location("archive_policy", SCRIPT)
POLICY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(POLICY)


class ArchivePolicyTests(unittest.TestCase):
    def setUp(self):
        self.ready = {key: True for key in POLICY.FLAGS}
        self.ready.update(user_keep_visible=False, currently_archived=False)

    def action(self, stage, **overrides):
        return POLICY.assess(self.ready | {"stage": stage} | overrides)["action"]

    def test_cleanup_only_after_confirmed_recoverable_handoff(self):
        self.assertEqual(self.action("after_handoff"), "archive_source")
        for key in ("handoff_confirmed", "routing_saved", "source_superseded", "source_recovery_ready"):
            with self.subTest(key=key):
                self.assertEqual(self.action("after_handoff", **{key: False}), "keep")

    def test_mutations_require_scope_isolation_capability_and_no_other_work(self):
        for stage in ("after_handoff", "recover", "restore"):
            state = self.ready | {"stage": stage}
            if stage == "recover":
                state.update(read_result="archive_blocked", currently_archived=True)
            for key in ("authorized", "archive_control_available", "archive_effect_isolated", "no_other_active_work"):
                for observed in (False, None):
                    with self.subTest(stage=stage, key=key, observed=observed):
                        result = POLICY.assess(state | {key: observed})
                        self.assertEqual(result["action"], "keep")

    def test_archive_state_unknown_is_not_guessed(self):
        self.assertEqual(self.action("after_handoff", currently_archived=None), "verify_archive_state")
        self.assertEqual(self.action("recover", read_result="archive_blocked", original_archived=None),
                         "verify_archive_state")

    def test_read_archived_source_before_attempting_restore(self):
        self.assertEqual(self.action("recover", currently_archived=True), "read_source")
        self.assertEqual(self.action("recover", currently_archived=True, read_result="success"), "use_context")
        self.assertEqual(self.action("recover", currently_archived=True, read_result="failed"), "fallback")

    def test_temporary_restore_requires_prior_recovery_receipt(self):
        state = dict(currently_archived=True, read_result="archive_blocked")
        self.assertEqual(self.action("recover", **state, recovery_receipt_saved=False), "record_recovery_receipt")
        self.assertEqual(self.action("recover", **state), "unarchive_for_recovery")

    def test_originally_unarchived_predecessor_stays_visible(self):
        self.assertEqual(self.action("restore", original_archived=False), "keep")
        self.assertEqual(self.action("restore", recovery_receipt_saved=False), "keep")

    def test_cleanup_rearchives_after_success_or_failure(self):
        for read_result in ("success", "failed", "archive_blocked"):
            with self.subTest(read_result=read_result):
                self.assertEqual(self.action("restore", read_result=read_result), "rearchive_source")

    def test_cleanup_complete_requires_observed_archive_state(self):
        self.assertEqual(self.action("restore", currently_archived=True), "cleanup_complete")
        self.assertEqual(self.action("restore", currently_archived=None), "reconcile_restore")
        self.assertEqual(self.action("restore", restored_for_recovery=False), "reconcile_restore")

    def test_human_visibility_override_prevents_every_mutation(self):
        for stage in ("after_handoff", "recover", "restore"):
            self.assertEqual(self.action(stage, user_keep_visible=True,
                                         read_result="archive_blocked", currently_archived=True), "keep")
        self.assertEqual(self.action("recover", user_keep_visible=True), "read_source")

    def test_unverified_identity_and_bad_input_never_select_mutation(self):
        self.assertEqual(self.action("after_handoff", target_verified=False), "verify_target")
        for value in ({}, {"stage": "delete"}, {"stage": "recover", "read_result": "assumed"},
                      {"stage": "recover", "authorized": "true"}, {"stage": "recover", "unknown": True}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                POLICY.assess(value)


if __name__ == "__main__":
    unittest.main()
