# PM Essential Skills

Skills that help AI assistants preserve useful context, retrieve sufficient evidence, and verify changes proportionately with less repeated work. They work across project types and preserve the user's goals, preferences, and required quality.

## Install, then work normally

1. Choose the full-suite download or the individual skill you want.
2. Extract it and open **Install.cmd** on Windows.
3. Continue using Codex normally when it next loads its instructions. No project activation prompt is needed.

The installer finds Codex's bundled Python runtime when available. It installs only the included skills and adds a small activation rule to your existing user-level instructions. It preserves existing preferences and saves originals for uninstall. It needs no Git account, plugin, server, project registration, or tracking service. It does not create project files or alter tool permissions.

| Download | What it helps with |
| --- | --- |
| Full suite | All three independent skills together. |
| Context Management | Keep related work together, preserve continuity, and perform justified handoffs with supported tools. |
| Execution Efficiency | Complete implementation and repair tasks with risk-based checks and evidence-driven retries. |
| Source Selection | Find, read, and revalidate sufficient evidence while avoiding unnecessary repeated retrieval. |

Each skill works independently. Installing one does not require the others. Explicit disabled, suggest-only, and persistent-stay preferences remain binding. Short chats normally proceed without management notices or extra files; a one-request stay in a long chat expires at the next request.

Workflow behavior is maintained inside each `skills/<name>/` folder. The installer and optional reminders point to those skills and record coordination scope; they do not hold a second copy of the decision rules. Bare folders can also be installed in a host's native discovery location, such as `~/.agents/skills` for current local Codex. Avoid installing a second copy with the same name.

Context Management's disclosed installation scope includes archiving superseded source chats after confirmed handoff and temporarily restoring/rearchiving them when required to recover context. It preserves other active work and keep-visible choices; it never deletes history or scans unrelated chats. Every handoff carries the needed working context plus a verified predecessor reference and a recovery map for useful omitted detail.

For other systems, or an advanced installation:

```sh
python3 scripts/install_suite.py install
```

The installer requires Python 3.10+; the skills themselves also work through ordinary host skill discovery without Python or the installer. You can install a skill folder directly in a supported skill location. The installer strengthens local activation; it does not make bare skills dependent on it.

## Check or remove

On Windows, run `Install.cmd status` or `Install.cmd uninstall`. On other systems:

```sh
python3 scripts/install_suite.py status
python3 scripts/install_suite.py uninstall
```

Uninstall restores preexisting skill files and removes only the managed activation rule. It preserves user text added outside that rule and refuses to overwrite customized installed files. Another installer or an interrupted operation leaves a lock that must be reconciled before retrying.

`CODEX_HOME` and `--codex-home PATH` select a profile. In a full source download, `install --skill source-selection`, `install --skill context-management`, or `install --skill execution-efficiency` selects one skill; installing another later keeps the first. Repeating installation updates unchanged managed files without duplicating guidance.

## Stronger automatic reminders

For local Codex hosts supporting hooks, add `--hooks` to installation. This registers compact reminders on session start and user prompt submission. Existing hook definitions are preserved. **Codex still requires review and trust before these reminders run.** Registration is reported separately from trust and live invocation.

Reminders make no model calls, read no transcripts, write no per-turn project state, and make no tool-approval decisions. They use only installed-skill metadata. Ordinary skills and the user-level rule remain useful without them. See [automatic activation and recovery](skills/context-management/references/automatic-activation.md).

## What to expect

Context Management checks each new request using available context. In a long project chat, it asks new same-project chat or continue here for this request, then waits. Choosing to stay completes that request in place; the next request gets another prompt with a stronger recommendation. At critical pressure, it announces and performs a safe authorized handoff without another location question. Explicit stop-asking, persistent stay, suggest-only, and disabled preferences remain binding. Short chats stay quiet; standalone chats use concise checkpoints. Source Selection preserves the actual task's required evidence and coverage. Execution Efficiency uses known decisions before asking questions, matches verification to changed behavior and risk, and avoids unchanged retry loops without imposing fixed attempt limits or skipping required gates.

Available cost comparisons can keep work in place when a handoff would repeat an investigation or cost more than continuing. Concise findings reuse evidence at known versions. An optional local reader hashes UTF-8 sources, returns bounded pages, and omits already-available unchanged text. These helpers need no persistent cache, per-turn report, or new service; native tools remain available.

Activation takes effect when the host rebuilds its instruction chain. Existing sessions can retain earlier instructions. Host overrides, disabled skills, unavailable tools, and cloud/local differences affect behavior. The current authoring host exposes chat continuation tools but no native app-project creation or current-context occupancy telemetry.

Installation checks verify files and instruction placement; they do not prove live model invocation or measured savings. No skill is an idle background monitor. More chats or fewer prompt words alone do not prove a benefit. See [suite principles](docs/suite-principles.md) and [behavioral cases](tests/behavioral-cases.md).

## Development and distribution

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
