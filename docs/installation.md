# Optional legacy Codex installer

For old unprefixed skill names, back up edits and disabled settings before replacing them. The installer refuses silent migration; status, explicit uninstall and recovery remain supported. See [skill-name migration](skill-naming-migration.md).

**Not required for normal skill use.** Prefer your skill manager or copy complete
skill folders as described in the [README](../README.md#install-as-regular-skills).
The skills require no custom installer, Python, hooks, or global instruction edits.
This page documents the retained installer for people who deliberately choose it
or need to manage an existing installer-managed installation.

## What this alternative changes

The installer targets local Codex. It copies selected skills to
`$CODEX_HOME/skills` (a backward-compatible user root), adds a managed activation
rule to user-level instructions, and saves originals for uninstall. Optional
`--hooks` also registers reminders in the host configuration. These are additional
changes, not prerequisites for discovering or selecting ordinary skills.
When Context Management is included, the managed user-level rule also records
the disclosed limited same-project continuation, routing, archival and recovery
scope. Review that separate opt-in behavior before choosing this installer; see
[its exact scope](../skills/ibbuilds-pm-context-management/references/automatic-activation.md#defaults-and-authority).
Bare skill installation supplies no such authorization, and a receipt or copied
template is not human permission. Other tool and action boundaries still apply.

It preserves existing preferences and does not create project files or change
tool permissions. Avoid installing another copy of the same skill through a
skill manager or a native directory while keeping an installer-managed copy.
Use this installer's uninstall/recovery commands for its managed files and rules.

## Install with this alternative

From the full source tree, open `Install.cmd` on Windows, or run:

```sh
python3 scripts/install_suite.py install
```

This optional installer requires Python 3.10+. The Windows launcher looks for
Codex's bundled runtime when available. No Git account, plugin, server, project
registration, or tracking service is required. Installation checks are separate
from host discovery, selection, and actual application. There is no certified
Codex-version compatibility matrix; see the [critical audit](audit-2026-10-22.md)
and [activation compatibility](activation-compatibility.md).

## Check or remove

On Windows, run `Install.cmd status` or `Install.cmd uninstall`. On other systems:

```sh
python3 scripts/install_suite.py status
python3 scripts/install_suite.py uninstall
```

Uninstall restores preexisting skill files and removes only the managed activation rule. It preserves user text added outside that rule and refuses to overwrite customized installed files. Interrupted operations retain a recovery journal. Run `Install.cmd recover` on Windows or `python3 scripts/install_suite.py recover` with the same profile to restore the pre-operation state, then retry. Recovery refuses to replace later user edits. If a force-killed installer left a lock, confirm no installer is running before removing only the stale `pm-essential-skills/install.lock`; keep the receipt and journal. See [recovery details](../skills/ibbuilds-pm-context-management/references/automatic-activation.md#recovery-and-checks).

Status also inspects the base user configuration for disabled installed skills and an explicit `skills.include_instructions` setting. To include a named Codex profile, use `python3 scripts/install_suite.py status --profile NAME` (add `--codex-home PATH` for a different home). This reads `config.toml` and `NAME.config.toml`; it changes neither. Python 3.10 still installs normally but reports TOML diagnostics unavailable; Python 3.11+ supplies the standard-library parser. Session overrides and actual activation remain unknown, and configuration warnings do not change the file-integrity exit code. See [source-backed activation compatibility and diagnostic limits](activation-compatibility.md).

Optional copy diagnostics (Python installer only):

```sh
python3 scripts/install_suite.py status --check-skill-root ~/.agents/skills
```

Repeat `--check-skill-root PATH` for other skills directories you want checked. This read-only check looks only for `<installed-name>/SKILL.md` in the managed installation and supplied roots, reporting resolved candidate paths, possible duplicates, and inspection errors. Symlink aliases of the same path count once. It does not search recursively, inspect other skills, change files, or affect status's exit code. [Codex's skill-loading documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) says same-name skills are not merged and both can appear. Distinct candidate files do not prove both are active; no duplicates found does not prove discovery or complete coverage. Activation remains unknown. Normal status checks remain unchanged without this option.

`CODEX_HOME` selects a profile for either installer. Advanced options belong to the Python installer, not `Install.cmd`: for example, `python3 scripts/install_suite.py install --skill ibbuilds-pm-source-selection --codex-home PATH`. Use `python` or `py -3` on Windows with a suitable Python runtime. In a full source download, `--skill NAME` selects any folder name in the [skill catalog](../README.md#the-seven-skills); repeat it for a subset. For example, `--skill ibbuilds-pm-concise-communication` installs only the reply skill; installing another later keeps the first. Repeating installation updates unchanged managed files without duplicating guidance.

## Stronger automatic reminders

For local Codex hosts supporting hooks, run `python3 scripts/install_suite.py install --hooks` (Windows: `py -3 scripts/install_suite.py install --hooks` with Python 3.10+). `Install.cmd` accepts only `install`, `status`, `uninstall`, or `recover`, not extra options. This registers compact reminders on session start and user prompt submission. Existing hook definitions are preserved. **Codex still requires review and trust before these reminders run.** Registration is reported separately from trust and live invocation.

Reminders make no model calls, read no stored transcripts, write no per-turn project state, and make no tool-approval decisions. They route only from installed-skill metadata; prompt contents never become instructions. The host input envelope includes the prompt: malformed or over-16-MiB envelopes deliberately receive no reminder. Reminder text still adds model-input context, so hooks are optional, not a guaranteed saving. Ordinary skills and the user-level rule remain useful without them. See [automatic activation and recovery](../skills/ibbuilds-pm-context-management/references/automatic-activation.md).
