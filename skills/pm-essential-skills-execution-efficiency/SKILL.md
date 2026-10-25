---
name: pm-essential-skills-execution-efficiency
description: For implementation or repair, not simple answers or retrieval-only work. Calibrate verification and retries, especially repeated failed attempts or checks that no longer add evidence.
---

# PM Essential Skills / Execution Efficiency

Complete the requested change with sufficient evidence. This standalone skill requires no setup, helper calls, or tracking files. Repairs include documents and spreadsheets. Domain workflows own implementation and required checks; this skill calibrates repetition, not priorities or chat routing.

For necessary decisions with concrete alternatives, use the host's permitted selectable-input tool when available, with concise options and a justified recommendation. Use free text for open-ended facts or when no suitable tool is available. Accept clear written answers; defaults and timeouts are not consent. Permission escalations use their dedicated mechanism.

## Choose the next action

- Reuse the request, accepted decisions, investigation, and applicable project instructions. Ask only for information materially affecting correctness, scope, or an irreversible choice; offer a specific choice and recommendation when useful. Do not invent answers or re-ask settled questions. Straightforward changes need no separate planning ceremony.
- Target actual acceptance conditions and unresolved risk with the smallest coherent change, not a green-check workaround or unrelated cleanup/redesign. Review concrete correctness or requirements defects; do not invent findings.
- Choose checks by changed behavior, dependencies, and failure consequences. Reuse suitable checks; add tests for meaningful gaps or regressions, not duplicate assertions. No mandatory TDD sequence or universal full suite is imposed; preserve user, repository, security, and release gates.
- Repeat optional checks only to resolve material uncertainty; required gates still apply. Retain results with tested inputs and coverage. Reuse only with adequate freshness and unchanged relevant code, dependencies, configuration, environment, and acceptance conditions. After edits, rerun affected checks and required aggregate gates against the final state. Unknown applicability is not a pass.

## When progress stalls

Retain failed approaches, relevant inputs, and ruling-out evidence in context; use existing notes only for a real continuation need, not a default failure ledger. Reference bulky logs by existing path/run ID and concise finding instead of repeatedly dumping them.

- **Deterministic failure, unchanged conditions:** inspect the cause, change the hypothesis, or fix the prerequisite rather than repeat.
- **Transient failure:** retry safely when its semantics warrant it.
- **Uncertain external outcome:** inspect before repeating a mutation.
- **Access/approval limits:** never bypass them through retries. If blocked, state the exact limit and smallest needed decision or access.

No arbitrary attempt cap: continue while an authorized next step can establish useful evidence or advance the requested outcome.

For ambiguous verification scope, failure classification, or delegated review, read [risk-based examples](references/verification-and-recovery.md); not for an obvious fix.

For pending work, use supported completion events or appropriately spaced waits, not busy polling. Delegate only independently scoped work worth coordinating, not by default or to duplicate investigations. Assign each outcome one owner and explicit scope; children should not recursively spawn duplicate reviewers.

## Finish on the outcome

Stop adding work when acceptance conditions and required gates are satisfied. Tests are evidence, not the requested result: neither declare completion from a narrow pass nor stop requested monitoring with its outcome pending. Report changes, actual checks, and material unverified behavior or blockers. Distinguish mechanical validation from demonstrated model behavior or measured usage savings.
