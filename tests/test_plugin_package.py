"""Verify actual distributable contents and independently packaged skills."""

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
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

    def test_duplicate_frontmatter_is_reported_and_later_skills_checked(self):
        import validate_repository as validator
        from unittest.mock import patch
        import contextlib
        import io

        root = self.directory / "repository"
        shutil.copytree(ROOT / "skills", root / "skills")
        shutil.copyfile(ROOT / "plugin.json", root / "plugin.json")
        first, later = sorted((root / "skills").glob("*/SKILL.md"))[:2]
        original = first.read_text(encoding="utf-8")
        later.write_text(f"---\nname: {later.parent.name}\ndescription: ''\n---\nInstructions.\n",
                         encoding="utf-8")
        original_description = yaml.safe_load(original.split("---", 2)[1])["description"]
        for key, value in (("name", first.parent.name),
                           ("description", original_description),
                           ('"description"', original_description)):
            with self.subTest(key=key):
                first.write_text(original.replace("---\n", f"---\n{key}: {json.dumps(value)}\n", 1),
                                 encoding="utf-8")
                with patch.object(validator, "ROOT", root), contextlib.redirect_stdout(io.StringIO()) as out:
                    self.assertEqual(validator.main(), 1)
                diagnostic = out.getvalue()
                self.assertIn(str(first.relative_to(root)), diagnostic)
                self.assertIn("duplicate explicit key", diagnostic)
                self.assertIn("line", diagnostic)
                self.assertIn(f"{later.relative_to(root)}: description must be nonempty", diagnostic)
                self.assertNotIn("Traceback", diagnostic)

    def test_explicit_duplicate_string_keys_in_yaml_mappings_are_rejected(self):
        from validate_repository import load_yaml

        for raw in (
            "name: first\nname: second\n",
            'description: first\n"description": second\n',
            "interface: {display_name: first, display_name: second}\n",
            "defaults: &base {author: first, author: second}\nmetadata: {<<: *base}\n",
            "&key description: first\n*key: second\n",
        ):
            with self.subTest(raw=raw):
                with self.assertRaisesRegex(yaml.YAMLError, "duplicate explicit key"):
                    load_yaml(raw)

    def test_yaml_preserves_optional_fields_aliases_and_merge_overrides(self):
        from validate_repository import load_yaml

        raw = ("name: &name pm-essential-skills-example\n"
               "description: A useful workflow.\nlicense: MIT\n"
               "compatibility: Requires Python.\nallowed-tools: Read\n"
               "metadata: &defaults {author: example, version: '1.0'}\n"
               "copy: *defaults\n"
               "override: {<<: *defaults, author: other}\n"
               "second: {<<: *defaults, version: '2.0'}\n"
               "alias: *name\n")
        parsed = load_yaml(raw)
        self.assertEqual(parsed["copy"], parsed["metadata"])
        self.assertEqual(parsed["override"], {"author": "other", "version": "1.0"})
        self.assertEqual(parsed["second"], {"author": "example", "version": "2.0"})
        self.assertEqual(parsed["alias"], parsed["name"])
        cycle = load_yaml("metadata: &cycle {self: *cycle}\n")
        self.assertIs(cycle["metadata"]["self"], cycle["metadata"])

    def test_validator_deep_yaml_is_reported_and_later_skills_checked(self):
        root = self.directory / "repository"
        shutil.copytree(ROOT / "skills", root / "skills")
        shutil.copyfile(ROOT / "plugin.json", root / "plugin.json")
        entries = sorted((root / "skills").glob("*/SKILL.md"))
        first, later = entries[:2]
        original = first.read_text(encoding="utf-8")
        ui = first.parent / "agents/openai.yaml"
        original_ui = ui.read_text(encoding="utf-8")
        later.write_text(f"---\nname: {later.parent.name}\ndescription: ''\n---\nInstructions.\n",
                         encoding="utf-8")
        code = ("import sys; from pathlib import Path; "
                "sys.path.insert(0, sys.argv[1]); import validate_repository as v; "
                "v.ROOT = Path(sys.argv[2]); sys.exit(v.main())")
        for location in ("frontmatter", "ui"):
            with self.subTest(location=location):
                first.write_text(original, encoding="utf-8")
                ui.write_text(original_ui, encoding="utf-8")
                if location == "frontmatter":
                    first.write_text("---\n" + "[" * 1100 + "\n---\nInstructions.\n", encoding="utf-8")
                else:
                    ui.write_text("[" * 1100, encoding="utf-8")
                run = subprocess.run([sys.executable, "-c", code, str(ROOT / "scripts"), str(root)],
                                     capture_output=True, text=True, timeout=10)
                self.assertEqual(run.returncode, 1, run.stderr)
                self.assertEqual(run.stderr, "")
                self.assertIn(f"{first.relative_to(root)}: YAML nesting exceeds parser capacity:", run.stdout)
                self.assertIn("maximum recursion depth exceeded", run.stdout)
                self.assertIn(f"{later.relative_to(root)}: description must be nonempty", run.stdout)
                self.assertEqual(len(run.stdout.splitlines()), 2)
                self.assertLess(len(run.stdout), 1000)

    def test_validator_reports_bad_manifest_and_unreadable_files_without_aborting(self):
        root = self.directory / "repository"
        shutil.copytree(ROOT / "skills", root / "skills")
        entry = next((root / "skills").glob("*/SKILL.md"))
        entry.write_bytes(b"\xff")
        (root / "README.md").write_bytes(b"\xff")
        (root / "bad_encoding.py").write_bytes(b"\xff")
        (root / "bad_syntax.py").write_text("def broken(\n", encoding="utf-8")
        code = ("import sys; from pathlib import Path; "
                "sys.path.insert(0, sys.argv[1]); import validate_repository as v; "
                "v.ROOT = Path(sys.argv[2]); sys.exit(v.main())")
        malformed_short = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        malformed_short["extensions"]["com.openai"]["interface"]["shortDescription"] = ["not text"]
        malformed_mapping = json.loads(json.dumps(malformed_short))
        malformed_mapping["extensions"]["com.openai"]["interface"]["shortDescription"] = {"not": "text"}
        for manifest in ([], None, malformed_short, malformed_mapping):
            with self.subTest(manifest=manifest):
                (root / "plugin.json").write_text(json.dumps(manifest), encoding="utf-8")
                run = subprocess.run([sys.executable, "-c", code, str(ROOT / "scripts"), str(root)],
                                     capture_output=True, text=True, timeout=10)
                self.assertEqual(run.returncode, 1, run.stderr)
                self.assertEqual(run.stderr, "")
                diagnostic = ("plugin short description must be text of 1-30 characters"
                              if isinstance(manifest, dict) else "plugin manifest must be a mapping")
                self.assertIn(f"plugin.json: {diagnostic}", run.stdout)
                self.assertIn(f"{entry.relative_to(root)}: cannot read skill entrypoint:", run.stdout)
                self.assertIn("README.md: cannot read Markdown:", run.stdout)
                self.assertIn("bad_encoding.py:", run.stdout)
                self.assertIn("bad_syntax.py:", run.stdout)
                self.assertNotIn("Traceback", run.stdout)

    def test_catalog_identity_is_consistent_and_has_no_alias_folders(self):
        expected = {"pm-essential-skills-" + suffix for suffix in (
            "task-coordination", "context-management", "resource-selection", "source-selection",
            "execution-efficiency", "workflow-improvement", "concise-communication")}
        self.assertEqual(set(NAMES), expected)
        self.assertEqual({p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}, expected)
        for name in expected:
            folder = ROOT / "skills" / name
            text = (folder / "SKILL.md").read_text(encoding="utf-8")
            metadata = yaml.safe_load(text.split("---", 2)[1])
            self.assertEqual(metadata["name"], name)
            self.assertLessEqual(len(name), 64)
            label = name.removeprefix("pm-essential-skills-").replace("-", " ").title()
            display = f"PM Essential Skills / {label}"
            ui = yaml.safe_load((folder / "agents/openai.yaml").read_text(encoding="utf-8"))["interface"]
            self.assertEqual(ui["display_name"], name)
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
