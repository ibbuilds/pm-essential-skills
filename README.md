# PM Essential Skills

General work skills for Claude Code. They help with any kind of work, not just software: stress-testing a plan, handing work to a fresh session, researching current facts, breaking work down, learning from a session and writing new skills.

Every skill here was added only after an eval showed Claude does worse without it. The previous eight-skill suite is preserved at the [`legacy-v0`](https://github.com/ibbuilds/pm-essential-skills/tree/legacy-v0) tag.

## Install

In Claude Code:

```
/plugin marketplace add ibbuilds/pm-essential-skills
/plugin install pm-essential-skills@pm-essential-skills
```

## Skills

| Skill | How it starts | What you get | Status |
| --- | --- | --- | --- |
| `grilling`, `/grill-me` | You say "grill me", or run `/grill-me` | One question at a time, each with a recommended answer, until every decision is settled | Ready |
| `handoff` | You run `/handoff`, or say the session should continue elsewhere | A `HANDOFF.md` and a prompt to paste into the next session | Ready |
| `research` | You ask for current facts, versions or prices | Sources with check dates, and a `research/` note when you ask for a write-up | Ready |
| `breakdown` | You ask to plan or break down a project | Ordered milestones, each with a "done when" and its dependencies | Ready |
| `write-skill` | You create or edit a skill or `CLAUDE.md` | A lean skill with eval cases written first | Ready |
| `/retro` | You say "retro" or run `/retro` | Each friction point routed to an exact fix, applied on approval | Ready |

## Also included

- **Context warning.** A hook that tells Claude to suggest `/handoff` once the conversation passes about 100k tokens of context, then again every 50k. It needs Node.js. Change the thresholds with the `PM_CONTEXT_WARN_TOKENS` and `PM_CONTEXT_WARN_STEP` environment variables.
- **Concise output style.** Answer first, in plain words. Turn it on with `/output-style`.
- **Work habits.** Optional lines for your own `CLAUDE.md` in [snippets/work-habits.md](snippets/work-habits.md).

## Development

See [.claude/CLAUDE.md](.claude/CLAUDE.md) for the skill standard and the checks to run.

## License

MIT. See [LICENSE](LICENSE).
