#!/usr/bin/env python3
"""Build standalone Windows-friendly downloads, with no Git or plugin dependency."""

import argparse
import json
from pathlib import Path
from archive_builder import write_archive

from skill_resources import resource_errors
from activation import NAMES as SKILLS

ROOT = Path(__file__).resolve().parents[1]


def build(output, skills, root=ROOT):
    if not skills or set(skills) - set(SKILLS):
        raise ValueError("Unknown or empty skill selection")
    entries = {"Install.cmd": root / "Install.cmd"}
    for name in ("install_suite.py", "activation.py"):
        entries[f"scripts/{name}"] = root / "scripts" / name
    for name in skills:
        folder = root / "skills" / name
        if not (folder / "SKILL.md").is_file():
            raise ValueError(f"Missing skill: {name}")
        errors = resource_errors(folder)
        if errors:
            raise ValueError("; ".join(errors))
        for source in sorted(folder.rglob("*")):
            if source.is_symlink():
                raise ValueError("Linked package files are not supported")
            if source.is_file() and "__pycache__" not in source.parts and source.suffix != ".pyc":
                entries[source.relative_to(root).as_posix()] = source
    if output.resolve().is_relative_to((root / "skills").resolve()):
        raise ValueError("Download must be outside skill sources")
    guide = ("PM Essential Skills\n\nExtract this download, open Install.cmd, then use Codex normally.\n"
             "Included: " + ", ".join(skills) + ".\n\n"
             "Installation copies only the included skills and adds their automatic user-level guidance.\n"
             + ("Context Management selects same-project routing, superseded-source archival, and temporary recovery defaults.\n"
                if "context-management" in skills else "No chat-management scope is selected.\n") +
             "Each skill contains its own workflow; the activation rule only points to it and records scope.\n"
             "Existing user preferences are preserved. No project activation prompt, Git account, or plugin is needed.\n"
             "Guidance takes effect when Codex next reloads instructions; existing sessions may retain an old snapshot.\n\n"
             "Check: Install.cmd status\nRemove and restore originals: Install.cmd uninstall\n\n"
             "Other systems: run python3 scripts/install_suite.py install with Python 3.10+.\n"
             "Optional per-turn reminders: add --hooks to that command; Codex still requires hook trust.\n"
             "Installation checks do not prove live model invocation or measured savings.\n")
    write_archive(output, entries, {"START-HERE.txt": guide})
    return {"archive": str(output.resolve()), "skills": list(skills), "files": len(entries) + 1}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "work/downloads")
    args = parser.parse_args()
    choices = [("pm-essential-skills", SKILLS), *( (name, (name,)) for name in SKILLS)]
    for name, skills in choices:
        print(json.dumps(build(args.output_dir / f"{name}.zip", skills)))


if __name__ == "__main__":
    main()
