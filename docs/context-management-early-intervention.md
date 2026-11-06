# Context Management: early intervention

The previous default reviewed at75% and rolled over at85%, with cost suppression and single-notice deduplication. It did not satisfy the requested early, persistent fresh-chat workflow. This revision requires intervention at40%;50% is the ceiling. Once triggered, only stabilization, checkpoint preservation and handoff are permitted until resolved. It does not promise a deterministic runtime restriction.

## Comparison with maintained original sources

Reviewed6November2026, using original repository content and official documentation:

| Source | Relevant design | Applied here |
| --- | --- | --- |
| [Matt Pocock handoff](https://github.com/mattpocock/skills/blob/main/skills/productivity/handoff/SKILL.md), blob a224edc643a20ddb989f9bca1547440169159810 | Small portable handoff, link existing artifacts, suggested skills, redact sensitive data. Its frontmatter disables model invocation. | Keep the useful handoff fields and reuse storage; retain implicit invocation because this user's requirement differs from that manual skill. |
| [Pocock invocation rules](https://github.com/mattpocock/skills/blob/main/.agents/invocation.md), blob4877b32cd55bf708be61d90b95b720003f0ffdb5 | Model-facing trigger descriptions and explicit host skill-tool invocation, with Codex metadata kept consistent. | Describe ongoing work and early context checks in the discovery metadata. Use the actual host skill mechanism; reading SKILL.md is supported on this authoring host. No invented Skill tool. |
| [Addy Osmani context-engineering](https://github.com/addyosmani/agent-skills/blob/main/skills/context-engineering/SKILL.md), blobabdfe2732255de944db13d0312a1634a425c7c5d | Proactive context budgeting, selective retrieval, retain current task/error/constraints, restartable boundaries and exact verification state. No universal40% threshold. | Preserve current error, revision/uncommitted work and exact checks; reduce needless output; stabilize before transfer rather than abandon an operation. |
| [Anthropic context engineering](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) | Context is a finite attention budget; degradation varies. High-fidelity compaction and selective durable notes support long work. | No claim of a universal quality cliff. Fresh successful compaction can clear pressure when essential state remains. Avoid full history replay. |
| [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) and [OpenAI compaction](https://developers.openai.com/api/docs/guides/compaction) | Active context differs from cumulative usage; native compaction and its thresholds belong to the runtime. Codex exposes configuration keys for compaction, not an unconditional guarantee that every agent turn receives a meter. | Prefer supplied fresh current occupancy/effective window. Do not change global compaction settings or claim a skill can access unavailable telemetry. |

These are relevant recognized implementations, not a measured leaderboard comparison. Their repository popularity is not proof of behavioral correctness. No other author's files were copied into the skill.

## Metric and behavior

Use full active context tokens divided by the active host's effective window. Include carried instructions and tool context. Do not use quotas, lifetime usage, age, or the advertised maximum when it differs from the usable limit.40/50 are conservative user-selected operating limits, not research-derived optima.

Without fresh telemetry, label occupancy unknown. A preventive budget of10 substantive user turns or3 observed tool outputs >=8,000characters since the last confirmed effective reset requires a handoff; already-visible substantial obsolete history or repeated loss/reconstruction can trigger sooner. These are workflow budgets, not percent estimates. Their effect on unnecessary handoffs and total task cost has not been measured.

At40%, pause substantive work. At50%, no new feature, test run or investigation may start; only minimum stabilization and handoff remain. Repeat one short reminder on each later user turn while pending, reuse the existing question and brief, and never poll or write per-turn logs. Prior request-scoped stay, cost estimates, projectless membership, missing tools and prior notices do not bypass the required gate. Later explicit human opt-outs remain authoritative.

Briefs retain goal, decisions, constraints, current revision/files and uncommitted changes, current error, exact verification commands/results and limits, pending actions/approvals, next step and relevant enabled skills. Store references instead of raw logs. Only an authorized, ready destination can take ownership. Missing tools produce a manual brief and paused source, not silent continued implementation. Effective compaction with a fresh low reading and preserved decisions can resolve the gate in place.

## Validation

Default-policy tests exercise exact boundaries, each membership mode, unresolved reminders, current-outcome choices, expensive reconstruction, missing context, unsafe operations, unknown/stale readings, explicit opt-outs, fresh compaction, completion/new work, input rejection and CLI behavior. Historical75/85 routing regressions now explicitly select the supported advisory mode; they do not test or imply those old defaults remain active.

An independent six-scenario application pass used only the skill and conditional references, with no expected answers or tests. It handled44% without creation tools, a repeated request to implement during a pending move, confirmed12% compaction, three large outputs without a meter,51% with an open transaction, and an explicit stop-reminders override. It found three stale adapter permissions and imprecise example wording; those were reconciled. This is synthetic behavioral evidence, not a native host invocation-rate study or proof of universal adherence.
