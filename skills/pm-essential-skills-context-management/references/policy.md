# Routing and measurement policy

Read when deciding whether to keep or transfer work. The existing 75%/85% ratios and 20-turn/6-output/2-compaction proxies are compatibility backstops, not proven cost-optimal limits. Review substantial replaceable history and requested phase boundaries immediately; do not wait for a numeric threshold.

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

`new_phase` means a genuinely requested next stage, such as implementation after accepted planning. `substantial_history` describes already-visible prior work that a brief can replace; it is not measured pressure. A qualifying distinct logical request can receive a location choice, subject to all below-critical cost/reconstruction guards. Related corrections, verification and status questions retain the current request identity and location answer, even after a delivery message. Below critical pressure, `ask_thread_choice` waits before domain work; it never dispatches.

Optional `boundary_choice` is `new-thread` or `current-thread`, from an actual human answer for this logical request. Use stable `request_id` and `choice_request_id` strings; mismatched IDs expire the answer. Related follow-ups reuse the logical request ID; a genuinely distinct outcome gets a new one. With no IDs, a supplied choice refers only to the current assessment. `user_keep_thread` likewise means a stay for this logical request. It does not suppress distinct future work or critical continuation. `new-thread` returns a transfer candidate with existing gates. Explicit `user_requested_new_thread` needs no location question. Persistent `settings.mode: stay`, `management_disabled: true`, and suggest-only remain binding; direct human prompting preferences override defaults.

