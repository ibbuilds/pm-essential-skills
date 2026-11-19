---
name: plan-first
description: 'Plan before work. Use when the user asks for anything that takes more than one step (build, change, improve, research, write, organize, move, launch) without a plan and a clear finish line, or says "grill me", "poke holes in this", "what am I missing", "stress-test my plan", "break this down", "where do I start", "what are the steps" or "what''s the order of things", even when the request looks clear enough to start right away.'
metadata:
  type: technique
---

# Plan first

Agree the finish line before doing the work. Skip this for one-step requests, for a concrete plan the user says to run, and for the next step of already agreed work.

## Process

1. Read what exists: the request, any plan or file the user points to, the documents or code around it. Every fact you can look up is a question you skip. Done when you know which decisions are still open.
2. Ask about the open decision that would hurt most if it were wrong. One sentence with one question mark, answerable in a line. Save every follow-up for a later turn.

   <question-template>
   **Q{n}. {the question}**
   Why it matters: {what goes wrong if this answer is wrong, in one sentence}
   My recommendation: {the answer you would pick, and why}
   </question-template>

   Done when the recommendation is the last line of your message, with no preview of later questions, and you are waiting for the answer.
3. Follow the answer's branch. A new dependency, a contradiction with an earlier answer, or a vague word such as "soon", "most" or "should be fine" earns the next question. Ask as many rounds as the request is vague; a clear request needs one confirmation. If the user says "just go" or "your call", adopt your recommendations. Done when every branch is settled or deliberately parked.
4. Close with the result:
   - The user had no plan: present one and ask "Go ahead?". Work begins when the user says go.
   - The user asked you to challenge their plan: give the decision table and the first action.

   <plan-template>
   **Finish line:** {checkable end state, date}

   | # | Milestone | Done when | Needs |
   | --- | --- | --- | --- |
   | M1 | {a state of the world, not an activity} | {verifiable condition} | none |

   **First action:** {the first concrete step on M1}
   **Biggest risk:** {the unknown most likely to move the finish line}

   | # | Decision | Answer | Settled or parked |
   | --- | --- | --- | --- |
   </plan-template>

   Put the riskiest milestone as early as its dependencies allow, and say which milestones can run in parallel. Done when every milestone has a done condition and its dependencies, and a new plan ends with "Go ahead?".
5. When the work spans more than one session, or the user asks, save the plan to `PLAN.md`.

If the user cannot answer a question, offer a questionnaire for whoever can: one question per line, with context and your recommended answer.
