# Context Management: early intervention

The original default reviewed at75% and rolled over at85%. An earlier revision required a pause at40% with a50% ceiling. The user's latest preference supersedes that policy: warn and prepare from40%, allow current work during the warning range, and require a pause at60%. At the ceiling, only stabilization, checkpoint preservation and handoff remain. This does not promise a deterministic runtime restriction.

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

Use full active context tokens divided by the active host's effective window. Include carried instructions and tool context. Do not use quotas, lifetime usage, age, or the advertised maximum when it differs from the usable limit.40/60 are user-selected operating limits, not research-derived optima. Explicit settings such as45/55 retain separate warning and pause boundaries; required enforcement rejects ceilings above60%.

Without fresh telemetry, label occupancy unknown. A preventive budget of10 substantive user turns or3 observed tool outputs >=8,000characters since the last confirmed effective reset requires a handoff; already-visible substantial obsolete history or repeated loss/reconstruction can trigger sooner. These are workflow budgets, not percent estimates. Their effect on unnecessary handoffs and total task cost has not been measured.

At40%, warn and prepare a concise continuation without pausing work solely for context pressure or manufacturing a blocking location question. At60%, no new feature, test run or investigation may start; only minimum stabilization and handoff remain. Repeat one short reminder per later user turn while pressure remains. Existing actual pending choices and explicit moves retain their authority. Prior request-scoped stay, cost estimates, projectless membership, missing tools and prior notices do not suppress the warning or bypass the ceiling. Later explicit human opt-outs remain authoritative. Never poll or write per-turn logs.

Briefs retain goal, decisions, constraints, current revision/files and uncommitted changes, current error, exact verification commands/results and limits, pending actions/approvals, next step and relevant enabled skills. Store references instead of raw logs. Only an authorized, ready destination can take ownership. At the ceiling, missing tools produce a manual brief and paused source. Effective compaction with preserved decisions and fresh occupancy below60% clears the hard gate; warnings continue from40% to <60% and clear below40%.

## Validation

Default-policy tests exercise exact boundaries, each membership mode, unresolved reminders, current-outcome choices, expensive reconstruction, missing context, unsafe operations, unknown/stale readings, explicit opt-outs, fresh compaction, completion/new work, input rejection and CLI behavior. Historical75/85 routing regressions now explicitly select the supported advisory mode; they do not test or imply those old defaults remain active.

An independent six-scenario application pass tested the earlier40/50 policy using only the skill and conditional references, with expected answers withheld. It covered44% without creation tools, a repeated request during a pending move,12% compaction, three large outputs without a meter,51% with an open transaction, and an explicit opt-out. It found stale adapter permissions and imprecise example wording, which were reconciled. Those observations are historical and do not prove the current40/60 boundary behavior. Current tests distinguish39.999%,40%,55%,59.999% and60%, retained choices, blocked media/access, compaction into the warning range and explicit45/55 settings. These remain synthetic policy checks, not a native invocation-rate study or proof of universal adherence.
