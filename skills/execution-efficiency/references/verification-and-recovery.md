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

## Scoped review and delegation

When independent review is warranted, supply the actual diff/artifact, acceptance criteria, and relevant constraints. Ask for reproducible correctness or requirements defects, with evidence and impact; “no actionable findings” is a valid result. Validate proposed findings before changing code. Style preferences or speculative redesign are not defects unless the requested review makes them requirements. This does not suppress requested security, style, or exhaustive reviews.

Delegate a distinct outcome, not “review everything again.” State its owner, scope, inputs, expected evidence, and completion condition in the handoff. Keep existing owners responsible for their outcomes; coordinate genuinely independent subtasks rather than allowing children to recursively commission the same review. Nested delegation can be useful for separate work, but is not a default escalation path or proof of quality. Batch routine worker progress when useful, but surface blockers and material decisions promptly rather than forcing silence. No fixed depth cap, mandatory agent count, or host configuration change is introduced.

Distinguish implemented, integrated, and verified: a code edit is not proof that the actual user path works. Tie relevant evidence to the tested revision/environment and report which stage remains unverified. Call a failure pre-existing only with baseline evidence; do not require an unrelated full baseline suite before every change.

For an unfamiliar tool or argument-validation error, inspect the available schema/help before another call rather than guessing fields. Reuse that schema while applicable and preserve returned IDs verbatim; reopen it only when new evidence warrants it. Schema validation errors are not evidence of application defects.
