"""Guard this suite's intended automatic-selection policy, not host compliance."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]


class SuiteInvocationTests(unittest.TestCase):
    def test_every_shipped_skill_allows_automatic_selection(self):
        for entry in sorted((ROOT / "skills").glob("*/agents/openai.yaml")):
            with self.subTest(skill=entry.parents[1].name):
                policy = yaml.safe_load(entry.read_text(encoding="utf-8")).get("policy", {})
                self.assertIs(policy.get("allow_implicit_invocation", True), True)
