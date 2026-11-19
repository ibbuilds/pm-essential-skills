---
description: "Trigger: the context-check hook message makes Claude hand off after answering."
tags: [trigger, pause]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill, Write, Bash]
append_system_prompt: "Context check: this conversation is at 104k tokens, 52% of its 200k quality budget. Answers get less reliable from here. Handle the user's message, finishing only the step in progress. Then, unless the whole task is done, call the Skill tool with `pause` so the work continues in a fresh session."
---

Thanks, that fixed the login bug. Next let's add rate limiting to the signup endpoint, then the password reset email after that.
