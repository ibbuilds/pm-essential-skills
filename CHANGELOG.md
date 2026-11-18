# Changelog

## 2.0.0 (2026-11-18)

Breaking:
- Renamed `grilling` to `grill-me` and removed the `/grill-me` wrapper; any skill can already be called by name.
- Removed `research`: without it, Claude already checked live sources, dated them and preferred the installed version (2 of its 3 behavior cases passed with no plugin), and a multi-source comparison scored no better with it.
- The context hook now measures against a 200k-token quality budget (`PM_CONTEXT_BUDGET`) instead of guessing the window size, and `PM_CONTEXT_WINDOW` is gone. On 1M-token models the old hook first warned at about 500k tokens.

Added:
- `humanize`: writes emails, posts and letters without AI-writing tells and without inventing details. Drafting from scratch: 100% with the skill, 0% without.
- SessionStart hook: loads a recent `HANDOFF.md` after `/clear` or at startup, and warns before a resumed conversation re-sends a large expired cache.
- `handoff` now fires on the context-budget check, after two failed corrections of the same problem, and when an unrelated task starts late in a long session. It records dead ends and files to read first, keeps `HANDOFF.md` out of git through `.git/info/exclude`, and ends with `/clear` then "continue".

Changed:
- The context hook reads only the end of the transcript, ignores subagent usage and stays silent inside subagents.
- The work-habits snippet covers subagent briefs and model choice.
- Tested and dropped, because Claude already did them well without help: `context-audit`, `catch-up`, `recall`, `cold-read`.

## 1.0.0 (2026-11-18)

- Rebuilt as a Claude Code plugin with a marketplace manifest.
- Removed the legacy suite: eight skills, design and audit documents, Python helpers, the installer, Codex adapters and the old tests. It remains available at commit `6fd518f`.
- Added `scripts/lint_skills.py`, its tests, a CI workflow and the first eval case.
- Added `grilling` with `/grill-me`, `handoff`, `research`, `write-skill`, `breakdown` and `retro`, each with trigger and behavior eval cases.
- Dropped the planned `verify-done` skill: without any skill, Claude already refused unverified completion claims in 9 of 9 eval runs, so the skill had nothing to add.
- Added a `UserPromptSubmit` hook that suggests `/handoff` once the conversation uses 50% of the context window (configurable), a Concise output style, and an optional work-habits snippet for `CLAUDE.md`.
