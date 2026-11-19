---
type: llm
---

PASS if the reply (1) lists the earlier attempts (the strip fix and the empty-value guard) and what each ruled out, (2) states at least two hypotheses, one of which questions an assumption about the input data format or says the cause is upstream of parse_date, and (3) shows that data/orders.csv was inspected and aims the fix at the real cause: the file uses DD/MM/YYYY (day-first slash dates) rather than YYYY-MM-DD.
FAIL if it only patches parse_date again without referring to the CSV contents, or never lists the earlier attempts.
