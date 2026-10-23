"""Protect package inputs and prior downloads when packaging fails."""

import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import archive_builder
import package_installers
import package_plugin


class ArchiveSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ("plugin.json", "Install.cmd", "scripts/install_suite.py", "scripts/activation.py", "docs/installer-download.md"):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        shutil.copytree(ROOT / "skills/pm-essential-skills-concise-communication", self.root / "skills/pm-essential-skills-concise-communication")

    def test_builders_refuse_outputs_that_are_sources(self):
        for name, build in (
            ("plugin.json", lambda output: package_plugin.build(output, self.root)),
            ("Install.cmd", lambda output: package_installers.build(output, ["pm-essential-skills-concise-communication"], self.root)),
        ):
            with self.subTest(name=name):
                output = self.root / name
                original = output.read_bytes()
                with self.assertRaisesRegex(ValueError, "overwrite a package source"):
                    build(output)
                self.assertEqual(output.read_bytes(), original)

    def test_failed_build_keeps_existing_archive_and_cleans_temporary(self):
        output = self.root / "previous.zip"
        output.write_bytes(b"previous artifact")
        with mock.patch.object(archive_builder.zipfile.ZipFile, "writestr", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                package_plugin.build(output, self.root)
        self.assertEqual(output.read_bytes(), b"previous artifact")
        self.assertEqual(list(self.root.glob(".pm-archive-*")), [])

    def test_hardlink_alias_cannot_overwrite_input(self):
        source, output = self.root / "plugin.json", self.root / "alias.zip"
        try:
            output.hardlink_to(source)
        except OSError as exc:
            self.skipTest(f"Hardlinks unavailable: {exc}")
        original = source.read_bytes()
        with self.assertRaisesRegex(ValueError, "overwrite a package source"):
            package_plugin.build(output, self.root)
        self.assertEqual(source.read_bytes(), original)
        self.assertEqual(output.read_bytes(), original)

    def test_unsafe_manifest_prefix_is_rejected_before_output(self):
        manifest = self.root / "plugin.json"
        value = json.loads(manifest.read_text())
        value["name"] = "../escaped"
        manifest.write_text(json.dumps(value))
        output = self.root / "plugin.zip"
        with self.assertRaisesRegex(ValueError, "Unsafe archive entry"):
            package_plugin.build(output, self.root)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
