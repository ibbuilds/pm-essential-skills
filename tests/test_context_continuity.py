"""Multi-turn policy and hook delivery; separate from model/host compliance."""
import json
from pathlib import Path
import sys
import tempfile
import subprocess
import unittest

from test_context_policy import POLICY, context

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import activation

REMINDER = ROOT / 'skills/pm-essential-skills-context-management/scripts/turn_reminder.py'


class ContextContinuityTests(unittest.TestCase):
    def test_standalone_reminder_cli_repeats_without_a_suite_receipt(self):
        for event, text in [('SessionStart', ''), ('UserPromptSubmit', 'STAY_ONLY_FOR_REQUEST'),
                            ('UserPromptSubmit', 'CORRECTION'), ('UserPromptSubmit', 'NEW_REQUEST')]:
            run = subprocess.run([sys.executable, str(REMINDER)],
                                 input=json.dumps({'hook_event_name': event, 'prompt': text}),
                                 text=True, capture_output=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            result = json.loads(run.stdout)
            self.assertEqual(set(result), {'hookSpecificOutput'})
            output = result['hookSpecificOutput']
            self.assertEqual(output['hookEventName'], event)
            self.assertIn('pm-essential-skills-context-management/SKILL.md', output['additionalContext'])
            self.assertLess(len(output['additionalContext']), 1000)
            if text:
                self.assertNotIn(text, output['additionalContext'])

    def test_standalone_reminder_does_not_expand_to_tool_events_or_block_bad_input(self):
        for payload in ['not json', '[]', '{"hook_event_name":"PreToolUse"}']:
            run = subprocess.run([sys.executable, str(REMINDER)], input=payload,
                                 text=True, capture_output=True)
            self.assertEqual(run.returncode, 0)
            self.assertEqual(json.loads(run.stdout), {})

    def test_stay_refinement_new_request_and_ceiling_keep_checks(self):
        # A real caller retains facts across turns; no instruction to opt out exists.
        state = {'safe_checkpoint': True, 'request_id': 'migration',
                 'last_notice_level': 'none'}
        sequence = [
            (46000, {}),
            (49000, {'boundary_choice': 'current-thread', 'choice_request_id': 'migration'}),
            (52000, {}),
            (56000, {'request_id': 'export', 'new_outcome': True}),
            (61000, {}),
        ]
        for used, update in sequence:
            state.update(update)
            result = POLICY.assess(state | {'context': context(used)})
            self.assertEqual(result['remind'], 'each_user_turn_until_resolved')
            self.assertEqual(result['notice'], 'review' if used < 60000 else 'rollover')
            self.assertEqual(result['domain_work_allowed'], used < 60000)
            state['last_notice_level'] = result['notice']
        # A fresh context clears pressure; old location choices do not create it.
        result = POLICY.assess(state | {'context': context(10000)})
        self.assertEqual(result['notice'], 'none')
        self.assertNotEqual(result.get('domain_work_allowed'), False)

    def test_missing_telemetry_does_not_turn_old_stay_into_a_reset(self):
        state = {'safe_checkpoint': True, 'boundary_choice': 'current-thread',
                 'choice_request_id': 'old', 'request_id': 'new',
                 'substantive_turns': 10, 'last_notice_level': 'rollover'}
        for turn in range(3):
            result = POLICY.assess(state | {'substantive_turns': 10 + turn})
            self.assertIsNone(result['context_ratio'])
            self.assertFalse(result['domain_work_allowed'])
            self.assertEqual(result['notice'], 'rollover')

    def test_each_prompt_gets_a_reminder_without_prompt_or_state_mutation(self):
        name = 'pm-essential-skills-context-management'
        with tempfile.TemporaryDirectory(dir=ROOT / 'work') as directory:
            home = Path(directory)
            (home / 'skills' / name).mkdir(parents=True)
            (home / 'skills' / name / 'SKILL.md').write_text('fixture', encoding='utf-8')
            metadata = home / 'pm-essential-skills/install.json'
            metadata.parent.mkdir()
            metadata.write_text(json.dumps({'version': 1, 'skills': [name]}))
            before = {str(p): p.read_bytes() for p in home.rglob('*') if p.is_file()}
            replies = []
            for event, prompt in [('SessionStart', ''),
                                  ('UserPromptSubmit', 'KEEP_CURRENT_REQUEST'),
                                  ('UserPromptSubmit', 'RELATED_CORRECTION'),
                                  ('UserPromptSubmit', 'DISTINCT_NEXT_REQUEST')]:
                result = activation.handle({'hook_event_name': event, 'prompt': prompt}, home)
                output = result['hookSpecificOutput']
                self.assertEqual(output['hookEventName'], event)
                self.assertIn(name + '/SKILL.md', output['additionalContext'])
                if prompt:
                    self.assertNotIn(prompt, output['additionalContext'])
                    replies.append(output['additionalContext'])
            self.assertEqual(len(replies), 3)
            self.assertTrue(all(text == replies[0] for text in replies))
            self.assertEqual(before, {str(p): p.read_bytes() for p in home.rglob('*') if p.is_file()})


if __name__ == '__main__':
    unittest.main()
