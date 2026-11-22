---
name: side-task
description: 'Side task. Use when the user brings up a different, unrelated piece of work while the current work is still unfinished: "oh, also...", "while you''re at it...", "remind me to...", "separately...", "before I forget...", "can we also do X" where X has nothing to do with the current goal, even when it looks quick and doing it right here feels simplest.'
metadata:
  type: technique
---

# Side task

One session covers one piece of work. A second goal in the same chat makes both slower and costlier, so the user decides where it goes before any of it starts.

## Process

1. Check that it is a side task. It is not one when it is the next step, a correction or a clarification of the current work, when the current work is already finished, or when it is a question answerable in one line (mention `/btw` for those if useful). Done when you can name the current goal and the new request in one line each and they are different pieces of work.
2. Bring only the step in progress to a state that survives a pause, then stop. Start none of the new request. Done when the current work can be resumed later without redoing anything.
3. Reply with this and wait:

   <side-task-reply>
   Current work: {goal}. New request: {request}. These are separate pieces of work.
   (a) Park it: I add it to `BACKLOG.md` and carry on. It is shown again when you next start a session in this folder.
   (b) Own session: {for code in a git repository: run `claude -w {short-name}` in a terminal; otherwise open a new chat}, then paste:
       > {the goal}. {relevant files or constraints}. First: {the first action}.
   (c) Do it now: {only when it takes about a minute and touches nothing in the current work}
   I recommend ({letter}) because {one reason}.
   </side-task-reply>

   Recommend (a) by default, (b) when the request is large or needs its own files and focus, and (c) only when it meets its condition. Done when the reply has the three options, one recommendation and a brief ready to paste.
4. After the user chooses:
   - Park it: append this line to `BACKLOG.md` in the working directory, creating the file if needed, then resume the current step.

     <backlog-line>
     - [ ] {YYYY-MM-DD} {request in the user's words}. Context: {one line on what was in progress}
     </backlog-line>

   - Own session: resume the current work.
   - Do it now: do it, then resume the current work.

   Done when the choice is carried out and the current work has continued.
