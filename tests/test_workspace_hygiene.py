"""Filesystem behavior, not prose matching or native model activation."""
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/pm-essential-skills-workspace-hygiene/scripts/inventory_workspace.py"
spec = importlib.util.spec_from_file_location("workspace_inventory", SCRIPT)
MODULE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(MODULE)


class WorkspaceHygieneTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def put(self, name, data):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def test_nested_backups_are_visible_and_user_material_is_unchanged(self):
        self.put("backups/old/backups/copy.zip", b"b" * 4096)
        self.put("outputs/report.docx", b"deliverable")
        self.put(".git/objects/retained", b"history")
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        report = MODULE.inventory(self.root, top=2)
        self.assertEqual(report["status"], "complete")
        self.assertEqual(report["logical_bytes"], sum(map(len, before.values())))
        self.assertEqual(report["largest_top_level_paths"][0]["path"], "backups")
        self.assertEqual(report["largest_files"][0]["path"], "backups/old/backups/copy.zip")
        self.assertEqual(before, {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_entry_and_time_limits_preserve_incomplete_coverage(self):
        for index in range(5):
            self.put(f"file-{index}", b"payload")
        report = MODULE.inventory(self.root, max_entries=2)
        self.assertEqual(report["status"], "partial")
        self.assertEqual(report["entries"], 2)
        self.assertIn("max_entries", report["limits"])
        with patch.object(MODULE.time, "monotonic", side_effect=[0, 10]):
            report = MODULE.inventory(self.root, max_seconds=1)
        self.assertEqual(report["status"], "partial")
        self.assertIn("max_seconds", report["limits"])

    def test_access_errors_are_not_a_clean_report(self):
        with patch.object(MODULE.os, "scandir", side_effect=PermissionError("denied")):
            report = MODULE.inventory(self.root)
        self.assertEqual(report["status"], "partial")
        self.assertEqual(report["error_count"], 1)
        self.assertEqual(report["files"], 0)

    def test_links_outside_and_cycles_are_not_followed(self):
        other = self.root / "outside"
        other.mkdir()
        (other / "keep").write_bytes(b"external" * 100)
        project = self.root / "project"
        project.mkdir()
        try:
            (project / "outside-link").symlink_to(other, target_is_directory=True)
            (project / "cycle").symlink_to(project, target_is_directory=True)
        except OSError:
            self.skipTest("Host does not permit directory symlinks")
        report = MODULE.inventory(project)
        self.assertEqual(report["files"], 0)
        self.assertEqual(report["skipped_links"], 2)
        with self.assertRaises(ValueError):
            MODULE.inventory(project / "outside-link")

    def test_windows_reparse_flag_is_detected_without_following_target(self):
        info = type("Info", (), {"st_mode": stat.S_IFDIR, "st_file_attributes": 1024})()
        self.assertTrue(MODULE.linked(info))

    def test_parent_traversal_is_rejected_before_normalizing_target(self):
        with self.assertRaises(ValueError):
            MODULE.inventory(self.root / "possible-link" / "..")

    def test_limited_scan_closes_every_open_iterator(self):
        self.put("nested/one", b"a")
        self.put("nested/two", b"b")
        original = os.scandir
        opened = []

        class TrackedIterator:
            def __init__(self, path):
                self.iterator = original(path)
                self.closed = False
                opened.append(self)
            def __next__(self):
                return next(self.iterator)
            def close(self):
                self.closed = True
                self.iterator.close()

        with patch.object(MODULE.os, "scandir", side_effect=TrackedIterator):
            report = MODULE.inventory(self.root, max_entries=2)
        self.assertEqual(report["status"], "partial")
        self.assertTrue(opened)
        self.assertTrue(all(iterator.closed for iterator in opened))

    def test_invalid_limits_and_filesystem_root_are_rejected(self):
        for settings in ({"top": 0}, {"top": 101}, {"max_entries": 0}, {"max_seconds": float("nan")}, {"max_seconds": 0}):
            with self.subTest(settings=settings), self.assertRaises(ValueError):
                MODULE.inventory(self.root, **settings)
        with self.assertRaises(ValueError):
            MODULE.inventory(Path(self.root.anchor))

    def test_cli_preserves_complete_partial_and_error_exit_status(self):
        for i in range(3):
            self.put(f"item-{i}", b"123")
        for args, expected in (([], (0, "complete")), (["--max-entries", "1"], (1, "partial")), (["--top", "0"], (2, "error"))):
            run = subprocess.run([sys.executable, "-B", str(SCRIPT), str(self.root), *args], capture_output=True, text=True)
            self.assertEqual((run.returncode, json.loads(run.stdout)["status"]), expected)


if __name__ == "__main__":
    unittest.main()
