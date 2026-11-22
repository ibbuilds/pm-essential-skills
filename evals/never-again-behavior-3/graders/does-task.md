---
type: llm
---

PASS if the reply does the corrected task: it installs or gives the command to install prettier as a dev dependency with pnpm (pnpm add -D prettier), not npm.
FAIL if it uses npm, or only discusses rules and never handles the install.
