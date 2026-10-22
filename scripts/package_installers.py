#!/usr/bin/env python3
"""Build standalone Windows-friendly downloads, with no Git or plugin dependency."""

import argparse
import json
import hashlib
import os
import tempfile
from pathlib import Path
from archive_builder import write_archive

from skill_resources import resource_errors
from activation import NAMES as SKILLS

ROOT = Path(__file__).resolve().parents[1]


def build(output, skills, root=ROOT):
    if not skills or set(skills) - set(SKILLS):
        raise ValueError("Unknown or empty skill selection")
    entries = {"Install.cmd": root / "Install.cmd",
               "README.md": root / "docs/installer-download.md"}
    if (root / "LICENSE").exists():
        entries["LICENSE"] = root / "LICENSE"
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
             "Check: Install.cmd status\nRemove and restore originals: Install.cmd uninstall\n"
             "Interrupted operation: Install.cmd recover (same profile).\n"
             "Read README.md for recovery, profiles, requirements, and evidence limits.\n\n"
             "Other systems: run python3 scripts/install_suite.py install with Python 3.10+.\n"
             "Optional per-turn reminders: add --hooks to that command; Codex still requires hook trust.\n"
             "Installation checks do not prove live model invocation or measured savings.\n")
    write_archive(output, entries, {"START-HERE.txt": guide})
    return {"archive": str(output.resolve()), "skills": list(skills), "files": len(entries) + 1,
            "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
            "size_bytes": output.stat().st_size, "license_included": "LICENSE" in entries}


def write_metadata(output, text):
    """Replace one metadata file atomically, without following output symlinks."""
    if output.is_symlink():
        raise ValueError("Linked metadata outputs are not supported")
    descriptor, temporary = tempfile.mkstemp(prefix=".pm-metadata-", dir=output.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(text.encode("utf-8"))
        os.replace(temporary, output)
    finally:
        Path(temporary).unlink(missing_ok=True)


def build_all(output_dir, root=ROOT):
    output_dir = Path(output_dir)
    if output_dir.resolve().is_relative_to((root / "skills").resolve()):
        raise ValueError("Downloads must be outside skill sources")
    output_dir.mkdir(parents=True, exist_ok=True)
    metadata = [output_dir / "distribution.json", output_dir / "SHA256SUMS"]
    for path in metadata:
        if path.is_symlink():
            raise ValueError("Linked metadata outputs are not supported")
    # A failed rebuild must not leave an old completeness/integrity claim.
    for path in metadata:
        path.unlink(missing_ok=True)
    version = json.loads((root / "plugin.json").read_text(encoding="utf-8"))["version"]
    choices = [("pm-essential-skills", SKILLS), *((name, (name,)) for name in SKILLS)]
    results = [build(output_dir / f"{name}.zip", skills, root) for name, skills in choices]
    artifacts = [{**result, "archive": Path(result["archive"]).name} for result in results]
    manifest = {"schema_version": 1, "source_version": version,
                "evidence": "Local packaging only; not a release or live host certification.",
                "artifacts": artifacts}
    try:
        write_metadata(metadata[0], json.dumps(manifest, indent=2) + "\n")
        write_metadata(metadata[1], "".join(
            f"{item['sha256']}  {item['archive']}\n" for item in artifacts))
    except Exception:
        for path in metadata:
            path.unlink(missing_ok=True)
        raise
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "work/downloads")
    args = parser.parse_args()
    for result in build_all(args.output_dir):
        print(json.dumps(result))


if __name__ == "__main__":
    main()
