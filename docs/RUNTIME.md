# What belongs in a runtime, not in this plugin

PM Essential Skills teaches Claude behaviors: plan first, keep one task per session, stop guessing, hand off, make corrections stick, write plainly. It keeps a hook only when that hook drives one of its own skills. Session-wide cost and context policy (when to compact, what a summary keeps, what a resume or model switch costs) belongs to whoever owns the user's global setup: Claude Code itself, the user's `~/.claude` configuration, or a separate optimization runtime.

## Moved out in this version

| Removed piece | What it did | Why it left | Where it belongs | Depends on |
| --- | --- | --- | --- | --- |
| PreCompact hook (`pre-compact.mjs`) | Told the compaction summary to keep the goal, decisions, dead ends, last check and next action | Claude Code's own compaction already writes a structured summary, so the gain was never measured. All PreCompact hooks run and their stdout becomes the summary instructions, so it stacked on top of any brief the user already had (this author's `~/.claude/hooks/compact-instructions.md` covers the same fields). | The runtime's compaction brief, with one owner | PreCompact stdout (`code.claude.com/docs/en/hooks#precompact-output`) |
| Cold-resume warning (SessionStart `resume`) | Warned before a resumed conversation re-sent a large expired cache | It is cost telemetry and drives no skill. Claude Code already compacts idle conversations before their cache expires (`idleCompaction`, on by default) and shows whether the cache is warm or cold in `/usage`. | The runtime, next to model-switch cost warnings | SessionStart `context_tokens`, `prompt_cache_likely_expired`, `estimated_cache_write_usd` (v2.1.251+) |
| Concise output style | Answer first, plain words | Claude Code has a built-in Concise style (v2.1.237+), and the plugin's copy had the same name | Built-in: `/output-style concise` | None |
| `snippets/work-habits.md` | Optional CLAUDE.md lines on scripts, subagents, temp files, git | Subagent routing and briefs are orchestration policy. The user's global rules and SWE Essential Skills cover them, and they were never evaluated here. | Global `CLAUDE.md` or rules | None |

## Kept, with a hand-off rule

**Context check (`context-watch.mjs`, UserPromptSubmit).** At 50% of a 200k-token budget, and every 25% after, it tells Claude to finish the current step and call `pause`. It stays because it is the automatic trigger for `pause`, and because a default Claude Code session on a 1M-window model would otherwise run to about 967k tokens before compacting.

It steps aside when the user already has a context policy: `CLAUDE_CODE_AUTO_COMPACT_WINDOW` is set, or `autoCompactWindow` appears in `~/.claude/settings.json` (or `$CLAUDE_CONFIG_DIR`), `.claude/settings.json` or `.claude/settings.local.json`, either at the top level or under `modelSettings`. Setting `PM_CONTEXT_BUDGET` turns it back on, and `PM_CONTEXT_WATCH=off` turns it off.

## What a runtime should own

1. **One threshold policy.** Pick the handoff and compaction points per model from measured sessions, not from a fixed number. Read the effective auto-compact window, offer a `pause` handoff a little before it, and let compaction be the fallback. Once that exists, users who run it already have `autoCompactWindow` set, so this plugin's check goes quiet without a change here.
2. **One compaction brief.** A single PreCompact hook. Verify on real compactions that the summary keeps the objective, decisions, dead ends, verification state and next step.
3. **Cost warnings at the moments the cache is lost:** cold resume (SessionStart `resume`/`fork`), model or effort switch (PreModelSwitch `prompt_cache_warm`, `estimated_cache_write_usd`), and skills or agents whose frontmatter forces a different model.
4. **Signals the plugin cannot see.** `UserPromptSubmit` also fires for `/loop` iterations, background subagent reports and cross-session messages, and the hook cannot tell those apart from a typed prompt. A runtime with session state can hold the pause nudge until a human turn.

## Boundary with SWE Essential Skills

| Situation | Owner | Why |
| --- | --- | --- |
| Open-ended goal of any kind (event, website, research, document) | `plan-first` | General planning with a "Go ahead?" gate |
| Software feature with open product decisions, or a spec or PRD | `swe-essential-skills:spec` | It reads the code and writes `SPEC.md`. `plan-first` hands over when `spec` is installed. |
| Splitting a spec into tickets | `swe-essential-skills:tickets` | `plan-first` hands over when it is installed |
| Same problem survives two fixes | `unstuck` | Lists what each fix ruled out, for any kind of work |
| A code bug that needs a reproduction | `swe-essential-skills:diagnose` | `unstuck` calls it for its check step when it is installed |
| Handoffs and writing that sounds human | `pause`, `humanize` | SWE removed its own copies |

Both packs run alone or together. Every hand-off to the other pack is conditional ("when the Skill tool lists ..."), and both packs load side by side with no skill-name or hook collision. SWE Essential Skills' `spec` now points plan stress-tests to `pm-essential-skills:plan-first`, and its SessionStart reminder no longer repeats on `resume`, where the transcript already holds it.

The requirements above are merged, with SWE Essential Skills' list and the author's global setup, into one Phase 3 runtime specification kept outside both plugins. This file stays the record of what this plugin needs from a runtime.
