---
name: execution-efficiency
description: Calibrate verification and retries during implementation or repair tasks, especially repeated failed attempts or checks that no longer add evidence. Not for simple answers or retrieval-only work.
---

# Execution Efficiency

Complete the requested change with sufficient evidence, not a growing ritual of plans, tests, and retries. Use independently of other skills, without setup, helper calls, or tracking files. Repairs include non-code artifacts such as documents and spreadsheets. Domain workflows still own implementation and required checks; this skill calibrates avoidable repetition, not project priorities or chat routing.

## Choose the useful next action

- Reuse the request, accepted decisions, existing investigation, and applicable project instructions before asking questions. Ask only when missing information materially changes correctness, scope, or an irreversible choice; offer an easy specific choice and recommendation where useful, without inventing an answer or re-asking settled questions. A straightforward change needs no separate planning ceremony.
- Identify the actual acceptance conditions and unresolved risk. Prefer the smallest coherent change that satisfies them, not a workaround that merely makes a check green. Do not broaden into unrelated cleanup or redesign. Scope reviews to concrete correctness or requirements defects; do not invent findings to justify a review.
- Select checks by changed behavior, dependencies, and consequence of failure. Reuse suitable existing checks before creating new ones. A new test should cover a meaningful gap or regression, not duplicate assertions or justify activity. There is no mandatory TDD sequence or universal full-suite requirement here; preserve user, repository, security, and release gates.
- Before repeating an optional check, identify the material uncertainty it can resolve. Required gates remain required. Keep available verification results with their tested inputs and coverage. Reuse them only while relevant code, dependencies, configuration, environment, and acceptance conditions remain unchanged and freshness is adequate. After edits, rerun affected checks and any required aggregate gates against the final state. Unknown applicability is not a pass.

## When progress stalls

Use observed failure evidence to choose the next action. Remember the failed approach, relevant inputs, and what ruled it out in current working context; use an existing note only when a real continuation need justifies it. Keep bulky logs at their existing path/run ID with a concise relevant finding rather than repeatedly dumping them. Do not create a failure ledger by default.

Avoid repeating a deterministic failure with unchanged conditions. Change the hypothesis, inspect the relevant cause, or fix the prerequisite. A transient failure may warrant a safe retry based on its semantics; inspect uncertain external outcomes before repeating a mutation. Never use retries to bypass access or approval limits. There is no arbitrary attempt cap: continue while an authorized next step can establish useful evidence or advance the requested outcome. If blocked, state the exact limit and smallest needed decision or access.

For ambiguous verification scope, failure classification, or delegated review, read [risk-based examples](references/verification-and-recovery.md). Do not load examples for an obvious fix.

Use supported completion events or appropriately spaced waits for pending work rather than busy polling. Delegate only independently scoped work whose benefit warrants coordination; do not create agents by default or duplicate an investigation. Give each delegated outcome one owner and an explicit scope; children should not recursively spawn duplicate reviewers.

## Finish on the outcome

Stop adding work once acceptance conditions and required gates are satisfied. Tests are evidence, not a substitute for the requested result. Do not declare completion just because a narrow check passes, or stop requested monitoring while its outcome is pending. Report what changed, what was actually checked, and any material unverified behavior or blocker. Distinguish mechanical validation from demonstrated model behavior or measured usage savings.
