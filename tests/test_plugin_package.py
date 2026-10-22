"""Verify actual distributable contents and independently packaged skills."""

import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from activation import NAMES

SPEC = importlib.util.spec_from_file_location("package_plugin", ROOT / "scripts/package_plugin.py")
PACKAGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PACKAGE)


class PluginPackageTests(unittest.TestCase):
    def setUp(self):
        work = ROOT / "work"
        work.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=work)
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)

    def test_catalog_identity_is_consistent_and_has_no_alias_folders(self):
        expected = {"ibbuilds-pm-" + suffix for suffix in (
            "task-coordination", "context-management", "resource-selection", "source-selection",
            "execution-efficiency", "workflow-improvement", "concise-communication")}
        self.assertEqual(set(NAMES), expected)
        self.assertEqual({p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}, expected)
        for name in expected:
            folder = ROOT / "skills" / name
            text = (folder / "SKILL.md").read_text()
            metadata = yaml.safe_load(text.split("---", 2)[1])
            self.assertEqual(metadata["name"], name)
            self.assertLessEqual(len(name), 64)
            label = name.removeprefix("ibbuilds-pm-").replace("-", " ").title()
            display = f"ibbuilds PM Essentials / {label}"
            ui = yaml.safe_load((folder / "agents/openai.yaml").read_text())["interface"]
            self.assertEqual(ui["display_name"], display)
            self.assertIn("$" + name, ui["default_prompt"])
            self.assertIn("# " + display, text)

    def test_archive_contains_skills_without_private_state_or_install_side_effects(self):
        output = self.directory / "plugin.zip"
        result = PACKAGE.build(output)
        self.assertEqual(result["skills"], sorted(NAMES))
        with zipfile.ZipFile(output) as archive:
            names = archive.namelist()
            manifest = json.loads(archive.read("pm-essential-skills/plugin.json"))
            self.assertEqual(manifest["name"], "pm-essential-skills")
            for path in names:
                relative = Path(path).relative_to("pm-essential-skills")
                self.assertTrue(relative.as_posix() in {"plugin.json", "LICENSE"} or relative.parts[0] == "skills")
                self.assertEqual(archive.read(path), (ROOT / relative).read_bytes())
            self.assertFalse(any(".pm-context" in path or "__pycache__" in path for path in names))

    def test_independent_skill_folders_retain_canonical_license(self):
        canonical = (ROOT / "LICENSE").read_bytes()
        for skill in NAMES:
            self.assertEqual((ROOT / "skills" / skill / "LICENSE").read_bytes(), canonical)
        output = self.directory / "licensed-plugin.zip"
        PACKAGE.build(output)
        with zipfile.ZipFile(output) as archive:
            self.assertEqual(archive.read("pm-essential-skills/LICENSE"), canonical)

    def test_each_skill_packages_without_companion(self):
        for skill in NAMES:
            with self.subTest(skill=skill):
                root = self.directory / skill
                root.mkdir()
                shutil.copyfile(ROOT / "plugin.json", root / "plugin.json")
                shutil.copytree(ROOT / "skills" / skill, root / "skills" / skill,
                                ignore=shutil.ignore_patterns("__pycache__"))
                output = self.directory / f"{skill}.zip"
                result = PACKAGE.build(output, root)
                self.assertEqual(result["skills"], [skill])
                with zipfile.ZipFile(output) as archive:
                    self.assertIn(f"pm-essential-skills/skills/{skill}/SKILL.md", archive.namelist())


if __name__ == "__main__":
    unittest.main()
