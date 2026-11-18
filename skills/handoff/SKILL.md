---
name: handoff
description: 'Session handoff. Use when the user says "hand off", "handoff", "continue in a new chat", "pick this up tomorrow", "save where we are" or "this chat is getting long", when a context check says the conversation is past its budget, when the user has corrected the same problem twice and it still fails, or when the user starts an unrelated task late in a long session, even when the work feels nearly finished and a quick summary in chat seems enough.'
metadata:
  type: technique
---

# Handoff

A **handoff** is a file that lets a fresh session, with no memory of this one, continue the work without asking the user anything. Fresh sessions answer better and cost less per turn, so one session covers one piece of work.

## Process

1. Decide whether a handoff is needed. Done when one of these holds:
   - The task is finished or one short step from finished: finish it, tell the user the next task deserves a fresh session (`/clear`), and stop.
   - The user's new request has nothing to do with the work so far: tell them to run `/clear` and ask it there, since nothing needs carrying over, and stop.
   - The same problem has failed after two corrections: the failed attempts now mislead you. Continue to step 2 and record each attempt under **Dead ends**, so the fresh session starts from a better brief.
   - Otherwise, continue to step 2.
2. Look at the real state instead of recalling it: for a repository, `git status`, the branch and the last commit; otherwise the files you created or changed. Done when every state claim you will write comes from something you just looked at.
3. Write `HANDOFF.md` in the working directory, replacing any older one, in under 400 words:

   <handoff-template>
   # Handoff: {task in a few words}
   **Goal:** {the outcome the user wants, in their terms}
   **Decisions:** {each decision and its reason}
   **Dead ends:** {what was tried and failed, and why, so nobody retries it; or "none"}
   **State:** {branch, last commit, changed files, what works}
   **Last check:** `{exact command}` → {exact result, e.g. 14 passed, 1 failed: test_name}
   **Read first:** {the 1–5 files the next session needs, as paths}
   **Next action:** {one step, concrete enough to start without questions}
   **Open questions:** {what the user still has to decide, or "none"}
   </handoff-template>

   Point to secrets by where they live, such as "the Stripe key in `.env`", and never copy their values. Point to logs and long outputs by path. In a git repository, add `HANDOFF.md` to `.git/info/exclude` unless git already ignores it. Done when every field is filled.
4. End your reply with these lines:

   <handoff-reply>
   Handoff saved to HANDOFF.md.
   Next: run `/clear`, then say "continue". The handoff loads on its own.
   In another tool, paste: Read HANDOFF.md and continue from "Next action".
   </handoff-reply>
