import json
import shutil
import subprocess
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "hooks" / "pre-compact.mjs"
NODE = shutil.which("node")


@unittest.skipIf(NODE is None, "node is not installed")
class PreCompactTests(unittest.TestCase):
    def run_hook(self, stdin):
        result = subprocess.run([NODE, str(HOOK)], input=stdin, capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_auto_compaction_asks_for_the_handoff_fields(self):
        out = self.run_hook(json.dumps({"trigger": "auto", "custom_instructions": None}))
        for field in ("goal", "decisions", "dead ends", "last check command", "files to read first", "next action", "open questions", "secret"):
            self.assertIn(field, out)
        self.assertLess(len(out.split()), 120)

    def test_manual_instructions_are_kept_first(self):
        out = self.run_hook(json.dumps({"trigger": "manual", "custom_instructions": "focus on the auth bug"}))
        self.assertTrue(out.startswith("The user's instructions"))
        self.assertIn("focus on the auth bug", out)
        self.assertLess(out.index("focus on the auth bug"), out.index("next action"))

    def test_subagent_is_skipped(self):
        self.assertEqual(self.run_hook(json.dumps({"trigger": "auto", "agent_id": "a1"})), "")

    def test_bad_input_is_ignored(self):
        self.assertEqual(self.run_hook("not json"), "")


if __name__ == "__main__":
    unittest.main()
