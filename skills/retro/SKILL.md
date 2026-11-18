---
name: retro
description: 'Session retrospective. Use when the user says "retro", "retrospective", "what went wrong", "what should we do differently" or "so this doesn''t happen again" about a working session with Claude, even when the lessons seem obvious enough to just list.'
metadata:
  type: technique
---

# Retro

A **retro** turns the friction in a working session into changes that stop it from coming back.

## Process

1. List each friction point as it happened: what Claude did, what the user wanted instead. Done when every point is one concrete line.
2. Give each point one destination, the cheapest one that will actually hold: no change, a fix to code or docs, a line in CLAUDE.md, a reply preference, a skill edit, or a hook when it must hold every time. Done when every point has a destination.
3. Present the changes for approval:

   <retro-template>
   | # | What happened | Destination | Exact change |
   | --- | --- | --- | --- |
   | 1 | {friction} | {file or mechanism} | {the exact line, setting or diff} |

   Apply these? {list the numbers}
   </retro-template>

   Done when each row holds text the user could apply as is.
4. Apply only the rows the user approves. For a skill edit, call the Skill tool with `write-skill`.
