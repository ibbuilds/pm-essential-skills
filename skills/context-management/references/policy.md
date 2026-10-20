# Routing and measurement policy

Read when deciding whether to keep or transfer work. These are tunable starting heuristics, not proven cost-optimal limits.

## Observation contract

The optional helper accepts a JSON object. Unavailable quantities are omitted or `null`.

```json
{
  "completed": false,
  "new_outcome": false,
  "safe_checkpoint": true,
  "user_keep_thread": false,
  "project_mode": "project",
  "project_offer_dismissed": false,
  "project_setup_allowed": false,
  "admission_check": false,
  "last_notice_level": "none",
  "context": {
    "kind": "current_context",
    "used_tokens": 85000,
    "window_tokens": 100000,
    "source": "host current-context meter",
    "fresh": true
  },
  "substantive_turns": null,
  "large_outputs": null,
  "compactions": null,
  "obsolete_context_evidence": []
}
```

Optional `settings` contains `mode` (`notify-and-transfer`, `suggest-only`, or `stay`) and `review_ratio`/`rollover_ratio`. Defaults are notify-and-transfer, 0.75, and 0.85. Ratios must satisfy `0 < review_ratio < rollover_ratio <= 1`. Preserve explicit user preferences in existing project notes; do not change global settings or tune thresholds silently from a single task.

`suggest-only` returns `suggest_rollover` instead of dispatching a rollover at a safe checkpoint. It never authorizes creation; respect prior notices and declined suggestions. `stay` continues this thread without pressure notices or project offers; completed work still returns `complete`. Notify-and-transfer still needs independently verified user authorization, capabilities, and safe transfer gates. It is not a grant of automatic authority.

`completed` describes the present outcome. `new_outcome` means the user has requested a distinct next outcome, not that the assistant has invented another task. `safe_checkpoint` is false while transfer would interrupt work that cannot safely pause. Omitted booleans default to false; supplied booleans must be true or false, not null. Missing safe-checkpoint evidence defaults to false in the helper.

`new_phase` means a requested next stage, such as implementation after accepted planning. `substantial_history` describes already-visible substantial prior work that can be represented by a concise brief; do not infer measured pressure from it. With either `new_phase` or `new_outcome`, substantial history, verified project membership, and a safe checkpoint, the default is `ask_thread_choice`. Ask new same-project chat or continue here, then wait before substantial domain work, regardless of occupancy, standing routing authorization, or estimated transfer costs. The result permits no dispatch. Small same-phase fixes do not qualify.

Optional `boundary_choice` is `new-thread` or `current-thread`, supplied only from an actual human choice applicable to this phase. Omit it while unanswered; an asynchronous pending question is not consent. `current-thread` continues without pressure notices. `new-thread` returns a transfer candidate, subject to essential-context and safe-transfer gates. Reuse the choice within that phase rather than asking on each edit. An explicit `user_requested_new_thread` already supplies the choice. Global stay/disabled preferences remain binding. If membership is unknown, `review` with `phase_project_unverified` means verify membership before asking; it is not permission to begin implementation. Verified standalone work retains its ordinary checkpoint policy.

Use `context` only for genuinely current window occupancy, with its source and freshness. Never place lifetime input/output totals, account percentages, a quota budget, or the last request's token count here unless the host explicitly defines it as current occupancy. Stale observations are ignored. The helper checks declared types, not the truth of their source.

Counters cover the current thread since its accepted handoff. Count substantive user work turns, observed tool outputs at least 8,000 characters, and actual observed compactions. Do not infer them from elapsed time or import predecessor counters. Unknown is not zero. `obsolete_context_evidence` contains distinct, concrete observations (not general statements that a chat is long).

At first use in an already-long chat, set `admission_check: true` and use already-visible pre-activation history when reliable. Missing historical counts remain unknown. Without fresh telemetry or a counter threshold, two concrete obsolete-context observations trigger `review`, not automatic rollover. See [existing chats](existing-chats.md) for immediate assessment and deduplicated user notices.

## Transfer cost and reconstruction

Optional `transfer_context_ready: false` prevents transfer when essential destination context is unavailable. If the user explicitly chose a new chat, return `blocked_transfer`: preserve the source and explain the blocker, without starting implementation here. Otherwise continue in place. Optional `reconstruction_repeats_work: true` returns a concise `checkpoint` at a safe boundary or `continue` otherwise. These avoid automatic reconstruction of completed investigations; no extra tools are needed when the facts are known. Checkpoint means retain only useful changed findings, not introduce a logging routine.

