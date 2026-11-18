---
type: llm
---

CLAUDE.md in this folder already says "Use pnpm, never npm".
PASS if the reply notices that the rule already exists in CLAUDE.md and proposes a stronger mechanism than repeating it, such as a PreToolUse hook that blocks npm commands.
FAIL if the reply only proposes adding or restating the pnpm rule in CLAUDE.md, or does not notice the existing rule.
