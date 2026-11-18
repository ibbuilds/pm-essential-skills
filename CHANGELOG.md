# Changelog

## Unreleased

- Rebuilt as a Claude Code plugin with a marketplace manifest.
- Removed the legacy suite: eight skills, design and audit documents, Python helpers, the installer, Codex adapters and the old tests. It remains available at the `legacy-v0` tag.
- Added `scripts/lint_skills.py`, its tests, a CI workflow and the first eval case.
- Added `grilling` with `/grill-me`, `handoff` and `research`, each with trigger and behavior eval cases.
- Dropped the planned `verify-done` skill: without any skill, Claude already refused unverified completion claims in 9 of 9 eval runs, so the skill had nothing to add.
