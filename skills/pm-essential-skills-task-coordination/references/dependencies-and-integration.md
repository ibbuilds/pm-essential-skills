# Ready work, shared state and usable handoffs

Read when ordering dependent work, preventing collisions or integrating outputs whose compatibility is uncertain. Use current context or the existing task system; no graph file, lock service or new coordinator is required.

## Make the dependency actionable

Identify what the next consumer actually needs: the producer's output, relevant scope/revision, format, units, definitions and acceptance evidence. A dependency is ready when the needed portion is usable, not merely when somebody says the whole predecessor is done. Known sufficient evidence needs no new status call.

| Situation | Coordinate this next |
| --- | --- |
| A chart needs monthly regional data; the producer promises annual totals | Reconcile the accepted output with its existing owner before chart production. Do not fabricate a breakdown or quietly reduce the requested chart. |
| The requested slice is delivered and checked; unrelated producer work continues | Start the authorized consumer when it can use that stable slice safely. Do not impose an unnecessary whole-task barrier. |
| Two tasks await each other's output | Identify the circular dependency. Settle the smallest required interface or authorized enabling step, then resume the dependent work. A provisional interface must be explicit; invented results do not resolve the cycle. |
| A missing input blocks delivery while cosmetic work is available | Prioritize resolving the delivery dependency within user priorities; do useful independent work while waiting, without mistaking activity for progress toward the blocked outcome. |

Keep decomposition proportional. Straightforward work needs no formal schedule. For substantial work, break it into usable outcomes rather than a long list of tool calls. Respect deadlines, capacity and user priorities; do not invent estimates, task-size limits or mandatory checkpoints.

## Check shared resources before parallel writes

Disjoint filenames do not guarantee independent effects. Tasks can share a database, a deployment slot, a live design canvas, an export destination or an account operation. Worktrees isolate source paths, not every runtime resource. Use established isolated targets or serialize the conflicting operation; do not change global services or introduce locking infrastructure merely to parallelize.

Keep one accountable owner for each output and shared mutation. Read-only review may overlap when safe and useful. Do not replace an active owner or duplicate an external action because progress appears slow. If ownership or termination is uncertain, reconcile the actual state before conflicting replacement; see [delegate reconciliation](delegated-work.md).

## Integrate against the consumer's contract

Before accepting a handoff, check its identity, current scope/revision and the semantics the consumer relies on. Reuse an existing agreed contract and applicable validation. Fix an unambiguous reversible mismatch within authority, or reconcile it with the owner; ask the user only when definitions, scope or consequences require their decision. Do not reopen a settled interface merely because another task starts.

Verify the assembled result using the domain's appropriate check. Two independently valid components can still fail together through mismatched units, interfaces or state. Recheck affected seams and required final gates, rather than rerunning every unrelated check. Keep remaining integration, publication and observation work explicit until the accepted outcome is complete.
