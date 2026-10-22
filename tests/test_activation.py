"""Exercise real hook contracts and the extracted user download in isolated profiles."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import activation
import install_suite
import package_installers


class ActivationTests(unittest.TestCase):
    def setUp(self):
        work = (ROOT / "work").resolve()
        work.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=work)
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.home = self.directory / "profile with spaces & punctuation"

    def test_single_skill_gets_independent_activation_and_no_other_skill(self):
        for name in install_suite.SKILLS:
            home = self.home / name
            result = install_suite.install(home, None, [name])
            self.assertEqual(result["skills"], [name])
            self.assertEqual("same-project" in result["defaults"], name == "context-management")
            self.assertEqual(install_suite.load_receipt(home)["defaults"], result["defaults"])
            self.assertTrue((home / "skills" / name / "SKILL.md").is_file())
            rule = (home / "AGENTS.md").read_text()
            self.assertIn(f"/{name}/SKILL.md", rule)
            for other in set(install_suite.SKILLS) - {name}:
                self.assertFalse((home / "skills" / other).exists())
                self.assertNotIn(f"/{other}/SKILL.md", rule)

    def test_installing_another_skill_keeps_the_first(self):
        install_suite.install(self.home, None, ["source-selection"])
        result = install_suite.install(self.home, install_suite.load_receipt(self.home), ["context-management"])
        self.assertEqual(result["skills"], ["context-management", "source-selection"])
        self.assertIn("same-project", result["defaults"])
        result = install_suite.install(self.home, install_suite.load_receipt(self.home), ["execution-efficiency"])
        self.assertIn("same-project", result["defaults"])

    def test_skill_catalogs_cover_every_shipped_entrypoint(self):
        shipped = sorted(path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(sorted(install_suite.SKILLS), shipped)
        self.assertEqual(sorted(package_installers.SKILLS), shipped)
        self.assertEqual(sorted(activation.NAMES), shipped)

    def test_three_skill_upgrade_preserves_existing_install_and_hook_selection(self):
        original = b"Keep my existing preferences.\n"
        self.home.mkdir(parents=True)
        (self.home / "AGENTS.md").write_bytes(original)
        install_suite.install(self.home, None, ["context-management", "execution-efficiency", "source-selection"], with_hooks=True)
        state = install_suite.load_receipt(self.home)
        before = {name: (self.home / "skills" / name / "SKILL.md").read_bytes()
                  for name in state["skills"]}
        result = install_suite.install(self.home, state)
        self.assertEqual(result["skills"], list(install_suite.SKILLS))
        self.assertEqual(install_suite.inspect(self.home, install_suite.load_receipt(self.home)), [])
        for name, content in before.items():
            self.assertEqual((self.home / "skills" / name / "SKILL.md").read_bytes(), content)
        for event in ("SessionStart", "UserPromptSubmit"):
            context = activation.handle({"hook_event_name": event}, self.home)["hookSpecificOutput"]["additionalContext"]
            for name in install_suite.SKILLS:
                self.assertIn(f"/{name}/SKILL.md", context)
        install_suite.uninstall(self.home, install_suite.load_receipt(self.home))
        self.assertEqual((self.home / "AGENTS.md").read_bytes(), original)
        self.assertFalse((self.home / "hooks.json").exists())

    def test_hooks_merge_idempotently_and_uninstall_preserves_other_hooks(self):
        self.home.mkdir(parents=True)
        unrelated = {"hooks": [{"type": "command", "command": "user-command"}]}
        original = (json.dumps({"description": "User hooks", "hooks": {"SessionStart": [unrelated]}}) + "\n").encode()
        (self.home / "hooks.json").write_bytes(original)
        install_suite.install(self.home, None, with_hooks=True)
        state = install_suite.load_receipt(self.home)
        self.assertEqual(install_suite.inspect(self.home, state), [])
        first = (self.home / "hooks.json").read_bytes()
        install_suite.install(self.home, state)
        self.assertEqual((self.home / "hooks.json").read_bytes(), first)
        install_suite.uninstall(self.home, install_suite.load_receipt(self.home))
        self.assertEqual((self.home / "hooks.json").read_bytes(), original)

    def test_later_user_hook_additions_survive_uninstall(self):
        install_suite.install(self.home, None, with_hooks=True)
        path = self.home / "hooks.json"
        config = json.loads(path.read_text())
        config["hooks"]["Stop"] = [{"hooks": [{"type": "command", "command": "later"}]}]
        path.write_text(json.dumps(config))
        install_suite.uninstall(self.home, install_suite.load_receipt(self.home))
        self.assertEqual(json.loads(path.read_text())["hooks"], {"Stop": config["hooks"]["Stop"]})

    def test_hook_context_uses_selected_paths_without_prompt_or_project_content(self):
        install_suite.install(self.home, None, ["source-selection"], with_hooks=True)
        before = {path: path.stat().st_mtime_ns for path in self.home.rglob("*") if path.is_file()}
        for event in ("SessionStart", "UserPromptSubmit"):
            response = activation.handle({"hook_event_name": event, "prompt": "UNTRUSTED_PROMPT"}, self.home)
            self.assertEqual(response["hookSpecificOutput"]["hookEventName"], event)
            context = response["hookSpecificOutput"]["additionalContext"]
            self.assertIn("/source-selection/SKILL.md", context)
            self.assertNotIn("/context-management/SKILL.md", context)
            self.assertNotIn("UNTRUSTED_PROMPT", context)
            self.assertLess(len(context.split()), 220)
            self.assertEqual(set(response), {"hookSpecificOutput"})
        self.assertEqual(before, {path: path.stat().st_mtime_ns for path in self.home.rglob("*") if path.is_file()})

    def test_prompt_reminder_is_smaller_than_session_guidance(self):
        install_suite.install(self.home, None, with_hooks=True)
        session = activation.handle({"hook_event_name": "SessionStart"}, self.home)
        prompt = activation.handle({"hook_event_name": "UserPromptSubmit"}, self.home)
        self.assertLess(len(prompt["hookSpecificOutput"]["additionalContext"]),
                        len(session["hookSpecificOutput"]["additionalContext"]))

    def test_malformed_hook_input_does_not_interrupt_work(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/activation.py"), "--codex-home", str(self.home)],
                                input="{broken", text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), {})
        self.assertFalse(self.home.exists())

    def test_changed_hook_definition_is_preserved(self):
        install_suite.install(self.home, None, with_hooks=True)
        path = self.home / "hooks.json"
        path.write_text('{"hooks": {}}')
        with self.assertRaises(ValueError):
            install_suite.uninstall(self.home, install_suite.load_receipt(self.home))
        self.assertEqual(path.read_text(), '{"hooks": {}}')

    def test_existing_install_lock_is_not_removed(self):
        lock = self.home / "pm-essential-skills/install.lock"
        lock.parent.mkdir(parents=True)
        lock.write_text("Existing installer")
        result = subprocess.run([sys.executable, str(ROOT / "scripts/install_suite.py"), "install", "--codex-home", str(self.home)],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(lock.read_text(), "Existing installer")
        self.assertFalse((self.home / "AGENTS.md").exists())

    def test_extracted_individual_download_installs_and_uninstalls(self):
        for skill in install_suite.SKILLS:
            package = self.directory / f"{skill}.zip"
            package_installers.build(package, [skill])
            extracted = self.directory / f"download-{skill}"
            with zipfile.ZipFile(package) as archive:
                self.assertNotIn("plugin.json", archive.namelist())
                self.assertNotIn(".pm-context/index.md", archive.namelist())
                guide = archive.read("START-HERE.txt").decode("utf-8")
                self.assertEqual("superseded-source archival" in guide, skill == "context-management")
                archive.extractall(extracted)
            home = self.home / skill
            script = extracted / "scripts/install_suite.py"
            for command in ("install", "status", "uninstall"):
                result = subprocess.run([sys.executable, str(script), command, "--codex-home", str(home)],
                                        text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                if command != "uninstall":
                    self.assertEqual(json.loads(result.stdout)["skills"], [skill])
            self.assertFalse((home / "AGENTS.md").exists())

    def test_extracted_full_download_installs_selected_catalog_and_runs_hook(self):
        package = self.directory / "full-suite.zip"
        package_installers.build(package, install_suite.SKILLS)
        extracted = self.directory / "full download"
        with zipfile.ZipFile(package) as archive:
            archive.extractall(extracted)
        script = extracted / "scripts/install_suite.py"
        result = subprocess.run([sys.executable, str(script), "install", "--hooks",
                                 "--codex-home", str(self.home)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["skills"], list(install_suite.SKILLS))
        helper = self.home / install_suite.HELPER
        result = subprocess.run([sys.executable, str(helper)],
                                input=json.dumps({"hook_event_name": "UserPromptSubmit"}),
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
        for name in install_suite.SKILLS:
            self.assertIn(f"/{name}/SKILL.md", context)
        self.assertIn("Select only relevant skills", context)
        self.assertIn("disabled", context)
        install_suite.uninstall(self.home, install_suite.load_receipt(self.home))
        self.assertFalse(helper.exists())

    @unittest.skipUnless(os.name == "nt", "Windows installer launch")
    def test_windows_launcher_rejects_extra_options_before_installing(self):
        environment = dict(os.environ, CODEX_HOME=str(self.home))
        result = subprocess.run(["cmd.exe", "/d", "/c", "Install.cmd", "install", "--hooks"],
                                cwd=ROOT, env=environment, text=True, capture_output=True, timeout=45)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("Extra arguments are not supported", result.stdout)
        self.assertFalse(self.home.exists())

    @unittest.skipUnless(os.name == "nt", "Windows installer launch")
    def test_windows_launcher_runs_complete_download_flow(self):
        package = self.directory / "suite.zip"
        package_installers.build(package, install_suite.SKILLS)
        extracted = self.directory / "suite download"
        with zipfile.ZipFile(package) as archive:
            archive.extractall(extracted)
        environment = dict(os.environ, CODEX_HOME=str(self.home))
        for command in ("install", "status", "uninstall"):
            # The only cmd shell usage is the batch entrypoint under test; deletion stays in Python.
            result = subprocess.run(["cmd.exe", "/d", "/c", "Install.cmd", command], cwd=extracted,
                                    env=environment, text=True, capture_output=True, timeout=45)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse((self.home / "AGENTS.md").exists())


if __name__ == "__main__":
    unittest.main()
