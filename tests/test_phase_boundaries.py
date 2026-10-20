"""Routing regressions for the observed planning-to-implementation failure.

These exercise the local policy, not live model compliance or token savings.
"""

import unittest

from test_context_policy import POLICY, context


class PhaseChoiceTests(unittest.TestCase):
    def setUp(self):
        self.phase = dict(new_phase=True, substantial_history=True,
                          project_mode="project", safe_checkpoint=True)

    def test_unanswered_choice_blocks_transfer_even_with_pressure_or_costs(self):
        costs = dict(basis="estimated", source="synthetic remaining-work estimate",
                     unit="tokens", scope="remaining_requested_work", fresh=True,
                     continue_=1, handoff=10, startup=20, reconstruction=30)
        costs["continue"] = costs.pop("continue_")
        for extra in ({}, {"context": context(10000)}, {"context": context()},
                      {"transfer_cost": costs}, {"transfer_context_ready": False},
                      {"reconstruction_repeats_work": True}):
            with self.subTest(extra=extra):
                result = POLICY.assess(self.phase | extra)
                self.assertEqual(result["action"], "ask_thread_choice")
                self.assertFalse(result["requires_transfer_checks"])
                self.assertEqual(result["notice"], "none")

    def test_missing_telemetry_remains_unknown(self):
        result = POLICY.assess(self.phase)
        self.assertEqual(result["measurement"], "unavailable")
        self.assertIsNone(result["context_ratio"])

    def test_completed_plan_with_requested_implementation_is_not_finished(self):
        self.assertEqual(POLICY.assess(self.phase | {"completed": True})["action"],
                         "ask_thread_choice")

    def test_distinct_outcome_in_substantial_chat_also_needs_choice(self):
        result = POLICY.assess(self.phase | {"new_phase": False, "new_outcome": True})
        self.assertEqual(result["action"], "ask_thread_choice")

    def test_small_work_and_same_phase_do_not_ask(self):
        for extra in ({"new_phase": False}, {"substantial_history": False}):
            self.assertEqual(POLICY.assess(self.phase | extra)["action"], "continue")

    def test_user_stays_without_pressure_prompt(self):
        result = POLICY.assess(self.phase | {"boundary_choice": "current-thread",
                                             "context": context()})
        self.assertEqual(result["action"], "continue")
        self.assertEqual(result["notice"], "none")

    def test_new_chat_choice_preserves_safe_transfer_gates(self):
        chosen = self.phase | {"boundary_choice": "new-thread"}
        result = POLICY.assess(chosen)
        self.assertEqual(result["action"], "rollover")
        self.assertTrue(result["requires_transfer_checks"])
        self.assertEqual(POLICY.assess(chosen | {"safe_checkpoint": False})["action"], "defer")
        blocked = POLICY.assess(chosen | {"transfer_context_ready": False})
        self.assertEqual(blocked["action"], "blocked_transfer")
        self.assertEqual(blocked["reason"], "transfer_context_unavailable")

    def test_explicit_choice_overrides_automatic_reconstruction_preference(self):
        costs = {"basis": "estimated", "source": "synthetic remaining-work estimate",
                 "unit": "tokens", "scope": "remaining_requested_work", "fresh": True,
                 "continue": 1, "handoff": 10, "startup": 20, "reconstruction": 30}
        result = POLICY.assess(self.phase | {"boundary_choice": "new-thread",
                                             "reconstruction_repeats_work": True,
                                             "transfer_cost": costs})
        self.assertEqual(result["action"], "rollover")

    def test_explicit_request_and_existing_stay_preferences_do_not_reask(self):
        for extra, expected in (({"user_requested_new_thread": True}, "rollover"),
                                ({"user_keep_thread": True}, "continue"),
                                ({"settings": {"mode": "stay"}}, "continue")):
            self.assertEqual(POLICY.assess(self.phase | extra)["action"], expected)

    def test_suggest_only_still_waits_for_location_choice(self):
        value = self.phase | {"settings": {"mode": "suggest-only"}}
        self.assertEqual(POLICY.assess(value)["action"], "ask_thread_choice")
        self.assertEqual(POLICY.assess(value | {"boundary_choice": "new-thread"})["action"],
                         "suggest_rollover")

    def test_unknown_membership_requires_verification_and_standalone_needs_no_setup(self):
        self.assertEqual(POLICY.assess(self.phase | {"project_mode": "unknown"})["reason"],
                         "phase_project_unverified")
        self.assertEqual(POLICY.assess(self.phase | {"project_mode": "standalone"})["action"],
                         "continue")

    def test_unsafe_boundary_defers_question(self):
        result = POLICY.assess(self.phase | {"safe_checkpoint": False})
        self.assertEqual(result["action"], "defer")
        self.assertEqual(result["notice"], "none")

    def test_choice_requires_explicit_supported_value(self):
        for value in (None, True, [], "", "unanswered", "automatic"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                POLICY.assess(self.phase | {"boundary_choice": value})


if __name__ == "__main__":
    unittest.main()
