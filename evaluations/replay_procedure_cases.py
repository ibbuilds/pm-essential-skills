"""Replay declared synthetic helper observations; no model or host integration."""
from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
HELPERS = {
    "pm-essential-skills-context-management/scripts/assess_context.py",
    "pm-essential-skills-source-selection/scripts/assess_source.py",
    "pm-essential-skills-context-management/scripts/preflight.py",
    "pm-essential-skills-context-management/scripts/assess_archive.py",
}


def main():
    cases = json.loads(Path(__file__).with_name("procedure-cases.json").read_text(encoding="utf-8"))["cases"]
    if len(cases) != 29 or len({case["case_id"] for case in cases}) != len(cases):
        raise ValueError("The frozen 29-case set must be complete and uniquely identified")
    loaded = {}
    for case in cases:
        relative = case["helper_path"]
        if relative not in HELPERS:
            raise ValueError("Unknown helper in case data")
        if relative not in loaded:
            spec = importlib.util.spec_from_file_location("procedure_helper_" + str(len(loaded)), ROOT / "skills" / relative)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            loaded[relative] = module
        actual = loaded[relative].assess(case["input_observations"])
        for field, expected in case["expected_output_fields"].items():
            if field not in actual or type(actual[field]) is not type(expected) or actual[field] != expected:
                raise AssertionError(f"{case['case_id']}: unexpected {field}")
    print(f"PASS: {len(cases)} synthetic helper cases; not model adherence or live transfer")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
