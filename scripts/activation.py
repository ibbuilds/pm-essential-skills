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
    "pm-essential-skills-task-coordination": "multi-step task intake, dependencies, and complete requested outcomes",
    "pm-essential-skills-context-management": "conversation continuity and task boundaries",
    "pm-essential-skills-resource-selection": "initial tool, skill, and supported model/agent choices",
    "pm-essential-skills-source-selection": "relevant evidence retrieval and reuse",
    "pm-essential-skills-execution-efficiency": "proportionate verification and evidence-driven recovery",
    "pm-essential-skills-workflow-improvement": "recurring friction, reusable lessons, and authorized workflow changes",
    "pm-essential-skills-concise-communication": "clear, brief plain-language replies without losing required substance",
}
NAMES = tuple(PURPOSES)
# UserPromptSubmit contains the full prompt, not just event metadata. Permit
# ordinary pasted source/documents while bounding malformed or extreme input.
MAX_INPUT_BYTES = 16 * 1024 * 1024
WORKFLOW_CONTRACT = (
    "Matching enabled skills define required workflows, not optional advice. "
    "Retain unmet obligations and scoped exceptions across handoffs; blocked is not complete. "
    "Preserve each skill's no-op paths and optional methods."
)


def render(home, skills, installation=False, brief=False):
    lines = ["## PM Essential Skills"]
    # Each prompt remains self-contained after compaction, without repeating the
    # absolute directory for every entry. Keep purposes so selection needs no reads.
    compact = brief and sum(name in skills for name in NAMES) > 1
    if compact:
        lines.append(f"Skill paths relative to `{(home / 'skills').as_posix()}`:")
    for name in NAMES:
        if name in skills:
            if compact:
                lines.append(f"- `{name}/SKILL.md`: {PURPOSES[name]}.")
            else:
                lines.append(f"Use `{(home / 'skills' / name / 'SKILL.md').as_posix()}` for {PURPOSES[name]}.")
    lines.append(WORKFLOW_CONTRACT)
    if brief:
        lines.append("Select only relevant skills/references, not the whole suite. Reuse loaded guidance; "
                     "honor disabled, suggest-only, stay, and user/project preferences.")
        lines.append("No new authority is granted.")
        return "\n".join(lines) + "\n"
    lines.append("Select only relevant skills and conditional references; do not load the whole suite for every request. "
                 "Reuse loaded guidance. Honor disabled, suggest-only, stay, and user/project preferences.")
    if installation and "pm-essential-skills-context-management" in skills:
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
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        result = {} if len(raw) > MAX_INPUT_BYTES else handle(json.loads(raw.decode("utf-8-sig")), args.codex_home.resolve())
    except (OSError, ValueError, TypeError, AttributeError, RecursionError):
        result = {}  # A broken reminder must not interrupt the user's task.
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
