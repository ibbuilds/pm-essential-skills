"""Validate maintainer fixture integrity, not model behavior or usage savings."""

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ExecutionFixtureTests(unittest.TestCase):
    def test_behavioral_cases_have_unique_ids_and_evaluable_inputs_and_outcomes(self):
        for path in sorted((ROOT / "tests").glob("*-cases.json")):
            with self.subTest(fixture=path.name):
                self.check_cases(json.loads(path.read_text(encoding="utf-8")))

    def check_cases(self, cases):
        self.assertIsInstance(cases, list)
        self.assertTrue(cases)
        seen = set()
        known_skills = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
        for case in cases:
            with self.subTest(case=case.get("id") if isinstance(case, dict) else case):
                self.assertIsInstance(case, dict)
                self.assertEqual(set(case), {"id", "available_skills", "context", "prompt", "expected", "must_not"})
                for key in ("id", "context", "prompt", "expected", "must_not"):
                    self.assertIsInstance(case[key], str)
                    self.assertTrue(case[key].strip(), key)
                self.assertNotIn(case["id"], seen)
                seen.add(case["id"])
                self.assertIsInstance(case["available_skills"], list)
                self.assertTrue(case["available_skills"])
                self.assertTrue(all(isinstance(name, str) for name in case["available_skills"]))
                self.assertEqual(len(case["available_skills"]), len(set(case["available_skills"])))
                self.assertTrue(set(case["available_skills"]) <= known_skills)


if __name__ == "__main__":
    unittest.main()
