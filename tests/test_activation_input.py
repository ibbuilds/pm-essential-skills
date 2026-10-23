"""Exercise bounded hook envelopes without running a model or host session."""

from contextlib import redirect_stdout
import io
import json
import os
import subprocess
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import activation
import install_suite


class ActivationInputTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        # Match the CLI's canonical home, including Windows short TEMP aliases.
        self.home = (Path(self.temp.name) / "profile").resolve()

    def invoke(self, payload):
        output = io.StringIO()
        with io.TextIOWrapper(io.BytesIO(payload), encoding="utf-8") as stream:
            with mock.patch.object(sys, "stdin", stream), mock.patch.object(sys, "argv", [
                "activation.py", "--codex-home", str(self.home)
            ]), redirect_stdout(output):
                self.assertEqual(activation.main(), 0)
        return json.loads(output.getvalue())

    def metadata_fixture(self):
        receipt = self.home / "pm-essential-skills/install.json"
        receipt.parent.mkdir(parents=True)
        skill = activation.NAMES[0]
        source = self.home / "skills" / skill / "SKILL.md"
        source.parent.mkdir(parents=True)
        source.write_text("isolated skill fixture")
        return receipt, skill

    def test_malformed_metadata_is_neutral_and_valid_subset_activates(self):
        receipt, skill = self.metadata_fixture()
        for state in ([], {"version": True, "skills": [skill]},
                      {"version": 1.0, "skills": [skill]},
                      {"version": 1, "skills": skill},
                      {"version": 1, "skills": {skill: False}},
                      {"version": 1, "skills": [skill, None]}):
            with self.subTest(state=state):
                receipt.write_text(json.dumps(state))
                self.assertEqual(self.invoke(b'{"hook_event_name":"UserPromptSubmit"}'), {})
        receipt.write_text(json.dumps({"version": 1, "skills": [skill]}))
        result = self.invoke(b'{"hook_event_name":"UserPromptSubmit","prompt":"UNTRUSTED"}')
        context = result["hookSpecificOutput"]["additionalContext"]
        self.assertIn(skill + "/SKILL.md", context)
        self.assertNotIn(activation.NAMES[1], context)
        self.assertNotIn("UNTRUSTED", context)

    def test_duplicate_metadata_fields_are_neutral(self):
        receipt, skill = self.metadata_fixture()
        receipt.write_text('{"version":1,"skills":[],"skills":' + json.dumps([skill]) + '}')
        self.assertEqual(self.invoke(b'{"hook_event_name":"SessionStart"}'), {})

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO unavailable")
    def test_fifo_metadata_is_prompt_neutral_noop(self):
        receipt, _ = self.metadata_fixture()
        os.mkfifo(receipt)
        result = subprocess.run([sys.executable, str(ROOT / "scripts/activation.py"),
                                 "--codex-home", str(self.home)],
                                input='{"hook_event_name":"SessionStart"}',
                                capture_output=True, text=True, timeout=3)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), {})
        self.assertEqual(result.stderr, "")

    @unittest.skipUnless(hasattr(os, "mkfifo") and hasattr(os, "O_NONBLOCK"),
                         "Nonblocking FIFO unavailable")
    def test_metadata_descriptor_rechecks_replaced_file(self):
        receipt, skill = self.metadata_fixture()
        receipt.write_text(json.dumps({"version": 1, "skills": [skill]}))
        real_open = os.open

        def replace_before_open(path, flags):
            receipt.unlink()
            os.mkfifo(receipt)
            return real_open(path, flags)

        with mock.patch.object(activation.os, "open", side_effect=replace_before_open):
            self.assertEqual(self.invoke(b'{"hook_event_name":"SessionStart"}'), {})

    def test_large_valid_prompt_gets_reminder_without_reflecting_prompt(self):
        install_suite.install(self.home, None, ["pm-essential-skills-source-selection"])
        payload = json.dumps({"hook_event_name": "UserPromptSubmit", "prompt": "UNTRUSTED " * 14000}).encode()
        self.assertGreater(len(payload), 65536)
        result = self.invoke(payload)
        context = result["hookSpecificOutput"]["additionalContext"]
        self.assertIn("pm-essential-skills-source-selection/SKILL.md", context)
        self.assertNotIn("UNTRUSTED", context)

    def test_oversized_envelope_is_bounded_neutral_noop(self):
        with mock.patch.object(activation, "MAX_INPUT_BYTES", 64):
            self.assertEqual(self.invoke(b"x" * 65), {})
        self.assertFalse(self.home.exists())

    def test_excessively_nested_input_is_neutral_noop(self):
        self.assertEqual(self.invoke(b"[" * 2000 + b"0" + b"]" * 2000), {})
        self.assertFalse(self.home.exists())


if __name__ == "__main__":
    unittest.main()
