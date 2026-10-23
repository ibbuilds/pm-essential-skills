# PM first-version readiness

Reviewed 22 October 2026 against source revision
`cb441a74cb90d58650fc7991c37f6d6fa39d9b17`, before adding this document.
“First version” means a usable candidate for the user's own trial, not a
published release, a claim of flawless behavior, or a benchmark target. The
manifest remains the unreleased 0.4.0 candidate; this document does not change it.

## Conclusion

Subsequent reinforcement pass (22 October 2026): applicable skill requirements
now explicitly enter Task Coordination's completion and handoff state. The
installer's guidance and both supported hook reminders carry the same required
workflow contract; context briefs retain outstanding obligations and scoped
exceptions. Optional methods/no-op paths, explicit opt-outs and authorization
boundaries remain intact. These changes strengthen emitted instructions and
continuity; they are not a live-model compliance result. Earlier test counts
below identify the earlier candidate, not this later change's final gate.

For this reinforcement change, the local required suite passed **238 tests total,
including 3 skipped**, and repository validation passed all seven skills. The
new activation test exercises installation plus both hook-handler events; seven
additional behavioral scenarios remain specifications, not model trials. Review
confirmed that routing thresholds, hook opt-in, permissions and standalone skill
dependencies were not changed. The user's two live chats were not inspected.

The implemented foundation covers the accepted **domain-independent** PM scope.
It does not need an eighth skill, a mandatory orchestrator, or engineering-specific
methods to be a first version. Static inspection found concrete procedures for
each requirement below, not merely names in a capability table. No additional
implementation change is justified by this readiness pass. Final local repository and packaging gates are recorded below. Remote CI and the
exact merged source still require verification before handoff; they are not
reasons to keep expanding the product.

One material policy limitation remains explicit: Context Management can require
an unanswered location choice before urgent domain work. An urgent-work exception
is **pending the user's explicit choice**. Broad permission to finish the
repository does not authorize changing the request/location/critical-pressure
policy. The current policy must not be presented as already containing that
exception. Other skills can be tried independently; a full-suite trial must use
and assess the current disclosed behavior unless the user chooses otherwise.

## Requirements traced to executable procedures and guidance

The links identify maintained owners, not a chain that every request must load.
Behavioral cases are specifications unless actual execution evidence is stated.

