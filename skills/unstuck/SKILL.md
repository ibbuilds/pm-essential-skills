---
name: unstuck
description: 'Unstuck. Use when the same problem has survived two or more fixes: "still broken", "same error", "that didn''t work either", "we''re going in circles", "third time", in code, a spreadsheet formula, a bouncing email or a failing export, even when one more variation of the last fix looks close enough.'
metadata:
  type: discipline
---

# Unstuck

Two failed fixes mean the picture of the problem is wrong, so a third variation of the same fix will fail too. Find the cause before touching anything.

## Process

1. Stop patching. List every attempt so far, one line each: what was changed and what its failure ruled out. Done when every attempt has a line.
2. Name 2-3 root-cause hypotheses that fit all of the evidence, never only the latest error. Include "my assumption about X is wrong" and "the problem is upstream of where we keep editing". Done when each hypothesis says what it predicts you would see.
3. Run the one cheapest check that separates them: read the real file, log or data, reproduce in a minimal case, or print the actual value. When the evidence lives with the user (their screen, their mailbox, their file), ask exactly one question for it and wait. For a code bug, when the Skill tool lists `swe-essential-skills:diagnose`, call the Skill tool with `swe-essential-skills:diagnose` for this check; it builds the failing reproduction. Done when one hypothesis is confirmed or the single question is out.
4. Propose the fix, aimed at the confirmed cause, and say how to tell it worked. Done when the reply shows the attempts, every hypothesis with the check's verdict on it, and the fix naming the cause it removes.
5. When the conversation is long or full of failed attempts, recommend a fresh session: call the Skill tool with `pause` so the dead ends are recorded and do not mislead the next try. Done when the user has been told why and which step comes next.

<unstuck-template>
**Tried:**
1. {attempt}: ruled out {what}
2. {attempt}: ruled out {what}

**Hypotheses:**
- {cause A}: would show as {observation}
- {cause B}: would show as {observation}

**Check:** {what I ran or read, and the result} / **One question:** {the single thing I need from you}

**Fix:** {change aimed at the confirmed cause, or "after your answer"}
</unstuck-template>

## Why the discipline

These excuses appeared in baseline runs:
- "The error is in this function, so I will patch the function again": the symptom shows where it surfaced, not where it began.
- "A different formula or wording might work": a fourth variant without new evidence is a guess.
- "I can fix it without looking at the input": the input is the cheapest evidence there is.
Do the check before the edit, and ask rather than guess when only the user can see the evidence.
