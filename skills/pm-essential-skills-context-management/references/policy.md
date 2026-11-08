# Early context intervention policy

Default: `enforcement: required`, `mode: notify-and-transfer`, `review_ratio: 0.40`, `rollover_ratio: 0.60`. The review ratio starts warnings and handoff preparation; current work may continue below the ceiling. The rollover ratio starts the required pause. Required mode rejects ceilings above 0.60. These are conservative workflow choices requested by the user, not empirically established universal model failure points.

## Measurement

The preferred metric is fresh occupancy of the full active context divided by the host's effective window for the active model. Include carried instructions and tools. Use the smaller usable host limit when known, not an advertised marketing maximum. Exclude account quotas, cumulative session usage and output allowance. Do not assume the last request's input tokens equals occupancy unless the host defines that relationship. Never scan private databases or run a second app server to get a meter.

Compaction changes active context; lifetime token totals do not reset with it. After effective compaction with essential decisions retained, a fresh reading below 0.60 clears the hard gate, 0.40 to <0.60 retains warnings, and below 0.40 clears them, even in an old chat. Stale readings cannot assert either pressure or recovery. Current segment counters reset only after a confirmed handoff or effective compaction; do not import predecessor counts. No telemetry means unknown, not zero and not an invented estimate.

With unknown occupancy, message/output counts can invite a cheap reassessment;
they do not establish saturation, require a warning or stop domain work by
themselves. The helper retains 10-turn/3-large-output review triggers for callers
already supplying counters, but returns nonblocking reassessment. Do not maintain
a counter file or scan history just to manufacture an intervention.

Substantial superseded history supports warning/preparation when grounded in
visible facts. Repeated lost constraints or repeated reconstruction that drops
active obligations can support a precautionary pause: declare critical history
and at least two distinct concrete continuity problems. A bare “long chat” flag,
an old percentage or output volume alone is insufficient. Explain the actual
evidence, preserve state and verify a usable destination before declaring transfer
complete. A note alone is not a working continuation.

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

At fresh occupancy from 0.40 to <0.60, output is `review` with `domain_work_allowed: true`, `allowed_work: continue_and_prepare_handoff`, and a repeated review notice at safe checkpoints. No mandatory location question is manufactured. Existing actual pending choices or explicit new-chat instructions retain their own routing and can still pause dependent work. Other task/media/authorization requirements remain binding.

At the 0.60 ceiling, or supported critical history with two concrete continuity
problems, output has `domain_work_allowed: false` and requires safe continuation
checks. `rollover` is a candidate at a safe checkpoint, `defer` permits only
stabilization, and `blocked_transfer` retains missing essentials. A candidate is
never permission or proof of creation; resolve readiness before dispatch.

Counter-only or unsupported history input returns `review`, unknown occupancy,
no forced handoff and no pressure warning. Supported noncritical history can
produce a repeated warning with work continuing. Explicit owner choices and
genuinely pending location questions retain their own authority/readiness rules.

`last_notice_level`, `user_keep_thread`, standalone membership, estimated transfer cost and repeated-investigation cost cannot suppress the early warning or the ceiling intervention. Existing pending choices remain distinct from a nonblocking pressure warning. Repeat one concise reminder per subsequent user turn while pending. Do not repeatedly ask the same unanswered question. Completion without further requested work returns quietly; a completed outcome with a newly requested phase still needs assessment.

An unsafe operation gets only the minimum steps to reach safety; do not extend the task to find a convenient boundary. At >=60% restrict activity to stabilization and handoff. Reduce output size before known large reads; avoid loading full transcripts or all skill references into the next window.

## Preferences and compatibility

Explicit later human preferences remain authoritative: `management_disabled: true`, `settings.mode: stay`, or `settings.mode: suggest-only` opt out of forced intervention. Never infer one from an old task's location choice. Installation and helper output grant no authority to create, message, archive, move or delete chats. Automatic selection remains enabled even when transfer requires authorization.

For an explicitly requested advisory workflow, `settings.enforcement: advisory` retains optional economic/location choices. Ratios are still 0.40/0.60 unless explicitly set; older 0.75/0.85 values are supported only with advisory enforcement. Historical test cases exercise that opt-in compatibility separately from default required-policy tests.

The existing optional fields remain validated: completed/new_outcome/new_phase, safe_checkpoint, user_keep_thread, management_disabled, project_mode (project/standalone/unknown), project_setup_allowed/project_offer_dismissed, admission_check, last_notice_level (none/review/rollover), counters, substantial_history/critical_history, obsolete_context_evidence (distinct strings), transfer_context_ready, reconstruction_repeats_work, user_requested_new_thread, boundary_choice, request_id/choice_request_id/last_prompt_request_id, choice_pending, stay_count, and settings. Unknown booleans are omitted, not null. Unknown counters/context may be null. See script validation for exact types.

In advisory mode, `boundary_choice` is new-thread/current-thread and belongs to the matching logical request; related follow-ups reuse that ID. Pending questions return await_thread_choice. Prior notices deduplicate ordinary advisory notices. Optional `transfer_cost` describes the same remaining requested work: basis (estimated/measured), source, unit (tokens/milliseconds/tool_calls), scope (remaining_requested_work), fresh boolean, nonnegative continue/handoff/startup/reconstruction, and optional destination_work. Without destination_work, transfer is an overhead lower bound. Supplied cost can suppress optional moves; it never establishes measured savings or overrides the required gate. Missing essential context, readiness and authorization always block dispatch.

## Evidence and limits

Keep goal, decisions, active error, exact checks and next action. Do not replay entire logs or predecessor history. After transfer retain one owner; recovery uses bounded source references when necessary. Tests of declared observations prove policy decisions, not host telemetry access or universal model obedience. Current host capabilities and actual invocation must be checked separately.

Research and comparison are recorded in the repository's context-management research document; the runtime skill has no dependency on that document.
