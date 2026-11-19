import json
import os
import shutil
import subprocess
import tempfile
import unittest
import uuid
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "hooks" / "context-watch.mjs"
NODE = shutil.which("node")


def assistant_line(input_tokens, cache_read, cache_write=0):
    usage = {"input_tokens": input_tokens, "cache_read_input_tokens": cache_read, "cache_creation_input_tokens": cache_write, "output_tokens": 10}
    return json.dumps({"type": "assistant", "message": {"role": "assistant", "usage": usage}})


@unittest.skipIf(NODE is None, "node is not installed")
class ContextWatchTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.transcript = Path(self._tmp.name) / "session.jsonl"
        self.session = f"test-{uuid.uuid4().hex}"

    def tearDown(self):
        self._tmp.cleanup()
        state = Path(tempfile.gettempdir()) / f"pm-context-watch-{self.session}.json"
        if state.exists():
            state.unlink()

    def run_hook(self, lines, payload_extra=None, **env):
        self.transcript.write_text("\n".join(lines) + "\n", encoding="utf-8")
        payload = json.dumps({"transcript_path": str(self.transcript), "session_id": self.session, **(payload_extra or {})})
        result = subprocess.run([NODE, str(HOOK)], input=payload, capture_output=True, text=True, env={**os.environ, **env}, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_silent_below_half_of_a_small_window(self):
        self.assertEqual(self.run_hook([assistant_line(5, 90_000)]), "")

    def test_warns_at_half_of_the_budget_using_the_last_call(self):
        output = self.run_hook([assistant_line(5, 150_000), json.dumps({"type": "user"}), assistant_line(10, 118_000, 2_000)])
        context = json.loads(output)["hookSpecificOutput"]
        self.assertEqual(context["hookEventName"], "UserPromptSubmit")
        self.assertIn("60%", context["additionalContext"])
        self.assertIn("`pause`", context["additionalContext"])

    def test_budget_does_not_grow_with_a_large_window(self):
        self.assertIn("150%", self.run_hook([assistant_line(0, 250_000), assistant_line(0, 300_000)]))

    def test_subagent_usage_is_ignored(self):
        sidechain = json.loads(assistant_line(0, 180_000))
        sidechain["isSidechain"] = True
        self.assertEqual(self.run_hook([assistant_line(0, 40_000), json.dumps(sidechain)]), "")

    def test_silent_inside_a_subagent(self):
        self.assertEqual(self.run_hook([assistant_line(0, 150_000)], payload_extra={"agent_id": "a1"}), "")

    def test_warns_once_per_step(self):
        self.assertNotEqual(self.run_hook([assistant_line(0, 102_000)]), "")
        self.assertEqual(self.run_hook([assistant_line(0, 110_000)]), "")
        self.assertNotEqual(self.run_hook([assistant_line(0, 122_000)]), "")

    def test_percent_and_budget_are_configurable(self):
        self.assertEqual(self.run_hook([assistant_line(0, 110_000)], PM_CONTEXT_WARN_PERCENT="60"), "")
        self.assertNotEqual(self.run_hook([assistant_line(0, 60_000)], PM_CONTEXT_BUDGET="100000"), "")

    def test_invalid_settings_fall_back_to_defaults(self):
        self.assertEqual(self.run_hook([assistant_line(0, 90_000)], PM_CONTEXT_BUDGET="abc", PM_CONTEXT_WARN_PERCENT="-5"), "")

    def test_bad_input_is_ignored(self):
        result = subprocess.run([NODE, str(HOOK)], input="not json", capture_output=True, text=True, timeout=20)
        self.assertEqual((result.returncode, result.stdout), (0, ""))


if __name__ == "__main__":
    unittest.main()
