# Early context intervention policy

Default: `enforcement: required`, `mode: notify-and-transfer`, `review_ratio: 0.40`, `rollover_ratio: 0.50`. The review ratio now starts the required fresh-chat gate; the rollover ratio is the ceiling, not the first warning. Required mode rejects ceilings above 0.50. These are conservative workflow choices requested by the user, not empirically established universal model failure points.

## Measurement

The preferred metric is fresh occupancy of the full active context divided by the host's effective window for the active model. Include carried instructions and tools. Use the smaller usable host limit when known, not an advertised marketing maximum. Exclude account quotas, cumulative session usage and output allowance. Do not assume the last request's input tokens equals occupancy unless the host defines that relationship. Never scan private databases or run a second app server to get a meter.

Compaction changes active context; lifetime token totals do not reset with it. A fresh low reading and retained essential decisions clear pressure, even in an old chat. Stale readings cannot assert either pressure or recovery. Current segment counters reset only after a confirmed handoff or effective compaction; do not import predecessor counts. No telemetry means unknown, not zero and not an invented estimate.

With unknown occupancy, 10 substantive user work turns or 3 observed tool outputs of at least 8,000 characters in the current segment trigger a precautionary handoff. Already-visible substantial superseded history, repeated lost constraints or repeated reconstruction also trigger it immediately. Counters are inexpensive preventive workflow budgets, not a proxy percentage or a quality benchmark. No history scan or helper call is required for every turn.

## Optional helper

`scripts/assess_context.py` takes JSON on stdin or `--input PATH`; it performs no host calls or writes. Example:

```json
{
  "safe_checkpoint": true,
  "project_mode": "project",
  "context": {
    "kind": "current_context",
    "used_tokens": 40000,
    "window_tokens": 100000,
    "source": "host current-context meter",
    "fresh": true
  }
}
```

At the required trigger, output has `domain_work_allowed: false`, `allowed_work: stabilize_checkpoint_and_handoff_only`, and `remind: each_user_turn_until_resolved`. `action` is `rollover` at a safe checkpoint, `defer` while stabilization is needed, or `blocked_transfer` if essential continuation context is unavailable. All require transfer readiness checks. `rollover` is a candidate, never permission or evidence of actual creation. Missing readiness means preserve state and resolve the blocker, not resume domain work.

`last_notice_level`, a pending location choice, `user_keep_thread`, standalone membership, estimated transfer cost and repeated-investigation cost cannot suppress required intervention. Repeat one concise reminder per subsequent user turn while pending. Do not repeatedly ask the same unanswered question. Completion without further requested work returns quietly; a completed outcome with a newly requested phase still needs assessment.

An unsafe operation gets only the minimum steps to reach safety; do not extend the task to find a convenient boundary. At >=50% restrict activity to stabilization and handoff. Reduce output size before known large reads; avoid loading full transcripts or all skill references into the next window.

## Preferences and compatibility

Explicit later human preferences remain authoritative: `management_disabled: true`, `settings.mode: stay`, or `settings.mode: suggest-only` opt out of forced intervention. Never infer one from an old task's location choice. Installation and helper output grant no authority to create, message, archive, move or delete chats. Automatic selection remains enabled even when transfer requires authorization.

For an explicitly requested advisory workflow, `settings.enforcement: advisory` retains optional economic/location choices. Ratios are still 0.40/0.50 unless explicitly set; older 0.75/0.85 values are supported only with advisory enforcement. Historical test cases exercise that opt-in compatibility separately from default required-policy tests.

The existing optional fields remain validated: completed/new_outcome/new_phase, safe_checkpoint, user_keep_thread, management_disabled, project_mode (project/standalone/unknown), project_setup_allowed/project_offer_dismissed, admission_check, last_notice_level (none/review/rollover), counters, substantial_history/critical_history, obsolete_context_evidence (distinct strings), transfer_context_ready, reconstruction_repeats_work, user_requested_new_thread, boundary_choice, request_id/choice_request_id/last_prompt_request_id, choice_pending, stay_count, and settings. Unknown booleans are omitted, not null. Unknown counters/context may be null. See script validation for exact types.

In advisory mode, `boundary_choice` is new-thread/current-thread and belongs to the matching logical request; related follow-ups reuse that ID. Pending questions return await_thread_choice. Prior notices deduplicate ordinary advisory notices. Optional `transfer_cost` describes the same remaining requested work: basis (estimated/measured), source, unit (tokens/milliseconds/tool_calls), scope (remaining_requested_work), fresh boolean, nonnegative continue/handoff/startup/reconstruction, and optional destination_work. Without destination_work, transfer is an overhead lower bound. Supplied cost can suppress optional moves; it never establishes measured savings or overrides the required gate. Missing essential context, readiness and authorization always block dispatch.

## Evidence and limits

Keep goal, decisions, active error, exact checks and next action. Do not replay entire logs or predecessor history. After transfer retain one owner; recovery uses bounded source references when necessary. Tests of declared observations prove policy decisions, not host telemetry access or universal model obedience. Current host capabilities and actual invocation must be checked separately.

Research and comparison are recorded in the repository's context-management research document; the runtime skill has no dependency on that document.
