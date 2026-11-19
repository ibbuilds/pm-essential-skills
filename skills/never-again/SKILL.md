---
name: never-again
description: 'Fixes that stick. Use when the user corrects the same thing a second time ("I already told you", "again? we use pnpm", "how many times", "like I said", "you did X again"), or asks for a "retro", to look back at how the session went, "what went wrong", "what should we do differently", "make that stick", "from now on, always", "never again", even when apologizing and complying looks like enough.'
metadata:
  type: technique
---

# Never again

A repeated correction or a retro becomes one durable change, applied only after the user approves it.

## Repeated correction

A first correction ("use pnpm, not npm") needs no skill: comply. Use this section when the user corrects the same thing again, in any wording.

1. Do the corrected task first, as the user now asks. Done when the reply carries the corrected result.
2. Pick the destination from the table. Done when exactly one destination is chosen.
3. Check the existing file first. If a line already covers it, replace or merge that line, or move up to a hook; never append a duplicate. Done when the change is a merge or a new line that nothing covers.
4. Add one short offer at the end of the reply, with the exact line or snippet, ending "Add it?". Done when the offer fits in a few lines.
5. Apply only after a yes.

## Destinations

| Situation | Destination |
| --- | --- |
| Personal preference of this one user | Auto memory (code.claude.com/docs/en/memory#auto-memory) |
| Rule the project or team needs every session | A line in the project `CLAUDE.md`, kept under 200 lines |
| Must happen every single time | A hook in `.claude/settings.json` |
| Repeated multi-step procedure | A skill: Anthropic's skill-creator, or a minimal `SKILL.md` |
| One-off or already handled | No change |

For a hook, give the exact `settings.json` entry, with a command that runs on the user's system.

## Retro

When the user asks for a retro, a look back at the session, or to make something stick:

1. List each friction point: what Claude did, what the user wanted instead. Done when every point is one concrete line.
2. Give each point one destination from the table, the cheapest that will hold. Done when every point has one.
3. Present the changes:

   <retro-template>
   | # | What happened | Destination | Exact change |
   | --- | --- | --- | --- |
   | 1 | {friction} | {file or mechanism} | {the exact line, setting or diff} |

   Apply these? {list the numbers}
   </retro-template>

   Done when each row holds text the user could apply as is.
4. Apply only the rows the user approves.
