"""Known-cost suppression of optional prompts at every below-critical boundary."""

import unittest

from test_context_policy import POLICY, advisory_assess, context


class PressurePromptCostTests(unittest.TestCase):
    def setUp(self):
        self.base = {"project_mode": "project", "safe_checkpoint": True, "request_id": "r",
                     "context": context(80000)}
        self.cost = {"basis": "estimated", "source": "synthetic remaining-work comparison",
                     "unit": "tokens", "scope": "remaining_requested_work", "fresh": True,
                     "continue": 100, "handoff": 40, "startup": 40, "reconstruction": 40}
        self.guards = ({"transfer_cost": self.cost}, {"reconstruction_repeats_work": True})

    def test_known_nonbeneficial_move_does_not_interrupt_with_new_question(self):
        for remaining in (120, 100):
            for signal in ({"context": context(80000)}, {"substantial_history": True}):
                result = advisory_assess((self.base | {"context": None}) | signal |
                                      {"transfer_cost": self.cost | {"continue": remaining}})
                self.assertEqual(result["action"], "continue")
                self.assertEqual(result["reason"], "transfer_cost_not_beneficial")
                self.assertEqual(result["notice"], "review")
                self.assertFalse(result["requires_transfer_checks"])
                self.assertNotIn("prompt_level", result)

    def test_known_reconstruction_reuses_checkpoint_not_question(self):
        result = advisory_assess(self.base | {"reconstruction_repeats_work": True})
        self.assertEqual((result["action"], result["reason"]),
                         ("checkpoint", "transfer_would_repeat_investigation"))
        self.assertEqual(result["notice"], "review")

    def test_nonblocking_notice_preserves_the_current_outcome_location(self):
        result = advisory_assess(self.base | {"boundary_choice": "current-thread",
                                           "choice_request_id": "r", "transfer_cost": self.cost})
        self.assertEqual(result["action"], "continue")
        self.assertEqual(result["notice"], "review")
        self.assertEqual(result["notice_reason"], "measured_context_review")
        self.assertFalse(result["requires_transfer_checks"])
        self.assertNotIn("prompt_level", result)

    def test_notice_keeps_its_evidence_when_cost_guard_changes_routing_reason(self):
        for signal, reason in (({"context": context(80000)}, "measured_context_review"),
                               ({"context": None, "substantial_history": True},
                                "substantial_replaceable_history")):
            result = advisory_assess(self.base | signal | {"transfer_cost": self.cost})
            self.assertEqual(result["reason"], "transfer_cost_not_beneficial")
            self.assertEqual(result["notice_reason"], reason)
            self.assertEqual(result["notice"], "review")
            if signal["context"] is None:
                self.assertIsNone(result["context_ratio"])
            else:
                self.assertEqual(result["context_ratio"], 0.8)

    def test_notice_deduplication_completion_opt_outs_and_compaction_are_independent(self):
        for extra in ({"last_notice_level": "review"}, {"completed": True},
                      {"management_disabled": True}, {"settings": {"mode": "stay"}},
                      {"safe_checkpoint": False},
                      {"context": context(10000), "substantial_history": True, "compactions": 10}):
            with self.subTest(extra=extra):
                result = advisory_assess(self.base | {"transfer_cost": self.cost} | extra)
                self.assertEqual(result["notice"], "none")
                self.assertNotIn("notice_reason", result)

    def test_standalone_replaceable_history_needs_no_telemetry_or_project_offer(self):
        result = advisory_assess({"project_mode": "standalone", "safe_checkpoint": True,
                                "substantial_history": True})
        self.assertEqual(result["action"], "continue")
        self.assertEqual(result["notice"], "review")
        self.assertEqual(result["notice_reason"], "substantial_replaceable_history")
        self.assertIsNone(result["context_ratio"])
        self.assertFalse(result["requires_transfer_checks"])
        self.assertNotIn("prompt_level", result)

    def test_unknown_stale_or_beneficial_costs_do_not_suppress_prompt(self):
        for cost in (None, self.cost | {"fresh": False}, self.cost | {"continue": 121}):
            self.assertEqual(advisory_assess(self.base | {"transfer_cost": cost})["action"],
                             "ask_thread_choice")

    def test_phase_and_outcome_boundaries_keep_the_value_guard(self):
        for guard in self.guards:
            for boundary in ("new_phase", "new_outcome"):
                for substantial in (False, True):
                    with self.subTest(guard=guard, boundary=boundary, substantial=substantial):
                        result = advisory_assess(self.base | guard |
                                              {boundary: True, "substantial_history": substantial})
                        self.assertEqual(result["action"],
                                         "checkpoint" if guard.get("reconstruction_repeats_work") else "continue")

    def test_pending_questions_still_wait_including_after_compaction(self):
        for guard in self.guards:
            for pending in ({"choice_pending": True}, {"last_prompt_request_id": "r"}):
                for used in (80000, 10000):
                    result = advisory_assess(self.base | guard | pending | {"context": context(used)})
                    self.assertEqual(result["action"], "await_thread_choice")

    def test_human_location_answers_and_requests_keep_precedence(self):
        for guard in self.guards:
            for answer, expected in (({"user_requested_new_thread": True}, "rollover"),
                                     ({"boundary_choice": "new-thread", "choice_request_id": "r"}, "rollover"),
                                     ({"boundary_choice": "current-thread", "choice_request_id": "r"}, "continue")):
                self.assertEqual(advisory_assess(self.base | guard | answer)["action"], expected)

    def test_critical_policy_and_readiness_are_unchanged(self):
        critical = self.base | {"context": context(85000), "transfer_cost": self.cost}
        self.assertEqual(advisory_assess(critical)["action"], "rollover")
        self.assertEqual(advisory_assess(critical | {"safe_checkpoint": False})["action"], "defer")
        self.assertEqual(advisory_assess(critical | {"transfer_context_ready": False})["action"], "blocked_transfer")
        self.assertEqual(advisory_assess(critical | {"reconstruction_repeats_work": True})["action"], "checkpoint")

    def test_safe_checkpoints_opt_outs_and_low_measurement_stay_intact(self):
        for guard in self.guards:
            base = self.base | guard
            self.assertEqual(advisory_assess(base | {"safe_checkpoint": False})["action"], "defer")
            for opt_out in ({"management_disabled": True}, {"settings": {"mode": "stay"}}):
                self.assertEqual(advisory_assess(base | opt_out)["action"], "continue")
            low = advisory_assess(base | {"context": context(10000), "compactions": 10})
            self.assertEqual((low["action"], low["reason"]), ("continue", "measured_context_below_review"))
            explicit = advisory_assess(base | {"settings": {"review_ratio": 0.9, "rollover_ratio": 0.95}})
            self.assertEqual(explicit["reason"], "measured_context_below_review")


