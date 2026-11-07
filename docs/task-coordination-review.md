# Task coordination through usable dependencies

Version 0.6.7. The previous skill preserved accepted scope, ownership, cancellation reconciliation and real completion, but left dependency readiness and shared-state coordination mostly implicit. The revision explains when a consumer may start, how to handle cycles or conflicting mutations, and why individually checked outputs still need compatible integration. Existing interview, approval, pending-operation and cancellation behavior is retained. No tracker, agent architecture, model default or new service is introduced.

## Primary-source comparison

Original procedures inspected on 2026-11-07. These inform the revision; they do not measure its effectiveness.

| Source | Applicable mechanism | Adaptation and limits |
| --- | --- | --- |
| Addy Osmani, [Planning and Task Breakdown](https://github.com/addyosmani/agent-skills/blob/main/skills/planning-and-task-breakdown/SKILL.md), blob `296249b64334bcfd1aeaefd27b9e3e5494e38ec0` | Order tasks by prerequisites, define acceptance and interfaces before parallel work, and deliver usable slices rather than disconnected layers. | Use sufficient inputs and an agreed consumer contract. Do not import mandatory task files, fixed file-count sizes, checkpoint cadence or a second tracker. |
| Superpowers, [Dispatching Parallel Agents](https://github.com/obra/superpowers/blob/main/skills/dispatching-parallel-agents/SKILL.md), blob `3fa091b348bbe0a18eaa0e17e9092c97f7005cbe` | Parallel work needs independent domains without shared state or sequential dependencies; assignments need bounded context and review before integration. | Check actual shared effects, preserve existing owners and integrate against acceptance. Do not impose one agent per failure, numeric dispatch thresholds or blanket new review machinery. |
| Superpowers, [Executing Plans](https://github.com/obra/superpowers/blob/main/skills/executing-plans/SKILL.md), relevant task-loop/completion sections, blob `ea23196d745043eefb0287387112825d2ca99f05` | Compare actual output with the task contract; a prior task's interface can contradict what a later task consumes. Completion needs evidence rather than a plausible diff. | Reconcile the affected seam and verify the assembled result. Do not import mandatory ledgers, TDD for every task, model changes, unconditional agent reviews or authority to decide user-owned tradeoffs. |

Matt Pocock's [implement](https://github.com/mattpocock/skills/blob/main/skills/engineering/implement/SKILL.md), blob `bd49e472984c7b99aac40286fdae749bb955a842`, was also inspected. Its testing/review/commit conventions add no separate dependency-coordination mechanism, so they were not imported.

## Resulting behavior

Ready work depends on usable inputs, authorization and safe shared resources, rather than a predecessor status alone. A stable validated slice can unblock its consumer before an unrelated producer assignment finishes. Conversely, different files or worktrees do not isolate shared database mutations. If nothing is ready, resolve the actual missing prerequisite, owner conflict or dependency cycle instead of adding workers.

The conditional reference explains readiness, shared state and integration. It preserves reversible decisions within authority, relevant existing checks and the existing owners for substantive mismatches. Material definition or scope choices still belong to the user. Existing cancellation and interview references are unchanged; no unrelated skills or global instructions change. Metadata and the generated selection pointer now expose dependency ordering, concurrency and integration, with implicit invocation preserved.

## Verification scope

Five new cases extend the existing 19 without changing their values: ready independent work, shared database conflicts across different files, a stable partial handoff, a dependency cycle with a settled interface, and incompatible component units despite separate passing checks.

An independent application pass received raw requests without expected answers and an isolated local integration task. It inspected the source and consumer contracts, converted 12,500 and 7,500 euro cents into 125 and 75 EUR, wrote only the permitted result file and checked the output. Its decisions preserved all 24 scenarios, including direct trivial work, approval reuse, existing owners, material tradeoffs, cancellation uncertainty and stopping at actual completion.

Local verification passed: 372 tests with 22 platform skips, 29 synthetic helper replays, skill-creator validation, repository metadata/reference checks and installer packaging. Packaged Task Coordination files were compared with the source before publication.

This is one application with a local artifact and simulated coordination decisions. It does not establish universal activation, live multi-agent collision prevention, runtime locking or measured resource savings. Structural checks, fixture validation and helper replays validate their own implemented contracts, not model adherence.
