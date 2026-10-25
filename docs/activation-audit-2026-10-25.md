# PM activation audit and native installation checks

Reviewed 25 October 2026 against published PM base
`596bf5e30432fec217ed2e06a79e4f0e5171b8bc` and SWE base
`dba82fe68ccd94221d116ad0a2d27bee6adca159`.

## Result

All seven PM and eighteen SWE skills were installed and present in the auditing
desktop session's supplied catalog. Comparing complete skill folders with their
published sources found no missing, extra or substantively changed files;
line-ending differences were normalized. PM used the compatible Codex-home
skills root; SWE used the current user `.agents/skills` root. No duplicate of
these exact identities was found across those two roots. This observation does
not cover other projects or remote environments.

All seven PM policies explicitly allowed implicit invocation. SWE omitted the
policy, which uses the same default. The inspected base and two local alternate
configuration files contained no `skills.config` disable rules or explicit
`skills.include_instructions` suppression. Those files do not identify every
effective setting of every running session. The supplied catalog independently
establishes availability in this session.

The registered PM checkout remained at an older two-skill revision, `89e0869`.
It was not the source of the current seven installed copies. A registered project
folder, published repository and installed skills are separate versioned objects;
checking only that older checkout would give a misleading inventory.

## Supported corrections

Context Management's description now states its capability and trigger directly:
preserve task context and manage authorized handoffs at new phases or costly
context pressure. Its existing policy, thresholds, references and opt-outs are
unchanged. No standing chat-mutation authority is introduced.

The README now distinguishes the candidate already present on published `main`
from later local edits, instead of suggesting that the whole seven-skill tree
is still unpublished. Ordinary installed folders still require a deliberate
update after a repository change.

The companion SWE audit shortened discovery descriptions and added boolean
invocation-policy validation. It did not add a mandatory PM dependency.

## Diagnose the layer that failed

1. **Files:** compare the complete installed folder with the intended revision,
   including references and scripts. Keep customized files and disabled choices.
   Do not overwrite them or install duplicate aliases to get a green result.
2. **Discovery:** inspect the host's actual skill catalog. Check the documented
   root for that execution environment and the exact canonical name. Local
   Windows installation does not establish cloud or WSL availability.
3. **Enablement:** inspect relevant name/path disable rules and invocation policy.
   `allow_implicit_invocation: false` permits explicit use but disables implicit
   use. An omitted policy allows implicit selection. Preserve intentional opt-outs.
4. **Exposure:** inspect the description actually supplied to the model. A valid
   source description can still be shortened in a crowded catalog. Put the useful
   trigger first. Do not increase context budgets or remove unrelated skills
   automatically to repair a suspected routing failure.
5. **Selection:** on the next suitable real task, compare an ordinary request
   with an explicit invocation if needed. A completed `SKILL.md` read establishes
   loading. An announcement alone is not file-read evidence.
6. **Application:** inspect whether the actual result respects the relevant
   procedure, failure handling and no-op boundary. Loading alone does not prove
   that the model followed the instructions or improved the result.

These are troubleshooting steps, not a checklist to run on every request.
`scripts/install_suite.py status` diagnoses its optional legacy managed install;
the absence of its receipt does not establish that ordinary copied skills are
missing. Do not run that installer merely to make native skills show as installed:
it also changes user instructions and can select additional coordination scope.

## Routing examples for the seven independent skills

These are review scenarios, not newly executed model evaluations. Other relevant
skills may compose with the named owner; no request must load the whole suite.

| Skill suffix | Request that should make it relevant | Adjacent request needing no such workflow |
| --- | --- | --- |
| task-coordination | Finish an audit, corrections and validated deliverables across two repositories | Answer one known factual question |
| context-management | Resume a long investigation with replaceable history and a justified authorized handoff | A short standalone chat without context pressure |
| resource-selection | Choose between a costly multi-agent route and an adequate deterministic tool | Run one established local check |
| source-selection | Audit current claims against primary documentation and exact source revisions | Answer from already sufficient supplied evidence |
| execution-efficiency | Repair a tool after repeated failures and choose affected verification | Retrieve a known document without changing anything |
| workflow-improvement | Fix a demonstrated recurring failure in a reusable skill toolkit | Make a one-off ordinary content correction |
| concise-communication | Explain the result and necessary evidence clearly | It must never shorten away a requested full audit |

Explicit invocation uses the full canonical identity, for example
`$pm-essential-skills-source-selection`. A suitable ordinary request should not
need that prefix every time. Explicit use is a diagnostic fallback, not a new
installation requirement.

## What the sources establish

[OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills) describes
metadata-first discovery, implicit/explicit invocation and catalog-budget
shortening. Its default catalog budget is 2% of model context, or 8,000 characters
when the window is unknown; `skills.max_context_tokens` can override that budget.
That is not an instruction to raise it to the maximum.

[OpenAI's current authoring guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
supports concise triggers and conditional references rather than unconditional
document stacks. [Anthropic's authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
similarly favors concise instructions, progressive disclosure and real-use tests.
The [Agent Skills specification](https://agentskills.io/specification) defines
portable metadata constraints; a structurally valid skill is not a behavior score.

Fresh source check: Matt Pocock `5beb35b`, Ras Mic `69558ea` and Addy Osmani
`aeac41d` still matched the versions in the suites' existing research. Their
methods are useful comparisons, not evidence that this suite outperforms a
baseline. See the existing [research decisions](research-and-edge-cases.md).

## Evidence boundary

The existing [paired pilot](cloud-workflow-evaluation-2026-10-23.md) found equal
acceptance results with higher observed source and response bytes in the guided
condition. Later bounded functional checks do not reverse that finding into a
general savings claim. This audit establishes installation, observed catalog
availability, scoped source review and applicable local mechanics. Native
implicit selection on future prompts and comparative task benefit require their
own observations; no paid model campaign is an installation prerequisite.