| Accepted requirement | Implemented procedure and failure prevented | Work avoided, quality safeguard, and evidence boundary |
| --- | --- | --- |
| Complete accepted outcomes across domains | [Task Coordination](../skills/pm-essential-skills-task-coordination/SKILL.md) starts from all still-open accepted requirements, defines observable completion, retains scope changes, owns integration and active operations through the requested stopping condition, and compares delivery with every accepted requirement. | Prevents replacing a finished report with an outline or treating a completed subtask as the whole result. Trivial tasks bypass planning/tracking. [Cases](../tests/task-coordination-cases.json) include report/PDF completion and blocked delivery; these are not model-run results. |
| Material decisions, dependencies and changing commitments | The same owner reuses settled choices, asks only consequential missing decisions, continues independent work, checks promised prerequisite outputs against consumer needs, and reassesses feasibility when scope/time/budget/capacity/dependencies materially change. | Catches incompatible research definitions or asset formats before dependent production; compatible shared specifications reuse validation without a new matrix. Conflicting requirements remain user decisions, not silent scope cuts. Cases distinguish incompatible, compatible and unresolved-definition handoffs. |
| Context continuity and recoverable handoffs | [Context Management](../skills/pm-essential-skills-context-management/SKILL.md), [recovery](../skills/pm-essential-skills-context-management/references/context-recovery.md), and [runtime](../skills/pm-essential-skills-context-management/references/runtime.md) preserve immediate context, source identity, reasons, constraints, remaining work and an omitted-detail recovery map. Dispatch gates include destination availability/access, settings, safe checkpoint and actual human authority. The journal records requesting state before dispatch, pauses the source, reconciles ambiguous creation, and confirms one destination owner. | Avoids repeated investigation and duplicate writers without a per-turn memory database. Brief fingerprints, revision checks and locks enforce local lifecycle mechanics, not semantic completeness or host authorization. Missing destination access blocks transfer rather than discarding essential context. Archive cleanup preserves other active work and original visibility. |
| Appropriate resources, not nominally cheap calls | [Resource Selection](../skills/pm-essential-skills-resource-selection/SKILL.md) compares setup, duplicated context, coordination, retries and verification; uses existing deterministic tools for suitable mechanics; retains adequate reasoning; delegates only separable bounded outcomes with integration ownership. | Avoids manual regeneration and trivial fanout while preserving explicit model choices and quality. Unsupported switches remain recommendations, not claimed actions. No new paid service or permission change is implied. [Cases](../tests/resource-selection-cases.json) cover unavailable switches, high-risk work and independent reviews. |
| Sufficient, current evidence without redundant retrieval | [Source Selection](../skills/pm-essential-skills-source-selection/SKILL.md) starts with missing facts, exact required coverage and available evidence; uses known sources and bounded interpretive units; broadens for conflicts, pagination, exceptions and missing authority. [Reuse](../skills/pm-essential-skills-source-selection/references/source-reuse.md) requires matching identity, available content, sufficient coverage and applicable freshness. | Avoids repeated reads without sampling away an exhaustive request. `read_source.py` hashes the current regular UTF-8 file, returns missing bounded spans, rejects skipped unread prefixes and restarts on revision changes. Forced rereads track their own pass. Helper coverage cannot prove comprehension. |
| Efficient execution and recovery | [Execution Efficiency](../skills/pm-essential-skills-execution-efficiency/SKILL.md) selects checks by changed behavior, dependencies and consequence, reuses only applicable results, reruns affected/final required gates after edits, and changes hypothesis or prerequisite after deterministic failures. Uncertain external writes are reconciled before retry. | Prevents unchanged retry/check loops without arbitrary task-abandonment limits or waived gates. [Recovery reference](../skills/pm-essential-skills-execution-efficiency/references/verification-and-recovery.md) separates environmental/access failures from artifact defects and includes non-code rendering/calculation checks. The narrower transfer journal deliberately has its own documented two-attempt safety bound; it is not a general execution cap. |
| Learning from recurring failure | [Workflow Improvement](../skills/pm-essential-skills-workflow-improvement/SKILL.md) requires demonstrated recurring friction or an explicit improvement request; reuses the canonical owner, preserves user edits, records trigger/evidence/correction/invalidation, makes the remedy discoverable and checks its consumers. Objective repeated invariants prefer tested mechanics. | Avoids rediscovery and duplicate rulebooks. One-off unexplained errors do not become permanent rules. Positive and negative checks must show both known-failure detection and valid-work acceptance. Missing usage telemetry does not block a justified correction; it prevents a savings claim. [Cases](../tests/workflow-improvement-cases.json) cover stale advice, deterministic report preparation and protected approval gates. |
| Concise, transparent communication | [Concise Communication](../skills/pm-essential-skills-concise-communication/SKILL.md) leads with the result, reports meaningful changes, preserves requested detail and complete artifacts, and distinguishes denied, pending, uncertain and unattempted actions in blockers. | Reduces repeated status narration without hiding warnings, uncertainty, citations or necessary instructions. A short chat reply is not a substitute for the requested artifact. [Composition cases](../tests/integration-cases.json) explicitly preserve complete audits despite concise defaults. |
| Portable, independently usable installation | Each skill has its own entrypoint, metadata, license and local resources. The [installer](../scripts/install_suite.py) supports selected/additive installs, original-byte receipts, modified-file refusal, instruction-block preservation, transaction recovery and uninstall. [Packaging](distribution.md) ships the full suite or individual folders with recovery instructions; resource validation rejects cross-skill file dependencies. | Consumers need no Git, project registration, mandatory hook or tracking service. Bare folders use the target host's native discovery; the automated installer/hooks are specifically local Codex adapters. Local mechanics do not establish universal discovery, session activation or live adherence. |

## Composition and low-overhead checks

- Task Coordination's independent-progress rule does not bypass a pending
  Context Management location gate for the same request. The integration fixture
  makes the current precedence explicit; urgency does not silently change it.
- Resource Selection does not waive a requested independent review, exhaustive
  source coverage, strong-enough judgment, or required checks to lower call count.
- Source freshness, verification applicability and workflow lessons have distinct
  owners. A checkpoint preserves evidence; it does not grant permission, prove
  a check passed, or overrule newer instructions.
