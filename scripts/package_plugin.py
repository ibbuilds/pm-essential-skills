#!/usr/bin/env python3
"""Build a skills-only plugin archive; no account upload or installation."""

import argparse
import json
from pathlib import Path
from archive_builder import write_archive

from skill_resources import resource_errors

ROOT = Path(__file__).resolve().parents[1]


def build(output, root=ROOT):
    for skill in sorted((root / "skills").glob("*/SKILL.md")):
        errors = resource_errors(skill.parent)
        if errors:
            raise ValueError("; ".join(errors))
    manifest = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
    entries = {"plugin.json": root / "plugin.json"}
    if (root / "LICENSE").exists():
        entries["LICENSE"] = root / "LICENSE"
    for entry in sorted((root / "skills").rglob("*")):
        if entry.is_symlink():
            raise ValueError("Linked package sources are not supported")
        if entry.is_file() and "__pycache__" not in entry.parts and entry.suffix != ".pyc":
            entries[entry.relative_to(root).as_posix()] = entry
    if not any(name.endswith("/SKILL.md") for name in entries):
        raise ValueError("No usable skill entrypoints")
    if output.resolve().is_relative_to((root / "skills").resolve()):
        raise ValueError("Archive must be outside packaged skills")
    write_archive(output, {f"{manifest['name']}/{relative}": path for relative, path in entries.items()})
    return {"archive": str(output.resolve()), "files": len(entries),
            "skills": sorted(name.split("/")[1] for name in entries if name.endswith("/SKILL.md"))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "work/pm-essential-skills.zip")
    args = parser.parse_args()
    print(json.dumps(build(args.output)))


if __name__ == "__main__":
    main()
