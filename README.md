# PM Essential Skills

Seven independent skills for AI assistants: coordinate outcomes, preserve context,
choose resources and evidence, execute efficiently, improve recurring workflows,
and communicate clearly. Install any one or any subset as regular skills.

## Install as regular skills

Use your usual skill manager. For example, with the Skills CLI:

```sh
npx skills add ibbuilds/pm-essential-skills
```

Or download the [source ZIP](https://github.com/ibbuilds/pm-essential-skills/archive/refs/heads/main.zip)
and copy each desired **complete** `skills/<skill-name>/` folder into your host's
normal skill directory:

| Host | User-wide | Repository-local |
| --- | --- | --- |
| Codex | `~/.agents/skills/<skill-name>/` | `.agents/skills/<skill-name>/` |
| Claude Code | `~/.claude/skills/<skill-name>/` | `.claude/skills/<skill-name>/` |

Keep `SKILL.md`, references, scripts, and license files together. No custom
installer, Python setup, hooks, global instruction edits, or project activation
prompt is required. Avoid duplicate copies of a skill in different discovery
locations. Let the host reload its skills; an existing session may need restarting.

The CLI and source ZIP install the current published `main`. The optional bundle
manifest uses version **0.4.0**; no versioned release tag is implied. Installed
copies need synchronization when the source changes. See the current
[outcome contract and readiness](docs/v1-readiness.md) for implemented behavior
and the evidence that supports it.

## Skill identity

Every skill uses the exact `repo-name-skill-name` format:
`pm-essential-skills-<skill-slug>`. For example,
`$pm-essential-skills-context-management` invokes Context Management where explicit
invocations are supported. Its display name is `pm-essential-skills-context-management`.

Already installed under a bare name or `ibbuilds-pm-*`? Follow the
[migration guide](docs/skill-naming-migration.md) to preserve custom edits and
disabled settings without duplicate copies.

## The seven skills

| Skill | Purpose |
| --- | --- |
| [Task Coordination](skills/pm-essential-skills-task-coordination/SKILL.md) | Clarify material gaps, coordinate dependencies, and finish the requested outcome. |
| [Context Management](skills/pm-essential-skills-context-management/SKILL.md) | Preserve continuity and manage chat boundaries and authorized handoffs. |
| [Resource Selection](skills/pm-essential-skills-resource-selection/SKILL.md) | Choose suitable available skills, tools, and supported agent/model routes. |
| [Source Selection](skills/pm-essential-skills-source-selection/SKILL.md) | Gather sufficient evidence, check freshness, and reuse known sources. |
| [Execution Efficiency](skills/pm-essential-skills-execution-efficiency/SKILL.md) | Match verification and recovery to the work and its risks. |
| [Workflow Improvement](skills/pm-essential-skills-workflow-improvement/SKILL.md) | Address recurring friction with proportionate, authorized improvements. |
| [Concise Communication](skills/pm-essential-skills-concise-communication/SKILL.md) | Give clear, brief replies without losing required detail or uncertainty. |

Each skill works independently; none requires the other six. Its behavior lives
inside its own folder, with conditional detail in references.

## Use normally

In hosts that support automatic skill selection, the assistant can select
relevant installed skills from your request without an explicit invocation. You can also name a skill explicitly. It
should load only relevant skills and references, not the entire suite for every
request. Simple requests need no planning, delegation, logging, or evaluation
pipeline.

Installation puts files in place; discovery makes them available to the host;
selection loads a relevant skill; application means following its instructions.
These are distinct: installed files do not prove invocation, and automatic
selection is not a guarantee of model adherence. Host capabilities, disabled
skills, and higher-priority instructions still apply.
For missing or inconsistent activation, use the
[native-install activation checks](docs/activation-audit-2026-10-25.md).

Applicable requirements remain outstanding through delegation or chat changes
until completed or changed within authority. The skills do not waive required
evidence or verification, turn optional methods into compulsory work, or override
explicit disabled, suggest-only, stay, and stop-asking preferences. Installation
alone grants no authority to create, message, archive, or restore chats, change
settings, install tools, or run benchmarks. Handoffs use supported tools and
verified authorization; unavailable capabilities remain unavailable.

No skill is an idle background monitor. Local checks do not establish live
integration success or measured savings. See [first-version readiness](docs/v1-readiness.md),
[scope coverage](docs/pm-scope-coverage.md), [suite principles](docs/suite-principles.md),
and [behavioral cases](tests/behavioral-cases.md) for deeper scope and evidence.

## Validation status

The [current outcome review](docs/v1-readiness.md) corrects negative-value handoff
prompts and keeps related corrections in the chosen chat. It preserves explicit
location decisions and transfer safeguards. Ordinary work uses only the relevant
skill and references, with no mandatory helper or chat-management call.

The [25 October functional validation](docs/functional-validation-2026-10-25.md)
exercised all seven workflows on completed tasks, including a real validator
repair, source-complete report, continuation decision, resource choice and a
wording-only control. It also retains 29 replayable helper observations. This
adds procedure/application evidence to the earlier installation checks.

Cloud checks have exercised multi-turn planning, context handoff, scoped
engineering verification and supported task admission. Real helper review also
led to merged capture-path and Unicode-output fixes. See the
[workflow evaluation](docs/cloud-workflow-evaluation-2026-10-23.md) for tested
behaviors, source revisions and limitations.

These are bounded functional observations, not proof of automatic host activation
or suite-wide benefit. Matched tasks succeeded in both conditions; reduced
supervision, total usage and billing savings remain unestablished. Earlier
reviews found the same two evaluator defects, fixed in
[PR #25](https://github.com/ibbuilds/pm-essential-skills/pull/25); skill exposure
and effective settings were not independently isolated. Those reviews and the
[workflow smoke test](docs/workflow-smoke-test-2026-10-23.md) remain separate,
scoped evidence rather than certification of the full suite.

## Optional legacy installer

A retained local-Codex installer is available for existing users and people who
explicitly want additional activation guidance. Unlike normal skill installation,
it **edits user-level instructions**, including disclosed Context Management
routing scope when selected, and can optionally register hooks that require
host review and trust. Neither is required to use these skills. See
[optional installation, status, uninstall, and recovery](docs/installation.md).
The installer location remains supported. Older skill identities require
[explicit migration](docs/skill-naming-migration.md); existing installs are never silently renamed or deleted.

## License

MIT licensed. The [license](LICENSE) permits use, modification, redistribution,
and commercial use with its copyright and permission notice retained. It does
not provide a warranty. Independent skill folders and generated archives retain
the notice; external projects cited in research keep their own licenses.

## Development and distribution

The seven-skill tree is distributed from published `main`; the optional bundle manifest is **0.4.0**, without a versioned release tag. The [source ZIP](https://github.com/ibbuilds/pm-essential-skills/archive/refs/heads/main.zip) tracks published `main`. Generated individual archives below are local build outputs, not published downloads.

Build the full-suite and individual downloads:

```sh
python scripts/package_installers.py
```

Archives, `SHA256SUMS`, and a portable `distribution.json` manifest are created under `work/downloads/`. Each individual download includes its own recovery guide. The validation workflow also retains verified candidate downloads for 14 days; these require GitHub sign-in and are not public versioned releases. See [reproducible distribution and integrity checks](docs/distribution.md). The optional [plugin manifest](plugin.json) remains available for hosts that prefer a skills bundle; plugin packaging is not required for normal use. `scripts/package_plugin.py` builds that alternative without installing or uploading it.

Run the required checks with the development dependency installed:

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests
python scripts/validate_repository.py
```

Helpers use the standard library; repository validation uses PyYAML. Tests cover policy decisions, capability checks, recoverable transfers, source reuse, isolated installer/hook behavior, and extracted downloads. The Windows launcher is tested on Windows; platform-specific tests are skipped elsewhere. Live model behavior and net usage effects need separate evaluation.

Use the optional [complete-task evaluator](docs/efficiency-evaluation.md) for supported usage exports. It includes startup/retry/handoff requests, preserves quality failures, and keeps missing telemetry unknown. It does not collect data during normal work.

See the [execution-efficiency research rationale](docs/execution-efficiency-design.md), [design notes](docs/context-management-design.md), [research decisions](docs/research-and-edge-cases.md), [transfer recovery](skills/pm-essential-skills-context-management/references/runtime.md), and [source reuse](skills/pm-essential-skills-source-selection/references/source-reuse.md). Keep skill entrypoints under 700 words, domain work independent, and conditional detail in references.
