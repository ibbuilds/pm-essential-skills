# Changelog

## 1.0.0 (2026-11-18)

- Rebuilt as a Claude Code plugin with a marketplace manifest.
- Removed the legacy suite: eight skills, design and audit documents, Python helpers, the installer, Codex adapters and the old tests. It remains available at commit `6fd518f`.
- Added `scripts/lint_skills.py`, its tests, a CI workflow and the first eval case.
- Added `grilling` with `/grill-me`, `handoff`, `research`, `write-skill`, `breakdown` and `retro`, each with trigger and behavior eval cases.
- Dropped the planned `verify-done` skill: without any skill, Claude already refused unverified completion claims in 9 of 9 eval runs, so the skill had nothing to add.
- Added a `UserPromptSubmit` hook that suggests `/handoff` once the conversation uses 50% of the context window (configurable), a Concise output style, and an optional work-habits snippet for `CLAUDE.md`.
