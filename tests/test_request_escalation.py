"""Repeated requests, one-request stays, and critical automatic continuation."""

import unittest

from test_context_policy import POLICY, context


class RequestEscalationTests(unittest.TestCase):
    def setUp(self):
        self.long = {"project_mode": "project", "safe_checkpoint": True,
                     "substantial_history": True, "request_id": "request-1"}

    def test_declining_one_request_does_not_silence_next_request(self):
        first = POLICY.assess(self.long)
        self.assertEqual((first["action"], first["prompt_level"]), ("ask_thread_choice", 1))
        answered = self.long | {"boundary_choice": "current-thread", "choice_request_id": "request-1",
                                "last_prompt_request_id": "request-1", "stay_count": 1}
        self.assertEqual(POLICY.assess(answered)["action"], "continue")
        next_request = POLICY.assess(answered | {"request_id": "request-2"})
        self.assertEqual((next_request["action"], next_request["prompt_level"]), ("ask_thread_choice", 2))
        third = POLICY.assess(answered | {"request_id": "request-3", "stay_count": 2})
        self.assertEqual(third["prompt_level"], 3)
        self.assertEqual(POLICY.assess(answered | {"request_id": "request-4", "stay_count": 100})["prompt_level"], 3)

    def test_repeated_assessments_never_stack_same_request_question(self):
        prompted = self.long | {"last_prompt_request_id": "request-1"}
        for _ in range(3):
            result = POLICY.assess(prompted)
            self.assertEqual(result["action"], "await_thread_choice")
            self.assertNotIn("prompt_level", result)
        self.assertEqual(POLICY.assess(self.long | {"choice_pending": True})["action"], "await_thread_choice")

    def test_pending_choice_survives_compaction_and_new_work(self):
        initial = {"project_mode": "project", "safe_checkpoint": True,
                   "request_id": "r", "context": context(80000)}
        self.assertEqual(POLICY.assess(initial)["action"], "ask_thread_choice")
        for pending in ({"choice_pending": True}, {"last_prompt_request_id": "r"}):
            for extra in ({}, {"new_outcome": True}, {"safe_checkpoint": False},
                          {"project_mode": "unknown"}, {"project_mode": "standalone"}):
                with self.subTest(pending=pending, extra=extra):
                    result = POLICY.assess(initial | {"context": context(10000)} | pending | extra)
                    self.assertEqual(result["action"], "await_thread_choice")
                    self.assertFalse(result["requires_transfer_checks"])

    def test_old_prompt_without_matching_known_identity_is_not_pending(self):
        for ids in ({}, {"last_prompt_request_id": "old"},
                    {"request_id": "new", "last_prompt_request_id": "old"}):
            with self.subTest(ids=ids):
                result = POLICY.assess({"project_mode": "project", "safe_checkpoint": True,
                                       "context": context(10000)} | ids)
                self.assertEqual(result["action"], "continue")

    def test_current_answers_override_pending_marker_after_compaction(self):
        value = {"project_mode": "project", "safe_checkpoint": True, "context": context(10000),
                 "request_id": "r", "choice_request_id": "r", "last_prompt_request_id": "r",
                 "choice_pending": True}
        for choice, expected in (("current-thread", "continue"), ("new-thread", "rollover")):
            self.assertEqual(POLICY.assess(value | {"boundary_choice": choice})["action"], expected)

    def test_matching_choice_is_required_for_current_request(self):
        current = {"user_keep_thread": True, "choice_request_id": "request-1"}
        self.assertEqual(POLICY.assess(self.long | current)["action"], "continue")
        self.assertEqual(POLICY.assess(self.long | current | {"request_id": "request-2"})["action"],
                         "ask_thread_choice")

    def test_critical_pressure_transfers_instead_of_asking_again(self):
        for extra in ({}, {"boundary_choice": "current-thread", "choice_request_id": "request-1"},
                      {"user_keep_thread": True, "choice_request_id": "request-1"},
                      {"choice_pending": True, "last_prompt_request_id": "request-1"}):
            with self.subTest(extra=extra):
                result = POLICY.assess(self.long | {"context": context()} | extra)
                self.assertEqual(result["action"], "rollover")
                self.assertTrue(result["requires_transfer_checks"])
                self.assertNotIn("prompt_level", result)

    def test_critical_transfer_preserves_safe_context_and_reconstruction_gates(self):
        critical = self.long | {"context": context()}
        self.assertEqual(POLICY.assess(critical | {"safe_checkpoint": False})["action"], "defer")
        self.assertEqual(POLICY.assess(critical | {"transfer_context_ready": False})["action"], "blocked_transfer")
        self.assertEqual(POLICY.assess(critical | {"reconstruction_repeats_work": True})["action"], "checkpoint")

    def test_critical_pressure_is_not_vetoed_by_estimated_transfer_cost(self):
        costs = {"basis": "estimated", "source": "synthetic comparison", "unit": "tokens",
                 "scope": "remaining_requested_work", "fresh": True,
                 "continue": 1, "handoff": 100, "startup": 100, "reconstruction": 100}
        self.assertEqual(POLICY.assess(self.long | {"context": context(), "transfer_cost": costs})["action"],
                         "rollover")

    def test_persistent_opt_outs_and_suggest_only_remain_effective(self):
        critical = self.long | {"context": context()}
        for extra in ({"management_disabled": True}, {"settings": {"mode": "stay"}}):
            self.assertEqual(POLICY.assess(critical | extra)["action"], "continue")
        self.assertEqual(POLICY.assess(critical | {"settings": {"mode": "suggest-only"}})["action"],
                         "suggest_rollover")

    def test_unmeasured_critical_history_requires_concrete_support(self):
        value = self.long | {"critical_history": True}
        self.assertEqual(POLICY.assess(value)["action"], "ask_thread_choice")
        supported = value | {"obsolete_context_evidence": ["Repeatedly lost approved constraint",
                                                           "Reconstructed resolved research again"]}
        result = POLICY.assess(supported)
        self.assertEqual(result["action"], "rollover")
        self.assertEqual(result["measurement"], "heuristic")
        self.assertIsNone(result["context_ratio"])
        self.assertEqual(POLICY.assess(supported | {"context": context(10000)})["action"], "ask_thread_choice")
        self.assertEqual(POLICY.assess(supported | {"project_mode": "standalone"})["action"], "checkpoint")

    def test_review_range_prompts_even_without_a_new_phase(self):
        result = POLICY.assess({"project_mode": "project", "safe_checkpoint": True,
                                "request_id": "request-1", "context": context(80000)})
        self.assertEqual(result["action"], "ask_thread_choice")
        self.assertEqual(POLICY.assess({"safe_checkpoint": True, "project_mode": "project"})["action"], "continue")

    def test_completed_work_does_not_prompt_or_spawn_empty_successor(self):
        result = POLICY.assess(self.long | {"completed": True, "context": context()})
        self.assertEqual(result["action"], "complete")

    def test_observations_reject_invalid_ids_and_counts(self):
        for extra in ({"request_id": ""}, {"choice_request_id": None}, {"last_prompt_request_id": []},
                      {"stay_count": -1}, {"stay_count": True}, {"critical_history": "yes"}):
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                POLICY.assess(self.long | extra)


if __name__ == "__main__":
    unittest.main()
