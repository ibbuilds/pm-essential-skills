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

    def legacy_installation(self, prefix=""):
        # Model an existing receipt without changing the current install catalog.
        self.install()
        state = INSTALL.load_receipt(self.home)
        files = {}
        for relative, record in state["files"].items():
            old = relative.replace("skills/pm-essential-skills-", "skills/" + prefix)
            source, destination = self.home / relative, self.home / old
            destination.parent.mkdir(parents=True, exist_ok=True)
            source.rename(destination)
            files[old] = record
        state["files"] = files
        state["skills"] = [prefix + name for name in INSTALL.BARE_SKILLS]
        (self.home / INSTALL.RECEIPT).write_text(json.dumps(state))
        return INSTALL.load_receipt(self.home)

    def test_deep_persisted_json_errors_preserve_state_and_release_locks(self):
        for relative, command in ((INSTALL.RECEIPT, "status"),
                                  (INSTALL.RECEIPT, "uninstall"),
                                  (INSTALL.JOURNAL, "recover")):
            for raw in ("[" * 10000, "[" * 10000 + '"PRIVATE_FIXTURE"' + "]" * 10000):
                with self.subTest(relative=relative, command=command, balanced=raw.endswith("]")):
                    target = self.home / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(raw, encoding="utf-8")
                    before = target.read_bytes()
                    result = subprocess.run(
                        [sys.executable, str(ROOT / "scripts/install_suite.py"), command,
                         "--codex-home", str(self.home)],
                        capture_output=True, text=True, timeout=5)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, "")
                    self.assertEqual(json.loads(result.stderr), {"error":
                        "Installation state JSON is nested too deeply; preserve it for recovery"})
                    self.assertNotIn("PRIVATE_FIXTURE", result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
                    self.assertEqual(target.read_bytes(), before)
                    self.assertFalse((self.home / "pm-essential-skills/install.lock").exists())
                    target.unlink()

    def test_legacy_receipt_status_and_explicit_uninstall_are_supported(self):
        state = self.legacy_installation()
        self.assertEqual(INSTALL.selected_skills(state), list(INSTALL.BARE_SKILLS))
        self.assertEqual(INSTALL.inspect(self.home, state), [])
        extra = self.home / "skills/context-management/personal.txt"
        extra.write_text("Keep my notes")
        before = (self.home / INSTALL.RECEIPT).read_bytes()
        with self.assertRaisesRegex(ValueError, "explicit migration"):
            INSTALL.install(self.home, state)
        self.assertEqual((self.home / INSTALL.RECEIPT).read_bytes(), before)
        INSTALL.uninstall(self.home, state)
        self.assertEqual(extra.read_text(), "Keep my notes")
        self.assertFalse((self.home / "skills/context-management/SKILL.md").exists())

    def test_legacy_customization_is_preserved(self):
        state = self.legacy_installation()
        target = self.home / "skills/context-management/SKILL.md"
        target.write_text("Custom old skill")
        with self.assertRaisesRegex(ValueError, "Preserving modified installation"):
            INSTALL.uninstall(self.home, state)
        self.assertEqual(target.read_text(), "Custom old skill")

    def test_unmanaged_legacy_copy_blocks_new_install_without_writes(self):
        target = self.home / "skills/context-management/SKILL.md"
        target.parent.mkdir(parents=True)
        target.write_text("Custom old skill")
        with self.assertRaisesRegex(ValueError, "explicit migration"):
            self.install()
        self.assertEqual(target.read_text(), "Custom old skill")
        self.assertFalse((self.home / INSTALL.RECEIPT).exists())
        self.assertFalse((self.home / "skills/pm-essential-skills-context-management").exists())

    def test_legacy_interrupted_transaction_can_be_recovered(self):
        relative = "skills/context-management/SKILL.md"
        target = self.home / relative
        target.parent.mkdir(parents=True)
        target.write_bytes(b"interrupted")
        journal = self.home / INSTALL.JOURNAL
        journal.parent.mkdir(parents=True)
        journal.write_text(json.dumps({"version": 1, "files": {relative: {
            "before": INSTALL.encode(b"original"), "after": INSTALL.encode(b"interrupted")}}}))
        self.assertEqual(INSTALL.recover(self.home)["status"], "recovered")
        self.assertEqual(target.read_bytes(), b"original")

    def test_previous_publisher_prefix_receipt_and_edits_are_preserved(self):
        state = self.legacy_installation("ibbuilds-pm-")
        self.assertEqual(INSTALL.selected_skills(state),
                         ["ibbuilds-pm-" + name for name in INSTALL.BARE_SKILLS])
        self.assertEqual(INSTALL.inspect(self.home, state), [])
        target = self.home / "skills/ibbuilds-pm-context-management/SKILL.md"
        original = target.read_bytes()
        target.write_bytes(b"Custom publisher-prefixed skill")
        for operation in (INSTALL.install, INSTALL.uninstall):
            with self.assertRaises(ValueError):
                operation(self.home, state)
        self.assertEqual(target.read_bytes(), b"Custom publisher-prefixed skill")
        # An explicit uninstall is supported once the user has reconciled edits.
        target.write_bytes(original)
        INSTALL.uninstall(self.home, state)
        self.assertFalse(target.exists())

    def test_previous_publisher_prefix_recovery_and_unmanaged_copy(self):
        relative = "skills/ibbuilds-pm-context-management/SKILL.md"
        target = self.home / relative
        target.parent.mkdir(parents=True)
        target.write_bytes(b"interrupted")
        journal = self.home / INSTALL.JOURNAL
        journal.parent.mkdir(parents=True)
        journal.write_text(json.dumps({"version": 1, "files": {relative: {
            "before": INSTALL.encode(b"original"), "after": INSTALL.encode(b"interrupted")}}}))
        self.assertEqual(INSTALL.recover(self.home)["status"], "recovered")
        with self.assertRaisesRegex(ValueError, "explicit migration"):
            self.install()
        self.assertEqual(target.read_bytes(), b"original")
        self.assertFalse((self.home / INSTALL.RECEIPT).exists())
        self.assertFalse((self.home / "skills/pm-essential-skills-context-management").exists())
        self.assertFalse(INSTALL.owned_target("skills/ibbuilds-pm-unrelated/SKILL.md"))
        self.assertFalse(INSTALL.owned_target("skills/pm-essential-skills-unrelated/SKILL.md"))

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
        target = self.home / "skills/pm-essential-skills-context-management/SKILL.md"
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
        (self.home / "skills/pm-essential-skills-source-selection/SKILL.md").write_text("User customization", encoding="utf-8")
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
        extra = self.home / "skills/pm-essential-skills-context-management/personal.txt"
        extra.write_text("Keep", encoding="utf-8")
        INSTALL.uninstall(self.home, INSTALL.load_receipt(self.home))
        self.assertEqual(extra.read_text(), "Keep")
        self.assertFalse((self.home / "AGENTS.md").exists())

    def test_invalid_receipt_path_cannot_escape_profile(self):
        self.install()
        path = self.home / INSTALL.RECEIPT
        state = json.loads(path.read_text())
        state["files"]["skills/pm-essential-skills-context-management/../../../outside"] = {"original": None}
        path.write_text(json.dumps(state), encoding="utf-8")
        with self.assertRaises(ValueError):
            INSTALL.load_receipt(self.home)

    def test_malformed_receipt_fields_are_rejected_without_writes(self):
        receipt = self.home / INSTALL.RECEIPT
        receipt.parent.mkdir(parents=True)
        valid = {"version": 1, "files": {}, "instructions": "AGENTS.md",
                 "instructions_existed": False, "block": INSTALL.encode(b"managed block")}
        for fields in ({"version": True}, {"version": 1.0},
                       {"files": []}, {"files": None}, {"instructions_existed": "false"},
                       {"block": None}, {"block": ""}, {"instructions": []},
                       {"files": {INSTALL.HELPER: []}},
                       {"files": {INSTALL.HELPER: {"original": 4, "sha256": "0" * 64}}},
                       {"files": {INSTALL.HELPER: {"original": None, "sha256": "bad"}}}):
            with self.subTest(fields=fields):
                raw = json.dumps({**valid, **fields}).encode()
                receipt.write_bytes(raw)
                with self.assertRaises(ValueError):
                    INSTALL.load_receipt(self.home)
                self.assertEqual(receipt.read_bytes(), raw)
                self.assertFalse((self.home / INSTALL.JOURNAL).exists())

    def test_malformed_owned_hooks_refuse_without_mutating_files(self):
        receipt = self.home / INSTALL.RECEIPT
        receipt.parent.mkdir(parents=True)
        guidance = self.home / "AGENTS.md"
        block = INSTALL.BEGIN + b"\nfixture\n" + INSTALL.END
        guidance.write_bytes(block)
        helper = self.home / INSTALL.HELPER
        helper.write_bytes(b"fixture helper")
        hooks = self.home / "hooks.json"
        original = b'{"description":"user hooks","hooks":{}}\n'
        hooks.write_bytes(original)
        merged, owned = INSTALL.hooks_content(self.home, add=True)
        hooks.write_bytes(merged)
        state = {"version": 1, "files": {INSTALL.HELPER: {
                    "original": None, "sha256": INSTALL.digest(helper.read_bytes())}},
                 "instructions": "AGENTS.md", "instructions_existed": True,
                 "block": INSTALL.encode(block)}
        malformed = [[], {}, None, False, 0, ""] + [
            {"original": None, "groups": groups} for groups in ([], {}, None, True, "invalid")]
        for ownership in malformed:
            with self.subTest(ownership=ownership):
                raw = json.dumps(state | {"hooks": ownership}).encode()
                receipt.write_bytes(raw)
                for command in ("status", "uninstall"):
                    result = subprocess.run([sys.executable, str(ROOT / "scripts/install_suite.py"),
                                             command, "--codex-home", str(self.home)],
                                            capture_output=True, text=True, timeout=5)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn("Invalid reminder hook receipt", json.loads(result.stderr)["error"])
                    self.assertNotIn("Traceback", result.stderr)
                    self.assertEqual(receipt.read_bytes(), raw)
                    self.assertEqual(guidance.read_bytes(), block)
                    self.assertEqual(helper.read_bytes(), b"fixture helper")
                    self.assertEqual(hooks.read_bytes(), merged)
                    self.assertFalse((self.home / INSTALL.JOURNAL).exists())
        # No-hooks writers omit the field; genuine records retain null originals.
        for valid in (state, state | {"hooks": owned},
                      state | {"hooks": owned | {"original": None}}):
            receipt.write_text(json.dumps(valid))
            self.assertEqual(INSTALL.load_receipt(self.home), valid)
        restored, remaining = INSTALL.hooks_content(self.home, owned)
        self.assertEqual(restored, original)
        self.assertIsNone(remaining)

    def test_malformed_receipt_cli_returns_structured_error(self):
        receipt = self.home / INSTALL.RECEIPT
        receipt.parent.mkdir(parents=True)
        receipt.write_text(json.dumps({"version": 1, "files": []}))
        result = subprocess.run([sys.executable, str(ROOT / "scripts/install_suite.py"),
                                 "status", "--codex-home", str(self.home)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("preserve it for recovery", json.loads(result.stderr)["error"])
        self.assertNotIn("Traceback", result.stderr)

    def test_interrupted_install_is_degraded_without_blind_retry(self):
        self.install()
        (self.home / "skills/pm-essential-skills-context-management/SKILL.md").unlink()
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
        source = package / "skills/pm-essential-skills-source-selection"
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
                    target = home / "skills/pm-essential-skills-source-selection/obsolete.txt"
                    target.parent.mkdir(parents=True)
                    target.write_bytes(b"Irreplaceable personal original")
                    (home / "AGENTS.md").write_bytes(b"User instructions\r\n")
                    (home / "hooks.json").write_bytes(b'{"description":"User hooks"}')
                    (source / "SKILL.md").write_bytes(b"Version one")
                    (source / "obsolete.txt").write_bytes(b"Old package file")
                    with patch.object(INSTALL, "ROOT", package):
                        if operation != "install":
                            INSTALL.install(home, None, ["pm-essential-skills-source-selection"], with_hooks=True)
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
                                    INSTALL.install(home, state, ["pm-essential-skills-source-selection"], with_hooks=True)
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

    def test_duplicate_recovery_fields_preserve_target_and_journal(self):
        target = self.home / "AGENTS.md"
        target.write_bytes(b"installed")
        journal = self.home / INSTALL.JOURNAL
        journal.parent.mkdir(parents=True)
        raw = (b'{"version":1,"files":{"AGENTS.md":{"before":"b3JpZ2luYWw=",'
               b'"before":null,"after":"aW5zdGFsbGVk"}}}')
        journal.write_bytes(raw)
        result = subprocess.run([sys.executable, str(ROOT / "scripts/install_suite.py"),
                                 "recover", "--codex-home", str(self.home)],
                                capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 2)
        self.assertIn("Duplicate installation state field; preserve it for recovery", json.loads(result.stderr)["error"])
        self.assertEqual(target.read_bytes(), b"installed")
        self.assertEqual(journal.read_bytes(), raw)
        for version in (True, 1.0):
            with self.subTest(version=version):
                raw = json.dumps({"version": version, "files": {"AGENTS.md": {
                    "before": None, "after": INSTALL.encode(b"installed")}}}).encode()
                journal.write_bytes(raw)
                with self.assertRaisesRegex(ValueError, "Invalid recovery journal"):
                    INSTALL.recover(self.home)
                self.assertEqual(target.read_bytes(), b"installed")
                self.assertEqual(journal.read_bytes(), raw)
        # A single null before value legitimately records a newly created file.
        journal.write_text(json.dumps({"version": 1, "files": {"AGENTS.md": {
            "before": None, "after": INSTALL.encode(b"installed")}}}))
        self.assertEqual(INSTALL.recover(self.home)["status"], "recovered")
        self.assertFalse(target.exists())
        self.assertFalse(journal.exists())

    def test_duplicate_receipt_fields_preserve_original_evidence(self):
        receipt = self.home / INSTALL.RECEIPT
        receipt.parent.mkdir(parents=True)
        target = self.home / INSTALL.HELPER
        target.write_bytes(b"installed")
        state = {"version": 1, "files": {INSTALL.HELPER: {
            "original": INSTALL.encode(b"original"), "sha256": INSTALL.digest(b"installed")}},
            "instructions": "AGENTS.md", "instructions_existed": True,
            "block": INSTALL.encode(INSTALL.BEGIN + b"\nmanaged\n" + INSTALL.END)}
        guidance = self.home / "AGENTS.md"
        guidance.write_bytes(INSTALL.decode(state["block"]))
        valid = json.dumps(state)
        fixtures = [valid.replace('"original": "b3JpZ2luYWw="',
                                  '"original": "b3JpZ2luYWw=", "original": null'),
                    valid.replace('"version": 1', '"version": 1, "version": 1')]
        for raw in fixtures:
            with self.subTest(raw=raw):
                receipt.write_text(raw)
                result = subprocess.run([sys.executable, str(ROOT / "scripts/install_suite.py"),
                                         "uninstall", "--codex-home", str(self.home)],
                                        capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 2)
                self.assertIn("Duplicate installation state field", json.loads(result.stderr)["error"])
                self.assertEqual(receipt.read_text(), raw)
                self.assertEqual(target.read_bytes(), b"installed")
                self.assertEqual(guidance.read_bytes(), INSTALL.decode(state["block"]))
                self.assertFalse((self.home / INSTALL.JOURNAL).exists())
        receipt.write_text(valid)
        self.assertEqual(INSTALL.load_receipt(self.home), state)

    def test_transaction_read_preserves_missing_and_regular_file_semantics(self):
        target = self.home / "AGENTS.md"
        self.assertIsNone(INSTALL.read(target))
        for content in (b"", b"original\x1a\xff\r\n"):
            target.write_bytes(content)
            self.assertEqual(INSTALL.read(target), content)
        target.unlink()
        target.mkdir()
        with self.assertRaisesRegex(ValueError, "nonregular installation file"):
            INSTALL.read(target)
        self.assertTrue(target.is_dir())

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO unavailable")
    def test_recovery_refuses_fifo_without_writes_and_resumes_after_reconciliation(self):
        first, second = self.home / "hooks.json", self.home / "AGENTS.md"
        first.write_bytes(b"new hooks")
        os.mkfifo(second)
        journal = self.home / INSTALL.JOURNAL
        journal.parent.mkdir(parents=True)
        raw = json.dumps({"version": 1, "files": {
            "hooks.json": {"before": INSTALL.encode(b"old hooks"), "after": INSTALL.encode(b"new hooks")},
            "AGENTS.md": {"before": INSTALL.encode(b"old instructions"),
                          "after": INSTALL.encode(b"new instructions")}}}).encode()
        journal.write_bytes(raw)
        command = [sys.executable, str(ROOT / "scripts/install_suite.py"),
                   "recover", "--codex-home", str(self.home)]
        result = subprocess.run(command, capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 2)
        self.assertIn("nonregular installation file", json.loads(result.stderr)["error"])
        self.assertEqual(journal.read_bytes(), raw)
        self.assertEqual(first.read_bytes(), b"new hooks")
        self.assertTrue(stat.S_ISFIFO(second.lstat().st_mode))
        # Model explicit user reconciliation; recovery itself never removes the FIFO.
        second.unlink()
        second.write_bytes(b"new instructions")
        self.assertEqual(INSTALL.recover(self.home)["status"], "recovered")
        self.assertEqual(first.read_bytes(), b"old hooks")
        self.assertEqual(second.read_bytes(), b"old instructions")
        self.assertFalse(journal.exists())

    @unittest.skipUnless(hasattr(os, "mkfifo") and hasattr(os, "O_NONBLOCK"), "Nonblocking FIFO unavailable")
    def test_transaction_read_checks_opened_file_after_path_replacement(self):
        target = self.home / "AGENTS.md"
        target.write_bytes(b"original")
        native_open = os.open

        def replace_before_open(path, flags, *args, **kwargs):
            self.assertTrue(flags & os.O_NONBLOCK)
            target.unlink()
            os.mkfifo(target)
            return native_open(path, flags, *args, **kwargs)

        with patch.object(INSTALL.os, "open", side_effect=replace_before_open):
            with self.assertRaisesRegex(ValueError, "nonregular installation file"):
                INSTALL.read(target)
        self.assertTrue(stat.S_ISFIFO(target.lstat().st_mode))

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
        target = self.home / "skills/pm-essential-skills-source-selection/scripts/read_source.py"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"Personal executable")
        target.chmod(0o751)
        instructions = self.home / "AGENTS.md"
        instructions.write_bytes(b"Shared user instructions")
        instructions.chmod(0o640)
        INSTALL.install(self.home, None, ["pm-essential-skills-source-selection"])
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o751)
        self.assertEqual(stat.S_IMODE(instructions.stat().st_mode), 0o640)
        state = INSTALL.load_receipt(self.home)
        INSTALL.uninstall(self.home, state)
        self.assertEqual(target.read_bytes(), b"Personal executable")
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o751)
        self.assertEqual(stat.S_IMODE(instructions.stat().st_mode), 0o640)
        INSTALL.install(self.home, None, ["pm-essential-skills-source-selection"])
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
        INSTALL.install(self.home, None, skills=["pm-essential-skills-source-selection"])
        extra = self.home / "other-skills"
        copy = extra / "pm-essential-skills-source-selection/SKILL.md"
        copy.parent.mkdir(parents=True)
        copy.write_text("Candidate copy", encoding="utf-8")
        # Neither uninstalled names nor nested roots are searched.
        for relative in ("pm-essential-skills-context-management/SKILL.md", "nested/source-selection/SKILL.md"):
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
        self.assertEqual(diagnostics["possible_duplicates"], ["pm-essential-skills-source-selection"])
        self.assertEqual(diagnostics["candidates"], {"pm-essential-skills-source-selection": [
            str(self.home / "skills/pm-essential-skills-source-selection/SKILL.md"), str(copy)]})
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
            (extra / "pm-essential-skills-source-selection").symlink_to(root / "pm-essential-skills-source-selection", target_is_directory=True)
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


