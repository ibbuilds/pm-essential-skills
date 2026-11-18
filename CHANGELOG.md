# Changelog

## Unreleased (0.9.0)

Not released yet. The first release will be 1.0.0, cut only after the pack has been tested in real use.

What the pack contains today, compared with the legacy suite (kept at commit `6fd518f`):

- Rebuilt as a Claude Code plugin with a marketplace manifest, a skill lint script, unit tests, CI and `claude plugin eval` cases for every skill.
- Skills: `grill-me`, `handoff`, `humanize`, `breakdown`, `retro` and `write-skill`.
- `UserPromptSubmit` hook: at 50% of a 200k-token quality budget (`PM_CONTEXT_BUDGET`), and every 10% after, Claude finishes the step in progress and runs `handoff`. It reads only the end of the transcript, ignores subagent usage and stays silent inside subagents.
- `SessionStart` hook: loads a recent `HANDOFF.md` after `/clear` or at startup, and warns before a resumed conversation re-sends a large expired cache.
- `handoff` fires on the context check, after two failed corrections of the same problem, and when an unrelated task starts late in a long session. It records dead ends and files to read first, keeps `HANDOFF.md` out of git through `.git/info/exclude`, and ends with `/clear` then "continue".
- `humanize` writes emails, posts and letters without AI-writing tells and without inventing details.
- A Concise output style and an optional work-habits snippet for `CLAUDE.md`.
- Tested and dropped, because Claude already did them well without help: `research`, `verify-done`, `context-audit`, `catch-up`, `recall`, `cold-read`, and a `/grill-me` wrapper that only duplicated the skill.

Withdrawn: versions 1.0.0 and 2.0.0 were tagged on 2026-11-18 before real-world testing. Their tags and GitHub releases have been deleted, and their changes are included above.
