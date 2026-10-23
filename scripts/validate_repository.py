#!/usr/bin/env python3
"""Repository packaging checks; not a behavioral skill evaluation."""

import re
import ast
import json
from pathlib import Path

import yaml

from skill_resources import resource_errors
from activation import NAMES

ROOT = Path(__file__).resolve().parents[1]


class UniqueStringKeyLoader(yaml.SafeLoader):
    """Reject explicit duplicate string keys, without rejecting merge overrides."""

    def __init__(self, stream):
        super().__init__(stream)
        self._checked_mappings = set()

    def flatten_mapping(self, node):
        # PyYAML mutates nodes while expanding merges. Check each original node
        # once, including shared aliases, before inherited keys are inserted.
        if node not in self._checked_mappings:
            self._checked_mappings.add(node)
            seen = set()
            for key, _ in node.value:
                if key.tag == "tag:yaml.org,2002:str":
                    if key.value in seen:
                        raise yaml.constructor.ConstructorError(
                            "while constructing a mapping", node.start_mark,
                            f"duplicate explicit key {key.value!r}", key.start_mark)
                    seen.add(key.value)
        return super().flatten_mapping(node)


def load_yaml(raw):
    """Keep parser exhaustion in the ordinary metadata-validation error path."""
    try:
        return yaml.load(raw, Loader=UniqueStringKeyLoader)
    except RecursionError as exc:
        raise ValueError(f"YAML nesting exceeds parser capacity: {exc}") from exc


def main():
    errors = []
    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if {path.parent.name for path in skills} != set(NAMES):
        errors.append("Skill folders must match the seven repository-qualified catalog names")
    if not skills:
        errors.append("No skills found")
    try:
        manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        if not isinstance(manifest, dict):
            raise ValueError("plugin manifest must be a mapping")
        if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
            raise ValueError("missing portable plugin schema")
        if manifest.get("name") != "pm-essential-skills":
            raise ValueError("unexpected plugin identity")
        if not re.fullmatch(r"\d+\.\d+\.\d+", manifest.get("version", "")):
            raise ValueError("plugin version must be SemVer")
        interface = manifest["extensions"]["com.openai"]["interface"]
        short = interface["shortDescription"]
        if not isinstance(short, str) or not 1 <= len(short) <= 30:
            raise ValueError("plugin short description must be text of 1-30 characters")
        if any(key in manifest for key in ("skills", "interface", "apps", "mcpServers")):
            raise ValueError("portable manifest uses unsupported top-level component fields")
    except (ValueError, OSError, KeyError, TypeError) as exc:
        errors.append(f"plugin.json: {exc}")
    for path in skills:
        errors.extend(resource_errors(path.parent))
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: cannot read skill entrypoint: {exc}")
            continue
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
        try:
            metadata = load_yaml(match.group(1)) if match else None
            if not isinstance(metadata, dict) or metadata.get("name") != path.parent.name:
                raise ValueError("required frontmatter/name is invalid")
            name = metadata["name"]
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
                raise ValueError("invalid skill name")
            if not name.startswith("pm-essential-skills-"):
                raise ValueError("skill name must use the pm-essential-skills repository prefix")
            description = metadata.get("description")
            if not isinstance(description, str) or not description.strip() or len(description) > 1024:
                raise ValueError("description must be nonempty text under 1,025 characters")
            # Portable Agent Skills format, not an emulation of host coercions.
            if "metadata" in metadata:
                extra = metadata["metadata"]
                if not isinstance(extra, dict) or any(
                    not isinstance(key, str) or not isinstance(value, str)
                    for key, value in extra.items()
                ):
                    raise ValueError("metadata must map string keys to string values; "
                                     "quote scalar values, or omit unused metadata/use {}")
            ui = load_yaml((path.parent / "agents/openai.yaml").read_text(encoding="utf-8"))
            if not isinstance(ui, dict) or not isinstance(ui.get("interface"), dict):
                raise ValueError("missing UI interface metadata")
            interface = ui["interface"]
            for key in ["display_name", "short_description", "default_prompt"]:
                if not isinstance(interface.get(key), str) or not interface[key].strip():
                    raise ValueError(f"UI {key} must be nonempty text")
            if interface["display_name"] != name:
                raise ValueError("UI display_name must equal the canonical repo-name-skill-name")
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
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: cannot read Markdown: {exc}")
            continue
        text = re.sub(r"^```.*?^```\s*$", "", text, flags=re.MULTILINE | re.DOTALL)
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if "://" in target or target.startswith("#"):
                continue
            local = target.split("#", 1)[0]
            try:
                resolved = (path.parent / local).resolve()
                if not resolved.is_relative_to(ROOT) or not resolved.exists():
                    errors.append(f"{path.relative_to(ROOT)}: broken/outside local link {target}")
            except (ValueError, OSError, RuntimeError) as exc:
                errors.append(f"{path.relative_to(ROOT)}: unreadable local link {target}: {exc}")
                continue

    for path in ROOT.rglob("*.py"):
        if any(part in {".git", ".venv", "work", ".pm-context"} for part in path.relative_to(ROOT).parts):
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (SyntaxError, OSError, UnicodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")

    if errors:
        print("\n".join(errors))
        return 1
    print(f"Validated {len(skills)} skill(s): YAML/UI metadata, entrypoint budget, local links, Python syntax.")
    print("This check does not certify runtime behavior, tool availability, or token savings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
