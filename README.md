# PM Essential Skills

A Claude Code plugin that handles the parts of working with Claude you'd otherwise manage yourself: agreeing a plan before work starts, keeping one task per session, breaking out of fix-it loops, handing work over to a fresh session, and making corrections stick so you stop repeating them.

You don't need to remember any of it. Each skill starts on its own when the situation fits, and you can still call one by name, such as `/pm-essential-skills:pause`. It works for any kind of work, not only code.

**Status:** pre-release (0.9.0), installed from `main`.

## Install

In Claude Code:

```
/plugin marketplace add ibbuilds/pm-essential-skills
/plugin install pm-essential-skills@pm-essential-skills
```

The hooks need [Node.js](https://nodejs.org) on your PATH. The skills work without it.

## The skills

### plan-first: agree the plan before the work

- **What it does:** turns a vague or large goal into a plan you have agreed to, so Claude doesn't build the wrong thing.
- **When it starts:** you ask for something open-ended ("I want a website for my bakery", "help me organize the school fundraiser", "research the best booking software for my clinic"), or you say "grill me", "poke holes in this", "break this down", "where do I start". It stays out of the way for specific requests like "fix the typo on line 3".
- **What happens:** Claude looks up what it can, then asks one question at a time, the riskiest first, each with its own recommended answer. Then you get a plan with a finish line, milestones you can check and a "Go ahead?". Nothing starts until you say go. Say "just go" and it takes its own recommendations.

### side-task: one task per session

- **What it does:** stops an unrelated request from quietly taking over the work in progress.
- **When it starts:** mid-task, you bring up something else: "oh, also…", "while you're at it…", "remind me to…", "separately, can we…".
- **What happens:** Claude saves the current step and offers three choices: park it in `BACKLOG.md`, start it in its own session (with a short brief to paste), or do it now if it takes a minute. Parked items show up again the next time you start Claude in that folder.

### unstuck: stop guessing after two failed fixes

- **What it does:** breaks the loop where each fix is a small variation of the last one.
- **When it starts:** the same problem survives two fixes: "still broken", "same error", "that didn't work either", "we're going in circles". It works for code, spreadsheet formulas, bounced emails or a broken export alike.
- **What happens:** no fourth guess. Claude lists what each attempt ruled out, names two or three possible causes and runs the one check that tells them apart. If only you can see the evidence, it asks you one question. The fix comes after that and targets the cause.

### pause: continue tomorrow, or in a fresh session

- **What it does:** writes down where the work stands so a new session can carry on without asking you anything.
- **When it starts:** "pause", "I have to stop", "pick this up tomorrow", "this chat is getting long", or when the context check below fires.
- **What happens:** Claude checks the real state of things and writes `HANDOFF.md` with the goal, decisions, dead ends, the last check and its exact result, and the next action. Run `/clear` (or come back tomorrow), say "continue", and the new session picks it up on its own.

### never-again: make a correction stick

- **What it does:** turns something you had to correct into a lasting fix, so you don't say it a third time.
- **When it starts:** you correct the same thing a second time ("I already told you, we use pnpm"), or you say "never again", "make that stick", "from now on, always…", "let's do a retro".
- **What happens:** Claude first does what you asked, then proposes the cheapest fix that will hold: a line in the project's `CLAUDE.md`, a note in its memory, a hook for something that must happen every time, or a skill for a repeated procedure. It shows the exact change and applies it only if you approve.

### humanize: writing that doesn't sound like a chatbot

- **What it does:** keeps emails, posts and letters you send as your own free of the habits that give AI text away.
- **When it starts:** you ask for something you'll send or publish yourself (an email to your team, a LinkedIn post, a cover letter), or say "this sounds like AI" or "make it sound like me".
- **What happens:** you get shorter, plainer text in your own tone, with no invented details. Where a fact is missing, you get a `[placeholder]` instead of a made-up story.

## Hooks: automatic, no skill needed

- **Context check.** At 50% of a 200k-token budget, and every 25% after that, Claude finishes the current step and runs `pause`. Every turn re-sends the whole conversation, and answers get less focused as it grows, so the budget doesn't grow with a 1M-token window. If you already set your own auto-compact window (`autoCompactWindow` in settings or `CLAUDE_CODE_AUTO_COMPACT_WINDOW`), the check stays quiet and leaves context to your setup.
- **Pick up where you left off.** At startup or after `/clear`, a `HANDOFF.md` from the last 72 hours loads by itself, and parked `BACKLOG.md` items are listed in one line.

| Variable | Default | Effect |
| --- | --- | --- |
| `PM_CONTEXT_WATCH` | on | `off` turns the context check off |
| `PM_CONTEXT_BUDGET` | `200000` | Tokens counted as 100%. Setting it also turns the check on when you have your own compact window |
| `PM_CONTEXT_WARN_PERCENT` | `50` | First pause prompt |
| `PM_CONTEXT_WARN_STEP` | `25` | Repeat every this many percent |
| `PM_HANDOFF_MAX_AGE_HOURS` | `72` | Ignore older handoffs |

## Does it help?

Each skill was tested with `claude plugin eval` on realistic prompts, with the plugin and without it (Claude Code 2.1.325–2.1.328, Opus 5.5, Sonnet judge). Passing runs out of total:

| Skill | Behavior cases: with plugin | Without plugin | Trigger cases (fires when it should, stays quiet when it shouldn't) |
| --- | --- | --- | --- |
| `plan-first` | 12/12 | 0/12 | 13 of 13 cases, 6 of them near-misses |
| `unstuck` | 6/6 | 0/6 | 8 of 8 cases |
| `pause` | 6/6 | 2/6 | 6 of 6 cases |
| `never-again` | 9/9 | 2/9 | 12 of 12 cases |
| `side-task` | 5/6 | 3/6 | 9 of 9 cases |
| `humanize` | 5/6 | 1/6 | 6 of 6 cases |

What this does and doesn't show:

- **Proven:** with the plugin, Claude asks before building, stops patching after two failed fixes, writes a usable handoff, offers a lasting fix for a repeated correction, and keeps an unrelated request from taking over. Without it, Claude mostly didn't do these things.
- **Weaker:** `side-task` adds little once you have already chosen "park it" (3/3 either way). `humanize` helps most when writing from scratch (3/3 vs 0/3). On rewriting obviously AI-sounding text, Claude already does fair work.
- **Not measured:** token savings in real use, the context check's effect on answer quality, and the hand-offs to SWE Essential Skills (the eval runner installs only this plugin). The hooks are covered by unit tests, not by evals.

## Spending fewer tokens

- **Keep sessions short.** Every turn re-sends the whole conversation. `pause`, `side-task` and the context check exist for this.
- **Keep `CLAUDE.md` short.** It's sent with every request. `never-again` merges new rules into existing lines instead of piling them up.
- **Don't switch model, effort or fast mode mid-session.** Each switch re-sends the conversation without the cache.
- **Resume on purpose.** A conversation resumed after its cache expired is re-sent at full price, so a handoff and a fresh session usually costs less.

## Works with

- **SWE Essential Skills.** If it's installed, `plan-first` hands software feature specs to its `spec` skill and ticket splitting to `tickets`, and `unstuck` uses `diagnose` to reproduce a code bug. Each situation has one owner.
- **Your own setup.** Compaction, cost warnings and model routing are left to Claude Code and your global configuration. [docs/RUNTIME.md](docs/RUNTIME.md) lists what moved out of this plugin and why.

## Left out on purpose

Each of these was tested or checked and dropped, because Claude or Claude Code already does it well:

- `research`, `verify-done`, `context-audit`, `catch-up`, `recall` and `cold-read` didn't beat Claude's default behavior in evals.
- `write-skill` overlapped Anthropic's skill-creator and the built-in `/skill-doctor`.
- The compaction brief, the cold-resume cost warning, the Concise output style and the work-habits snippet duplicated Claude Code's built-ins or your global setup. See [docs/RUNTIME.md](docs/RUNTIME.md).
- Built-ins already cover searching with subagents (Explore), worktrees (`claude -w`), quick side questions (`/btw`), undoing a wrong turn (`/rewind`) and "remember this" (auto memory).

## Credits

Ideas adapted from these sources, with the text rewritten:

- [Matt Pocock's skills](https://github.com/mattpocock/skills) (MIT): grill-me (now part of `plan-first`) and handoff (now `pause`).
- [obra/superpowers](https://github.com/obra/superpowers) (MIT, Jesse Vincent): plan before building, stop after repeated failed fixes, baseline-first skill testing.
- [blader/humanizer](https://github.com/blader/humanizer) (MIT) and [pstack's unslop](https://github.com/cursor/plugins/tree/main/pstack) (MIT, Lauren Tan): the catalogue of AI-writing tells.
- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT): what a session boundary must carry.
- [HumanLayer](https://github.com/humanlayer/humanlayer) (Apache-2.0, Dex Horthy): recording dead ends and keeping context well below the window.
- [Chroma's "Context Rot" study](https://www.trychroma.com/research/context-rot) and the [Claude Code docs](https://code.claude.com/docs): quality drops with length, start fresh after two failed corrections, and anything corrected twice belongs in `CLAUDE.md`.

## Contributing

The skill standard and the check commands are in [.claude/CLAUDE.md](.claude/CLAUDE.md). Eval cases and their format are in [evals/](evals), and the hook tests are in [tests/](tests).

## License

MIT. See [LICENSE](LICENSE).
