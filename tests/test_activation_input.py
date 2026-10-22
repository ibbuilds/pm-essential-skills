"""Exercise bounded hook envelopes without running a model or host session."""

from contextlib import redirect_stdout
import io
import json
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
        self.home = Path(self.temp.name) / "profile"

    def invoke(self, payload):
        output = io.StringIO()
        with io.TextIOWrapper(io.BytesIO(payload), encoding="utf-8") as stream:
            with mock.patch.object(sys, "stdin", stream), mock.patch.object(sys, "argv", [
                "activation.py", "--codex-home", str(self.home)
            ]), redirect_stdout(output):
                self.assertEqual(activation.main(), 0)
        return json.loads(output.getvalue())

    def test_large_valid_prompt_gets_reminder_without_reflecting_prompt(self):
        install_suite.install(self.home, None, ["source-selection"])
        payload = json.dumps({"hook_event_name": "UserPromptSubmit", "prompt": "UNTRUSTED " * 14000}).encode()
        self.assertGreater(len(payload), 65536)
        result = self.invoke(payload)
        context = result["hookSpecificOutput"]["additionalContext"]
        self.assertIn("source-selection/SKILL.md", context)
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
