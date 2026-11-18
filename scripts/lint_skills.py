#!/usr/bin/env python3
"""Check skills and eval cases against this pack's skill standard.

Usage: python scripts/lint_skills.py [REPO_ROOT]

Prints one line per problem and exits 1 when any problem is found.
Model-backed behavior is not checked here; that is what `claude plugin eval` is for.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

MAX_DESCRIPTION_CHARS = 500
MAX_SKILL_BYTES = 20_000
DEFAULT_WORD_BUDGET = 500
WORD_BUDGETS = {"discipline": 1500}
SKILL_TYPES = {"technique", "discipline", "collaborative", "reference"}
GRADER_TYPES = {"regex", "tool_used", "tool_order", "file_exists", "llm", "baseline"}
REPO_PREFIXES = ("pm-essential-skills", "swe-essential-skills")
NESTED_MARKDOWN_DIRS = {"assets"}
EVAL_SKIP_DIRS = {"results", "mocks"}

NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+){0,2}$")
AT_LINK_PATTERN = re.compile(r"(?<![\w`/])@(?:\.{1,2}/)?[\w.-]+(?:/[\w.-]+)*\.md\b")
LINK_PATTERN = re.compile(r"\]\(([^)\s]+)\)")
URL_SCHEME_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter, body). Raise ValueError when the fence is missing."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing YAML frontmatter: the file must start with '---'")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[1:index]), "\n".join(lines[index + 1 :])
    raise ValueError("unterminated YAML frontmatter: no closing '---'")


def parse_frontmatter(text: str) -> tuple[dict, str, str]:
    """Return (fields, raw frontmatter, body). Raise ValueError on bad YAML."""
    raw, body = split_frontmatter(text)
    try:
        fields = yaml.safe_load(raw) or {}
    except yaml.YAMLError as error:
        mark = getattr(error, "problem_mark", None)
        where = f" (frontmatter line {mark.line + 1})" if mark else ""
        raise ValueError(f"frontmatter is not valid YAML{where}; quote values that contain ': '") from None
    if not isinstance(fields, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return fields, raw, body


def description_is_one_line(raw_frontmatter: str) -> bool:
    lines = raw_frontmatter.split("\n")
    for index, line in enumerate(lines):
        if not line.startswith("description:"):
            continue
        value = line[len("description:") :].strip()
        if not value or value[0] in "|>":
            return False
        following = lines[index + 1] if index + 1 < len(lines) else ""
        return not (following[:1].isspace())
    return True


def lint_skill(skill_dir: Path, eval_case_names: set[str]) -> list[str]:
    problems: list[str] = []
    name = skill_dir.name
    skill_file = skill_dir / "SKILL.md"

    def report(message: str) -> None:
        problems.append(f"skills/{name}: {message}")

    if not NAME_PATTERN.match(name):
        report("folder name must be lowercase kebab-case with at most three words")
    if name.startswith(REPO_PREFIXES):
        report("folder name must not repeat the repository prefix; plugin namespacing handles collisions")
    if not skill_file.is_file():
        report("missing SKILL.md")
        return problems

    size = skill_file.stat().st_size
    if size > MAX_SKILL_BYTES:
        report(f"SKILL.md is {size} bytes; the hard cap is {MAX_SKILL_BYTES}")

    try:
        fields, raw, body = parse_frontmatter(read_text(skill_file))
    except ValueError as error:
        report(str(error))
        return problems

    declared_name = fields.get("name")
    if declared_name is not None and declared_name != name:
        report(f"frontmatter name '{declared_name}' must match the folder name")

    model_invoked = fields.get("disable-model-invocation") is not True
    description = fields.get("description")
    if not isinstance(description, str) or not description.strip():
        report("description is required")
    else:
        if not description_is_one_line(raw):
            report("description must be written on a single line")
        if len(description) > MAX_DESCRIPTION_CHARS:
            report(f"description is {len(description)} characters; the limit is {MAX_DESCRIPTION_CHARS}")
        if model_invoked and "use when" not in description.lower():
            report("model-invoked description must say 'Use when' followed by the phrases users type")

    metadata = fields.get("metadata") or {}
    skill_type = metadata.get("type") if isinstance(metadata, dict) else None
    if skill_type is not None and skill_type not in SKILL_TYPES:
        report(f"metadata.type '{skill_type}' must be one of: {', '.join(sorted(SKILL_TYPES))}")
    budget = WORD_BUDGETS.get(skill_type, DEFAULT_WORD_BUDGET)
    words = len(body.split())
    if words > budget:
        report(f"body is {words} words; the budget for this skill type is {budget}")

    for match in AT_LINK_PATTERN.finditer(body):
        report(f"'{match.group(0)}' force-loads a file; link it from the step that needs it instead")

    skill_root = skill_dir.resolve()
    for target in LINK_PATTERN.findall(body):
        if target.startswith("#") or URL_SCHEME_PATTERN.match(target):
            continue
        relative = target.split("#", 1)[0]
        resolved = (skill_dir / relative).resolve()
        if skill_root != resolved and skill_root not in resolved.parents:
            report(f"link '{target}' leaves the skill folder; skills must not link across folders")
        elif not resolved.exists():
            report(f"link '{target}' points to a missing file")

    for markdown in skill_dir.rglob("*.md"):
        parts = markdown.relative_to(skill_dir).parts
        if len(parts) > 1 and parts[0] not in NESTED_MARKDOWN_DIRS:
            report(f"'{'/'.join(parts)}' is nested; keep reference files one level deep")

    if model_invoked and not any(case.startswith(f"{name}-trigger-") for case in eval_case_names):
        report(f"model-invoked skill needs at least one eval case named '{name}-trigger-<kind>-<n>'")

    return problems


def lint_eval_case(case_dir: Path) -> list[str]:
    problems: list[str] = []

    def report(message: str) -> None:
        problems.append(f"evals/{case_dir.name}: {message}")

    prompt = case_dir / "prompt.md"
    has_case_yaml = (case_dir / "case.yaml").is_file()
    if not prompt.is_file() and not has_case_yaml:
        report("needs prompt.md or case.yaml")
    elif prompt.is_file():
        try:
            _, _, body = parse_frontmatter(read_text(prompt))
        except ValueError as error:
            report(f"prompt.md: {error}")
        else:
            if not body.strip():
                report("prompt.md has no prompt text")

    graders = sorted((case_dir / "graders").glob("*.md"))
    if not graders and not has_case_yaml:
        report("needs at least one grader in graders/")
    for grader in graders:
        try:
            fields, _, _ = parse_frontmatter(read_text(grader))
        except ValueError as error:
            report(f"graders/{grader.name}: {error}")
            continue
        grader_type = fields.get("type")
        if grader_type not in GRADER_TYPES:
            report(f"graders/{grader.name}: type must be one of: {', '.join(sorted(GRADER_TYPES))}")
    return problems


def lint_repo(root: Path) -> tuple[list[str], int, int]:
    """Return (problems, skill count, eval case count)."""
    problems: list[str] = []
    evals_dir = root / "evals"
    case_dirs = []
    if evals_dir.is_dir():
        case_dirs = [
            path
            for path in sorted(evals_dir.iterdir())
            if path.is_dir() and path.name not in EVAL_SKIP_DIRS and not path.name.startswith(".")
        ]
    for case_dir in case_dirs:
        problems.extend(lint_eval_case(case_dir))

    skills_dir = root / "skills"
    skill_dirs = []
    if skills_dir.is_dir():
        skill_dirs = [path for path in sorted(skills_dir.iterdir()) if path.is_dir()]
    case_names = {case.name for case in case_dirs}
    for skill_dir in skill_dirs:
        problems.extend(lint_skill(skill_dir, case_names))
    return problems, len(skill_dirs), len(case_dirs)


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent
    problems, skills, cases = lint_repo(root)
    for problem in problems:
        print(problem)
    print(f"{skills} skills, {cases} eval cases, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
