# PM Essential Skills

Seven independent skills that help AI assistants coordinate complete outcomes, preserve context, choose resources and evidence, execute efficiently, improve recurring workflows, and communicate clearly. They work across project types and preserve the user's goals, preferences, and required quality.

## Install, then work normally

This tree is an unreleased **0.4.0 candidate** with seven skills. The download link tracks published `main`, not a versioned release.

1. Download the [full suite source ZIP](https://github.com/ibbuilds/pm-essential-skills/archive/refs/heads/main.zip), with the skills and installer published on `main`.
2. Extract it, open the extracted **pm-essential-skills-main** folder, and open **Install.cmd** on Windows.
3. Continue using Codex normally when it next loads its instructions. No project activation prompt is needed.

Installation is checked independently of host activation. Native skill listing, instruction loading, trusted hook execution, and model adherence are distinct: this candidate has no certified Codex-version compatibility matrix. See the [critical audit and evidence limits](docs/audit-2026-10-22.md). An installed file is not proof that your host invoked it.

The installer finds Codex's bundled Python runtime when available. It installs only the included skills and adds a small activation rule to your existing user-level instructions. It preserves existing preferences and saves originals for uninstall. It needs no Git account, plugin, server, project registration, or tracking service. It does not create project files or alter tool permissions.

| Install option | What it helps with |
| --- | --- |
| [Full suite source ZIP](https://github.com/ibbuilds/pm-essential-skills/archive/refs/heads/main.zip) | Published suite source and installer; candidate builds contain all seven. |
| Task Coordination | Clarify only material gaps, coordinate dependencies, and finish the full requested outcome. |
| Context Management | Keep related work together, preserve continuity, and perform justified handoffs with supported tools. |
| Execution Efficiency | Complete implementation and repair tasks with risk-based checks and evidence-driven retries. |
| Resource Selection | Choose a suitable existing skill, tool, or supported model/agent route before substantial work. |
| Source Selection | Find, read, and revalidate sufficient evidence while avoiding unnecessary repeated retrieval. |
| Workflow Improvement | Address recurring friction through proportionate lessons, toolkit reuse, and authorized improvements. |
| Concise Communication | Answer briefly in plain language while preserving required detail, uncertainty, and exact blockers. |

Each skill works independently. Installing one does not require the others. Automatic selection means loading only relevant skills and conditional references, not all seven for every request. Simple requests proceed directly; no universal planning, delegation, logging, or evaluation pipeline is added. Explicit disabled, suggest-only, and persistent-stay preferences remain binding. Short chats normally proceed without management notices or extra files; a one-request stay in a long chat expires at the next request.

For just one skill, use the source ZIP's Python installer with `--skill` as described below, or build the individual downloads under [Development and distribution](#development-and-distribution). The individual options above are not links to published downloads.

Workflow behavior is maintained inside each `skills/<name>/` folder. The installer and optional reminders point to those skills and record coordination scope; they do not hold a second copy of the decision rules. Bare folders can also be installed in a host's native discovery location, such as `~/.agents/skills` for current local Codex. Avoid installing a second copy with the same name.

Context Management's disclosed installation scope includes archiving superseded source chats after confirmed handoff and temporarily restoring/rearchiving them when required to recover context. It preserves other active work and keep-visible choices; it never deletes history or scans unrelated chats. Every handoff carries the needed working context plus a verified predecessor reference and a recovery map for useful omitted detail.

For local Codex on other operating systems, or an advanced installation:

```sh
python3 scripts/install_suite.py install
```

The installer and hooks target local Codex, not every host. Other skill-capable hosts can use individual folders through their own native discovery, subject to their capabilities and policies; neither universal automatic invocation nor API model controls are promised.

The installer requires Python 3.10+; the skills themselves also work through ordinary host skill discovery without Python or the installer. You can install a skill folder directly in a supported skill location. The installer strengthens local activation; it does not make bare skills dependent on it.

## Check or remove

On Windows, run `Install.cmd status` or `Install.cmd uninstall`. On other systems:

```sh
python3 scripts/install_suite.py status
python3 scripts/install_suite.py uninstall
```

Uninstall restores preexisting skill files and removes only the managed activation rule. It preserves user text added outside that rule and refuses to overwrite customized installed files. Interrupted operations retain a recovery journal. Run `Install.cmd recover` on Windows or `python3 scripts/install_suite.py recover` with the same profile to restore the pre-operation state, then retry. Recovery refuses to replace later user edits. If a force-killed installer left a lock, confirm no installer is running before removing only the stale `pm-essential-skills/install.lock`; keep the receipt and journal. See [recovery details](skills/context-management/references/automatic-activation.md#recovery-and-checks).

Optional copy diagnostics (Python installer only):

```sh
python3 scripts/install_suite.py status --check-skill-root ~/.agents/skills
```

Repeat `--check-skill-root PATH` for other skills directories you want checked. This read-only check looks only for `<installed-name>/SKILL.md` in the managed installation and supplied roots, reporting resolved candidate paths, possible duplicates, and inspection errors. Symlink aliases of the same path count once. It does not search recursively, inspect other skills, change files, or affect status's exit code. [Codex's skill-loading documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) says same-name skills are not merged and both can appear. Distinct candidate files do not prove both are active; no duplicates found does not prove discovery or complete coverage. Activation remains unknown. Normal status checks remain unchanged without this option.

`CODEX_HOME` selects a profile for either installer. Advanced options belong to the Python installer, not `Install.cmd`: for example, `python3 scripts/install_suite.py install --skill source-selection --codex-home PATH`. Use `python` or `py -3` on Windows with a suitable Python runtime. In a full source download, `--skill NAME` selects any name in the ownership table below; repeat it for a subset. For example, `--skill concise-communication` installs only the reply skill; installing another later keeps the first. Repeating installation updates unchanged managed files without duplicating guidance.

## Stronger automatic reminders

For local Codex hosts supporting hooks, run `python3 scripts/install_suite.py install --hooks` (Windows: `py -3 scripts/install_suite.py install --hooks` with Python 3.10+). `Install.cmd` accepts only `install`, `status`, `uninstall`, or `recover`, not extra options. This registers compact reminders on session start and user prompt submission. Existing hook definitions are preserved. **Codex still requires review and trust before these reminders run.** Registration is reported separately from trust and live invocation.

Reminders make no model calls, read no stored transcripts, write no per-turn project state, and make no tool-approval decisions. They route only from installed-skill metadata; prompt contents never become instructions. The host input envelope includes the prompt: malformed or over-16-MiB envelopes deliberately receive no reminder. Reminder text still adds model-input context, so hooks are optional, not a guaranteed saving. Ordinary skills and the user-level rule remain useful without them. See [automatic activation and recovery](skills/context-management/references/automatic-activation.md).

## What to expect

| Skill name | Owns | Does not own |
| --- | --- | --- |
| `task-coordination` | Requested outcome, acceptance, material gaps, dependencies, and completion | Chat placement or permission grants |
| `context-management` | Continuity, chat boundaries, and authorized transfers | New project priorities |
| `resource-selection` | Initial execution resources, supported agent/model options, division of work | Evidence coverage or settings changes without authority |
| `source-selection` | Evidence selection, provenance, coverage, and freshness | A parallel project-memory system |
| `execution-efficiency` | Risk-based verification and recovery during execution | Waiving required gates |
| `workflow-improvement` | Conditional lessons, reusable toolkit changes, and evaluation governance | Automatic installs, background reviews, or unauthorized benchmarks |
| `concise-communication` | Clear, concise replies with enough substance | Shrinking the user's requested deliverable |

Resource choices use capabilities actually available and authorized; unsupported model switching stays a recommendation, not a claimed action. Delegation is conditional, with bounded ownership and integration, not a requirement. Workflow improvements follow recurring or consequential evidence; recording lessons, changing shared instructions, installing tools, and running evaluations remain subject to the user's scope and permissions. No routine request triggers new bookkeeping or benchmarks.

Context Management checks each new request using available context. In a long project chat, it asks new same-project chat or continue here for this request, then waits. Choosing to stay completes that request in place; the next request gets another prompt with a stronger recommendation. At critical pressure, it announces and performs a safe authorized handoff without another location question. Explicit stop-asking, persistent stay, suggest-only, and disabled preferences remain binding. Short chats stay quiet; standalone chats use concise checkpoints. Source Selection preserves the actual task's required evidence and coverage. Execution Efficiency uses known decisions before asking questions, matches verification to changed behavior and risk, and avoids unchanged retry loops without imposing fixed attempt limits or skipping required gates.

Available cost comparisons can keep work in place when a handoff would repeat an investigation or cost more than continuing. Concise findings reuse evidence at known versions. An optional local reader hashes UTF-8 sources, returns bounded pages, and omits already-available unchanged text. These helpers need no persistent cache, per-turn report, or new service; native tools remain available.

Activation takes effect when the host rebuilds its instruction chain. Existing sessions can retain earlier instructions. Host overrides, disabled skills, unavailable tools, and cloud/local differences affect behavior. The current authoring host exposes chat continuation tools but no native app-project creation or current-context occupancy telemetry.

Installation checks verify files and instruction placement; they do not prove live model invocation or measured savings. No skill is an idle background monitor. More chats or fewer prompt words alone do not prove a benefit. See the [full project scope map](docs/pm-scope-coverage.md), [suite principles](docs/suite-principles.md) and [behavioral cases](tests/behavioral-cases.md).

## Development and distribution

The expanded seven-skill tree is a **0.4.0 candidate**, not a claim of a published release or live validation. The source ZIP above tracks published `main`; unpushed candidate changes are not included there. Generated individual archives below are local build outputs, not published downloads.

Build the full-suite and individual downloads:

```sh
python scripts/package_installers.py
```

Archives are created under `work/downloads/`. The optional [plugin manifest](plugin.json) remains available for hosts that prefer a skills bundle; plugin packaging is not required for normal use. `scripts/package_plugin.py` builds that alternative without installing or uploading it.

Run the required checks with the development dependency installed:

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests
python scripts/validate_repository.py
```

Helpers use the standard library; repository validation uses PyYAML. Tests cover policy decisions, capability checks, recoverable transfers, source reuse, isolated installer/hook behavior, and extracted downloads. The Windows launcher is tested on Windows; platform-specific tests are skipped elsewhere. Live model behavior and net usage effects need separate evaluation.

Use the optional [complete-task evaluator](docs/efficiency-evaluation.md) for supported usage exports. It includes startup/retry/handoff requests, preserves quality failures, and keeps missing telemetry unknown. It does not collect data during normal work.

See the [execution-efficiency research rationale](docs/execution-efficiency-design.md), [design notes](docs/context-management-design.md), [research decisions](docs/research-and-edge-cases.md), [transfer recovery](skills/context-management/references/runtime.md), and [source reuse](skills/source-selection/references/source-reuse.md). Keep skill entrypoints under 700 words, domain work independent, and conditional detail in references.
