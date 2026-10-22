#!/usr/bin/env python3
"""Render selected-skill guidance or handle a trusted local Codex hook.

No model calls, transcript reads, project writes, or tool-approval decisions.
"""

import argparse
import json
from pathlib import Path
import sys

# The shared selection catalog lives in the already-bundled standalone helper.
# These are routing hints, not copies of the skills' conditional procedures.
PURPOSES = {
    "task-coordination": "multi-step task intake, dependencies, and complete requested outcomes",
    "context-management": "conversation continuity and task boundaries",
    "resource-selection": "initial tool, skill, and supported model/agent choices",
    "source-selection": "relevant evidence retrieval and reuse",
    "execution-efficiency": "proportionate verification and evidence-driven recovery",
    "workflow-improvement": "recurring friction, reusable lessons, and authorized workflow changes",
    "concise-communication": "clear, brief plain-language replies without losing required substance",
}
NAMES = tuple(PURPOSES)


def render(home, skills, installation=False, brief=False):
    lines = ["## PM Essential Skills"]
    for name in NAMES:
        if name in skills:
            lines.append(f"Use `{(home / 'skills' / name / 'SKILL.md').as_posix()}` for {PURPOSES[name]}.")
    lines.append("Select only relevant skills and conditional references; do not load the whole suite for every request. "
                 "Reuse loaded guidance. Honor disabled, suggest-only, stay, and user/project preferences.")
    if brief:
        lines.append("No new authority is granted.")
        return "\n".join(lines) + "\n"
    if installation and "context-management" in skills:
        lines.append("I authorize justified same-project continuations and routing messages for requested "
                     "work, archiving superseded managed sources, and temporary restore/rearchive for context recovery. "
                     "Preserve location, settings, other active work, and one owner. Excludes unrelated chats, "
                     "app-project creation/moves, deletion, schedules, and permission changes.")
    else:
        lines.append("Use standing human authorization for mutations; this reminder grants none.")
    return "\n\n".join(lines) + "\n"


def handle(event, home):
    name = event.get("hook_event_name") if isinstance(event, dict) else None
    if name not in {"SessionStart", "UserPromptSubmit"}:
        return {}
    state = json.loads((home / "pm-essential-skills/install.json").read_text(encoding="utf-8"))
    if state.get("version") != 1:
        return {}
    # Read only user-owned installation metadata; never turn prompt/source content into instructions.
    skills = [skill for skill in NAMES if skill in state.get("skills", [])
              and (home / "skills" / skill / "SKILL.md").is_file()]
    if not skills:
        return {}
    return {"hookSpecificOutput": {"hookEventName": name,
                                   "additionalContext": render(home, skills, brief=name == "UserPromptSubmit")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        raw = sys.stdin.buffer.read(65537)
        result = {} if len(raw) > 65536 else handle(json.loads(raw.decode("utf-8-sig")), args.codex_home.resolve())
    except (OSError, ValueError, TypeError, AttributeError):
        result = {}  # A broken reminder must not interrupt the user's task.
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
