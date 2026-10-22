# ibbuilds PM Essentials

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

This tree is an unreleased **0.4.0 candidate**. The CLI and ZIP use the published
repository, so they do not include unpushed candidate changes.

## Skill identity

Every skill uses `ibbuilds-pm-<skill-slug>`: **ibbuilds** is the publisher,
**PM Essentials** is the suite, and the suffix identifies the skill. For example,
`$ibbuilds-pm-context-management` invokes Context Management where explicit
invocations are supported. Display labels use **ibbuilds PM Essentials / Context Management**.
These names identify provenance, not a host verification badge.

Already installed under an unprefixed name? Follow the [migration guide](docs/skill-naming-migration.md)
to preserve custom edits and disabled settings without duplicate copies.

## The seven skills

| Skill | Purpose |
| --- | --- |
| [Task Coordination](skills/ibbuilds-pm-task-coordination/SKILL.md) | Clarify material gaps, coordinate dependencies, and finish the requested outcome. |
| [Context Management](skills/ibbuilds-pm-context-management/SKILL.md) | Preserve continuity and manage chat boundaries and authorized handoffs. |
| [Resource Selection](skills/ibbuilds-pm-resource-selection/SKILL.md) | Choose suitable available skills, tools, and supported agent/model routes. |
| [Source Selection](skills/ibbuilds-pm-source-selection/SKILL.md) | Gather sufficient evidence, check freshness, and reuse known sources. |
| [Execution Efficiency](skills/ibbuilds-pm-execution-efficiency/SKILL.md) | Match verification and recovery to the work and its risks. |
| [Workflow Improvement](skills/ibbuilds-pm-workflow-improvement/SKILL.md) | Address recurring friction with proportionate, authorized improvements. |
| [Concise Communication](skills/ibbuilds-pm-concise-communication/SKILL.md) | Give clear, brief replies without losing required detail or uncertainty. |

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

## Optional legacy installer

A retained local-Codex installer is available for existing users and people who
explicitly want additional activation guidance. Unlike normal skill installation,
it **edits user-level instructions**, including disclosed Context Management
routing scope when selected, and can optionally register hooks that require
host review and trust. Neither is required to use these skills. See
[optional installation, status, uninstall, and recovery](docs/installation.md).
The installer location remains supported. Older unprefixed skill identities require
[explicit migration](docs/skill-naming-migration.md); existing installs are never silently renamed or deleted.

## License

MIT licensed. The [license](LICENSE) permits use, modification, redistribution,
and commercial use with its copyright and permission notice retained. It does
not provide a warranty. Independent skill folders and generated archives retain
the notice; external projects cited in research keep their own licenses.

## Development and distribution

The expanded seven-skill tree is a **0.4.0 candidate**, not a claim of a published release or live validation. The [source ZIP](https://github.com/ibbuilds/pm-essential-skills/archive/refs/heads/main.zip) tracks published `main`; unpushed candidate changes are not included there. Generated individual archives below are local build outputs, not published downloads.

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

See the [execution-efficiency research rationale](docs/execution-efficiency-design.md), [design notes](docs/context-management-design.md), [research decisions](docs/research-and-edge-cases.md), [transfer recovery](skills/ibbuilds-pm-context-management/references/runtime.md), and [source reuse](skills/ibbuilds-pm-source-selection/references/source-reuse.md). Keep skill entrypoints under 700 words, domain work independent, and conditional detail in references.
