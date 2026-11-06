---
name: pm-essential-skills-context-management
description: "Use proactively during ongoing multi-step work and at each substantive turn to keep context fresh: warn and prepare a handoff from 40% current context, require it at the 60% ceiling; also use for long chats, lost decisions, context recovery and continuation with relevant images, videos or attachments."
---

# PM Essential Skills / Context Management

Keep the active context small and preserve the decisions needed to finish the work. Apply automatically during ongoing work; the user need not ask for a context check.

## Check early, using real evidence

Before substantive work each turn, after a large tool-output batch, and before a consequential next step, reuse the host's fresh **current-context tokens / effective context-window tokens** when exposed. Include instructions, tools and conversation, not only user messages. Remaining percent can be converted to used percent. Account allowance, lifetime totals, chat age and message count are not occupancy. Never invent a percentage or inspect private session storage to obtain one.

| Current evidence | Required behavior |
| --- | --- |
| Fresh occupancy below 40% | Continue related work; reuse decisions and evidence. |
| Fresh occupancy 40% to <60% | Warn and prepare a fresh-chat continuation. Current work may continue; do not treat this warning alone as a stop. |
| Fresh occupancy >=60% | Ceiling reached. Only stabilize an already-running unsafe operation, preserve state and complete the handoff. Never finish another feature here first. |
| No fresh telemetry | Label occupancy unknown. Use visible structural evidence or a conservative budget of 10 substantive user turns or 3 tool outputs >=8,000 characters in the current context segment to require a precautionary handoff. These are workflow limits, not equivalent percentages. |

Assess an already-long chat immediately from visible evidence; do not wait for ten more turns. Repeated lost constraints, repeated reconstruction or substantial superseded history also justify intervention without a meter. A small answer needs no helper, scan or state file.

## Keep the change pending until resolved

At 40%, state the observed value and prepare early: “Current context is 44%. I am preparing a fresh-chat continuation before the 60% ceiling.” At 60%, announce the required pause. With unknown occupancy, state the actual evidence.

From 40%, remind once per subsequent user turn and prepare the brief without forcing a location choice. At 60% or a supported critical heuristic, pause substantive work. Honor actual pending choices and explicit handoffs. Avoid stacked questions, repeated in-turn reminders, polling or duplicate destinations. Prior notices, request-scoped stays, cost or missing tools cannot suppress warnings or clear the hard gate. Explain blockers and the manual fallback.

A verified fresh destination or effective compaction retaining essential decisions resets pressure. Fresh occupancy below 60% clears the hard gate; 40% to <60% keeps warnings; below 40% clears them. Honor later explicit stay, disabled or suggest-only preferences. Unknown telemetry cannot prove a reset.

## Preserve a useful continuation

Use an existing brief or the [handoff template](assets/handoff-template.md): goal, constraints and accepted decisions, current files/revision and uncommitted changes, active error, exact verification commands/results and limits, pending operations/approvals, next action and relevant enabled skills. Reference durable artifacts instead of copying logs. Redact secrets. Reuse suitable storage; do not produce per-turn logs or backup copies.

Carry necessary images, videos and attachments with original provenance, task purpose and verified destination access. Recover source-chat originals through supported tools; summaries or path mentions do not prove delivery. The destination opens needed media before dependent work. Missing essential media keeps the transfer incomplete. Read [media recovery](references/context-recovery.md#images-videos-and-other-attachments) when attachments matter; omit irrelevant media and reuse originals.

For actual transfers read [runtime readiness](references/runtime.md), [context recovery](references/context-recovery.md) and the [Codex adapter](references/codex-desktop.md). Create only with explicit human authorization and supported tools; do not fork for a fresh context. Confirm destination readiness before ending source ownership; reconcile ambiguous creation before retrying. Unsupported transfer means a ready-to-copy brief and a paused source. [Archive rules](references/archive-lifecycle.md) apply only when separately authorized.

For measurement, helper fields and optional advisory mode read [policy](references/policy.md). [Request choices](references/existing-chats.md) govern optional below-trigger moves; [project setup](references/project-setup.md) is conditional. [Automatic activation](references/automatic-activation.md) explains host discovery and its limits. A skill defines required behavior; deterministic runtime enforcement requires host support and cannot be promised by Markdown alone.
