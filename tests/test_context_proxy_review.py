"""Output counts invite reassessment; they do not establish context saturation."""
import unittest
from test_context_policy import POLICY, context


class ProxyReviewTests(unittest.TestCase):
    def test_three_outputs_alone_do_not_pause_or_require_handoff(self):
        result = POLICY.assess({'safe_checkpoint': True, 'large_outputs': 3})
        self.assertEqual(result['action'], 'review')
        self.assertTrue(result['domain_work_allowed'])
        self.assertFalse(result['requires_transfer_checks'])
        self.assertEqual(result['notice'], 'none')
        self.assertIsNone(result['context_ratio'])

    def test_many_turns_alone_do_not_establish_saturation(self):
        result = POLICY.assess({'safe_checkpoint': True, 'substantive_turns': 80})
        self.assertTrue(result['domain_work_allowed'])
        self.assertFalse(result['requires_transfer_checks'])

    def test_vague_history_without_support_does_not_pause(self):
        result = POLICY.assess({'safe_checkpoint': True, 'critical_history': True})
        self.assertTrue(result['domain_work_allowed'])

    def test_supported_continuity_failure_retains_a_safe_handoff(self):
        result = POLICY.assess({'safe_checkpoint': True, 'critical_history': True,
            'obsolete_context_evidence': ['Repeatedly lost accepted authorization scope',
                                          'Repeated reconstruction drops the active pending decision']})
        self.assertFalse(result['domain_work_allowed'])
        self.assertTrue(result['requires_transfer_checks'])

    def test_fresh_current_context_remains_the_preferred_signal(self):
        for used, allowed in [(10000, True), (45000, True), (65000, False)]:
            result = POLICY.assess({'safe_checkpoint': True, 'large_outputs': 80,
                                   'context': context(used)})
            self.assertEqual(result.get('domain_work_allowed', True), allowed)


if __name__ == '__main__':
    unittest.main()
