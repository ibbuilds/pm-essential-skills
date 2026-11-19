---
type: llm
---

PASS if the reply stops proposing formula rewrites, lists the three earlier attempts and what they ruled out, names at least two hypotheses (for example amounts in column C stored as text, hidden characters or trailing spaces in column B, calculation set to manual), and asks exactly one targeted question or request for evidence (for example what =ISNUMBER(C2) or =LEN(B2) returns) before proposing a fix.
FAIL if it offers a fourth formula variant as the answer without separating the hypotheses, or asks several unrelated questions.