When comparable remaining-work costs are actually available, optional `transfer_cost` accepts:

```json
{
  "basis": "estimated",
  "source": "Labeled assessment of the same remaining requested work",
  "unit": "tokens",
  "scope": "remaining_requested_work",
  "fresh": true,
  "continue": 2000,
  "handoff": 500,
  "startup": 500,
  "reconstruction": 1500
}
```

All four costs are nonnegative integers in one unit: `tokens`, `milliseconds`, or `tool_calls`. Compare the same remaining work and include handoff, startup, and reconstruction. `basis` is `measured` or `estimated` with a nonempty observation source; the helper validates declarations, not economic truth. Tokens are usage units, not billing amounts. Estimates are not savings measurements. Do not make an extra model call, inspect private logs, or invent telemetry to fill this object.

A fresh total transfer cost at least as large as continuing returns `continue` for ordinary pressure transfers. It does not suppress a phase-location question or override its answer. Stale or absent comparisons leave ordinary routing intact. A favorable comparison still needs all transfer/authorization gates. Reassess only at a meaningful change, not by polling. Explicit `user_requested_new_thread: true` or a phase choice of `new-thread` bypasses cost/repeated-work preferences, but not inaccessible essential context, safe checkpoints, authorization, or explicit stay constraints. Use the latest human preference when normalizing conflicting observations.

## Decision order

1. Completed outcome with no requested next outcome/phase or explicit new-chat request: `complete`. No successor.
2. User asks to remain here: `continue`, even with pressure.
   An explicit new-chat request needs no question. Otherwise, a requested next phase/outcome with substantial history takes precedence over pressure: apply the phase choice above. A safe unanswered choice in a verified project returns `ask_thread_choice`; an unsafe boundary defers until a checkpoint. Never treat an unanswered choice as a transfer or start implementing while waiting.
3. Verified standalone chat with fresh occupancy at least 75%, or proxy/catch-up pressure when fresh telemetry is missing: by default, `checkpoint` at a safe checkpoint or `continue` while work cannot safely pause; neither needs project setup. Only when `project_setup_allowed: true` reflects a useful, permitted offer, return `offer_project` at a safe checkpoint or `defer`. A dismissed offer yields `review` without asking again. This result grants no creation/move permission.
4. Distinct requested outcome: `rollover` candidate at a safe checkpoint, otherwise `defer`.
5. Fresh measured occupancy at least 85%: `rollover` candidate, or `defer` if unsafe.
6. Fresh measured occupancy at least 75%: `review`.
7. Fresh measured occupancy below 75%: `continue`. Do not let historical counters override successful compaction.
8. No fresh measurement and at least 20 substantive turns, 6 large outputs, or 2 compactions: `review`. With at least two distinct obsolete-context observations, `rollover` candidate or `defer`.
9. First-use catch-up with at least two obsolete-context observations and no fresh telemetry/counter threshold: `review`.
10. Otherwise: `continue`. Unknown occupancy alone is not a reason to interrupt.

`project_mode` is `project`, `standalone`, or `unknown` (default). It describes verified membership, not a folder guess. `project_setup_allowed` defaults to false: standalone work needs no organization interview. When a project offer is useful and permitted, explicitly set it true; this permits an offer, not creation. `project_offer_dismissed` records the scoped decision and never implies prior consent. A completed task with no next work never generates an offer.

For `review`, evaluate whether a short handoff removes substantial obsolete material without causing expensive reconstruction. Continue if the history is still relevant. A review is not a user approval request, a warning to repeat every turn, or authority to create a thread. Save the last observation and decision; do not run the helper once per tool call.

At a safe checkpoint, `notice` requests one brief review/rollover explanation when the pressure level exceeds `last_notice_level`. Record the level after displaying it. User overrides, task completion, low pressure, unsafe deferrals, and standalone project offers produce no additional pressure notice. These fields track communication, not authorization.

Before any rollover, separately verify management is enabled, host capabilities, trusted authorization, project association, accessible references, and a sufficient handoff. Check that the transfer can leave substantial irrelevant context behind without losing essential state. If it would mostly duplicate useful context or force expensive reconstruction, continue and record that judgment. If other gates fail, preserve the current thread and provide the supported fallback. Numeric thresholds never override user preferences or safety at a checkpoint.

## Honest reporting

Record why a transfer happened and whether the signal was measured or heuristic. The helper's ratio is current context occupancy, not percent of plan allowance and not percent of wasted tokens. Rollover can reduce carried context but can also increase total usage. Assess the total completed task, including handoff and startup work, before claiming a benefit.
