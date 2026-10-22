"""Exercise reproducible archives and complete, portable distribution metadata."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import archive_builder
import package_installers
import package_plugin


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)

    def test_archive_normalizes_order_time_platform_and_permissions(self):
        a, b = self.directory / "a.txt", self.directory / "b.txt"
        a.write_bytes(b"alpha")
        b.write_bytes(b"beta")
        first, second = self.directory / "first.zip", self.directory / "second.zip"
        archive_builder.write_archive(first, {"b.txt": b, "a.txt": a}, {"guide": "Guide"})
        os.utime(a, (1700000000, 1700000000))
        a.chmod(0o600)
        archive_builder.write_archive(second, {"a.txt": a, "b.txt": b}, {"guide": "Guide"})
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with zipfile.ZipFile(first) as archive:
            self.assertEqual(archive.namelist(), ["a.txt", "b.txt", "guide"])
            for info in archive.infolist():
                self.assertEqual(info.date_time, (1980, 1, 1, 0, 0, 0))
                self.assertEqual(info.create_system, 3)
                self.assertEqual(info.external_attr >> 16, 0o100644)

    def test_all_downloads_have_matching_portable_metadata_and_reproduce(self):
        first, second = self.directory / "first", self.directory / "second"
        results = package_installers.build_all(first)
        package_installers.build_all(second)
        manifest = json.loads((first / "distribution.json").read_text())
        self.assertEqual(manifest["source_version"], json.loads((ROOT / "plugin.json").read_text())["version"])
        self.assertEqual(len(manifest["artifacts"]), len(package_installers.SKILLS) + 1)
        self.assertEqual(len(results), len(manifest["artifacts"]))
        checksums = []
        for item in manifest["artifacts"]:
            name = item["archive"]
            self.assertEqual(Path(name).name, name)
            payload = (first / name).read_bytes()
            self.assertEqual(hashlib.sha256(payload).hexdigest(), item["sha256"])
            self.assertEqual(len(payload), item["size_bytes"])
            checksums.append(f"{item['sha256']}  {name}\n")
            with zipfile.ZipFile(first / name) as archive:
                self.assertEqual(len(archive.namelist()), item["files"])
                actual = sorted(n.split("/")[1] for n in archive.namelist() if n.endswith("/SKILL.md"))
                self.assertEqual(actual, sorted(item["skills"]))
                guide = archive.read("README.md").decode()
                for required in ("recover", "uninstall", "install.lock", "journal", "trust", "github.com/ibbuilds"):
                    self.assertIn(required, guide)
        self.assertEqual((first / "SHA256SUMS").read_text(), "".join(checksums))
        for path in first.iterdir():
            self.assertEqual(path.read_bytes(), (second / path.name).read_bytes(), path.name)

    def test_failed_batch_invalidates_old_metadata(self):
        package_installers.build_all(self.directory)
        real_build = package_installers.build
        count = 0
        def fail_second(*args, **kwargs):
            nonlocal count
            count += 1
            if count == 2:
                raise OSError("simulated failure")
            return real_build(*args, **kwargs)
        with mock.patch.object(package_installers, "build", side_effect=fail_second):
            with self.assertRaises(OSError):
                package_installers.build_all(self.directory)
        self.assertFalse((self.directory / "distribution.json").exists())
        self.assertFalse((self.directory / "SHA256SUMS").exists())

    def test_failed_second_metadata_write_removes_first(self):
        real_write = package_installers.write_metadata
        def fail_checksum(path, text):
            if path.name == "SHA256SUMS":
                raise OSError("simulated metadata failure")
            return real_write(path, text)
        with mock.patch.object(package_installers, "write_metadata", side_effect=fail_checksum):
            with self.assertRaises(OSError):
                package_installers.build_all(self.directory)
        self.assertFalse((self.directory / "distribution.json").exists())
        self.assertFalse((self.directory / "SHA256SUMS").exists())

    def test_linked_checksum_output_is_rejected_without_following_it(self):
        target = self.directory / "keep.txt"
        target.write_bytes(b"keep")
        checksum = self.directory / "SHA256SUMS"
        try:
            checksum.symlink_to(target)
        except OSError as exc:
            self.skipTest(f"Symlinks unavailable: {exc}")
        with self.assertRaisesRegex(ValueError, "Linked metadata"):
            package_installers.build_all(self.directory)
        self.assertEqual(target.read_bytes(), b"keep")
        self.assertTrue(checksum.is_symlink())
        self.assertFalse((self.directory / "pm-essential-skills.zip").exists())

    def test_optional_license_is_copied_without_inventing_one(self):
        root = self.directory / "source"
        for name in ("Install.cmd", "scripts/install_suite.py", "scripts/activation.py", "docs/installer-download.md"):
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        shutil.copytree(ROOT / "skills/ibbuilds-pm-concise-communication", root / "skills/ibbuilds-pm-concise-communication")
        output = self.directory / "skill.zip"
        result = package_installers.build(output, ["ibbuilds-pm-concise-communication"], root)
        self.assertFalse(result["license_included"])
        (root / "LICENSE").write_bytes(b"Owner-selected terms fixture\n")
        result = package_installers.build(output, ["ibbuilds-pm-concise-communication"], root)
        self.assertTrue(result["license_included"])
        with zipfile.ZipFile(output) as archive:
            self.assertEqual(archive.read("LICENSE"), (root / "LICENSE").read_bytes())

    def test_plugin_build_is_reproducible(self):
        first, second = self.directory / "first.zip", self.directory / "second.zip"
        package_plugin.build(first)
        package_plugin.build(second)
        self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_archive_rejects_special_file_before_read(self):
        if not hasattr(os, "mkfifo"):
            self.skipTest("FIFO unavailable")
        source = self.directory / "pipe"
        os.mkfifo(source)
        with self.assertRaisesRegex(ValueError, "regular files"):
            archive_builder.write_archive(self.directory / "bad.zip", {"pipe": source})


if __name__ == "__main__":
    unittest.main()
