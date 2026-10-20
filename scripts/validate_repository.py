#!/usr/bin/env python3
"""Repository packaging checks; not a behavioral skill evaluation."""

import re
import ast
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def main():
    errors = []
    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if not skills:
        errors.append("No skills found")
    for path in skills:
        text = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
        try:
            metadata = yaml.safe_load(match.group(1)) if match else None
            if not isinstance(metadata, dict) or metadata.get("name") != path.parent.name:
                raise ValueError("required frontmatter/name is invalid")
            name = metadata["name"]
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
                raise ValueError("invalid skill name")
            description = metadata.get("description")
            if not isinstance(description, str) or not 1 <= len(description) <= 1024:
                raise ValueError("description must be nonempty text under 1,025 characters")
            ui = yaml.safe_load((path.parent / "agents/openai.yaml").read_text(encoding="utf-8"))
            if not isinstance(ui, dict) or not isinstance(ui.get("interface"), dict):
                raise ValueError("missing UI interface metadata")
            interface = ui["interface"]
            for key in ["display_name", "short_description", "default_prompt"]:
                if not isinstance(interface.get(key), str) or not interface[key].strip():
                    raise ValueError(f"UI {key} must be nonempty text")
            if not 25 <= len(interface["short_description"]) <= 64:
                raise ValueError("UI short_description must be 25-64 characters")
            if "$" + name not in interface["default_prompt"]:
                raise ValueError("UI default_prompt must invoke this skill")
            policy = ui.get("policy", {})
            if not isinstance(policy, dict) or type(policy.get("allow_implicit_invocation", True)) is not bool:
                raise ValueError("invalid invocation policy")
        except (ValueError, OSError, yaml.YAMLError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
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

    for path in ROOT.rglob("*.py"):
        if any(part in {".git", ".venv", "work", ".pm-context"} for part in path.relative_to(ROOT).parts):
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")

    if errors:
        print("\n".join(errors))
        return 1
    print(f"Validated {len(skills)} skill(s): YAML/UI metadata, entrypoint budget, local links, Python syntax.")
    print("This check does not certify runtime behavior, tool availability, or token savings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
