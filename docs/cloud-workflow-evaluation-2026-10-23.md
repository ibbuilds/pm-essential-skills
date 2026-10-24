# Cloud-only workflow evaluation — 2026-10-23

Follow-up: [evaluation corrections and guarded entrypoint refactors](efficiency-corrections-2026-10-23.md). The follow-up separates legitimate inspection cost from skill overhead and records an unsuccessful activation-change hypothesis.

## What was measured

This pass used isolated cloud execution, with no Codex task/CLI, external model API, or user screenshot required. It measures accepted work and instrumented workflow costs, **not Codex quota, billing, hidden reasoning, or total model tokens**. No claim is made that cloud inference itself is universally free.

A paired pilot replayed two real historical PM evaluator defects from commit `8facb21aaab2d2552dba72335538743e26635cb4`: loss of known failure evidence for unpaired tasks and numeric errors escaping the CLI boundary. One executor diagnosed and left a handoff; a fresh executor implemented the repair. The baseline had ordinary task instructions. The other arm additionally had a metadata catalog for four optional PM/SWE skills and could selectively load their packaged instructions. This is not a native host-installation/activation test.

Both arms had identical initial code, public regression tests, requirements, tools and inherited runner settings. Effective provider model/effort IDs and billed usage were not exposed. Diagnosis launch order was baseline then treatment; repair order was reversed. This was one pair, not randomized replication. Scheduling time is not reported as a performance advantage.

## Outcome and observed burden

| Measure across diagnosis and repair | Baseline | Skill-enabled |
| --- | ---: | ---: |
| Independent acceptance checks passed | 14/14 | 14/14 |
| Original regression tests preserved | Yes | Yes |
| Clarification requests observed by coordinator | 0 | 0 |
| Coordinator-requested correction rounds | 0 | 0 |
| Instrumented source reads | 10 | 17 |
| Source payload, including skill/catalog loads | 49,307 B | 83,995 B |
| Instrumented request-wrapper invocations | 16 | 24 |
| Verification invocations | 4 | 5 |
| Wrapper response bytes | 64,560 B | 108,174 B |
| Repeated unchanged source bytes | 15,506 B | 23,499 B |

The skill-enabled workflow emitted **70.35% more source payload** and **67.56% more wrapper-response bytes**, with equal results on the fixed acceptance checks. These are observed byte differences, not percentages of tokens or allowance saved. Skill/catalog loading accounted for 12,265 B of its source payload. The diagnostic worker loaded SWE Software Debugging; the repair worker loaded PM Execution Efficiency.

Both retained project decisions through the handoff. The skill-enabled repair replayed the existing failing tests before changing code; the baseline proceeded from the supplied failure evidence. Repeated reads/checks are not automatically waste: necessary verification and fresh-context inspection still count as work. Expected red regression runs are not failed repair outcomes.

The independent oracle was validated before repair: the historical implementation passed 11/14 checks and the previously published fix passed 14/14. Two additional numeric boundaries discovered during diagnosis were assessed separately, not retroactively counted in the frozen primary score. Both final repairs passed these two supplementary checks. Original test files and skill resources retained their recorded hashes; only the intended original evaluator source changed, with new tests and handoffs added. Production runtime files were not changed by this experiment.

## A component that helped, and where it did not

A separate deterministic microcheck exercised the actual Source Selection bounded reader against a real repository document. It retained returned text, requested overlapping ranges, repeated an unchanged range, and changed the source to test stale-receipt invalidation. Every requested character was reconstructed and checked against the current source, not merely trusted from a success flag.

| Four-read workload | Helper request + response bytes | Plain wrapped read request + response bytes | Difference |
| --- | ---: | ---: | ---: |
| Substantial overlapping ranges | 15,430 | 21,730 | −6,300 (−28.99%) |
| Small requested ranges | 3,138 | 1,810 | +1,328 (+73.37%) |

A genuinely four-line source excerpt was also a negative control: receipt reuse cost 1,339 B more than wrapped rereads. All coverage and invalidation assertions passed; repeated execution produced identical results. The helper still reads and hashes the local source, so this does not establish reduced filesystem I/O.

The comparison includes receipt request overhead and full JSON response metadata. Raw-text and same-helper-without-reuse baselines were also retained. It excludes skill loading, outer transport envelopes and model reasoning. Path lengths and workload composition affect the totals. There is no universal file-size threshold or token-saving percentage.

## Decision

The reader mechanism reduces payload on the tested substantial-repeat workload, but indiscriminate use makes small reads worse. Existing bounded-reader guidance already limits it to substantial or repeated reads; this result supports that condition, not mandatory use everywhere.

The paired agent pilot did **not** demonstrate a workflow-efficiency benefit. It exposes a concrete optimization target: selective skill loading, handoff size and avoidable repeat verification. Do not add more instructions merely to explain this result, or remove safety/quality gates to improve counts. Test proposed changes on additional representative tasks before claiming a reliable gain.

