---
name: handoff
description: 'Session handoff. Use when the user says "hand off", "handoff", "continue in a new chat", "pick this up tomorrow", "save where we are", or the conversation is getting too long to continue, even when the work feels nearly finished and a quick summary in chat seems enough.'
metadata:
  type: technique
---

# Handoff

A **handoff** is a file that lets a fresh session with no memory of this one continue the work without asking the user anything.

## Process

1. Check the real state instead of recalling it: for a repository, the branch, the last commit and uncommitted or untracked files; otherwise the files you created or changed. Done when every state claim in the handoff comes from something you just looked at.
2. Write `HANDOFF.md` in the working directory, replacing any older one:

   <handoff-template>
   # Handoff: {task in a few words}
   **Goal:** {the outcome the user wants}
   **Decisions:** {each decision and the reason for it}
   **State:** {branch, last commit, changed files, what works}
   **Last check:** `{exact command}` → {exact result, e.g. 14 passed, 1 failed: test_name}
   **Next action:** {the single next step, concrete enough to start without questions}
   **Open questions:** {what the user still has to decide, or "none"}
   </handoff-template>

   Refer to secrets by where they live, such as "the Stripe key in `.env`", and never copy their values. Point to long logs by path instead of pasting them. Done when the file has every field filled.
3. End your reply with a prompt the user can paste into the new session:

   <paste-prompt>
   Read HANDOFF.md and continue from "Next action".
   </paste-prompt>
