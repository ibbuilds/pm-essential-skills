#!/usr/bin/env python3
"""Build standalone Windows-friendly downloads, with no Git or plugin dependency."""

import argparse
import json
from pathlib import Path
import zipfile

from skill_resources import resource_errors

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("context-management", "source-selection")


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
    output.parent.mkdir(parents=True, exist_ok=True)
    guide = ("PM Essential Skills\n\nExtract this download, open Install.cmd, then use Codex normally.\n"
             "Included: " + ", ".join(skills) + ".\n\n"
             "Installation copies only the included skills and adds their automatic user-level guidance.\n"
             "Context Management selects same-project routing, superseded-source archival, and temporary recovery defaults.\n"
             "Each skill contains its own workflow; the activation rule only points to it and records scope.\n"
             "Existing user preferences are preserved. No project activation prompt, Git account, or plugin is needed.\n"
             "Guidance takes effect when Codex next reloads instructions; existing sessions may retain an old snapshot.\n\n"
             "Check: Install.cmd status\nRemove and restore originals: Install.cmd uninstall\n\n"
             "Other systems: run python3 scripts/install_suite.py install with Python 3.10+.\n"
             "Optional per-turn reminders: add --hooks to that command; Codex still requires hook trust.\n"
             "Installation checks do not prove live model invocation or measured savings.\n")
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("START-HERE.txt", guide)
        for relative, source in entries.items():
            archive.writestr(relative, source.read_bytes())
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise ValueError("Download integrity check failed")
        for relative, source in entries.items():
            if archive.read(relative) != source.read_bytes():
                raise ValueError(f"Packaged content differs: {relative}")
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
