# Efficiency corrections after the cloud pilot

The first pilot found extra work, not a universal defect in the suites. We separated instruction cost, useful verification, and evaluation-tool limitations before changing production guidance.

## What explained the initial extra 34,688 source bytes

- Skill/catalog loading: 12,265 B.
- Diagnosis worker reading its own handoff: 6,060 B.
- Longer handoff read by the fresh worker: 767 B.
- Longer reproduction-test source: 1,460 B.
- Final source and new-test inspection: 14,136 B.

These sum to the measured difference. Direct loading was only 35.36% of the excess. Fresh-worker reads and final inspection are not inherently waste. The original harness exposed read/list/check but no diff, although debugging guidance correctly requires inspecting final changes. Removing that quality step would be the wrong optimization.

## Corrected comparison, including an unsuccessful hypothesis

Both follow-up arms received a complete diff operation with new/deleted-file and snapshot-integrity checks. A candidate narrowed PM Execution Efficiency's activation description to unresolved verification/recovery decisions rather than routine implementation.

The first follow-up was not evidence for that metadata change: its candidate worker never read the metadata catalog. Candidate text was also finalized between launches; recorded read hashes were reconciled, and no causal claim was made from that pair.

A second comparison supplied the actual metadata directly in both initial prompts, matching normal metadata-first discovery more closely. It kept the same repair handoff, source, tests, four resource folders, and tool affordances. Only PM's candidate description differed.

| Preloaded metadata repair comparison | Current description | Narrower candidate |
| --- | ---: | ---: |
| Independent acceptance checks | 14/14 | 14/14 |
| Skill-body bytes loaded | 0 | 0 |
| Source reads | 3 | 6 |
| Verification invocations | 2 | 2 |
| Diff inspections | 2 | 2 |
| Wrapper response bytes | 29,861 | 48,985 |

Both continued from the existing plan, omitted unnecessary skill-body loading, and completed the repair correctly. The candidate did more contract/source reading. One pair cannot attribute that difference causally, but it does **not** support a savings claim. The narrower activation description was **not shipped**. Its eight routing-decision probes retained the intended positive/negative boundaries, but that classification result does not override the execution evidence.

No additional runs were launched merely to seek a favorable metadata result. None of these comparisons measures provider billing, hidden reasoning or Codex allowance.

## Production change: smaller loaded instructions, unchanged safeguards

Instead of adding rules or deleting verification, two entrypoint bodies were refactored to remove repetition and express existing decisions more directly:

| Entrypoint | Before | After | UTF-8 text reduction |
| --- | ---: | ---: | ---: |
| PM Execution Efficiency | 4,120 B | 3,645 B | 11.53% |
| SWE Software Debugging | 4,849 B | 4,274 B | 11.86% |
| Combined | 8,969 B | 7,919 B | 11.71% |

Names, descriptions, UI metadata, licenses, and supporting references remain byte-identical. No installer, dependency, service, mandatory tracker, or new orchestration layer was added. The PM opening explicitly says helper calls are not required for activation; it does not prohibit useful domain helpers.

Independent source comparison found no consequential semantic loss. Sixteen explicit-invocation decision probes were reviewed against the retained rules: required gates, stale evidence, uncertain external effects, ready-work stopping, pending monitoring, deterministic retries, no arbitrary attempt cap, scope preservation, reproduction versus setup failure, intermittent evidence, causal fast paths, event ordering, failed-patch reassessment, workaround distinctions, and final-diff inspection. All produced the expected guard-preserving decisions. These are bounded decision probes, not executed production incidents or a proof of general adherence.

The verified improvement is **smaller instruction payload when these skills are loaded**, with preserved constraints under review and those probes. It is not evidence that whole-task tokens, elapsed time, or allowance fell by 11.71%. Keeping descriptions unchanged also means no claim of reduced automatic activation.

## What remains to establish

Broader usefulness needs representative tasks and repeated measurements. Keep successful outcome quality alongside recorded work; do not reward skipped requirements or call every reread waste. The existing reader's substantial-repeat payload benefit and its short-read penalty remain valid conditional mechanism results. Normal installation stays unchanged.

References: [OpenAI skill activation](https://developers.openai.com/plugins/concepts/skills#how-skills-activate), [Anthropic skill authoring and evaluation](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills), [SkillsBench v4 applicability findings](https://arxiv.org/html/2602.12670v4#A6), and the [original measured pilot](cloud-workflow-evaluation-2026-10-23.md). Supporting records remain in the updated evidence bundle; no rejected hypothesis is omitted.
