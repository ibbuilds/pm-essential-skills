---
name: grilling
description: 'Plan interrogation. Use when the user says "grill me", "poke holes in this", "stress-test my plan", "challenge me", "play devil''s advocate" or "what am I missing" about a plan or decision, even when the plan looks complete and a written review would be quicker.'
metadata:
  type: collaborative
---

# Grilling

**Grilling** is a relentless interview that walks the decision tree of a plan one question at a time, until you and the user share the same picture of what will happen.

## Process

1. Read what already exists: the plan, any file the user points to, the documents or code around it. Every fact you can look up is a question you skip. Done when you know which decisions are still open.
2. Pick the open decision that would hurt most if it were wrong. Ask one question about it: a single sentence with a single question mark, answerable in a line. Save every follow-up for a later turn.

   <question-template>
   **Q{n}. {the question}**
   Why it matters: {what goes wrong if this answer is wrong, in one sentence}
   My recommendation: {the answer you would pick, and why}
   </question-template>

   Done when your message ends with the recommendation line and you are waiting for the answer.
3. Take the answer and follow its branch. A new dependency, a contradiction with an earlier answer, or a vague word such as "soon", "most" or "should be fine" gets the next question. When a branch is settled, return to the most dangerous decision still open. Done when every branch is settled or deliberately parked.
4. Close with the decision log, then name the first concrete action:

   <decision-log>
   | # | Decision | Answer | Status: settled, or parked and why |
   </decision-log>

When the user can't answer a question themselves, offer to turn the open decisions into a questionnaire for whoever can: one question per line, each with its context and your recommended answer.
