---
type: llm
focus: { source: file, path: HANDOFF.md }
---

PASS if the document states all of these: the goal; the decision to use the csv module instead of pandas and the reason; the exact test command `python -m pytest -q` with its last result (14 passed, 1 failed, test_export_handles_unicode); the cause (file opened without an encoding); and one concrete next action.
FAIL if any of these is missing or vague.
