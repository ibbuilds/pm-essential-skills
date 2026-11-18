---
type: llm
---

PASS if the reply explains that a skill or CLAUDE.md instruction cannot guarantee something every time, and proposes a hook instead (for example a PostToolUse hook on Edit and Write in .claude/settings.json that runs the linter).
FAIL if the reply just writes a skill or a CLAUDE.md rule for it without recommending a hook.