- Ordinary requests do not require all seven bodies, helpers, per-turn files,
  agents, usage collection or benchmarks. Conditional references answer a live
  decision. The installer adds pointers and disclosed scope, not a copied policy.
- Optional output capture retains actual producer status, raw recovery paths,
  byte counts and truncation. It is not a redactor, sandbox, timeout manager or
  guarantee that a bounded preview contains the decisive diagnostic.

These are traceable mechanisms for reducing avoidable work. Their net effect on
usage, time, quality and interventions remains unmeasured for this candidate.

## Research comparison: what transfers and what does not

This audit reused the project's [research and edge cases](research-and-edge-cases.md),
[scope review](pm-scope-coverage.md), [critical audit](audit-2026-10-22.md), and
[efficiency evaluation contract](efficiency-evaluation.md). It also inspected the
adjacent SWE repository's `docs/expert-comparison.md` and
`docs/empirical-evidence.md` as existing research, not as PM's product definition.
It did not conduct a new web-source refresh or execute upstream software.

The useful cross-domain mechanisms are accepted-outcome preservation, compatible
prerequisites, evidence identity/applicability, recoverable operations and truthful
separation of installation, activation and effectiveness. PM already implements
these, including the recent dependency-consumer check. Runtime/build identity in
SWE generalizes here to tying a claim to the actual artifact/source version and
checks exercised; it does not require a PM browser harness or deployment workflow.

Engineering-specific pooled-session rules, TDD/reviewer sequences, process runners,
security audits and database procedures remain with domain owners. Popularity,
repository activity and an expert's authorship do not establish comparative
benefit. The empirical research's relevant caution is to inspect **extra actions
induced by guidance**, not infer savings from shorter files or remove necessary
quality gates. No numerical skill quota, mandatory benchmark, external index,
or new evaluation service follows from that research.

## What was actually observed versus still unverified

| Evidence layer | Available evidence | Not established by it |
| --- | --- | --- |
| This readiness pass | Read all seven entrypoints; traced relevant conditional continuity/source/recovery references, installer and packaging implementations, policy/transfer/source/capture/evaluation helpers, fixture definitions and validator/CI responsibilities. The working tree was clean at the inspected starting revision. | This is static inspection, not a newly executed model trial, exhaustive proof over all inputs, or live host test. |
| Prior mechanics and regressions | The [critical audit](audit-2026-10-22.md) records specific repairs and local regression coverage. Tests exercise policy inputs, source pagination/revision handling, transfer recovery, isolated installation/rollback and extracted packages. | Test presence and earlier reports alone are not fresh final-state results. Integration must retain the actual command results for the final candidate; Windows-specific skips on Linux are not Windows passes. |
| Behavioral specifications | Per-skill and integration cases state observable outcomes and prohibited shortcuts. `test_execution_fixtures.py` checks their structure and identities. | The fixture-integrity test does not run the prompts, grade artifacts, or demonstrate adherence. |
| Earlier interpretation/user observations | The research notes report limited earlier expected-answer-withheld forward passes and a user-reported phase-choice success; they also record a later observed missed post-delivery location prompt and subsequent guidance correction. | These historical reports are not a complete current seven-skill trial. The later correction's live success remains unverified. No new forward/model evaluation was run here. |
| Activation compatibility | [Compatibility review](activation-compatibility.md) records source-backed Codex 0.163.0 discovery/configuration behavior. Installer status separates integrity, user configuration and unknown effective activation. | A healthy receipt, catalog entry or trusted hook registration does not prove a particular session selected or obeyed the skill. Other hosts need their own discovery and capability checks. |
| User value and savings | The implemented mechanisms and known failure cases support reasoned expectations of less avoidable work. The supplied-data evaluator preserves unknowns and quality failures. | No measured token, allowance, latency or quality improvement for this candidate; no certified threshold optimum or universal behavior guarantee. |

### Verified starting-candidate gate evidence

