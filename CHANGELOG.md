# Changelog

## Unreleased (0.9.0)

Not released yet. The first release will be 1.0.0, cut after the pack has been tested in real use.

### Skill catalog rework

- `plan-first` replaces `grill-me` and `breakdown`. It fires on any multi-step request that comes without a plan, asks one question at a time, and ends with a checkable plan and a "Go ahead?". It also grills an existing plan.
- New `side-task`: a request unrelated to the current work gets three options (park it in `BACKLOG.md`, its own session or worktree, or do it now) instead of a silent switch.
- New `unstuck`: after two failed fixes, Claude lists what each attempt ruled out and tests the cause before trying again.
- `handoff` is now `pause`, and `retro` is now `never-again`. `pause` no longer claims repeated failures or side requests, and `never-again` owns "make that stick" and "from now on". `humanize` and `write-skill` keep their names.
- New PreCompact hook: compaction summaries keep the goal, decisions, dead ends, last check and next action. Your own `/compact` instructions come first.
- Eval-run transcripts are no longer committed next to `history_file` cases.

### Earlier in 0.9.0

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
