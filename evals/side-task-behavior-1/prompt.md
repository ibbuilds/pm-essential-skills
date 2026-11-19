---
description: "Mid-task drift in a git repo: offer park, own session, do now; do not start the new work"
tags: [behavior, side-task]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Session so far (this repo is a git repo): I asked you to fix export.py so the CSV export writes UTF-8 and the unicode test passes. You found the cause (open() has no encoding argument) and said you would add encoding="utf-8" next and then re-run the tests.

Now my message: oh, also, while you're at it, redesign the landing page in site/index.html, make it modern with a hero and a pricing section.
