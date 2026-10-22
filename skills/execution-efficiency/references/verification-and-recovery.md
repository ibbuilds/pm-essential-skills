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
