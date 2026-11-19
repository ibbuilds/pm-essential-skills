# PM Essential Skills

Skills that make Claude Code plan before it works, stay on one task, get unstuck, and keep sessions short so you spend fewer tokens. They work for anyone who uses Claude Code, whatever your job.

You don't call them. Each skill fires on its own when the moment fits, and you can still call one by name, such as `/pm-essential-skills:pause`.

**Status: pre-release (0.9.0).** It installs from `main` until 1.0.0.

## Install

```
/plugin marketplace add ibbuilds/pm-essential-skills
/plugin install pm-essential-skills@pm-essential-skills
```

The hooks need [Node.js](https://nodejs.org) on your PATH.

## Skills

| Skill | Fires when | What you get |
| --- | --- | --- |
| `plan-first` | You ask for anything with more than one step and no plan ("I want to make a website for my bakery"), or say "grill me", "poke holes in this", "where do I start" | One question at a time, the riskiest first, each with a recommended answer. Then a plan with a finish line and milestones you can check, and a "Go ahead?" before any work starts. Say "just go" and it uses its recommendations. |
| `side-task` | Mid-task, you bring up something unrelated ("oh, also…", "remind me to…") | Three options instead of a silent switch: park it in `BACKLOG.md`, open its own session (`claude -w <name>` for code, with a brief to paste), or do it now if it takes a minute. |
| `unstuck` | The same problem survives two fixes ("still broken", "same error", "we're going in circles") | No fourth guess. A list of what each attempt ruled out, two or three possible causes, and the one check that tells them apart, or one question for you. Then a fix aimed at the cause. |
| `pause` | "Pause", "pick this up tomorrow", "this chat is getting long", or the context hook fires | A `HANDOFF.md` with the goal, decisions, dead ends, verified state and next action. Run `/clear`, say "continue", and the new session starts where you left off. |
| `never-again` | "Never again", "make that stick", "from now on, always…", "what went wrong" | Each problem matched to the cheapest fix that will hold: a line in CLAUDE.md, a hook, a skill change, or nothing. Nothing changes until you approve it. |
| `humanize` | Writing an email, post or letter you'll send as your own, or "this sounds like AI" | Text without the habits that give away a chatbot, and with no invented details. |
| `write-skill` | "Create a skill that…", "this skill never fires" | The right tool for the job (hook, CLAUDE.md line or skill). For a skill: eval cases first, then a short SKILL.md. |

No two skills share a trigger. Each one has eval cases that check it fires when it should and stays silent on near misses.

## Hooks

- **Context budget.** At 50% of a 200k-token budget, and every 10% after that, Claude finishes the current step and runs `pause`. Quality drops with conversation length, not with window size, so a 1M window doesn't move this point.
- **Auto-resume.** After `/clear`, or when you restart in the same folder, a `HANDOFF.md` from the last 72 hours loads by itself.
- **Better compaction.** When the conversation compacts, the summary keeps the goal, decisions, dead ends, last check and next action, and drops raw tool output. Your own `/compact` instructions come first.
- **Cold-resume warning.** Resuming a big conversation whose cache has expired tells you what the next message will re-send, so you can start fresh instead.

| Variable | Default | Effect |
| --- | --- | --- |
| `PM_CONTEXT_BUDGET` | `200000` | Tokens counted as 100% |
| `PM_CONTEXT_WARN_PERCENT` | `50` | First pause prompt |
| `PM_CONTEXT_WARN_STEP` | `10` | Repeat every this many percent |
| `PM_HANDOFF_MAX_AGE_HOURS` | `72` | Ignore older handoffs |
| `PM_RESUME_WARN_TOKENS` | `50000` | Smallest conversation that gets a cold-resume warning |

## Does it help?

Measured with `claude plugin eval`: 3 runs per case, Sonnet as judge, the same prompts with and without the plugin. Scores are the share of checks passed.

| Skill | With the plugin | Without |
| --- | --- | --- |
| `plan-first` | Asks one sharp question before building: 100%. Grills an existing plan one question at a time: 100%. Reads PLAN.md instead of asking what's in it: 100% | 0%, 0%, 50% |
| `side-task` | Offers park, new session or now instead of starting the side task: 100% | 0% |
| `unstuck` | Asks for the one missing piece of evidence instead of a fourth variant: 100%. States causes and checks the input first: 100% | 0%, 50% |
| `pause` | Handoff with verified state and the exact last test result: 100% | 56–58% |
| `never-again` | Routes each fix to the right place: 100% | 0% |
| `humanize` | Drafts without AI tells: 100%. Rewriting a draft: about even | 0% |
| `write-skill` | Writes a skill to the standard: 67–89%. Picking a hook over a skill: about even | 33% |

Triggers fire on every measured prompt that should fire them, and every near miss stays silent. Two `plan-first` prompts (dark mode, EHR research) are not fully measured yet. The `pause`, `never-again`, `humanize` and `write-skill` behavior numbers come from 0.9.0. Their skill bodies haven't changed since.

## Saving tokens

- **Short sessions.** Every turn re-sends the whole conversation, and the hooks above keep it small.
- **Short CLAUDE.md.** It's part of every request.
- **Don't switch mid-session** between models, effort levels or fast mode. Each switch re-sends the conversation without the cache.
- **Resume on purpose.** A conversation resumed after its cache expired is re-sent at full price, so a handoff and a fresh session usually costs less.

## Also included

- **Concise output style:** answer first, in plain words. Turn it on with `/output-style`.
- **Work habits:** optional lines for your own `CLAUDE.md`, in [snippets/work-habits.md](snippets/work-habits.md).

## Left out on purpose

These were tested and dropped because Claude already does them well: research, verify-done, context-audit, catch-up, recall, cold-read. Built-ins already cover subagent search (Explore), worktree setup (`claude -w`) and quick side questions (`/btw`).

## Credits

Ideas adapted from, with the text rewritten:

- [Matt Pocock's skills](https://github.com/mattpocock/skills) (MIT): grill-me (now part of `plan-first`) and handoff (now `pause`).
- [obra/superpowers](https://github.com/obra/superpowers) (MIT, Jesse Vincent): plan before building, stop after repeated failed fixes, baseline-first skill testing.
- [blader/humanizer](https://github.com/blader/humanizer) (MIT) and [pstack's unslop](https://github.com/cursor/plugins/tree/main/pstack) (MIT, Lauren Tan): the catalogue of AI-writing tells.
- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT): what a session boundary must carry.
- [HumanLayer](https://github.com/humanlayer/humanlayer) (Apache-2.0, Dex Horthy): recording dead ends and keeping context well below the window.
- [Chroma's "Context Rot" study](https://www.trychroma.com/research/context-rot) and the [Claude Code docs](https://code.claude.com/docs): quality drops with length, and you should start fresh after two failed corrections.

## Contributing

The skill standard and the check commands are in [.claude/CLAUDE.md](.claude/CLAUDE.md). Eval cases live in [evals/](evals), and hook tests in [tests/](tests).

## License

MIT. See [LICENSE](LICENSE).
