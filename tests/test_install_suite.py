"""Installer tests in disposable profiles; no live account or host operations."""

import importlib.util
import json
import os
import stat
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

    def test_install_activates_all_skills_without_project_files(self):
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

        def fail_once(path, data, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 3:
                raise OSError("Simulated disk failure")
            return real_write(path, data, **kwargs)

        with patch.object(INSTALL, "atomic_write", side_effect=fail_once):
            with self.assertRaises(OSError):
                self.install()
        self.assertEqual((self.home / "AGENTS.md").read_bytes(), b"Keep original\r\n")
        self.assertFalse((self.home / INSTALL.RECEIPT).exists())
        self.assertEqual(list((self.home / "skills").rglob("*.*")), [])

    def test_interrupted_operations_recover_original_bytes_at_every_write(self):
        # A minimal package makes every checkpoint deterministic, including a
        # retired file whose pre-install original must survive an upgrade crash.
        package = self.home / "package"
        source = package / "skills/source-selection"
        source.mkdir(parents=True)
        (source / "SKILL.md").write_bytes(b"Version one")
        (source / "obsolete.txt").write_bytes(b"Old package file")
        helper = package / "scripts/activation.py"
        helper.parent.mkdir()
        helper.write_bytes(b"# helper")

        def snapshot(home):
            return {path.relative_to(home).as_posix(): path.read_bytes()
                    for path in home.rglob("*") if path.is_file()
                    and path.relative_to(home).as_posix() != INSTALL.JOURNAL}

        real_write = INSTALL.atomic_write
        for operation in ("install", "upgrade", "uninstall"):
            # journal + receipt + selected files + guidance + hooks/helper
            for checkpoint in range(1, 9):
                with self.subTest(operation=operation, checkpoint=checkpoint):
                    home = self.home / f"{operation}-{checkpoint}"
                    target = home / "skills/source-selection/obsolete.txt"
                    target.parent.mkdir(parents=True)
                    target.write_bytes(b"Irreplaceable personal original")
                    (home / "AGENTS.md").write_bytes(b"User instructions\r\n")
                    (home / "hooks.json").write_bytes(b'{"description":"User hooks"}')
                    (source / "SKILL.md").write_bytes(b"Version one")
                    (source / "obsolete.txt").write_bytes(b"Old package file")
                    with patch.object(INSTALL, "ROOT", package):
                        if operation != "install":
                            INSTALL.install(home, None, ["source-selection"], with_hooks=True)
                        before = snapshot(home)
                        if operation == "upgrade":
                            (source / "obsolete.txt").unlink()
                            (source / "SKILL.md").write_bytes(b"Version two")
                            (source / "new.txt").write_bytes(b"New package file")
                        calls = 0

                        def interrupt_after_write(path, data, **kwargs):
                            nonlocal calls
                            calls += 1
                            real_write(path, data, **kwargs)
                            if calls == checkpoint:
                                raise KeyboardInterrupt("Simulated process interruption")

                        interrupted = False
                        with patch.object(INSTALL, "atomic_write", side_effect=interrupt_after_write):
                            try:
                                state = INSTALL.load_receipt(home)
                                if operation == "uninstall":
                                    INSTALL.uninstall(home, state)
                                else:
                                    INSTALL.install(home, state, ["source-selection"], with_hooks=True)
                            except KeyboardInterrupt:
                                interrupted = True
                        if interrupted:
                            self.assertTrue(INSTALL.pending_transaction(home))
                            for action in (INSTALL.install, INSTALL.uninstall):
                                with self.assertRaisesRegex(ValueError, "needs recovery"):
                                    action(home, INSTALL.load_receipt(home))
                            self.assertEqual(INSTALL.recover(home)["status"], "recovered")
                            self.assertEqual(snapshot(home), before)
                            self.assertFalse(INSTALL.pending_transaction(home))
                            self.assertEqual(INSTALL.recover(home)["status"], "nothing_to_recover")
                        (source / "new.txt").unlink(missing_ok=True)
                        if checkpoint == 8:
                            self.assertFalse(interrupted, "Increase checkpoint bound to cover every write")

    def test_recovery_refuses_later_edits_before_writing_and_can_resume(self):
        first, second = self.home / "AGENTS.md", self.home / "hooks.json"
        first.write_bytes(b"old instructions")
        second.write_bytes(b"old hooks")
        real_write = INSTALL.atomic_write

        def interrupt(path, data, **kwargs):
            real_write(path, data, **kwargs)
            if path == second:
                raise KeyboardInterrupt()

        with patch.object(INSTALL, "atomic_write", side_effect=interrupt):
            with self.assertRaises(KeyboardInterrupt):
                INSTALL.apply({first: b"new instructions", second: b"new hooks"}, self.home)
        first.write_bytes(b"later user edit")
        with self.assertRaisesRegex(ValueError, "later changes"):
            INSTALL.recover(self.home)
        self.assertEqual(second.read_bytes(), b"new hooks")
        first.write_bytes(b"new instructions")
        # Recovery can itself be interrupted and restarted without losing backups.
        with patch.object(INSTALL, "atomic_write", side_effect=interrupt):
            with self.assertRaises(KeyboardInterrupt):
                INSTALL.recover(self.home)
        self.assertTrue(INSTALL.pending_transaction(self.home))
        INSTALL.recover(self.home)
        self.assertEqual(first.read_bytes(), b"old instructions")
        self.assertEqual(second.read_bytes(), b"old hooks")

    def test_failed_rollback_keeps_journal_and_cli_recovers(self):
        target = self.home / "AGENTS.md"
        target.write_bytes(b"Keep original")
        real_write = INSTALL.atomic_write

        def fail_rollback(path, data, **kwargs):
            if path == target:
                if data == b"new":
                    real_write(path, data, **kwargs)
                raise OSError("Persistent write failure")
            real_write(path, data, **kwargs)

        with patch.object(INSTALL, "atomic_write", side_effect=fail_rollback):
            with self.assertRaises(OSError):
                INSTALL.apply({target: b"new"}, self.home)
        self.assertTrue(INSTALL.pending_transaction(self.home))
        command = [sys.executable, str(ROOT / "scripts/install_suite.py")]
        status = subprocess.run(command + ["status", "--codex-home", str(self.home)],
                                capture_output=True, text=True)
        self.assertEqual(status.returncode, 2)
        self.assertIn("needs recovery", json.loads(status.stderr)["error"])
        result = subprocess.run(command + ["recover", "--codex-home", str(self.home)],
                                capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout)["status"], "recovered")
        self.assertEqual(target.read_bytes(), b"Keep original")

    @unittest.skipIf(os.name == "nt", "POSIX access mode semantics")
    def test_original_modes_survive_install_uninstall_and_legacy_receipts(self):
        target = self.home / "skills/source-selection/scripts/read_source.py"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"Personal executable")
        target.chmod(0o751)
        instructions = self.home / "AGENTS.md"
        instructions.write_bytes(b"Shared user instructions")
        instructions.chmod(0o640)
        INSTALL.install(self.home, None, ["source-selection"])
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o751)
        self.assertEqual(stat.S_IMODE(instructions.stat().st_mode), 0o640)
        state = INSTALL.load_receipt(self.home)
        INSTALL.uninstall(self.home, state)
        self.assertEqual(target.read_bytes(), b"Personal executable")
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o751)
        self.assertEqual(stat.S_IMODE(instructions.stat().st_mode), 0o640)
        INSTALL.install(self.home, None, ["source-selection"])
        state = INSTALL.load_receipt(self.home)
        for record in state["files"].values():
            record.pop("original_mode")
            record.pop("mode")
        # Old releases saved bytes, not modes: preserve the current mode instead
        # of inventing or expanding permissions that cannot be recovered.
        target.chmod(0o600)
        INSTALL.uninstall(self.home, state)
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o600)

    @unittest.skipIf(os.name == "nt", "POSIX access mode semantics")
    def test_recovery_restores_modes_and_refuses_later_chmod(self):
        target = self.home / "AGENTS.md"
        target.write_bytes(b"original")
        target.chmod(0o751)
        real_write = INSTALL.atomic_write

        def interrupt(path, data, **kwargs):
            real_write(path, data, **kwargs)
            if path == target:
                raise KeyboardInterrupt()

        with patch.object(INSTALL, "atomic_write", side_effect=interrupt):
            with self.assertRaises(KeyboardInterrupt):
                INSTALL.apply({target: b"updated"}, self.home, {target: 0o640})
        target.chmod(0o444)
        with self.assertRaisesRegex(ValueError, "later changes"):
            INSTALL.recover(self.home)
        self.assertEqual(target.read_bytes(), b"updated")
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o444)
        target.chmod(0o640)
        INSTALL.recover(self.home)
        self.assertEqual(target.read_bytes(), b"original")
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o751)

    def test_cli_uses_selected_profile_and_read_only_status(self):
        script = ROOT / "scripts/install_suite.py"
        result = subprocess.run([sys.executable, str(script), "install", "--codex-home", str(self.home)],
                                capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout)["status"], "installed")
        before = (self.home / INSTALL.RECEIPT).stat().st_mtime_ns
        subprocess.run([sys.executable, str(script), "status", "--codex-home", str(self.home)],
                       capture_output=True, text=True, check=True)
        self.assertEqual((self.home / INSTALL.RECEIPT).stat().st_mtime_ns, before)

    def test_optional_copy_diagnostics_are_read_only_and_do_not_degrade_status(self):
        INSTALL.install(self.home, None, skills=["source-selection"])
        extra = self.home / "other-skills"
        copy = extra / "source-selection/SKILL.md"
        copy.parent.mkdir(parents=True)
        copy.write_text("Candidate copy", encoding="utf-8")
        # Neither uninstalled names nor nested roots are searched.
        for relative in ("context-management/SKILL.md", "nested/source-selection/SKILL.md"):
            path = extra / relative
            path.parent.mkdir(parents=True)
            path.write_text("Not in scope", encoding="utf-8")
        before = {path: path.read_bytes() for path in self.home.rglob("*") if path.is_file()}
        command = [sys.executable, str(ROOT / "scripts/install_suite.py"),
                   "status", "--codex-home", str(self.home)]
        plain = json.loads(subprocess.run(command, capture_output=True, text=True, check=True).stdout)
        self.assertNotIn("skill_copy_diagnostics", plain)
        result = subprocess.run(command + ["--check-skill-root", str(extra)],
                                capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        diagnostics = data.pop("skill_copy_diagnostics")
        self.assertEqual(data, plain)
        self.assertEqual(diagnostics["possible_duplicates"], ["source-selection"])
        self.assertEqual(diagnostics["candidates"], {"source-selection": [
            str(self.home / "skills/source-selection/SKILL.md"), str(copy)]})
        self.assertEqual(diagnostics["activation"], "unknown")
        self.assertEqual(diagnostics["inspection_errors"], [])
        self.assertEqual(before, {path: path.read_bytes() for path in self.home.rglob("*") if path.is_file()})

    def test_copy_diagnostics_deduplicate_root_and_skill_symlink_aliases(self):
        self.install()
        root = self.home / "skills"
        alias = self.home / "alias"
        extra = self.home / "other-skills"
        extra.mkdir()
        try:
            alias.symlink_to(root, target_is_directory=True)
            (extra / "source-selection").symlink_to(root / "source-selection", target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"Symlinks unavailable: {exc}")
        result = INSTALL.skill_copy_diagnostics(self.home, INSTALL.load_receipt(self.home),
                                                [root, alias, extra])
        self.assertEqual(result["possible_duplicates"], [])
        self.assertEqual(result["roots"], [str(root), str(extra)])
        self.assertTrue(all(len(paths) == 1 for paths in result["candidates"].values()))

    def test_copy_diagnostics_report_missing_and_inaccessible_roots(self):
        self.install()
        missing = self.home / "missing"
        denied = self.home / "denied"
        denied.mkdir()
        original_stat = Path.stat

        def checked_stat(path, *args, **kwargs):
            if path == denied:
                raise PermissionError("Simulated inaccessible root")
            return original_stat(path, *args, **kwargs)

        with patch.object(Path, "stat", checked_stat):
            result = INSTALL.skill_copy_diagnostics(self.home, INSTALL.load_receipt(self.home),
                                                    [missing, denied])
        self.assertEqual([item["path"] for item in result["inspection_errors"]],
                         [str(missing), str(denied)])
        self.assertEqual(result["possible_duplicates"], [])

    def test_copy_option_rejected_before_install_writes(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/install_suite.py"),
                                 "install", "--codex-home", str(self.home),
                                 "--check-skill-root", str(self.home / "skills")],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("status only", json.loads(result.stderr)["error"])
        self.assertEqual(list(self.home.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
