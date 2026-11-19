# Changelog

## Unreleased (0.9.0)

Not released yet. The first release will be 1.0.0, cut after the pack has been tested in real use.

### Responsibilities pass

- The context check steps aside when you already set an auto-compact window (`autoCompactWindow` or `CLAUDE_CODE_AUTO_COMPACT_WINDOW`), so it no longer competes with your own context policy. It repeats every 25% instead of every 10%, and `PM_CONTEXT_WATCH=off` turns it off.
- Removed the PreCompact brief and the cold-resume cost warning. Compaction and cost policy belong to Claude Code and your global setup. [docs/RUNTIME.md](docs/RUNTIME.md) records what moved and what a runtime should own.
- Removed the Concise output style (Claude Code has a built-in one with the same name) and the work-habits snippet (orchestration rules that belong in your global setup).
- `plan-first` hands software specs and ticket splitting to SWE Essential Skills' `spec` and `tickets` when they're installed, and `unstuck` uses its `diagnose` to reproduce a code bug.
- `humanize`'s last scan also checks for lists of three.

### First-version audit

- `never-again` now fires on its own when you correct the same thing a second time ("I already told you, we use pnpm"): Claude does the task, then offers one exact durable fix and applies it only after a yes. It routes personal preferences to Claude Code's auto memory, merges into existing `CLAUDE.md` lines instead of appending, and no longer claims "remember this", which auto memory handles.
- `side-task` fires only while the current work is unfinished. Its own-session option no longer suggests `/fork`, which copies the whole conversation. A finished task followed by the next one is no longer claimed by `side-task` or `pause`.
- Parked `BACKLOG.md` items now come back: at startup and after `/clear`, a one-line message lists how many are open and the first one.
- `plan-first` adds a stop rule, starts no work before "go", and saves an approved multi-session plan to `PLAN.md` as checkable milestones. New near-miss cases confirm it stays silent on clear, specific requests.
- `write-skill` is removed: Anthropic's skill-creator and `/skill-doctor` cover skill authoring. The eval case format moved to `evals/README.md`.
- The context check is framed around cost and focus. The README is rewritten around what each skill does, when it starts and what you get.

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
