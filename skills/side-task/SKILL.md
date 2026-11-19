---
name: side-task
description: 'Side task. Use when, mid-session, the user brings up a different, unrelated piece of work: "oh, also...", "while you''re at it...", "remind me to...", "separately...", "next let''s do X" where X has nothing to do with the current goal, even when it looks quick and doing it right here in the same session feels simplest.'
metadata:
  type: technique
---

# Side task

One session covers one piece of work. A second goal in the same chat makes both slower and costlier, so the user decides where it goes before any of it starts.

## Process

1. Check that it is a side task. It is not one when it is the next step of the current work, a clarification or correction of it, the first message of the session, or a question answerable in one line (mention `/btw` for those if useful). Otherwise continue. Done when you can name the current goal and the new request in one line each and they are different pieces of work.
2. Finish or checkpoint only the current step, then stop. Do not begin the new request, even partly. Done when the current work is in a state that survives a pause.
3. Reply with this and wait:

   <side-task-reply>
   Current work: {goal}. New request: {request}. These are separate pieces of work.
   (a) Park it: I add one line to `BACKLOG.md` and carry on with the current work.
   (b) Own session: {command and brief for the right case, see below}
   (c) Do it now: only when it takes about a minute and touches nothing in the current work.
   I recommend ({letter}) because {one reason}.
   </side-task-reply>

   Option (b) depends on where the work lives:
   - Code in a git repository: `claude -w <short-name>` opens a new git worktree and branch. Add a 3-line brief to paste: the goal, the relevant files or constraints, the first action.
   - Code you can hand to a background copy: `/fork <prompt>`.
   - Anything else (writing, planning, research): open a fresh chat and paste the same 3-line brief.

   Recommend (a) by default, (b) when the request is large or needs its own files and focus, and (c) only when it truly meets the condition. If the current work is finished, recommend (b) and say this session's context would only add cost to the new work.

   Done when the reply gives the three options, one recommendation, and the brief for (b).
4. After the user chooses:
   - Park it: append one line to `BACKLOG.md` in the working directory, creating the file if needed, then resume the current step.

     <backlog-line>
     - [ ] {YYYY-MM-DD} {request in the user's words}. Context: {one line on what is in progress now}
     </backlog-line>

     Done when the line is in the file and you have continued the current work.
   - Own session: give the command and brief again, ready to copy, then resume the current work.
   - Do it now: do it, then return to the current work.
