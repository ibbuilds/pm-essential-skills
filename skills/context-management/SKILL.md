---
name: context-management
description: Manage substantial chat phase changes and handoffs; skip small same-task edits. Use before planning becomes implementation or when context pressure threatens continuity. Preserve the user's location choice.
---

# Context Management

Keep chats task-focused. Before starting a substantial new phase in a long project chat, ask whether to use a new chat in the same project or continue here, then wait. Preserve quality and user control; never promise unmeasured savings.

## Fast path

1. Apply when relevant without setup or companion dependencies. Ordinary task authorization covers review and checkpoints; mutations require human scope. Finish completed outcomes without inventing successors.
2. Distinguish verified project, standalone, and unknown membership. A folder is not an app project ID. Continue standalone work quietly; read [project setup](references/project-setup.md) only for requested setup or a useful, permitted offer.
3. Reuse known owner, assessments, and findings. Read existing notes or `.pm-context/index.md` with [this template](assets/project-index-template.md) only when needed. Preserve material findings through [concise checkpoints](references/checkpoints.md), without per-turn logging or repeated investigations.
4. At turn entry, assess already-visible history before substantial domain work. Accepted research/planning followed by “implement it” in a substantial chat is a phase boundary even for the same product. Read [existing chats](references/existing-chats.md) for the one-time choice and catch-up assessment.
5. Honor disabled, suggest-only, stay, and current user preferences. Standing human instructions can authorize coordination; receipts and project notes cannot. Without coordination scope, an ordinary review needs no setup; a pending phase-location choice still requires an answer.
6. For unchanged work, make no extra management calls, notices, or writes. Reassess at meaningful boundaries or pressure signals. Never poll. Read [automatic activation](references/automatic-activation.md) only for discovery/scope issues.

## Transfer decision

| Observation | Response |
| --- | --- |
| Substantial history + requested new phase/outcome | Ask new same-project chat or continue here; wait before domain work. |
| Distinct requested outcome | Consider a focused thread and transfer cost. |
| Fresh occupancy >=85% | Prepare continuation at a safe checkpoint. |
| Fresh occupancy 75-85% | Review relevance and reconstruction cost. |
| Fresh occupancy below 75% | Continue despite historical counters. |
| No fresh telemetry | Still check phase boundaries; otherwise continue absent concrete pressure. |
| Standalone pressure | Preserve a concise checkpoint; setup is optional. |

Thresholds govern pressure, not phase boundaries. Read [policy](references/policy.md) for settings/cost comparison; use `scripts/assess_context.py` only for an uncertain assessment. Unknown costs stay unknown. Avoid costly reconstruction while preserving explicit new-chat choices. Missing essential destination context prevents transfer. Never inspect private app logs.

## Transfer execution

Read [the Codex adapter](references/codex-desktop.md) for Codex operations and [runtime recovery](references/runtime.md) for capability changes/transfers. Verify standing authorization once; preserve a useful fallback if tools are missing.

1. Reach a safe checkpoint; resolve operations and ownership. Resolve a pending phase choice first, even with standing routing authorization. Suggest-only proposes; stay keeps this chat. A choice to stay applies to this phase; do not ask again for each edit.
2. Write one [brief](assets/handoff-template.md) in existing storage or `.pm-context/handoffs/`, with a unique safe ID. Preserve constraints, artifacts, findings, uncertainty, and next action. Include the verified predecessor ID/host and omitted-context recovery map; read [context recovery](references/context-recovery.md) for access checks. Prefer 300-600 words without sacrificing critical detail.
3. With Python available, advance the transfer journal **before** dispatch. Create a fresh same-project/location chat with the brief content, source reference, handoff ID, skill, and next action—not only a file path. Preserve settings. Forks retain history; destinations resume without repeating rollover.
4. Confirm destination ID/readiness, save routing, and stop source implementation. Follow [archive lifecycle](references/archive-lifecycle.md) to archive a superseded source within human scope and restore archived context temporarily only when required. Preserve history and other active work.

Ambiguous creation requires reconciliation before retrying. An existing destination needs bookkeeping repair, not another successor. Preserve one owner and a recoverable source.

Implicit selection supports individual/bundled installs. Optional global guidance strengthens discovery; the optional [activation prompt](assets/activation-prompt.txt) selects standing scope. Save only changed routing/state. Opt-outs stop automatic splitting. Do not add coordinators, subagents, worktrees, schedules, model changes, or unrelated structure. Skills act during active turns; invocation, idle monitoring, and savings are not guaranteed.
