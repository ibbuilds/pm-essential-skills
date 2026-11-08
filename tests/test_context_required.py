"""Default preventive policy: routing, source-work gate and recovery, not prose matching."""
import json
import subprocess
import sys
import unittest
from test_context_policy import POLICY, context, SCRIPT


class RequiredContextTests(unittest.TestCase):
    def assess(self, used=60000, **extra):
        return POLICY.assess({"safe_checkpoint": True, "context": context(used), **extra})

    def test_default_boundaries(self):
        for used, blocked in ((0, False), (39999, False), (40000, False),
                              (50000, False), (59999, False), (60000, True), (99999, True)):
            with self.subTest(used=used):
                r = self.assess(used)
                self.assertEqual(r.get("domain_work_allowed", True), not blocked)
                if blocked:
                    self.assertEqual(r["action"], "rollover")
                    self.assertTrue(r["requires_transfer_checks"])
                    self.assertEqual(r["reason"], "context_ceiling_reached")
                elif used >= 40000:
                    self.assertEqual(r["action"], "review")
                    self.assertEqual(r["notice"], "review")
                    self.assertFalse(r["requires_transfer_checks"])

    def test_gate_survives_optional_location_and_cost_guards(self):
        cost = dict(basis="estimated", source="synthetic remaining work", unit="tokens",
                    scope="remaining_requested_work", fresh=True, **{"continue": 1},
                    handoff=10, startup=10, reconstruction=10)
        guards = [{"user_keep_thread": True}, {"transfer_cost": cost},
                  {"reconstruction_repeats_work": True}, {"choice_pending": True},
                  {"last_notice_level": "rollover"},
                  {"boundary_choice": "current-thread", "request_id": "r", "choice_request_id": "r"}]
        for mode in ("project", "standalone", "unknown"):
            for guard in guards:
                with self.subTest(mode=mode, guard=guard):
                    r = self.assess(project_mode=mode, **guard)
                    self.assertFalse(r["domain_work_allowed"])
                    self.assertEqual(r["notice"], "rollover")
                    self.assertEqual(r["remind"], "each_user_turn_until_resolved")

    def test_warning_prepares_without_stopping_current_work(self):
        for used in (40000, 44000, 50000, 55000, 59999):
            for mode in ("project", "standalone", "unknown"):
                with self.subTest(used=used, mode=mode):
                    r = self.assess(used, project_mode=mode, user_keep_thread=True,
                                    transfer_context_ready=False, last_notice_level="review")
                    self.assertEqual(r["action"], "review")
                    self.assertTrue(r["domain_work_allowed"])
                    self.assertFalse(r["requires_transfer_checks"])
                    self.assertEqual(r["notice"], "review")
                    self.assertEqual(r["allowed_work"], "continue_and_prepare_handoff")

    def test_warning_does_not_erase_an_existing_pending_choice(self):
        for extra in ({"choice_pending": True},
                      {"request_id": "r", "last_prompt_request_id": "r"}):
            r = self.assess(44000, **extra)
            self.assertEqual(r["action"], "await_thread_choice")
            self.assertFalse(r["domain_work_allowed"])
            self.assertEqual(r["notice"], "review")

    def test_explicit_move_before_the_ceiling_remains_authoritative(self):
        for extra in ({"user_requested_new_thread": True},
                      {"request_id": "r", "choice_request_id": "r", "boundary_choice": "new-thread"}):
            r = self.assess(44000, **extra)
            self.assertEqual(r["action"], "rollover")
            self.assertFalse(r["domain_work_allowed"])
            self.assertTrue(r["requires_transfer_checks"])

    def test_warning_does_not_interrupt_unsafe_work(self):
        r = self.assess(55000, safe_checkpoint=False)
        self.assertTrue(r["domain_work_allowed"])
        self.assertEqual(r["action"], "review")
        self.assertEqual(r["notice"], "none")

    def test_fresh_compaction_into_warning_range_clears_hard_gate_only(self):
        r = self.assess(55000, last_notice_level="rollover", large_outputs=20,
                        substantial_history=True, critical_history=True)
        self.assertTrue(r["domain_work_allowed"])
        self.assertEqual(r["notice"], "review")
        r = self.assess(12000, last_notice_level="rollover")
        self.assertEqual(r["notice"], "none")

    def test_explicit_45_55_configuration_has_separate_boundaries(self):
        settings = {"review_ratio": .45, "rollover_ratio": .55}
        for used, warning, allowed in ((44999, False, True), (45000, True, True),
                                       (54999, True, True), (55000, False, False)):
            r = self.assess(used, settings=settings)
            self.assertEqual(r.get("domain_work_allowed", True), allowed)
            self.assertEqual(r["notice"] == "review", warning)

    def test_cli_40_percent_warns_without_a_pause(self):
        run = subprocess.run([sys.executable, str(SCRIPT)],
                             input=json.dumps({"context": context(40000), "safe_checkpoint": True}),
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        result = json.loads(run.stdout)
        self.assertTrue(result["domain_work_allowed"])
        self.assertEqual(result["notice"], "review")

    def test_unsafe_operations_only_reach_checkpoint(self):
        for used in (60000, 80000, 90000):
            r = self.assess(used, safe_checkpoint=False)
            self.assertEqual(r["action"], "defer")
            self.assertFalse(r["domain_work_allowed"])
            self.assertEqual(r["allowed_work"], "stabilize_checkpoint_and_handoff_only")
            self.assertEqual(r["notice"], "none")

    def test_missing_context_is_a_blocker_not_permission_to_resume(self):
        r = self.assess(transfer_context_ready=False)
        self.assertEqual(r["action"], "blocked_transfer")
        self.assertFalse(r["domain_work_allowed"])

    def test_opt_outs_are_explicit_and_still_authoritative(self):
        for extra in ({"management_disabled": True}, {"settings": {"mode": "stay"}},
                      {"settings": {"mode": "suggest-only"}}):
            with self.subTest(extra=extra):
                r = self.assess(90000, **extra)
                self.assertNotEqual(r.get("domain_work_allowed"), False)

    def test_completed_work_is_quiet_but_new_work_checks_again(self):
        self.assertEqual(self.assess(completed=True)["action"], "complete")
        for field in ("new_outcome", "new_phase"):
            self.assertFalse(self.assess(completed=True, **{field: True})["domain_work_allowed"])

    def test_fresh_compaction_clears_pressure_despite_old_history(self):
        r = self.assess(10000, substantive_turns=250, large_outputs=30,
                        substantial_history=True, critical_history=True, compactions=5)
        self.assertNotEqual(r.get("domain_work_allowed"), False)
        self.assertEqual(r["notice"], "none")

    def test_stale_measurements_cannot_prove_pressure_or_recovery(self):
        for used in (1000, 99000):
            r = self.assess(context=context(used, fresh=False))
            self.assertIsNone(r["context_ratio"])
            self.assertNotEqual(r.get("domain_work_allowed"), False)
            r = self.assess(context=context(used, fresh=False), large_outputs=3)
            self.assertTrue(r["domain_work_allowed"])
            self.assertEqual(r["notice"], "none")
            self.assertIsNone(r["context_ratio"])

    def test_unknown_occupancy_counts_trigger_review_not_saturation(self):
        for field, limit in (("substantive_turns", 10), ("large_outputs", 3)):
            r = self.assess(context=None, **{field: limit-1})
            self.assertNotEqual(r.get("domain_work_allowed"), False)
            for mode in ("project", "standalone", "unknown"):
                r = self.assess(context=None, project_mode=mode, **{field: limit})
                self.assertTrue(r["domain_work_allowed"])
                self.assertEqual(r["measurement"], "unknown")
                self.assertFalse(r["requires_transfer_checks"])
                self.assertEqual(r["notice"], "none")
                self.assertIsNone(r["context_ratio"])

    def test_history_is_assessed_without_forcing_transfer_from_a_label(self):
        for signal in ({"substantial_history": True}, {"critical_history": True},
                       {"admission_check": True, "obsolete_context_evidence": ["old scope superseded", "lost active constraint"]}):
            r = self.assess(context=None, **signal)
            self.assertTrue(r["domain_work_allowed"])
        r = self.assess(context=None, critical_history=True,
                        obsolete_context_evidence=["repeated lost active constraint",
                                                   "reconstruction omits pending work"])
        self.assertFalse(r["domain_work_allowed"])

    def test_required_policy_rejects_late_or_malformed_ceilings(self):
        for settings in ({"rollover_ratio": .61}, {"review_ratio": .75, "rollover_ratio": .85},
                         {"enforcement": []}, {"enforcement": "automatic"}):
            with self.subTest(settings=settings), self.assertRaises(ValueError):
                self.assess(settings=settings)

    def test_advisory_policy_remains_explicitly_available(self):
        r = self.assess(80000, settings={"enforcement": "advisory", "review_ratio": .75, "rollover_ratio": .85})
        self.assertEqual(r["action"], "review")
        self.assertNotEqual(r.get("domain_work_allowed"), False)

    def test_gate_does_not_skip_validation(self):
        for bad in ({"made_up_field": True}, {"transfer_cost": {}},
                    {"safe_checkpoint": "yes"}, {"context": context(kind="cumulative_usage")}):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.assess(**bad)

    def test_sequence_reminds_until_fresh_low_measurement(self):
        for used in (60000, 64000, 91000):
            r = self.assess(used, last_notice_level="rollover", choice_pending=True)
            self.assertFalse(r["domain_work_allowed"])
            self.assertEqual(r["notice"], "rollover")
        r = self.assess(12000)
        self.assertNotEqual(r.get("domain_work_allowed"), False)

    def test_cli_default_enforces_60_percent(self):
        run = subprocess.run([sys.executable, str(SCRIPT)],
                             input=json.dumps({"context": context(60000), "safe_checkpoint": True}),
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertFalse(json.loads(run.stdout)["domain_work_allowed"])


if __name__ == "__main__":
    unittest.main()
