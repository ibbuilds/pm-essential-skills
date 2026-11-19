---
type: llm
---

PASS if the reply stops proposing formula rewrites, lists the three earlier attempts and what they ruled out, names at least two possible causes (for example amounts in column C stored as text, hidden characters or trailing spaces in column B, calculation set to manual), and asks the user for one targeted piece of evidence (for example what =ISNUMBER(C2), =LEN(B2) or =COUNTIF(B2:B50,"Paid") returns). A fix that depends on the answer to that check is fine.
FAIL if its main answer is a fourth formula variant to try, or it asks several unrelated questions.