class ConfigurationDiagnosticsTests(unittest.TestCase):
    setUp = InstallSuiteTests.setUp
    install = InstallSuiteTests.install
    def config(self, text, filename="config.toml"):
        (self.home / filename).write_text(text, encoding="utf-8")

    def diagnose(self, profile=None):
        return INSTALL.configuration_diagnostics(self.home, INSTALL.load_receipt(self.home), profile)

    @unittest.skipIf(INSTALL.tomllib is None, "stdlib TOML parser unavailable")
    def test_ordered_name_path_rules_and_profile_override_are_read_only(self):
        self.install()
        path = self.home / "skills/pm-essential-skills-source-selection/SKILL.md"
        self.config('[[skills.config]]\nname="pm-essential-skills-source-selection"\nenabled=false\n'
                    '[[skills.config]]\npath=' + json.dumps(str(path)) + '\nenabled=true\n'
                    '[skills]\ninclude_instructions=false\n')
        self.config('[[skills.config]]\nname="pm-essential-skills-source-selection"\nenabled=false\n', "Work_2-.config.toml")
        before = {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()}
        base = self.diagnose()
        selected = self.diagnose("Work_2-")
        self.assertEqual(base["configured_disabled_skills"], [])
        self.assertEqual(selected["configured_disabled_skills"], ["pm-essential-skills-source-selection"])
        self.assertIs(selected["include_instructions"], False)
        self.assertEqual(selected["effective_activation"], "unknown")
        self.assertTrue(selected["user_layer_resolution_complete"])
        self.assertEqual(before, {p: p.read_bytes() for p in self.home.rglob("*") if p.is_file()})

    @unittest.skipIf(INSTALL.tomllib is None, "stdlib TOML parser unavailable")
    def test_missing_and_malformed_config_do_not_leak_contents(self):
        self.install()
        self.assertEqual(self.diagnose()["files"][0]["status"], "missing")
        self.config('secret="never-print-me"\n[broken')
        result = self.diagnose()
        self.assertEqual(result["status"], "partial")
        self.assertNotIn("never-print-me", json.dumps(result))
        command = [sys.executable, str(ROOT / "scripts/install_suite.py"), "status", "--codex-home", str(self.home)]
        completed = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0)
        self.assertNotIn("never-print-me", completed.stdout + completed.stderr)

    def test_python310_diagnostics_unavailable_without_dependency(self):
        with patch.object(INSTALL, "tomllib", None):
            result = self.diagnose()
        self.assertEqual(result["status"], "unavailable")
        self.assertFalse(result["user_layer_resolution_complete"])
        self.assertEqual(result["files"], [])

    def test_profile_validation_prevents_escape_and_mutating_commands(self):
        for profile in ("", "../escape", "a/b", "a\\b", ".", "a.b", "é", "a b"):
            with self.subTest(profile=profile), self.assertRaises(ValueError):
                self.diagnose(profile)
        completed = subprocess.run([sys.executable, str(ROOT / "scripts/install_suite.py"),
                                    "install", "--codex-home", str(self.home), "--profile", "work"],
                                   capture_output=True, text=True)
        self.assertEqual(completed.returncode, 2)
        self.assertEqual(list(self.home.iterdir()), [])

    @unittest.skipIf(INSTALL.tomllib is None, "stdlib TOML parser unavailable")
    def test_invalid_types_ignored_selectors_relative_paths_and_unselected_profile(self):
        self.install()
        self.config('[[skills.config]]\npath="skills/pm-essential-skills-source-selection/SKILL.md"\nenabled=false\n'
                    '[[skills.config]]\nname="pm-essential-skills-source-selection"\npath="x"\nenabled=true\n')
        self.config('[[skills.config]]\nname="pm-essential-skills-source-selection"\nenabled=true\n', "unused.config.toml")
        self.assertEqual(self.diagnose()["configured_disabled_skills"], ["pm-essential-skills-source-selection"])
        self.config('[[skills.config]]\nname="pm-essential-skills-source-selection"\nenabled="false"\n')
        self.assertEqual(self.diagnose()["status"], "partial")

    @unittest.skipIf(INSTALL.tomllib is None, "stdlib TOML parser unavailable")
    def test_canonical_path_selector_and_later_name_rule(self):
        self.install()
        alias = self.home / "alias"
        try:
            alias.symlink_to(self.home / "skills", target_is_directory=True)
        except OSError as exc:
            self.skipTest(str(exc))
        self.config('[[skills.config]]\npath=' + json.dumps(str(alias / "pm-essential-skills-source-selection/SKILL.md"))
                    + '\nenabled=false\n')
        self.assertEqual(self.diagnose()["configured_disabled_skills"], ["pm-essential-skills-source-selection"])
        self.config('[[skills.config]]\nname=" pm-essential-skills-source-selection "\nenabled=true\n', "work.config.toml")
        self.assertEqual(self.diagnose("work")["configured_disabled_skills"], [])

    @unittest.skipIf(INSTALL.tomllib is None, "stdlib TOML parser unavailable")
    def test_nonregular_oversized_and_legacy_configuration_is_partial(self):
        config = self.home / "config.toml"
        config.mkdir()
        self.assertEqual(self.diagnose()["status"], "partial")
        config.rmdir()
        config.write_bytes(b"#" * (1024 * 1024 + 1))
        self.assertEqual(self.diagnose()["status"], "partial")
        self.config('[profiles.work]\nmodel="placeholder"\n')
        result = self.diagnose("work")
        self.assertEqual(result["status"], "partial")
        self.assertTrue(any("Legacy" in warning for warning in result["warnings"]))


    @unittest.skipIf(INSTALL.tomllib is None, "stdlib TOML parser unavailable")
    def test_native_nonzero_budget_and_required_enabled_contract(self):
        self.install()
        for text in ('[skills]\nmax_context_tokens=0\ninclude_instructions=false\n',
                     '[[skills.config]]\nname="pm-essential-skills-source-selection"\n'):
            with self.subTest(text=text):
                self.config(text)
                result = self.diagnose()
                self.assertEqual(result["status"], "partial")
                self.assertFalse(result["user_layer_resolution_complete"])
                self.assertEqual(result["configured_disabled_skills"], [])
        self.config('[skills]\nmax_context_tokens=1\ninclude_instructions=false\n')
        result = self.diagnose()
        self.assertEqual(result["status"], "inspected")
        self.assertIs(result["include_instructions"], False)

    @unittest.skipIf(INSTALL.tomllib is None, "stdlib TOML parser unavailable")
    def test_config_open_requests_binary_mode_and_does_not_hide_control_z_suffix(self):
        self.config('# valid comment\n' + chr(26) + '[broken')
        native_open = os.open
        calls = []
        def binary_open(path, flags, *args, **kwargs):
            calls.append(flags)
            return native_open(path, flags, *args, **kwargs)
        with patch.object(INSTALL.os, "open", binary_open):
            result = self.diagnose()
        self.assertEqual(result["status"], "partial")
        self.assertTrue(calls)
        if hasattr(os, "O_BINARY"):
            self.assertTrue(all(flags & os.O_BINARY for flags in calls))

    @unittest.skipIf(INSTALL.tomllib is None, "stdlib TOML parser unavailable")
    def test_linked_profile_is_not_read(self):
        target = self.home / "outside.toml"
        target.write_text('[[skills.config]]\nname="pm-essential-skills-source-selection"\nenabled=false\n')
        try:
            (self.home / "work.config.toml").symlink_to(target)
        except OSError as exc:
            self.skipTest(str(exc))
        result = self.diagnose("work")
        self.assertEqual(result["status"], "partial")
        self.assertFalse(result["user_layer_resolution_complete"])



if __name__ == "__main__":
    unittest.main()
