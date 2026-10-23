"""Check resource closure and helper execution without a companion or AGENTS.md."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from skill_resources import resource_errors
import package_installers
import package_plugin


class IndependentResourceTests(unittest.TestCase):
    def setUp(self):
        work = ROOT / "work"
        work.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=work)
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.skill = self.directory / "skills/pm-essential-skills-context-management"
        self.skill.mkdir(parents=True)

    def test_nested_resources_resolve_within_skill(self):
        refs = self.skill / "references"
        refs.mkdir()
        (self.skill / "SKILL.md").write_text("[details](references/details.md)")
        (refs / "details.md").write_text("[main](../SKILL.md#main)")
        self.assertEqual(resource_errors(self.skill), [])

    def test_existing_repository_resource_is_not_an_independent_dependency(self):
        (self.directory / "README.md").write_text("Not shipped with a bare skill")
        (self.skill / "SKILL.md").write_text("[required](../../README.md)")
        self.assertEqual(len(resource_errors(self.skill)), 1)

    def test_missing_local_resource_is_reported(self):
        (self.skill / "SKILL.md").write_text("[details](references/missing.md)")
        self.assertEqual(len(resource_errors(self.skill)), 1)

    def test_urls_anchors_and_fenced_examples_are_not_packaged_dependencies(self):
        (self.skill / "SKILL.md").write_text(
            "[official](https://example.org/docs) [here](#main)\n"
            "```markdown\n[example](not-a-resource.md)\n```\n")
        self.assertEqual(resource_errors(self.skill), [])

    def test_machine_local_links_cannot_hide_as_url_schemes(self):
        for target in ("C:/machine/skill.md", "C:\\machine\\skill.md", "file:///machine/skill.md"):
            with self.subTest(target=target):
                (self.skill / "SKILL.md").write_text(f"[required]({target})")
                self.assertEqual(len(resource_errors(self.skill)), 1)

    def test_builders_reject_unshipped_resources_before_writing_archive(self):
        (self.skill / "SKILL.md").write_text("[required](missing.md)")
        for builder in (lambda path: package_plugin.build(path, self.directory),
                        lambda path: package_installers.build(path, ["pm-essential-skills-context-management"], self.directory)):
            output = self.directory / "invalid.zip"
            with self.assertRaises(ValueError):
                builder(output)
            self.assertFalse(output.exists())

    def test_unreadable_markdown_is_reported_and_builders_reject_it(self):
        (self.skill / "SKILL.md").write_bytes(b"\xff")
        (self.skill / "later.md").write_text("[missing](missing.md)", encoding="utf-8")
        errors = resource_errors(self.skill)
        self.assertTrue(any("Cannot read skill resource SKILL.md:" in error for error in errors))
        self.assertTrue(any("Missing skill resource: later.md: missing.md" in error for error in errors))
        for builder in (lambda path: package_plugin.build(path, self.directory),
                        lambda path: package_installers.build(path, [self.skill.name], self.directory)):
            output = self.directory / "invalid.zip"
            with self.assertRaisesRegex(ValueError, "Cannot read skill resource"):
                builder(output)
            self.assertFalse(output.exists())

    def test_symlink_loop_is_reported_and_later_links_are_checked(self):
        loop = self.skill / "loop"
        try:
            loop.symlink_to(loop.name)
        except (OSError, NotImplementedError):
            self.skipTest("Symlink creation unavailable")
        (self.skill / "SKILL.md").write_text("[loop](loop) [missing](missing.md)", encoding="utf-8")
        errors = resource_errors(self.skill)
        # Newer Python versions may leave a non-strict loop unresolved and
        # report it as missing; either result must still reject the resource.
        self.assertTrue(any(error.startswith(("Unreadable skill resource: SKILL.md: loop:",
                                              "Missing skill resource: SKILL.md: loop"))
                            for error in errors))
        self.assertTrue(any("Missing skill resource: SKILL.md: missing.md" in error for error in errors))

    def test_each_bare_skill_runs_its_helper_without_activation_or_companion(self):
        cases = {
            "pm-essential-skills-context-management": ("assess_context.py", {
                "project_mode": "project", "safe_checkpoint": True,
                "new_phase": True, "substantial_history": True}, "ask_thread_choice"),
            "pm-essential-skills-source-selection": ("assess_source.py", {
                "source_id": "fixture:requested-document", "content_available": False}, "fetch"),
        }
        for skill, (helper, observation, expected) in cases.items():
            with self.subTest(skill=skill):
                root = self.directory / skill
                shutil.copytree(ROOT / "skills" / skill, root / "skills" / skill,
                                ignore=shutil.ignore_patterns("__pycache__"))
                shutil.copyfile(ROOT / "plugin.json", root / "plugin.json")
                output = self.directory / f"{skill}.zip"
                package_plugin.build(output, root)
                extracted = self.directory / f"extracted-{skill}"
                with zipfile.ZipFile(output) as archive:
                    archive.extractall(extracted)
                folder = extracted / "pm-essential-skills/skills" / skill
                self.assertEqual(resource_errors(folder), [])
                self.assertEqual([p.name for p in folder.parent.iterdir()], [skill])
                self.assertFalse(list(extracted.rglob("AGENTS.md")))
                result = subprocess.run([sys.executable, str(folder / "scripts" / helper)],
                                        input=json.dumps(observation), text=True, capture_output=True,
                                        cwd=extracted, timeout=15)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)["action"], expected)


if __name__ == "__main__":
    unittest.main()