class EarlyEconomicReviewTests(unittest.TestCase):
    def setUp(self):
        self.cost = {"basis": "estimated", "source": "synthetic complete comparison",
                     "unit": "tokens", "scope": "remaining_requested_work", "fresh": True,
                     "continue": 100, "handoff": 10, "startup": 10, "reconstruction": 10,
                     "destination_work": 20}
        self.base = {"project_mode": "project", "safe_checkpoint": True, "request_id": "r",
                     "context": context(10000), "transfer_cost": self.cost}

    def test_complete_benefit_recommends_early_without_pressure_or_dispatch(self):
        for meter in (None, context(10000)):
            result = advisory_assess(self.base | {"context": meter})
            self.assertEqual((result["action"], result["reason"]),
                             ("ask_thread_choice", "supplied_transfer_cost_beneficial"))
            self.assertEqual(result["notice"], "none")
            self.assertFalse(result["requires_transfer_checks"])
            self.assertEqual(result["transfer_cost"]["basis"], "estimated")
            self.assertTrue(result["transfer_cost"]["complete"])
            self.assertEqual(result["transfer_cost"]["transfer"], 50)
            self.assertEqual(result["measurement"], "unavailable" if meter is None else "measured")

    def test_unknown_incomplete_stale_and_nonbeneficial_cost_do_not_prove_benefit(self):
        legacy = {k: v for k, v in self.cost.items() if k != "destination_work"}
        for cost in (None, legacy, self.cost | {"fresh": False},
                     self.cost | {"destination_work": 70}, self.cost | {"destination_work": 71}):
            result = advisory_assess(self.base | {"transfer_cost": cost})
            self.assertEqual(result["action"], "continue")
        result = advisory_assess(self.base | {"transfer_cost": legacy})
        self.assertFalse(result["transfer_cost"]["complete"])
        self.assertEqual(result["transfer_cost"]["transfer"], 30)

    def test_zero_destination_cost_is_valid_but_unknown_is_not_zero(self):
        result = advisory_assess(self.base | {"transfer_cost": self.cost | {"destination_work": 0}})
        self.assertEqual(result["action"], "ask_thread_choice")
        self.assertTrue(result["transfer_cost"]["complete"])
        for value in (None, True, -1, 1.5, "20"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                advisory_assess(self.base | {"transfer_cost": self.cost | {"destination_work": value}})

    def test_full_execution_cost_can_reverse_apparent_overhead_advantage(self):
        cost = self.cost | {"destination_work": 80}
        result = advisory_assess(self.base | {"context": context(80000), "transfer_cost": cost})
        self.assertEqual((result["action"], result["reason"]),
                         ("continue", "transfer_cost_not_beneficial"))
        self.assertEqual(result["transfer_cost"]["transfer"], 110)

    def test_missing_context_and_reconstruction_guard_beneficial_recommendations(self):
        for used in (10000, 80000):
            for extra, expected in (({"transfer_context_ready": False}, "continue"),
                                    ({"reconstruction_repeats_work": True}, "checkpoint")):
                self.assertEqual(advisory_assess(self.base | {"context": context(used)} | extra)["action"],
                                 expected)

    def test_existing_choices_boundaries_and_critical_rules_retain_precedence(self):
        for extra, expected in (({"choice_pending": True}, "await_thread_choice"),
                                ({"last_prompt_request_id": "r"}, "await_thread_choice"),
                                ({"boundary_choice": "current-thread", "choice_request_id": "r"}, "continue"),
                                ({"user_requested_new_thread": True}, "rollover"),
                                ({"new_outcome": True}, "rollover"),
                                ({"new_phase": True}, "continue"),
                                ({"new_phase": True, "substantial_history": True}, "ask_thread_choice"),
                                ({"context": context(85000)}, "rollover")):
            self.assertEqual(advisory_assess(self.base | extra)["action"], expected)

    def test_safe_scope_and_explicit_opt_out_gates_remain(self):
        for extra in ({"safe_checkpoint": False}, {"management_disabled": True},
                      {"settings": {"mode": "stay"}}, {"project_mode": "unknown"},
                      {"project_mode": "standalone"}, {"user_keep_thread": True, "choice_request_id": "r"}):
            self.assertEqual(advisory_assess(self.base | extra)["action"], "continue")
        self.assertEqual(advisory_assess(self.base | {"settings": {"mode": "suggest-only"}})["action"],
                         "ask_thread_choice")


if __name__ == "__main__":
    unittest.main()