The integration owner verified the starting `main` revision above and tree
`3c0f5a67f683bdb24c1f9a169c54eabb54cc2692` with a clean worktree. Its local
required test gate reported **237 tests total, OK, with 3 skipped** (not 237
executed passes plus skips). The owner also verified successful PR 12 workflow
run `39767109886` and post-merge run `39767304165`. These are existing mechanical
results supplied by the integration owner, not tests rerun by this audit or live
model evidence. The final local integration pass, including the new readiness document and its
README entry, also completed: `python -m unittest discover -s tests` reported
237 total tests, OK with 3 skipped; `python scripts/validate_repository.py`
validated all seven skills. README/document local-file links passed.
`scripts/package_installers.py` built all eight candidate archives in an isolated
output directory; their distribution-manifest checksums matched. No archive was
installed into a user profile or published as a release. Runtime files match the
starting candidate; the integration adds documentation only.

## Known limits and pending choice

1. **Urgent-work exception — pending, not denied or implemented.** The current
   long-chat request gate waits before domain investigation/implementation;
   critical pressure follows its existing authorized safe-transfer rules.
   Urgency alone is not an exception. Only the user can choose whether to change
   this policy. No such change was made in this audit.
2. **Live behavior remains a trial question.** Skill discovery, actual selection,
   post-delivery request identification and destination recovery depend on the
   host and model. Supported tools and real authority remain necessary.
3. **Installation/recovery is bounded.** Original bytes and supported POSIX modes
   are protected, not every ACL, extended attribute or power-loss scenario.
   Modified targets and uncertain operations require reconciliation; do not erase
   receipts or journals to force success. Configuration diagnostics are not the
   effective running session's settings.
4. **No background coordinator.** These skills act during active turns, not while
   idle. No new service, schedule, paid evaluation or installation is needed to
   call this a trial candidate.

## Finite first-version gate

Stop preparation when all of the following are established for the chosen
candidate; do not reopen research merely to find more features:

1. The requirement/procedure mapping above still matches final files and no known
   accepted-scope defect is being hidden behind passing tests.
2. The final required repository gates pass: `python -m unittest discover -s tests`
   and `python scripts/validate_repository.py`. Record source revision, platform,
   failures/skips and command outcome. Reuse applicable existing results rather
   than rerun unchanged tests repeatedly; the final local results above cover this documentation integration, and
   final remote CI must still pass before handoff.
3. The user's selected source checkout or archive is identified and contains the
   actual final skills/resources. If archives are rebuilt, check their manifest
   and checksums; local output or CI artifacts are not a published release.
4. The user receives the candidate, the current Context Management limitation and
   the short trial below. No hidden urgent-policy edit, live-adherence claim or
   measured-savings claim is included.

A published release, paid/model benchmark, universal host certification and a
future improvement backlog are **not** first-version completion criteria. The
pending policy choice blocks that proposed change, not unrelated completed work.

## Short user trial

Use a low-stakes task and the user's chosen installation/discovery method. This
is a proposed manual trial, **not authorization for the assistant to install or
run it now**. Hooks are unnecessary. Keep the existing model and settings.

1. **Quiet path:** ask for a one-sentence correction. It should answer directly,
   without a plan, agent, tracker, setup prompt or invented savings report.
2. **Complete non-code outcome:** supply two small documents and request a final
   comparison with a recommendation and source references. State one settled
   preference and one exclusion. Check that the final artifact satisfies all
   requirements, preserves exceptions, does not re-ask the settled preference,
   and does not stop at an outline. A material missing decision should be asked
   concisely while independent work continues where the location policy permits.
3. **Correction and reuse:** request a change to one supplied fact. Check that
   affected conclusions and checks update, unchanged available evidence is
   reused, and the report distinguishes completed from unverified work. If a
   recurring mistake is actually observed, request a scoped remedy at its owner;
   do not manufacture incidents or demand a new skill after a one-off error.
4. **Continuity, only when relevant and authorized:** in a qualifying long project
   chat, check the current location-choice behavior. An actual transfer must
   preserve constraints, useful evidence and one owner, with an accessible
   predecessor/fallback; unsupported capabilities should produce an honest
   limitation, not a fabricated success. Do not manufacture critical pressure or
   require a transfer merely to finish the trial.

Stop when these relevant observations and the requested artifact can be judged.
Report only concrete misses, unnecessary interruptions/repeated work and useful
behavior, plus host/version and selected skills when known. An inaccessible
transfer path is a recorded capability limit, not a reason to keep testing
indefinitely. A trace or short example is enough to guide the next scoped fix;
no token export, new service or benchmark is required.
