# PM Essential Skills

A Claude Code plugin that makes Claude better at the work around the work: stress-testing a plan, keeping every session short and focused, writing like a person, planning a project and learning from each session. Nothing here depends on your profession. It helps an engineer, a nurse, a researcher or a founder alike.

Every skill earned its place in an eval: Claude does measurably worse without it. Ideas that Claude already handles on its own were tested and dropped (see [What was cut](#what-was-cut)).

## Install

In Claude Code:

```
/plugin marketplace add ibbuilds/pm-essential-skills
/plugin install pm-essential-skills@pm-essential-skills
```

Skills load on their own when your request matches them. You can also call any of them by name, for example `/pm-essential-skills:handoff`. The hooks need [Node.js](https://nodejs.org) on your PATH.

## Skills

| Skill | Say something like | What you get |
| --- | --- | --- |
| `grill-me` | "Grill me on this plan", "poke holes in this", "what am I missing?" | One question at a time, the riskiest first, each with a recommended answer. Ends with a log of every decision. |
| `handoff` | "Hand this off", "continue tomorrow", "this chat is getting long" | A `HANDOFF.md` with the goal, decisions, dead ends, verified state, last check and next action. Run `/clear`, say "continue", and the fresh session picks it up. |
| `humanize` | "Write a post announcing…", "this sounds like ChatGPT", "make it sound like me" | Emails, posts and letters without the habits that make readers think a chatbot wrote them, and without invented details. |
| `breakdown` | "Break this down", "plan this project", "where do I start?" | Milestones written as states you can check, each with its dependencies and a "done when". |
| `retro` | "Let's do a retro", "how do we stop this happening again?" | Each friction point paired with the cheapest fix that will hold: a CLAUDE.md line, a hook, a skill change or nothing. Applied only after you approve. |
| `write-skill` | "Create a skill that…", "make this stick" | The right tool for the job (hook, CLAUDE.md, output style or skill). For a skill: eval cases first, then a lean SKILL.md. |

Measured with `claude plugin eval`, pass rate with the plugin vs without:

| Skill | Behavior cases | Trigger cases |
| --- | --- | --- |
| `grill-me` | 100% vs 0–50% | 6/6 |
| `handoff` | 100% vs 56–58% | 10/10 |
| `humanize` | drafting: 100% vs 0%; rewriting: about even | 6/6 |
| `breakdown` | 100% vs 0% | 6/6 |
| `retro` | 100% vs 0% on routing fixes; even on spotting an ignored rule | 6/6 |
| `write-skill` | 89% vs 33% on writing a skill to the standard | 6/6 |

## Sessions that stay sharp

Answers get less reliable as a conversation grows, whatever the size of the model's window. The plugin keeps each session to one piece of work, with two hooks:

- **Context budget.** Before each prompt, a hook reads how many tokens the conversation uses. At 50% of a 200k-token quality budget (100k tokens), and every 10% after, it tells Claude to finish the step in progress and run `handoff`. The budget is deliberately not the model's window: on a 1M-token model, 50% of the window would be 500k tokens, far past the point where quality drops.
- **Auto-resume.** After `/clear`, or when you start Claude Code in the same folder, a hook loads a `HANDOFF.md` written in the last 72 hours. Say "continue" and the new session re-checks the state and starts from the next action. It deletes the file when the work is done.
- **Cold-resume warning.** When you resume a large conversation whose prompt cache has expired, a hook tells you what the next message will re-send (for example "182k tokens, about $1.14 at API rates") so you can start fresh instead.

Settings, as environment variables:

| Variable | Default | Effect |
| --- | --- | --- |
| `PM_CONTEXT_BUDGET` | `200000` | Tokens treated as 100% |
| `PM_CONTEXT_WARN_PERCENT` | `50` | First handoff prompt |
| `PM_CONTEXT_WARN_STEP` | `10` | Repeat every this many percent |
| `PM_HANDOFF_MAX_AGE_HOURS` | `72` | Ignore older handoffs |
| `PM_RESUME_WARN_TOKENS` | `50000` | Smallest conversation that gets a cold-resume warning |

## Saving tokens

Claude Code caches the start of every request on its own. No skill can switch caching on or off, so the plugin works on the two things that do move cost: how big each request is, and how often the cache is thrown away.

- **Short sessions.** Every turn re-sends the whole conversation. The hooks above keep it small.
- **Keep `CLAUDE.md` short.** It is part of every request. Edits take effect at the next session or `/clear`, so they don't break the cache mid-session.
- **Don't switch mid-session** between models, effort levels or fast mode, or add and remove MCP servers that load their tools up front. Each one re-sends the conversation without the cache.
- **Resume deliberately.** A resumed conversation past its cache lifetime (5 minutes on API keys, 1 hour on most subscriptions) is re-sent at full price. A handoff plus a fresh session is usually cheaper.
- **Install only the skills you use.** Each model-invoked skill adds its description to every request.

## Also included

- **Concise output style.** Answer first, in plain words. Turn it on with `/output-style`.
- **Work habits.** Optional lines for your own `CLAUDE.md` in [snippets/work-habits.md](snippets/work-habits.md): scripts for bulk work, cheaper models for subagent lookups, temporary files cleaned up, git instead of backup copies.

## What was cut

Each of these was built as an eval first and dropped because Claude already does it well without help:

- **research**: Claude already checks live sources, dates them and prefers the installed version over newer docs.
- **verify-done**: Claude already refused unverified "done" claims in 9 of 9 runs.
- **context-audit**: Claude already finds oversized `@` imports and stale rules in a project.
- **catch-up**: asked "catch me up", Claude already leads with the decisions waiting on you.
- **recall**: Claude already finds earlier sessions in its local transcripts.
- **cold-read**: Claude already spots the gaps a reader without your context would hit.
- **grill-me as a wrapper**: any skill can be called by name, so the wrapper only duplicated the skill.

## How the skills are tested

Each skill has cases in [evals/](evals) for `claude plugin eval`:

- prompts that should trigger the skill, direct and reworded
- near misses that should not trigger it
- behavior cases scored with and without the plugin

The hooks have unit tests in [tests/](tests). The standard every skill follows, and the commands to run, are in [.claude/CLAUDE.md](.claude/CLAUDE.md).

## Credits

These skills adapt ideas from the people below. Text is rewritten, not copied, unless noted.

- [Matt Pocock's skills](https://github.com/mattpocock/skills) (MIT): the grill-me interview and the handoff document.
- [blader/humanizer](https://github.com/blader/humanizer) (MIT) and [pstack's unslop](https://github.com/cursor/plugins/tree/main/pstack) (MIT, Lauren Tan): the catalogue of AI-writing tells and the final re-scan for tells that survive.
- [obra/superpowers](https://github.com/obra/superpowers) (MIT, Jesse Vincent): baseline-first skill testing and descriptions that never summarize the workflow.
- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT): what a restartable session boundary must carry.
- [HumanLayer](https://github.com/humanlayer/humanlayer) (Apache-2.0, Dex Horthy): recording dead ends, and keeping context well below the window.
- [Chroma's "Context Rot" study](https://www.trychroma.com/research/context-rot) and the [Claude Code docs](https://code.claude.com/docs): evidence that quality drops with absolute length, and the advice to start fresh after two failed corrections.

## License

MIT. See [LICENSE](LICENSE).
