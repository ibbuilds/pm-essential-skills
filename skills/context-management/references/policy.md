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

`new_phase` means a requested next stage, such as implementation after accepted planning. `substantial_history` describes already-visible substantial prior work that can be represented by a concise brief; do not infer measured pressure from it. In a verified project, substantial history or supported review-level pressure prompts on every new substantive request, including small follow-ups. Below critical pressure, `ask_thread_choice` waits before domain work; it never dispatches. Short chats without a qualifying signal remain quiet.

Optional `boundary_choice` is `new-thread` or `current-thread`, from an actual human answer for this request. Use stable `request_id` and `choice_request_id` strings; mismatched IDs expire the answer. With no IDs, a supplied choice refers only to the current assessment and must never be carried into a later request. `user_keep_thread` likewise means a one-request stay. A current stay continues without another prompt for that request; it does not suppress future requests or critical automatic continuation. `new-thread` returns a transfer candidate with the existing gates. Explicit `user_requested_new_thread` needs no location question. Persistent `settings.mode: stay`, `management_disabled: true`, and suggest-only remain explicit opt-outs rather than inferred consequences of one stay answer.

Supply `last_prompt_request_id` only for a question actually shown. The same pending request, or `choice_pending: true`, returns `await_thread_choice`; it does not ask twice or permit domain work. `stay_count` is a nonnegative count of actual earlier stay answers in this chat, incremented once per answer; `prompt_level` saturates at 3. When no reliable count is available, omit it and use neutral wording without inventing earlier declines. Choice replies, status checks, and mid-request clarifications retain the request ID. No extra database or per-tool writes are required. See [request prompts](existing-chats.md) for wording and tracking.

At fresh occupancy >= rollover ratio, transfer automatically at a safe checkpoint rather than ask again. Without fresh telemetry, a proxy threshold plus two independent obsolete-context observations is critical. Alternatively `critical_history: true` plus two such observations declares a severe structural assessment: repeated lost constraints, repeated reconstruction, or extensive superseded work materially obstructing continuation. A bare “long chat” assertion is insufficient. This fallback is heuristic, not a measured percentage; fresh low telemetry overrides pressure-only heuristics. All transfer/readiness/authorization gates and persistent opt-outs still apply. Unknown membership must be resolved before creation; standalone work retains its checkpoint fallback.

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

A fresh total transfer cost at least as large as continuing can prevent ordinary outcome-based transfers. It does not suppress per-request questions, override their answers, or veto a critical continuation. Repeated-investigation/context-loss guards still apply at critical pressure: preserve the needed findings before dispatch. Explicit new-chat choices bypass cost/repeated-work preferences, but not inaccessible essential context, safe checkpoints, authorization, or persistent stay constraints. Use the latest human preference when normalizing conflicting observations.

## Decision order

1. Completed outcome with no requested next outcome/phase or explicit new-chat request: `complete`. No successor.
2. Explicit disabled/persistent stay: `continue`. An explicit new-chat request needs no question and uses the existing transfer gates.
3. Standalone pressure: preserve the existing concise-checkpoint fallback. Offer setup only when `project_setup_allowed: true` reflects useful permitted scope; a dismissed offer is not repeated. This grants no creation/move permission.
4. Critical measured or concretely supported heuristic pressure: `rollover`/`defer` candidate, subject to context/readiness gates and suggest-only overrides. This takes precedence over a one-request stay or pending below-critical prompt; announce rather than ask. Missing essential context blocks dispatch.
5. Below critical pressure, reuse an answer only if it belongs to the current request. A current stay continues this request; a new-chat choice prepares its handoff. Old request IDs expire their answers.
6. A qualifying long project chat: `ask_thread_choice` or `await_thread_choice` before domain work; defer to a safe checkpoint if needed. Known prior stay choices raise `prompt_level`, capped at 3. Resolve unknown project membership before offering a same-project destination. Unknown occupancy alone never establishes that a chat qualifies.
7. Otherwise a distinct requested outcome can prepare a transfer. Fresh occupancy below review overrides pressure-only historical counters; it does not erase an independently justified structural/task boundary. Unresolved review-level pressure with unverified membership returns `review`, not permission to dispatch.
8. Otherwise continue quietly. Complete outcomes do not produce idle prompts or invented successors.

`project_mode` is `project`, `standalone`, or `unknown` (default). It describes verified membership, not a folder guess. `project_setup_allowed` defaults to false: standalone work needs no organization interview. When a project offer is useful and permitted, explicitly set it true; this permits an offer, not creation. `project_offer_dismissed` records the scoped decision and never implies prior consent. A completed task with no next work never generates an offer.

For `review`, resolve the specific uncertain evidence or membership using available context and supported tools; then apply the per-request/critical policy. It is not authority to create a thread. Reuse facts instead of running the helper per tool call. Unchanged same-request assessments must not duplicate questions; a new qualifying request must not inherit a stale answer.

At a safe checkpoint, `notice` requests an informational pressure explanation only when its level exceeds `last_notice_level`. Record it after displaying. This deduplication does not suppress the next request's location prompt; `last_prompt_request_id` handles that separate boundary. Task completion, persistent opt-outs, low pressure, unsafe deferrals, and standalone project offers produce no extra pressure notice. Communication fields do not grant authorization.

Before rollover, verify management, capabilities, trusted scope, project association, accessible references, source recovery, and sufficient context. Critical pressure cannot excuse losing essential state or interrupting unsafe work; resolve that gap before dispatch. Estimated cost alone does not veto critical continuation. Preserve the source and supported fallback when gates fail. Thresholds never override explicit persistent opt-outs or host permissions.

## Honest reporting

Record why a transfer happened and whether the signal was measured or heuristic. The helper's ratio is current context occupancy, not percent of plan allowance and not percent of wasted tokens. Rollover can reduce carried context but can also increase total usage. Assess the total completed task, including handoff and startup work, before claiming a benefit.
