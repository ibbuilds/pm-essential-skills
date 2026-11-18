---
name: breakdown
description: 'Project breakdown. Use when the user says "break this down", "plan this project", "what are the steps", "where do I start" or "what''s the order of things" for a goal that takes more than a day, even when a quick bullet list of tasks would answer faster.'
metadata:
  type: technique
---

# Breakdown

A **breakdown** turns a goal into milestones, where each milestone is a state of the world you can check, not an activity.

## Process

1. Name the finish line: what is true when the whole goal is done, and by when. Done when it is one checkable sentence.
2. Work backwards to milestones. Each one ends in a state someone could verify, such as "venue contract signed for March 14" instead of "find a venue". Put the riskiest or slowest unknown as early as its dependencies allow. Done when every milestone has a checkable done condition.
3. Mark what each milestone needs first. Milestones with no dependency between them can run in parallel; say so. Done when every milestone lists its dependencies or "none".
4. Present the plan:

   <breakdown-template>
   **Finish line:** {checkable end state, date}

   | # | Milestone | Done when | Needs | Target date |
   | --- | --- | --- | --- | --- |
   | M1 | {name} | {verifiable condition} | none | {date} |

   **Start now:** {the first concrete action on M1}
   **Biggest risk:** {the unknown most likely to move the finish line}
   </breakdown-template>

When the user asks to save or track the plan, write the same table to a file they name, or to `PLAN.md`.
