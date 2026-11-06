# Resource selection by required result

Version 0.6.5. The previous skill preserved user choices and discouraged unnecessary agents, but left tool suitability and adaptation mostly abstract. The revision adds a compact route table and a practical distinction between missing evidence/access and insufficient reasoning. Selection covers reconsideration during work, not only initial setup. No new helper, provider, model default, permission, hook or companion-skill dependency is introduced.

## Primary-source comparison

Sources read on 2026-11-06; these are engineering guidance, not measured results for this suite.

| Source | Applicable reasoning | Adaptation and limits |
| --- | --- | --- |
| Addy Osmani, [How agents think](https://addyosmani.com/agents/02-how-agents-think/) | Match capability to task difficulty, cost, speed and reliability; simple extraction differs from consequential reasoning. | Use sufficient capability where supported and authorized; preserve explicit user choices. Do not import model names, vendor tiers, temperature settings or claimed success rates. |
| Anthropic, [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Start with the simplest sufficient solution; routing and parallelization serve distinct needs. Extra complexity must justify its cost. | Direct work, deterministic tools, suitable connectors and bounded agents are alternatives that can be combined. No universal orchestration architecture or benchmark is required. |
| Anthropic, [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | Delegation helps separable research but duplicates tokens and coordination. Shared context and dependencies weaken its fit; selecting tools that reach the actual data matters. | Prefer parallel tool calls when enough; delegate independent reasoning with bounded context and review. Do not generalize the article's workload-specific token multipliers or agent counts. |
| Superpowers, [Dispatching parallel agents](https://github.com/obra/superpowers/blob/main/skills/dispatching-parallel-agents/SKILL.md) | Divide independent problem domains; avoid interference and provide focused tasks. Read content blob: `3fa091b348bbe0a18eaa0e17e9092c97f7005cbe`. | Preserve one owner per outcome and sufficient delegate context. Do not require one agent per failure, discard relevant shared context, or assume tool availability authorizes delegation. |

## Behavior and discovery

The 13 scenarios in `tests/resource-selection-cases.json` include direct answers, bulk transformation, consequential judgment, unavailable switching, explicit choices, useful delegation and missing visual capability. Five contrasting cases add unavailable private evidence, editable output, parallel reads without agents, an evaluated authorized lighter route, and dependent shared-state work.

One independent application pass received the revised skill and raw scenario inputs without expected answers or prior conclusions. Its decisions preserved all 13 scenario expectations. Routine answers, simple tracker reads and dependent edits took the direct path; missing access did not trigger reasoning escalation. This was a decision simulation, not 13 isolated sessions, executed integrations, or proof of automatic host activation. Borderline routine cases can reasonably skip loading when the sufficient route is already obvious.

The description now includes reconsideration, time and capability gaps; `allow_implicit_invocation: true` is preserved. The repository guidance and generated selection pointer no longer restrict ownership to initial choices. Structural validation checks metadata and references; unit tests and helper replays check their own implemented contracts. They do not prove universal model adherence or measured resource savings.
