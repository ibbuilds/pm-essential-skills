# Verification and recovery examples

Use these as risk judgments, not a fixed checklist or test quota. Required project and user checks still apply.

| Situation | Useful evidence and next action | Avoid |
| --- | --- | --- |
| Static copy correction, no logic changes | Inspect the final text and affected rendered layout when wrapping matters; run any required checks. | Inventing a new test framework or broad redesign for one label. |
| Boundary-condition bug in a calculation | Reproduce the failing boundary, fix its cause, check neighboring valid/invalid inputs with existing tests, add missing regression coverage. | Only adding a test while leaving the reported behavior broken. |
| Authentication, permissions, money, or destructive data flow | Exercise relevant negative paths, integration boundaries, and regression/security gates; inspect consequences beyond the happy path. | Treating a one-line diff as low risk or a mocked unit pass as end-to-end proof. |
| Previously passing checks, then a shared dependency or configuration change | Reassess affected coverage and rerun relevant checks plus required final-state gates. | Reusing old results because the edited application file is unchanged. |
| Test cannot start because a required service is unavailable | Identify the prerequisite from the failure, restore it if authorized, then rerun. Otherwise report the blocked check and continue independent work. | Repeated identical runs, weakening assertions, or labeling an unavailable check passed. |
| Request times out after a possible external write | Check the supported operation status or target state before retrying; use supported idempotency semantics where available. | Assuming timeout means no effect and issuing duplicate writes. |
| Repeated repair attempts fail for different reasons | Retain what each observation ruled out; continue with a new supported hypothesis and a targeted check. | Stopping at a fixed retry count despite a clear recoverable cause, or cycling through rejected fixes. |
| User asks to track CI until the specified result | Observe the actual run/commit until the requested stopping condition or a real blocker; choose waits appropriate to the process. | Calling a pending run complete, or launching duplicate runs merely to show activity. |

A sufficient completion report ties evidence to the requested behavior: “Fixed the empty-input crash; the regression and related parser tests pass. The service integration check could not run because the test service is unavailable.” Do not imply a full pass from partial evidence.

For non-code repairs, apply the same judgment to the artifact: a formula correction needs affected calculations checked; a document correction needs its final rendering inspected when layout matters. This skill does not replace the relevant artifact workflow.

## Distinguish the failure before repairing

A failed check can reflect application behavior, a missing dependency/service, a mismatched environment, authentication, or an access restriction. Use the command's actual status and relevant diagnostic to distinguish them. Missing credentials or a sandbox denial is not evidence that application code is wrong. Fix an environment prerequisite only within existing authority; otherwise report the blocked check and continue independent work. Do not weaken assertions, edit application behavior, change permissions, or rerun an identical denied command to make infrastructure failures disappear. A supported approval path is not permission to bypass a denial.

A normal tool return can still report an operation failure through documented status or flags such as MCP `isError`. Inspect status and diagnostics before consuming success fields; absent optional `structuredContent` alone is not failure. Distinguish a known pre-execution denial from an error after possible partial execution: reported failure does not prove that no side effect occurred. Preserve the actual denial or diagnostic, not an invented parsing failure.

Failure of a parallel mutation batch does not establish atomic rollback. If A succeeded, B errored, and C remains pending, do not replay A or assume C stopped. Before retrying, reconcile only already-dispatched operations with uncertain effects, using existing receipts, supported status, or target state. Complete per-item receipts or authoritative evidence of documented atomic rollback can settle outcomes without new queries. Read-only failures need coverage recovery, not write reconciliation. No particular concurrency primitive or new ledger is required.

For an unfamiliar tool or argument-validation error, inspect the available schema/help before another call rather than guessing fields. Reuse that schema while applicable and preserve returned IDs verbatim; reopen it only when new evidence warrants it. Schema validation errors are not evidence of application defects.

## Prevent a confirmed recurring mistake

After resolving a recurring costly failure, reuse its evidence before trying the rejected approach again under the same conditions. Keep any reusable lesson scoped to its trigger, verified correction, and invalidation condition in current context or an existing authorized record; do not create a file for every incident.

If the cause exposes an objective invariant and prevention is within the requested scope, prefer a missing regression assertion or validation in an existing check over another prose warning. Verify that it catches the known failure and accepts a relevant valid case. Judgment calls remain guidance; do not turn uncertain explanations or preferences into blocking rules. A note is not mechanical enforcement. A lesson alone does not authorize global hooks or permission changes. Any requested host-level enforcement must respect its supported events, approval requirements, and legitimate alternative workflows.

## Scoped review and delegation

When independent review is warranted, supply the actual diff/artifact, acceptance criteria, and relevant constraints. Ask for reproducible correctness or requirements defects, with evidence and impact; “no actionable findings” is a valid result. Validate proposed findings before changing code. Style preferences or speculative redesign are not defects unless the requested review makes them requirements. This does not suppress requested security, style, or exhaustive reviews.

Delegate a distinct outcome, not “review everything again.” State its owner, scope, inputs, expected evidence, and completion condition in the handoff. Keep existing owners responsible for their outcomes; coordinate genuinely independent subtasks rather than allowing children to recursively commission the same review. Nested delegation can be useful for separate work, but is not a default escalation path or proof of quality. Batch routine worker progress when useful, but surface blockers and material decisions promptly rather than forcing silence. No fixed depth cap, mandatory agent count, or host configuration change is introduced.

Distinguish implemented, integrated, and verified: a code edit is not proof that the actual user path works. Tie relevant evidence to the tested revision/environment and report which stage remains unverified. Call a failure pre-existing only with baseline evidence; do not require an unrelated full baseline suite before every change.
