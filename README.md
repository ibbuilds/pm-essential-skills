# PM Essential Skills

General work skills for Claude Code. They help with any kind of work, not just software: stress-testing a plan, handing work to a fresh session, researching current facts, verifying before claiming something is done, breaking work down and writing new skills.

> **Rebuild in progress.** The previous eight-skill suite is preserved at the [`legacy-v0`](https://github.com/ibbuilds/pm-essential-skills/tree/legacy-v0) tag. A skill is added here only after an eval shows Claude does worse without it.

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
| `/retro` | You run it at the end of a session | Lessons routed to the right place | Planned |

## Development

See [.claude/CLAUDE.md](.claude/CLAUDE.md) for the skill standard and the checks to run.

## License

MIT. See [LICENSE](LICENSE).
