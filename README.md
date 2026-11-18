# PM Essential Skills

Skills that make Claude Code better at the work around the work: thinking a plan through, keeping long sessions sharp, checking current facts, planning projects and learning from each session. Nothing here is about code, so it helps an engineer, a nurse, a researcher or a founder alike.

Every skill was kept only after an eval showed Claude does worse without it. Ideas that Claude already handles on its own were dropped. The previous suite is preserved at commit [`6fd518f`](https://github.com/ibbuilds/pm-essential-skills/tree/6fd518f).

## Install

In Claude Code:

```
/plugin marketplace add ibbuilds/pm-essential-skills
/plugin install pm-essential-skills@pm-essential-skills
```

Skills load on their own when your request matches them. You can also call any of them by name, for example `/pm-essential-skills:handoff`.

## Skills

| Skill | Say something like | What you get |
| --- | --- | --- |
| `grilling` | "Grill me on this plan", "poke holes in this", "play devil's advocate" | One question at a time, the riskiest first, each with a recommended answer. Ends with a log of every decision. |
| `/grill-me` | `/grill-me` followed by your plan | The same interview, started on purpose. |
| `handoff` | "Hand this off", "continue in a new chat", "save where we are" | A `HANDOFF.md` with the goal, decisions, real state, last check and next action, plus a prompt to paste into the fresh session. |
| `research` | "Look up…", "is it still true that…", "what's the latest…" | An answer from sources opened now, each with its date. When you ask for a write-up, a `research/<topic>.md` note. |
| `breakdown` | "Break this down", "plan this project", "where do I start?" | Milestones written as states you can check, each with its dependencies and a "done when". |
| `retro` | "Let's do a retro", "what should we do differently?" | Each friction point from the session paired with the exact fix: a CLAUDE.md line, a hook, a skill change or nothing. Applied only after you approve. |
| `write-skill` | "Create a skill that…", "make this stick" | The right tool for the job (hook, CLAUDE.md, output style or skill). For a skill: eval cases first, then a lean SKILL.md. |

## Keeping sessions sharp

Long conversations get worse as old detail piles up. This plugin includes a hook that watches how much of the context window the conversation uses. At 50%, and again every 10% after that, it asks Claude to finish the current step and offer `/handoff`, so a fresh session continues with only what matters.

- It needs [Node.js](https://nodejs.org) on your PATH.
- The hook can't read the window size directly. It assumes 1M tokens once a session has gone past 200k, and 200k otherwise.
- Change the behavior with these environment variables:
  - `PM_CONTEXT_WARN_PERCENT`: the first warning, default `50`.
  - `PM_CONTEXT_WARN_STEP`: how often to warn again, default `10`.
  - `PM_CONTEXT_WINDOW`: your real window size in tokens.

## Saving tokens

Claude Code caches the start of each conversation automatically. You can't switch caching on with a skill, but these habits keep the cache working and the context small:

- Keep `CLAUDE.md` short and stable. It sits at the front of every request, so every word is paid for on every turn, and changing it means the next session starts with a cold cache.
- Avoid switching models or adding and removing MCP servers in the middle of a session.
- Hand off early instead of letting one session grow without limit. The hook above does the reminding.
- Install only the skills you use. Each one adds its description to every request.

## Also included

- **Concise output style.** Answer first, in plain words. Turn it on with `/output-style`.
- **Work habits.** Optional lines for your own `CLAUDE.md` in [snippets/work-habits.md](snippets/work-habits.md): scripts for bulk work, temporary files cleaned up, git instead of backup copies.

## How the skills are tested

Each skill has cases in [evals/](evals) for `claude plugin eval`:

- **Prompts that should trigger the skill,** both direct and reworded.
- **Near misses that should not trigger it.**
- **Behavior cases scored with and without the plugin.**

The skill standard and the checks to run are in [.claude/CLAUDE.md](.claude/CLAUDE.md).

## License

MIT. See [LICENSE](LICENSE).
