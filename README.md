# PM Essential Skills

Skills that help AI assistants preserve useful context and retrieve sufficient evidence with less repeated work. They work across project types and preserve the user's goals, preferences, and required quality.

## Install, then work normally

1. Choose the full-suite download or the individual skill you want.
2. Extract it and open **Install.cmd** on Windows.
3. Continue using Codex normally when it next loads its instructions. No project activation prompt is needed.

The installer finds Codex's bundled Python runtime when available. It installs only the included skills and adds a small activation rule to your existing user-level instructions. It preserves existing preferences and saves originals for uninstall. It needs no Git account, plugin, server, project registration, or tracking service. It does not create project files or alter tool permissions.

| Download | What it helps with |
| --- | --- |
| Full suite | Both independent skills together. |
| Context Management | Keep related work together, preserve continuity, and perform justified handoffs with supported tools. |
| Source Selection | Find, read, and revalidate sufficient evidence while avoiding unnecessary repeated retrieval. |

Each skill works independently. Installing one does not require the other. Existing user choices such as disabled, suggest-only, and stay remain binding. Short work should usually proceed without management notices or extra files.

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

`CODEX_HOME` and `--codex-home PATH` select a profile. In a full source download, `install --skill source-selection` or `install --skill context-management` selects one skill; installing another later keeps the first. Repeating installation updates unchanged managed files without duplicating guidance.

## Stronger automatic reminders

For local Codex hosts supporting hooks, add `--hooks` to installation. This registers compact reminders on session start and user prompt submission. Existing hook definitions are preserved. **Codex still requires review and trust before these reminders run.** Registration is reported separately from trust and live invocation.

Reminders make no model calls, read no transcripts, write no per-turn project state, and make no tool-approval decisions. They use only installed-skill metadata. Ordinary skills and the user-level rule remain useful without them. See [automatic activation and recovery](skills/context-management/references/automatic-activation.md).

## What to expect

Context Management checks useful task boundaries during active work. It keeps related work together, uses concise checkpoints for standalone chats, and transfers only when justified, authorized, and supported. Source Selection retrieves enough evidence for the actual task and preserves explicit full-read or exhaustive-coverage requirements.

Available cost comparisons can keep work in place when a handoff would repeat an investigation or cost more than continuing. Concise findings reuse evidence at known versions. An optional local reader hashes UTF-8 sources, returns bounded pages, and omits already-available unchanged text. These helpers need no persistent cache, per-turn report, or new service; native tools remain available.

Activation takes effect when the host rebuilds its instruction chain. Existing sessions can retain earlier instructions. Host overrides, disabled skills, unavailable tools, and cloud/local differences affect behavior. The current authoring host exposes chat continuation tools but no native app-project creation or current-context occupancy telemetry.

Installation checks verify files and instruction placement; they do not prove live model invocation or measured savings. Neither skill is an idle background monitor. More chats or fewer prompt words alone do not prove a benefit. See [suite principles](docs/suite-principles.md) and [behavioral cases](tests/behavioral-cases.md).

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

See the [design notes](docs/context-management-design.md), [research decisions](docs/research-and-edge-cases.md), [transfer recovery](skills/context-management/references/runtime.md), and [source reuse](skills/source-selection/references/source-reuse.md). Keep skill entrypoints under 700 words, domain work independent, and conditional detail in references.
