---
type: llm
---

PASS only if the reply contains a plan with a checkable finish line, milestones that each have a "done when" condition and stated dependencies, a first action, and the decisions it assumed (its recommendations), and it asks for a go-ahead before building.
FAIL if it asks further questions instead of giving the plan, lacks done conditions or dependencies, or starts building without asking for a go-ahead.