Supply `last_prompt_request_id` only for a location question actually shown. A matching pending request or `choice_pending: true` returns `await_thread_choice`, including after compaction; it does not ask twice or permit dependent domain work. Missing or mismatched IDs alone do not establish a pending question. `stay_count` remains accepted for compatibility but no longer strengthens recommendations; `prompt_level` is 1 when an optional question is recommended. Question strength must follow current evidence, not previous declines. Related corrections, location answers and clarifications retain the logical request ID. No new database or per-tool state writes are required. See [request choices](existing-chats.md).

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
  "reconstruction": 1500,
  "destination_work": 1000
}
```

All costs are nonnegative integers in one unit: `tokens`, `milliseconds`, or `tool_calls`. Compare the same remaining work: `continue` covers finishing it here; a complete transfer total includes disjoint handoff, startup, reconstruction, and `destination_work` (actual remaining execution there). Optional `destination_work` must be an explicitly supplied nonnegative integer, including valid zero—not an unknown filled with zero. The returned `complete` flag is true only when supplied. Legacy objects without it remain accepted: their `transfer` is an overhead lower bound, not a full total. A lower bound at least as large as continuing can rule out benefit, but a smaller lower bound cannot establish benefit. `basis` is `measured` or `estimated` with a nonempty observation source; the helper validates declarations, not economic truth. Tokens are usage units, not billing amounts. Estimates are not savings measurements. Do not make an extra model call, inspect private logs, or invent telemetry to fill this object.

A fresh total transfer cost at least as large as continuing suppresses optional below-critical location questions, including at requested phase or outcome boundaries. Known repeated-investigation reconstruction yields a concise checkpoint; unavailable essential context keeps work in place. Reuse supplied observations; do not estimate costs through extra calls, history scans or invented telemetry. These guards do not answer pending questions, override explicit location choices or veto critical continuation. Critical repeated-investigation/context-loss guards still apply: preserve needed findings before dispatch. Explicit new-chat choices bypass cost/repeated-work preferences, but not missing essential context, safe checkpoints, authorization or persistent stay constraints. Normalize conflicting preferences against the latest actual human instruction.

Fresh complete comparable supplied costs with total transfer cost strictly less than continuing can also justify an early location recommendation in a verified project at a safe checkpoint, below numeric backstops. This uses the same remaining requested work, including handoff/startup/reconstruction/destination execution, not a vague goal label. Report the supplied basis (`estimated` or `measured`); an estimate is not measured savings. Before declaring a favorable estimate, account for uncertainty and warning/coordination overhead within the existing disjoint cost categories. A tiny nominal difference within estimation uncertainty is not a supported advantage: do not manufacture precision or populate favorable numbers to trigger a prompt. The helper validates declared observations, not their economic truth; no extra model call is warranted to fill gaps. The result is `ask_thread_choice` with reason `supplied_transfer_cost_beneficial`, not automatic transfer or a pressure notice. Occupancy remains independently measured/unknown. Missing essential destination context or known repeated investigation prevents this new question. Explicit requested boundaries, current human choices and pending answers retain precedence. Unknown, incomplete, stale or nonbeneficial costs do not establish early benefit.

## Decision order

1. Completed outcome with no requested next outcome/phase or explicit new-chat request: `complete`. No successor.
2. Explicit disabled/persistent stay: `continue`. An explicit new-chat request needs no question and uses the existing transfer gates.
3. Standalone work first honors a location choice belonging to the current request. Otherwise, a live unanswered location question remains pending; without one, standalone pressure preserves the existing concise-checkpoint fallback. Offer setup only when `project_setup_allowed: true` reflects useful permitted scope; a dismissed offer is not repeated. This grants no creation/move permission.
4. Critical measured or concretely supported heuristic pressure: `rollover`/`defer` candidate, subject to context/readiness gates and suggest-only overrides. This takes precedence over a one-request stay or pending below-critical prompt; announce rather than ask. Missing essential context blocks dispatch.
5. Below critical pressure, reuse an answer only if it belongs to the current request. A current stay continues this request; a new-chat choice prepares its handoff. Old request IDs expire their answers. After current answers and critical overrides, a still-pending location question waits regardless of changed pressure; only a known matching historical prompt ID or an explicit live pending flag establishes this.
6. A qualifying long project chat with a new logical request: `ask_thread_choice` or `await_thread_choice` before dependent domain work; defer unsafe boundaries. Suppress any new optional below-critical question when essential destination context is unavailable (`continue`), supplied comparable fresh costs show no benefit (`continue`), or reconstruction repeats work (`checkpoint`), including new phases/outcomes. Earlier branches preserve pending choices, answers and critical policy. Recommendation strength does not escalate with stay count. Resolve unknown membership before offering a same-project destination.
7. Otherwise a distinct requested outcome can prepare a transfer only for non-standalone work. Standalone outcomes continue quietly unless the user explicitly requested or chose a new thread. Fresh occupancy below review overrides pressure-only historical counters; it does not erase an independently justified structural/task boundary. Unresolved review-level pressure with unverified membership returns `review`, not permission to dispatch.
8. Before otherwise continuing, a fresh complete supplied favorable comparison may recommend a location choice at a safe checkpoint for verified-project work without a new explicit phase/outcome; apply the context/reconstruction guards above. This is an economic recommendation, not a measured-pressure claim. Otherwise continue quietly. Complete outcomes do not produce idle prompts or invented successors.

`project_mode` is `project`, `standalone`, or `unknown` (default). It describes verified membership, not a folder guess. `project_setup_allowed` defaults to false: standalone work needs no organization interview. When a project offer is useful and permitted, explicitly set it true; this permits an offer, not creation. `project_offer_dismissed` records the scoped decision and never implies prior consent. A completed task with no next work never generates an offer.

For `review`, resolve the specific uncertain evidence or membership using available context and supported tools; then apply the per-request/critical policy. It is not authority to create a thread. Reuse facts instead of running the helper per tool call. Unchanged same-request assessments must not duplicate questions; a new qualifying request must not inherit a stale answer.

At a safe checkpoint, `notice` requests an informational pressure explanation only when its level exceeds `last_notice_level`. Record it after displaying. This deduplication does not suppress the next request's location prompt; `last_prompt_request_id` handles that separate boundary. Task completion, persistent opt-outs, low pressure, unsafe deferrals, and standalone project offers produce no extra pressure notice. Communication fields do not grant authorization.

Before rollover, verify management, capabilities, trusted scope, project association, accessible references, source recovery, and sufficient context. Critical pressure cannot excuse losing essential state or interrupting unsafe work; resolve that gap before dispatch. Estimated cost alone does not veto critical continuation. Preserve the source and supported fallback when gates fail. Thresholds never override explicit persistent opt-outs or host permissions.

## Honest reporting

Record why a transfer happened and whether the signal was measured or heuristic. The helper's ratio is current context occupancy, not percent of plan allowance and not percent of wasted tokens. Rollover can reduce carried context but can also increase total usage. Assess the total completed task, including handoff and startup work, before claiming a benefit.
