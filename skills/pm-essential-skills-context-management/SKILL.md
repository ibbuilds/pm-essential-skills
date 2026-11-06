---
name: pm-essential-skills-context-management
description: "Use proactively during ongoing multi-step work and at each substantive turn to keep context fresh: require a fresh-chat handoff at 40% current context, never wait beyond 50%; also use for visibly long chats, lost decisions, context recovery or continuation."
---

# PM Essential Skills / Context Management

Keep the active context small and preserve the decisions needed to finish the work. Apply automatically during ongoing work; the user need not ask for a context check.

## Check early, using real evidence

Before substantive work each turn, after a large tool-output batch, and before a consequential next step, reuse the host's fresh **current-context tokens / effective context-window tokens** when exposed. Include instructions, tools and conversation, not only user messages. Remaining percent can be converted to used percent. Account allowance, lifetime totals, chat age and message count are not occupancy. Never invent a percentage or inspect private session storage to obtain one.

| Current evidence | Required behavior |
| --- | --- |
| Fresh occupancy below 40% | Continue related work; reuse decisions and evidence. |
| Fresh occupancy 40% to <50% | Require a fresh chat now. Pause substantive work at the next safe checkpoint; prepare the handoff. |
| Fresh occupancy >=50% | Ceiling reached. Only stabilize an already-running unsafe operation, preserve state and complete the handoff. Never finish another feature here first. |
| No fresh telemetry | Label occupancy unknown. Use visible structural evidence or a conservative budget of 10 substantive user turns or 3 tool outputs >=8,000 characters in the current context segment to require a precautionary handoff. These are workflow limits, not equivalent percentages. |

Assess an already-long chat immediately from visible evidence; do not wait for ten more turns. Repeated lost constraints, repeated reconstruction or substantial superseded history also justify intervention without a meter. A small answer needs no helper, scan or state file.

## Keep the change pending until resolved

At the trigger, state the observed value and next action plainly: “Current context is 44%, above the 40% intervention limit. I am pausing implementation and preparing a fresh-chat continuation.” With unknown occupancy, say what was actually observed instead.

While unresolved, repeat one short reminder on each subsequent user turn and keep substantive work paused. Reuse the pending choice and brief; do not stack questions, reminders within a turn, background polls or duplicate destinations. A previous notice, one-request stay, transfer cost or missing creation tool does not clear the gate. Explain transfer blockers and offer the smallest manual step. Do not silently resume implementation here.

Clear the gate only after a verified fresh destination, fresh post-compaction occupancy below 40% with essential decisions retained, or a later explicit human override (including persistent stay, disabled or suggest-only). Age of chat alone cannot veto successful compaction. Unknown telemetry cannot prove a reset.

## Preserve a useful continuation

Use an existing brief or the [handoff template](assets/handoff-template.md): goal, constraints and accepted decisions, current files/revision and uncommitted changes, active error, exact verification commands/results and limits, pending operations/approvals, next action and relevant enabled skills. Reference durable artifacts instead of copying logs. Redact secrets. Reuse suitable storage; do not produce per-turn logs or backup copies.

For actual transfers read [runtime readiness](references/runtime.md), [context recovery](references/context-recovery.md) and the [Codex adapter](references/codex-desktop.md). Create only with explicit human authorization and supported tools; do not fork for a fresh context. Confirm destination readiness before ending source ownership; reconcile ambiguous creation before retrying. Unsupported transfer means a ready-to-copy brief and a paused source. [Archive rules](references/archive-lifecycle.md) apply only when separately authorized.

For measurement, helper fields and optional advisory mode read [policy](references/policy.md). [Request choices](references/existing-chats.md) govern optional below-trigger moves; [project setup](references/project-setup.md) is conditional. [Automatic activation](references/automatic-activation.md) explains host discovery and its limits. A skill defines required behavior; deterministic runtime enforcement requires host support and cannot be promised by Markdown alone.