The measurement route now works without Codex: independent artifact acceptance plus instrumented actions and payloads. It can detect improvements and regressions. Actual user satisfaction, general effectiveness and total token/allowance savings remain separate, unproven outcomes. Keep unsuccessful and unfavorable observations; do not run until a favorable result appears.

## Method references and evidence

- [Anthropic: evaluate outcomes and transcripts](https://www.anthropic.com/research/demystifying-evals-for-ai-agents).
- [SWE-bench: apply patches and grade actual test outcomes](https://www.swebench.com/SWE-bench/guides/evaluation/).
- [OpenAI: task-specific evaluation and human calibration](https://developers.openai.com/api/docs/guides/evaluation-best-practices).
- [Recorded comparison](cloud-workflow-evaluation-2026-10-23.json).

The accompanying reproducibility bundle contains the wrapper, fixture provenance/hashes, both final artifacts, recorded read/check events, frozen and supplementary acceptance checks, mechanism inputs/outputs, and scope notes. Instrumentation is not a security sandbox or a complete trace: only wrapper-observed reads/checks are counted; ordinary edits and non-wrapper activity are outside its coverage. No installed runtime skill needs this harness.

## Later functional observations: 23 October 2026

These observations supplement, not replace, the earlier comparisons:

- With explicitly activated Context Management, a source-authored brief and one
  fresh successor yielded the two authorized migration documents after one
  scripted necessary location choice, without a user-written summary. One schema
  error was safely corrected. Transport was controller-assisted and host identity
  assurances simulated; this was not autonomous native discovery or activation.
- A recovery follow-on retrieved historical migration content and produced a
  correct comparison note. A strict full pass was **not established**: the note
  lacked the required immutable historical citation, separate transport capture
  was unavailable, and an initially overbroad read preceded the narrow read.
- Explicitly activated SWE Verification at `77efd89` verified the actual PM
  decoder-boundary patch, rejecting a synthetic wrong-path/no-tests proposal
  without requesting user rescue. The recorded suite ran 310 tests (OK, three
  Windows-only skips); 18 independent probes supported the repair and state safety.
  This was patch verification, not an unguided-assistant comparison.

[PM PR #36](https://github.com/ibbuilds/pm-essential-skills/pull/36) and
[PM PR #37](https://github.com/ibbuilds/pm-essential-skills/pull/37) merged bounded
JSON/unknown-field diagnostics and decoder-failure handling. These are shipped
robustness corrections, not measured user-effort or token savings. Fixed diagnostic
sizes apply only to the exercised malformed-input cases, not arbitrary resource
exhaustion. Neither correction changes skill entrypoint text, discovery metadata
or reference prose, or adds a mandatory workflow step. The observations above
concern frozen runs, not reruns of current main.

Local receipts and independent artifact checks support bounded functional
application, not complete native-session telemetry. Causal usefulness, automatic
host selection, broad user-effort reduction and provider billing remain unknown.

## Core workflow follow-through: 24 October 2026

The [SWE core workflow report](https://github.com/ibbuilds/swe-essential-skills/blob/main/docs/core-workflow-checks-2026-10-24.md)
adds a multi-turn planning pair (both 16/16) and a synthetic SQLite engineering
pair (both 20/20; each passed 12 contract checks plus three reviewer probes).
These extend observed functional coverage without demonstrating incremental suite
benefit or replacing the earlier results. The planning instruction candidate
remains held: 2,117 fewer read bytes, 2,764 more written-work bytes and the same
11 operations do not establish an overall efficiency gain.

[PM PR #40](https://github.com/ibbuilds/pm-essential-skills/pull/40) normalizes the
capture helper's invalid-output-path failure before producer execution.
[PM PR #41](https://github.com/ibbuilds/pm-essential-skills/pull/41) preserves JSON
values while emitting direct UTF-8 where supported, safely escaping lone
surrogates and retaining non-UTF-8 fallback. One fixed synthetic Unicode stdout
sample shrank from 828 to 740 bytes; raw streams and stored summary behavior
were preserved. Both were merged by PM revision `940c127`, not instruction-body
changes, new mandatory steps or measured token/billing savings.

The planning and engineering pairs used earlier frozen PM revisions (`108e228`
and `5c0df50`, respectively) with SWE `6d2cf828`. They used cloud agents, not the
user's actual Codex session; partial blinding and observer coverage limit claims.
The planning holdout's documented prelaunch sequencing deviation remains a limit,
not erased by later checks. See the linked report for scope and exclusions.

A separate coordination clarification now distinguishes notification-only messages,
supported work admission/start-or-resume, and completion. A bounded read-only
follow-up through an existing completed owner verified the merged SWE skill tree
and local case links without creating another worker. This is one cloud-host
functional observation, not a comparative gain or guaranteed behavior elsewhere.
The metadata trigger is unchanged; no installer, helper or extra tracking file is
required. Four mock admission cases were reviewed as reasoning checks, not live
integrations.
