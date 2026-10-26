"""Regression contracts for avoiding negative-value handoff interruptions.

Synthetic supplied costs test the decision, not measured token savings.
"""
import unittest

from test_context_policy import POLICY, context


class ContextValueTests(unittest.TestCase):
    def setUp(self):
        self.base = {"project_mode": "project", "safe_checkpoint": True,
                     "substantial_history": True, "request_id": "accepted-outcome"}
        self.cost = {"basis": "estimated", "source": "frozen synthetic comparison",
                     "unit": "tool_calls", "scope": "remaining_requested_work", "fresh": True,
                     "continue": 1, "handoff": 1, "startup": 1, "reconstruction": 2,
                     "destination_work": 1}

    def test_stage_labels_do_not_override_known_negative_value(self):
        for stage in ({"new_phase": True}, {"new_outcome": True}, {}):
            with self.subTest(stage=stage):
                result = POLICY.assess(self.base | stage | {"transfer_cost": self.cost})
                self.assertEqual(result["action"], "continue")
                self.assertNotIn("prompt_level", result)

    def test_phase_change_does_not_require_repeating_completed_investigation(self):
        for stage in ("new_phase", "new_outcome"):
            result = POLICY.assess(self.base | {stage: True, "reconstruction_repeats_work": True})
            self.assertEqual(result["action"], "checkpoint")

    def test_unavailable_context_does_not_prompt_for_an_unready_optional_move(self):
        result = POLICY.assess(self.base | {"new_phase": True, "transfer_context_ready": False})
        self.assertEqual(result["action"], "continue")

    def test_number_of_declines_is_not_evidence_for_stronger_recommendation(self):
        levels = [POLICY.assess(self.base | {"stay_count": n})["prompt_level"]
                  for n in (0, 1, 2, 100)]
        self.assertEqual(levels, [1, 1, 1, 1])

    def test_related_correction_reuses_accepted_outcome_choice(self):
        result = POLICY.assess(self.base | {"boundary_choice": "current-thread",
                                           "choice_request_id": "accepted-outcome",
                                           "stay_count": 1})
        self.assertEqual(result["action"], "continue")

    def test_distinct_outcome_can_still_offer_a_useful_new_chat(self):
        result = POLICY.assess(self.base | {"new_outcome": True})
        self.assertEqual(result["action"], "ask_thread_choice")

    def test_explicit_destination_choice_still_wins_over_cost_estimate(self):
        result = POLICY.assess(self.base | {"user_requested_new_thread": True,
                                           "transfer_cost": self.cost})
        self.assertEqual(result["action"], "rollover")

    def test_pending_choice_is_not_silently_answered_by_cost_estimate(self):
        result = POLICY.assess(self.base | {"new_phase": True, "choice_pending": True,
                                           "transfer_cost": self.cost})
        self.assertEqual(result["action"], "await_thread_choice")

    def test_critical_continuation_still_requires_separate_transfer_checks(self):
        result = POLICY.assess(self.base | {"context": context(85000),
                                           "transfer_cost": self.cost})
        self.assertEqual(result["action"], "rollover")
        self.assertTrue(result["requires_transfer_checks"])


if __name__ == "__main__":
    unittest.main()
