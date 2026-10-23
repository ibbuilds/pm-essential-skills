"""Stateless helper error envelopes using only isolated deterministic input."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONTEXT = "skills/pm-essential-skills-context-management/scripts/"
SOURCE = "skills/pm-essential-skills-source-selection/scripts/"
SCRIPTS = (CONTEXT + "assess_context.py", CONTEXT + "assess_archive.py",
           CONTEXT + "preflight.py", SOURCE + "assess_source.py",
           SOURCE + "read_source.py", "scripts/evaluate_usage.py")


class JsonCliBoundaryTests(unittest.TestCase):
    def invoke(self, script, raw, *args):
        return subprocess.run([sys.executable, str(ROOT / script), *args], input=raw,
                              text=True, capture_output=True, timeout=5)

    def test_deep_decoder_failures_are_structured_without_input_echo(self):
        # Exercise the interpreter's decoder limit, not a helper-specific cap.
        for script in SCRIPTS:
            for raw in ("[" * 10000, "[" * 10000 + '"PRIVATE_FIXTURE"' + "]" * 10000):
                with self.subTest(script=script, balanced=raw.endswith("]")):
                    result = self.invoke(script, raw)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, "")
                    error = json.loads(result.stderr)
                    self.assertEqual(set(error), {"error"})
                    self.assertIsInstance(error["error"], str)
                    self.assertTrue(error["error"].strip())
                    self.assertNotIn("PRIVATE_FIXTURE", result.stderr)
                    self.assertNotIn("Traceback", result.stderr)

    def test_normal_inputs_remain_usable_via_stdin_and_input_file(self):
        with tempfile.TemporaryDirectory(prefix="pm-json-boundary-") as directory:
            source = Path(directory) / "source.txt"
            source.write_text("isolated source\n", encoding="utf-8")
            cases = (
                ({"completed": True}, "action", "complete"),
                ({"stage": "recover"}, "action", "verify_target"),
                ({}, "status", "unavailable"),
                ({"source_id": "fixture"}, "action", "fetch"),
                ({"path": str(source)}, "action", "read"),
                ({"runs": []}, "all_pairs_measured", False),
            )
            for script, (value, key, expected) in zip(SCRIPTS, cases):
                payload = json.dumps(value)
                input_file = Path(directory) / "input.json"
                input_file.write_text(payload, encoding="utf-8")
                for raw, args in ((payload, ()), ("", ("--input", str(input_file)))):
                    with self.subTest(script=script, args=args):
                        result = self.invoke(script, raw, *args)
                        self.assertEqual(result.returncode, 0, result.stderr)
                        self.assertEqual(result.stderr, "")
                        self.assertEqual(json.loads(result.stdout)[key], expected)


if __name__ == "__main__":
    unittest.main()
