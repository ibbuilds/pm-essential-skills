"""Deterministic capture behavior, not a model/token usage benchmark."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/pm-essential-skills-source-selection/scripts/capture_command.py'
spec = importlib.util.spec_from_file_location('capture_command', SCRIPT)
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)


class CaptureTests(unittest.TestCase):
    def run_capture(self, code, budget=32):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        result = subprocess.run([sys.executable, str(SCRIPT), '--output-dir', temp.name,
                                 '--preview-bytes', str(budget), '--', sys.executable,
                                 '-c', code], capture_output=True, text=True)
        return result, json.loads(result.stdout)

    def test_success_raw_streams_hashes_and_unicode(self):
        result, report = self.run_capture("import os; os.write(1, 'hé🙂'.encode()); os.write(2, b'warning\\n')")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(report['status'], 'completed')
        self.assertEqual(report['stdout']['head'], 'hé🙂')
        for key in ('stdout', 'stderr'):
            info = report[key]
            raw = Path(info['path']).read_bytes()
            self.assertEqual(info['bytes'], len(raw))
            self.assertEqual(info['sha256'], hashlib.sha256(raw).hexdigest())
            self.assertFalse(info['truncated'])
        self.assertEqual(json.loads((Path(report['artifact_dir']) / 'summary.json').read_text()), report)

    def test_failed_exit_survives_missing_middle_diagnostic(self):
        result, report = self.run_capture("import os; os.write(1,b'a'*100+b'FAILURE'+b'z'*100); raise SystemExit(7)", 16)
        self.assertEqual(result.returncode, 7)
        self.assertEqual(report['exit_code'], 7)
        self.assertNotIn('FAILURE', report['stdout']['head'] + report['stdout']['tail'])
        self.assertIn(b'FAILURE', Path(report['stdout']['path']).read_bytes())
        self.assertEqual(report['stdout']['head'], 'a'*8)
        self.assertEqual(report['stdout']['tail'], 'z'*8)

    def test_empty_failure_and_zero_preview(self):
        result, report = self.run_capture('raise SystemExit(9)', 0)
        self.assertEqual(result.returncode, 9)
        self.assertEqual(report['stdout']['bytes'], 0)
        result, report = self.run_capture("print('hidden')", 0)
        self.assertEqual(report['stdout']['preview_bytes'], 0)
        self.assertTrue(report['stdout']['truncated'])

    def test_binary_and_split_unicode(self):
        result, report = self.run_capture("import os; os.write(1, '🙂🙂'.encode()+b'\\xff')", 3)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(report['stdout']['preview_bytes'], 3)
        self.assertIn('\ufffd', report['stdout']['head'])
        self.assertEqual(Path(report['stdout']['path']).read_bytes(), '🙂🙂'.encode()+b'\xff')

    def test_launch_failure_and_bad_input(self):
        with tempfile.TemporaryDirectory() as directory:
            report, code = capture.capture(['/nonexistent/capture-fixture-command'], directory, 4)
            self.assertEqual(code, 2)
            self.assertEqual(report['status'], 'launch_error')
            self.assertIsNone(report['exit_code'])
            for argv, budget in (([], 4), (['echo'], -1), (['echo'], 65537)):
                with self.assertRaises(ValueError):
                    capture.capture(argv, directory, budget)
        result = subprocess.run([sys.executable, str(SCRIPT), '--output-dir', '/nonexistent/capture-dir', '--', 'echo'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)['status'], 'capture_error')

    def test_once_no_shell_and_unique_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            counter = Path(directory) / 'counter'
            command = [sys.executable, '-c', "import pathlib,sys; p=pathlib.Path(sys.argv[1]); p.write_text(p.read_text()+'x' if p.exists() else 'x'); print(sys.argv[2])", str(counter), '$(echo injected); *']
            first, _ = capture.capture(command, directory, 100)
            second, _ = capture.capture(command, directory, 100)
            self.assertEqual(counter.read_text(), 'xx')
            self.assertNotEqual(first['artifact_dir'], second['artifact_dir'])
            self.assertEqual(first['stdout']['head'].strip(), '$(echo injected); *')

    def test_output_resolution_runtime_error_does_not_launch_producer(self):
        with patch.object(capture.Path, 'resolve', side_effect=RuntimeError('Symlink loop')):
            with patch.object(capture.subprocess, 'run') as producer:
                with self.assertRaisesRegex(ValueError, 'Symlink loop'):
                    capture.capture(['unused-producer'], 'unused-output', 4)
                producer.assert_not_called()
        # Unrelated runtime failures remain visible rather than being normalized.
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(capture.subprocess, 'run', side_effect=RuntimeError('unrelated')):
                with self.assertRaisesRegex(RuntimeError, 'unrelated'):
                    capture.capture(['unused-producer'], directory, 4)

    @unittest.skipUnless(os.name == 'posix', 'POSIX symlink fixture')
    def test_output_symlink_loop_has_json_error_and_never_launches(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            loop = root / 'loop'
            loop.symlink_to('loop')
            marker = root / 'producer-ran'
            result = subprocess.run([
                sys.executable, str(SCRIPT), '--output-dir', str(loop), '--',
                sys.executable, '-c',
                'from pathlib import Path; Path(' + repr(str(marker)) + ').touch()',
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stderr, '')
            report = json.loads(result.stdout)
            self.assertEqual(report['status'], 'capture_error')
            self.assertIsNone(report['exit_code'])
            self.assertFalse(marker.exists())
            self.assertEqual(list(root.iterdir()), [loop])

    @unittest.skipUnless(os.name == 'posix', 'POSIX signal status')
    def test_signal_status(self):
        result, report = self.run_capture('import os,signal; os.kill(os.getpid(),signal.SIGTERM)')
        self.assertEqual(report['exit_code'], -signal.SIGTERM)
        self.assertEqual(result.returncode, 128 + signal.SIGTERM)

    def test_large_output_bounded_delivery_and_short_overhead(self):
        small, short = self.run_capture("print('ok')", 128)
        large, long = self.run_capture("import os; os.write(1,b'row: unchanged\\n'*100000); os.write(2,b'notice\\n'*10000)", 128)
        self.assertGreater(len(small.stdout.encode()), short['stdout']['bytes'])
        self.assertLess(len(large.stdout.encode()), 2000)
        self.assertEqual(long['stdout']['bytes'], 1500000)
        self.assertEqual(long['stderr']['bytes'], 70000)
        self.assertEqual(long['stdout']['preview_bytes'] + long['stderr']['preview_bytes'], 256)


if __name__ == '__main__':
    unittest.main()
