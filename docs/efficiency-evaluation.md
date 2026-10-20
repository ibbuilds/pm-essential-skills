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

The compact user-level rule and brief prompt reminders reduce always-loaded text. Source Selection's optional [bounded reader](../skills/source-selection/references/bounded-reading.md) returns only missing unchanged coverage; it is not a remote-cache interceptor. Context Management's [cost comparison](../skills/context-management/references/policy.md) can avoid expensive reconstruction. [Concise findings](../skills/context-management/references/checkpoints.md) preserve applicable results without creating a new tracking system.

Local tests verify these mechanics using synthetic data and temporary files. Live implicit activation, judgment quality, and net usage effects require separate evidence. Keep the normal experience quiet: evaluations run only when requested or as development verification, not after every user turn.
