#!/usr/bin/env python3
"""Small dependency-free structural check; not a behavioral skill evaluation."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    errors = []
    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if not skills:
        errors.append("No skills found")
    for path in skills:
        text = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\nname: ([a-z0-9]+(?:-[a-z0-9]+)*)\ndescription: ([^\n]+)\n---\n", text)
        if not match or match.group(1) != path.parent.name:
            errors.append(f"{path.relative_to(ROOT)}: invalid required frontmatter/name")
        elif len(match.group(2)) > 1024:
            errors.append(f"{path.relative_to(ROOT)}: description too long")
        if len(text.split()) > 700:
            errors.append(f"{path.relative_to(ROOT)}: entrypoint exceeds suite's 700-word budget")

    # Validate checked-in Markdown navigation; ignore external URLs and fenced examples.
    for path in ROOT.rglob("*.md"):
        if any(part in {".git", ".venv", "work", ".pm-context"} for part in path.relative_to(ROOT).parts):
            continue
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"^```.*?^```\s*$", "", text, flags=re.MULTILINE | re.DOTALL)
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if "://" in target or target.startswith("#"):
                continue
            local = target.split("#", 1)[0]
            resolved = (path.parent / local).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)}: broken/outside local link {target}")

    if errors:
        print("\n".join(errors))
        return 1
    print(f"Validated {len(skills)} skill(s): required frontmatter, entrypoint budget, local Markdown links.")
    print("This check does not certify runtime behavior, tool availability, or token savings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
