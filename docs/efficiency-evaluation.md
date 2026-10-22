# Evaluate complete-task efficiency without runtime tracking

Use this maintainer workflow when evaluating a change. It is not an activation step, per-turn checklist, background collector, or user requirement. The skills do not need telemetry to remain useful.

`scripts/evaluate_usage.py` reads supplied JSON from stdin or `--input` and emits a comparison. It makes no model calls, accesses no accounts or private logs, and writes no files. Use supported host exports when available. If a host exposes no complete-task usage, leave it unknown and compare observable behavior without claiming token savings.

## Comparison contract

Pair runs using the same `task_id`, with `variant` equal to `baseline` or `suite`. Both need matching, nonempty `conditions_id`, `model`, and `effort`. The conditions ID identifies a documented matching task/source setup; the script cannot verify that conditions were genuinely comparable. For repeated trials, use a distinct task ID per pair.

Each run can supply:

```json
{
  "task_id": "sample-pair-1",
  "variant": "suite",
  "conditions_id": "same-task-sources-and-environment",
  "model": "actual-host-model",
  "effort": "actual-host-setting",
  "quality": {
    "completed": true,
    "coverage_met": true,
    "constraints_preserved": true,
    "accepted": true
  },
  "usage": {
    "source": "Actual supported host export",
    "scope": "complete_task",
    "complete": true,
    "requests": [
      {"request_id": "actual-stable-request-id", "total_tokens": null}
    ]
  },
  "observations": {"tool_calls": null, "repeated_reads": null, "user_interventions": null, "elapsed_ms": null}
}
```

Wrap runs in `{"runs": [...]}`. The example is a schema illustration, not observed usage. Do not turn placeholders into claims. Missing quality verdicts are unknown; set `accepted` only using actual evaluation evidence, not because the assistant declared itself finished.

## Count the whole outcome

Include every model request attributable to the task: discovery, skill loading, handoff preparation, fresh-thread startup, retries, reconstruction, validation, and failed attempts. Preserve the same boundary in both runs. An export with missing branches or known gaps must have `complete: false`; a missing request total remains `null`, never zero. Zero requests cannot establish a measured comparison.

Use only the host's per-request `total_tokens` with stable IDs. Do not add input/output/cached-input/reasoning subtotals to totals again. The evaluator rejects unknown request fields and duplicate IDs across runs to reduce double counting. A host's cumulative thread counter, account quota, or dollar spend is not a per-request token total. If an export cannot be normalized accurately, do not calculate token deltas.

For each comparable complete pair, report suite minus baseline usage, with a negative value meaning lower observed usage. All pairs, including quality failures, remain in the report. An incomplete/unpaired/conditions-unknown run prevents an aggregate usage claim; the evaluator does not silently select only successful pairs. `observed_improvement` requires every pair to be measured, every quality check to pass, and a negative aggregate token delta. It is not a causal or statistical guarantee.

When token telemetry is unavailable, supplied observations can still reveal repeated reads, user interruptions, calls, or elapsed time. These remain separate measures; fewer calls do not automatically mean lower tokens or equal quality. Review missed exceptions, lost constraints, needless handoffs, and the suite's own overhead. Reject changes that reduce counts by narrowing the requested work or making users supervise routine management.

## Current mechanical improvements

The compact user-level rule and brief prompt reminders reduce always-loaded text. Source Selection's optional [bounded reader](../skills/ibbuilds-pm-source-selection/references/bounded-reading.md) returns only missing unchanged coverage; it is not a remote-cache interceptor. Context Management's [cost comparison](../skills/ibbuilds-pm-context-management/references/policy.md) can avoid expensive reconstruction. [Concise findings](../skills/ibbuilds-pm-context-management/references/checkpoints.md) preserve applicable results without creating a new tracking system.

Local tests verify these mechanics using synthetic data and temporary files. Live implicit activation, judgment quality, and net usage effects require separate evidence. Keep the normal experience quiet: evaluations run only when requested or as development verification, not after every user turn.

## Skill behavior before usage claims

[Representative prompts](../tests/skill-prompts.json) cover implicit discovery, phase transitions, pending answers, individual installs, full reads, truncation, negative controls, and skills together. They are maintainer fixtures, not shipped runtime instructions. Keep expected outcomes out of the model's input when evaluating.

Evaluate each case first with only its listed skill metadata and packaged resources, without the suite's global reminder or a companion. Repeat with ordinary installed discovery and, when relevant, the optional reminder. This separates a weak skill from a helpful installer pointer. Test full descriptions and a shortened prefix; record omissions as discovery failures rather than changing host budgets. Use actual supported traces/artifacts, not the model's promise to follow the skill.

For a phase case, inspect ordering: the location question must precede substantial domain reads or changes, and no implementation/dispatch may occur while the answer is pending. For source cases, inspect sufficient coverage, missed exceptions, unnecessary reads, and truncation recovery. For continuity, check that the creation prompt carries immediate context and a usable predecessor reference; retrieval should resolve missing details without reloading everything. For archival, check cleanup eligibility, original-state receipts, restoration after failed reads, and isolation from active work. Negative controls must stay quiet. Check returned work quality before comparing usage. Keep helper/packaging tests, isolated model forward tests, and real desktop integration results separate.

For optional Codex CLI evaluations, `codex exec --json` supplies a structured run trace; the CLI does not expose desktop chat-creation behavior merely because the desktop does. Run only in disposable fixtures with existing permissions and settings. Do not add a background collector, hidden model call, or live-user-project mutation to the normal skill flow.

For request escalation, evaluate a sequence: prompt, actual stay answer, completed request, next request, firmer prompt, then critical pressure. The answer and clarification messages must reuse the current request identity. A critical transition must prepare continuation without asking again, while retaining safe-checkpoint/context gates. Explicit persistent opt-outs are separate controls. Repeated questions are an intentional human-requested behavior in long chats; they are not automatically evidence of an efficiency regression, but their usage still counts in complete-task comparisons.

Execution Efficiency adds [behavioral fixtures](../tests/execution-efficiency-cases.json) for risk-based verification, stale evidence, recovery, and quiet negative controls. Provide only context and prompt as model input; grade observable actions against `expected` and `must_not`. These fixtures are not executed by unit tests and do not establish savings. Include skipped necessary checks and unresolved user-visible failures as quality failures, even when test counts or usage fall.

[Output-reduction fixtures](../tests/source-output-cases.json) cover producer/filter status separation, pre-ingestion field selection, raw recovery, and explicit full reviews. Their JSON integrity is unit-tested; their expected model behavior is not.
