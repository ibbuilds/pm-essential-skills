---
description: "Trigger, non-code: a VLOOKUP still returns #N/A after two fixes."
tags: [trigger, unstuck]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill, Write]
---

My VLOOKUP still returns #N/A. First you told me to set the last argument to FALSE, then to wrap the lookup value in TRIM, and I'm still getting #N/A on every row. Formula is =VLOOKUP(A2,Prices!A:B,2,FALSE).
