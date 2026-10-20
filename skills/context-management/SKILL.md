---
name: context-management
description: Manage conversation continuity during ongoing work, existing long chats, task boundaries, or handoffs, without a setup prompt. Works independently or in a suite. Preserve focused outcomes and user preferences; do not manage priorities or split every small task.
---

# Context Management

Keep related work together. Transfer only when a requested boundary or context pressure justifies the complete cost. Preserve quality and user control; never promise unmeasured savings.

## Fast path

1. Apply when relevant without setup or companion dependencies. Ordinary task authorization covers review and checkpoints; mutations require human scope. Finish completed outcomes without inventing successors.
2. Distinguish verified project, standalone, and unknown membership. A folder is not an app project ID. Continue standalone work quietly; read [project setup](references/project-setup.md) only for requested setup or a useful, permitted offer.
3. Reuse known owner, assessments, and findings. Read existing notes or `.pm-context/index.md` with [this template](assets/project-index-template.md) only when needed. Preserve material findings through [concise checkpoints](references/checkpoints.md), without per-turn logging or repeated investigations.
4. On joining an existing chat, assess already-visible history now; do not reset counters or wait for growth. Read [existing chats](references/existing-chats.md) for catch-up assessment and deduplicated notices.
5. Honor disabled, suggest-only, stay, and current user preferences. Standing human instructions can authorize coordination; receipts and project notes cannot. Missing coordination scope does not block useful same-chat work.
6. For unchanged work, make no extra management calls, notices, or writes. Reassess at meaningful boundaries or pressure signals. Never poll. Read [automatic activation](references/automatic-activation.md) only for discovery/scope issues.

## Transfer decision

| Observation | Response |
| --- | --- |
| Distinct requested outcome | Consider a focused thread and transfer cost. |
| Fresh occupancy >=85% | Prepare continuation at a safe checkpoint. |
| Fresh occupancy 75-85% | Review relevance and reconstruction cost. |
| Fresh occupancy below 75% | Continue despite historical counters. |
| No fresh telemetry | Continue unless concrete pressure warrants review. |
| Standalone pressure | Preserve a concise checkpoint; setup is optional. |

Thresholds are configurable heuristics. Read [policy](references/policy.md) for settings/cost comparison; use `scripts/assess_context.py` only for a material uncertain assessment. Unknown costs stay unknown. Avoid transfers that repeat investigations or cost more than continuing, while preserving explicit new-chat requests. Missing essential destination context prevents transfer. Never inspect private app logs.

## Transfer execution

Read [the Codex adapter](references/codex-desktop.md) for Codex operations and [runtime recovery](references/runtime.md) for capability changes/transfers. Verify standing authorization once; preserve a useful fallback if tools are missing.

1. Reach a safe checkpoint; resolve operations and ownership. Suggest-only proposes; stay keeps this chat.
2. Write one [brief](assets/handoff-template.md) in existing storage or `.pm-context/handoffs/`, with a unique safe ID. Preserve constraints, accessible artifacts, evidence, uncertainty, and next action. Prefer 300-600 words without sacrificing critical detail.
3. With Python available, advance the transfer journal **before** dispatch. Create a fresh same-project/location chat with the brief, handoff ID, skill, and next action. Preserve settings. Forks retain history; destinations resume without repeating rollover.
4. Confirm destination ID/readiness, save routing, and stop source implementation. Retain history unless archival was authorized.

Ambiguous creation requires reconciliation before retrying. An existing destination needs bookkeeping repair, not another successor. Preserve one owner and a recoverable source.

Implicit selection supports individual/bundled installs. Optional global guidance strengthens discovery; the optional [activation prompt](assets/activation-prompt.txt) selects standing scope. Save only changed routing/state. Opt-outs stop automatic splitting. Do not add coordinators, subagents, worktrees, schedules, model changes, or unrelated structure. Skills act during active turns; invocation, idle monitoring, and savings are not guaranteed.
