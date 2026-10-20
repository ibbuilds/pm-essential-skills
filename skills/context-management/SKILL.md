---
name: context-management
description: Manage conversation context with focused project threads and safe handoffs. Use for chat organization, long-chat continuation, standalone chats growing into ongoing work, or projects activated for context management. Keep related edits together; do not manage priorities or split every small task.
---

# Context Management

Keep one coherent outcome per working thread. Transfer only when a requested task boundary or context pressure justifies the cost. Preserve essential decisions; never promise unmeasured token savings.

## Fast path

1. On activation, distinguish verified project membership, standalone chat, and unknown membership. A folder name is not an app project ID. For standalone pressure, read [project setup](references/project-setup.md); offer once, respect declines, and require the user's name/consent before creating or moving anything. Never interpret unknown membership as standalone.
2. In a verified project, reuse existing notes or `.pm-context/index.md` with [this template](assets/project-index-template.md). Verify authorization scope.
   First use in an existing chat: assess already-visible history now; do not start counters at zero or wait for future growth. For pressure notices and catch-up assessment, read [existing chats](references/existing-chats.md).
3. At turn entry, reuse known status/outcome/owner and latest assessment; read only missing current state. If disabled, work normally. Installation or state files do not grant authority.
4. Continue unchanged related work without extra tools, warnings, or writes. Assess at task boundaries, actual pressure signals, or substantial-work checkpoints. Never poll. Load only the reached branch's references.

| Signal | Action |
| --- | --- |
| Outcome complete; no requested successor | Finish. No empty successor. |
| User wants this thread | Stay here. |
| Standalone + meaningful context pressure | Offer project setup once; never force it. |
| Distinct requested outcome | Prepare a fresh task thread. |
| Fresh current-context occupancy >=85% | Prepare continuation at a safe checkpoint. |
| Fresh occupancy 75-85% | Review relevance and transfer cost. |
| Fresh occupancy below 75% | Continue; historical counters do not override it. |
| No fresh telemetry | Continue unless observed pressure justifies review. |

Thresholds are heuristics. For fallback signals or numeric validation, read [policy](references/policy.md); optionally run `scripts/assess_context.py` once per material assessment. Do not manufacture counters, treat cumulative usage as occupancy, or inspect private app logs. Do not restart merely because a chat is old. If a handoff would duplicate useful context or force expensive reconstruction, continue instead.

## Transfer path

Read [the Codex adapter](references/codex-desktop.md) only for actual Codex thread operations. Verify standing user authorization once; reuse it within its scope. Without supported creation tools or resolved project identity, preserve the source and prepare the smallest usable fallback.

1. Reach a safe checkpoint. Resolve running operations and existing ownership; do not introduce concurrent writers.
2. Write one brief from [the handoff template](assets/handoff-template.md) under `.pm-context/handoffs/` or existing equivalent storage. Give it a unique filesystem-safe ID. Preserve constraints, accessible artifacts, evidence, uncertainty, and the exact next action. Prefer 300-600 words; retain critical detail over length targets.
3. Create a **fresh** thread in the same project/location with the brief text, handoff ID, skill invocation, and authorized next action. Preserve user settings. A history fork is not a context reset. Destination counters start fresh; it resumes work instead of repeating rollover.
4. Confirm the real destination ID and readiness, then update routing and finish the source turn. Do no further implementation in the source. Keep history available unless archival was authorized.

Failure: source remains recoverable. Ambiguous creation: reconcile by project and handoff ID before retrying. Destination already exists but bookkeeping failed: repair routing; do not create another successor. Preserve one active owner per outcome.

## Persistence and limits

For persistent activation, use [the activation rule](assets/activation-prompt.txt); preserve existing instructions. Update changed routing/state at checkpoints. Record observation source, notice level, and reason; read current state, not historical handoffs.

On user opt-out, mark disabled and stop splitting; retain notes. Do not add coordinator chats, subagents, worktrees, schedules, model changes, or unrelated structure. A skill acts during active turns; it cannot guarantee invocation or idle monitoring. Explain missing capabilities once and keep useful work moving.
