import json
import os
import shutil
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "hooks" / "session-start.mjs"
NODE = shutil.which("node")


@unittest.skipIf(NODE is None, "node is not installed")
class SessionStartTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.cwd = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def run_hook(self, payload, **env):
        result = subprocess.run([NODE, str(HOOK)], input=json.dumps(payload), capture_output=True, text=True, env={**os.environ, **env}, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout) if result.stdout else None

    def write_handoff(self, text="# Handoff: csv export\n**Next action:** fix encoding", hours_old=0):
        path = self.cwd / "HANDOFF.md"
        path.write_text(text, encoding="utf-8")
        stamp = time.time() - hours_old * 3600
        os.utime(path, (stamp, stamp))

    def test_clear_loads_a_fresh_handoff(self):
        self.write_handoff()
        output = self.run_hook({"source": "clear", "cwd": str(self.cwd)})
        context = output["hookSpecificOutput"]["additionalContext"]
        self.assertEqual(output["hookSpecificOutput"]["hookEventName"], "SessionStart")
        self.assertIn("fix encoding", context)
        self.assertIn("Delete HANDOFF.md", context)
        self.assertIn("continue", output["systemMessage"])

    def test_startup_loads_a_fresh_handoff(self):
        self.write_handoff()
        self.assertIsNotNone(self.run_hook({"source": "startup", "cwd": str(self.cwd)}))

    def test_old_handoff_is_ignored(self):
        self.write_handoff(hours_old=100)
        self.assertIsNone(self.run_hook({"source": "clear", "cwd": str(self.cwd)}))
        self.assertIsNotNone(self.run_hook({"source": "clear", "cwd": str(self.cwd)}, PM_HANDOFF_MAX_AGE_HOURS="200"))

    def git(self, *args, hours_ago=0):
        stamp = f"@{int(time.time() - hours_ago * 3600)} +0000"
        env = {**os.environ, "GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp}
        subprocess.run(["git", "-c", "user.email=t@example.invalid", "-c", "user.name=t", *args], cwd=self.cwd, env=env, check=True, capture_output=True)

    @unittest.skipIf(shutil.which("git") is None, "git is not installed")  # runtime-allow: environment guard, same as the node check above
    def test_commits_after_the_handoff_are_flagged(self):
        self.git("init", "-q")
        (self.cwd / "a.txt").write_text("a")
        self.git("add", "-A")
        self.git("commit", "-qm", "before", hours_ago=3)
        self.write_handoff(hours_old=2)
        output = self.run_hook({"source": "clear", "cwd": str(self.cwd)})
        self.assertNotIn("since the handoff", output["hookSpecificOutput"]["additionalContext"])
        (self.cwd / "b.txt").write_text("b")
        self.git("add", "-A")
        self.git("commit", "-qm", "after the handoff")
        output = self.run_hook({"source": "clear", "cwd": str(self.cwd)})
        context = output["hookSpecificOutput"]["additionalContext"]
        self.assertIn("1 commit since the handoff", context)
        self.assertIn("after the handoff", context)
        self.assertIn("1 commit since", output["systemMessage"])

    def test_no_git_no_staleness_note(self):
        self.write_handoff(hours_old=2)
        output = self.run_hook({"source": "clear", "cwd": str(self.cwd)})
        self.assertNotIn("since the handoff", output["hookSpecificOutput"]["additionalContext"])

    def test_no_handoff_no_output(self):
        self.assertIsNone(self.run_hook({"source": "clear", "cwd": str(self.cwd)}))

    def test_compact_does_not_reload_the_handoff(self):
        self.write_handoff()
        self.assertIsNone(self.run_hook({"source": "compact", "cwd": str(self.cwd)}))

    def test_long_handoff_is_truncated(self):
        self.write_handoff("x" * 20_000)
        context = self.run_hook({"source": "clear", "cwd": str(self.cwd)})["hookSpecificOutput"]["additionalContext"]
        self.assertLess(len(context), 10_000)
        self.assertIn("truncated", context)

    def write_backlog(self, text):
        (self.cwd / "BACKLOG.md").write_text(text, encoding="utf-8")

    def test_open_backlog_items_are_shown_to_the_user_only(self):
        self.write_backlog("- [x] 2026-11-01 done thing\n- [ ] 2026-11-18 book flights to Lisbon. Context: lit review\n- [ ] 2026-11-18 leave rota\n")
        output = self.run_hook({"source": "startup", "cwd": str(self.cwd)})
        self.assertIn("2 parked items", output["systemMessage"])
        self.assertIn("book flights to Lisbon", output["systemMessage"])
        self.assertNotIn("hookSpecificOutput", output)

    def test_backlog_and_handoff_are_both_reported(self):
        self.write_handoff()
        self.write_backlog("- [ ] 2026-11-18 leave rota\n")
        output = self.run_hook({"source": "clear", "cwd": str(self.cwd)})
        self.assertIn("1 parked item.", output["systemMessage"])
        self.assertIn("fix encoding", output["hookSpecificOutput"]["additionalContext"])

    def test_plain_bullets_count_as_open_items(self):
        self.write_backlog("# Backlog\n\nSome notes.\n\n- Redesign site/index.html (parked 2026-11-18)\n* [X] old\n1. leave rota\n")
        message = self.run_hook({"source": "startup", "cwd": str(self.cwd)})["systemMessage"]
        self.assertIn("2 parked items. First: Redesign site/index.html", message)

    def test_finished_backlog_is_silent(self):
        self.write_backlog("- [x] 2026-11-01 done thing\n")
        self.assertIsNone(self.run_hook({"source": "startup", "cwd": str(self.cwd)}))
        self.write_backlog("- [ ] 2026-11-18 leave rota\n")
        self.assertIsNone(self.run_hook({"source": "resume", "cwd": str(self.cwd)}))

    def test_resume_is_silent(self):
        self.write_handoff()
        self.assertIsNone(self.run_hook({"source": "resume", "cwd": str(self.cwd), "context_tokens": 182_340, "prompt_cache_likely_expired": True}))

    def test_bad_input_is_ignored(self):
        result = subprocess.run([NODE, str(HOOK)], input="not json", capture_output=True, text=True, timeout=20)
        self.assertEqual((result.returncode, result.stdout), (0, ""))


if __name__ == "__main__":
    unittest.main()
