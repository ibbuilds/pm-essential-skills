"""Installer tests in disposable profiles; no live account or host operations."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("install_suite", ROOT / "scripts/install_suite.py")
INSTALL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALL)


class InstallSuiteTests(unittest.TestCase):
    def setUp(self):
        work = ROOT / "work"
        work.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=work)
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name).resolve()

    def install(self):
        return INSTALL.install(self.home, INSTALL.load_receipt(self.home))

    def test_install_activates_both_skills_without_project_files(self):
        result = self.install()
        self.assertEqual(result["status"], "installed")
        self.assertFalse(result["live_invocation_verified"])
        for name in INSTALL.SKILLS:
            self.assertTrue((self.home / "skills" / name / "SKILL.md").is_file())
        self.assertEqual(INSTALL.inspect(self.home, INSTALL.load_receipt(self.home)), [])
        self.assertFalse((self.home / ".pm-context").exists())

    def test_existing_user_instructions_and_override_precedence(self):
        base = self.home / "AGENTS.md"
        override = self.home / "AGENTS.override.md"
        base.write_bytes(b"Base instructions\r\n")
        original = b"\xef\xbb\xbfOverride instructions\r\n"
        override.write_bytes(original)
        self.install()
        self.assertEqual(base.read_bytes(), b"Base instructions\r\n")
        self.assertTrue(override.read_bytes().startswith(original))
        state = INSTALL.load_receipt(self.home)
        self.assertEqual(state["instructions"], "AGENTS.override.md")
        INSTALL.uninstall(self.home, state)
        self.assertEqual(override.read_bytes(), original)

    def test_reinstall_is_idempotent(self):
        self.install()
        rule = (self.home / "AGENTS.md").read_bytes()
        receipt = (self.home / INSTALL.RECEIPT).read_bytes()
        self.install()
        self.assertEqual((self.home / "AGENTS.md").read_bytes(), rule)
        self.assertEqual((self.home / INSTALL.RECEIPT).read_bytes(), receipt)

    def test_uninstall_restores_existing_skills_and_keeps_later_user_notes(self):
        target = self.home / "skills/context-management/SKILL.md"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"Previous personal installation\r\n")
        original = b"Existing personal preferences\r\n"
        (self.home / "AGENTS.md").write_bytes(original)
        self.install()
        with (self.home / "AGENTS.md").open("ab") as stream:
            stream.write(b"\nLater user preference\n")
        INSTALL.uninstall(self.home, INSTALL.load_receipt(self.home))
        self.assertEqual(target.read_bytes(), b"Previous personal installation\r\n")
        self.assertEqual((self.home / "AGENTS.md").read_bytes(), original + b"\nLater user preference\n")
        self.assertFalse((self.home / INSTALL.RECEIPT).exists())

    def test_modified_skill_blocks_update_and_uninstall_before_writes(self):
        self.install()
        (self.home / "skills/source-selection/SKILL.md").write_text("User customization", encoding="utf-8")
        before = (self.home / "AGENTS.md").read_bytes()
        for operation in (INSTALL.install, INSTALL.uninstall):
            with self.assertRaises(ValueError):
                operation(self.home, INSTALL.load_receipt(self.home))
        self.assertEqual((self.home / "AGENTS.md").read_bytes(), before)

    def test_new_override_reports_shadowed_activation(self):
        self.install()
        (self.home / "AGENTS.override.md").write_text("User override", encoding="utf-8")
        state = INSTALL.load_receipt(self.home)
        self.assertIn("global_rule_shadowed_by_override", INSTALL.inspect(self.home, state))
        INSTALL.uninstall(self.home, state)
        self.assertEqual((self.home / "AGENTS.override.md").read_text(), "User override")

    def test_uninstall_removes_only_owned_files(self):
        self.install()
        extra = self.home / "skills/context-management/personal.txt"
        extra.write_text("Keep", encoding="utf-8")
        INSTALL.uninstall(self.home, INSTALL.load_receipt(self.home))
        self.assertEqual(extra.read_text(), "Keep")
        self.assertFalse((self.home / "AGENTS.md").exists())

    def test_invalid_receipt_path_cannot_escape_profile(self):
        self.install()
        path = self.home / INSTALL.RECEIPT
        state = json.loads(path.read_text())
        state["files"]["skills/context-management/../../../outside"] = {"original": None}
        path.write_text(json.dumps(state), encoding="utf-8")
        with self.assertRaises(ValueError):
            INSTALL.load_receipt(self.home)

    def test_interrupted_install_is_degraded_without_blind_retry(self):
        self.install()
        (self.home / "skills/context-management/SKILL.md").unlink()
        state = INSTALL.load_receipt(self.home)
        self.assertTrue(INSTALL.inspect(self.home, state))
        with self.assertRaises(ValueError):
            self.install()

    def test_write_failure_rolls_back_prior_changes(self):
        (self.home / "AGENTS.md").write_bytes(b"Keep original\r\n")
        real_write = INSTALL.atomic_write
        calls = 0

        def fail_once(path, data):
            nonlocal calls
            calls += 1
            if calls == 3:
                raise OSError("Simulated disk failure")
            return real_write(path, data)

        with patch.object(INSTALL, "atomic_write", side_effect=fail_once):
            with self.assertRaises(OSError):
                self.install()
        self.assertEqual((self.home / "AGENTS.md").read_bytes(), b"Keep original\r\n")
        self.assertFalse((self.home / INSTALL.RECEIPT).exists())
        self.assertEqual(list((self.home / "skills").rglob("*.*")), [])

    def test_cli_uses_selected_profile_and_read_only_status(self):
        script = ROOT / "scripts/install_suite.py"
        result = subprocess.run([sys.executable, str(script), "install", "--codex-home", str(self.home)],
                                capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout)["status"], "installed")
        before = (self.home / INSTALL.RECEIPT).stat().st_mtime_ns
        subprocess.run([sys.executable, str(script), "status", "--codex-home", str(self.home)],
                       capture_output=True, text=True, check=True)
        self.assertEqual((self.home / INSTALL.RECEIPT).stat().st_mtime_ns, before)


if __name__ == "__main__":
    unittest.main()
