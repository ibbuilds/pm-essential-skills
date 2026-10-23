# Codex activation compatibility

Reviewed October 22, 2026 against stable Codex **0.163.0** (October 15).
These are source-backed compatibility findings, not observed model invocation.
No model benchmark or subscription-funded test is required for installer status.

## Discovery and global instructions

The installer keeps its existing `$CODEX_HOME/skills` destination. Stable Codex
explicitly discovers that deprecated, backward-compatible user root alongside
`$HOME/.agents/skills`. Moving or duplicating an installation is not necessary.
The [stable root resolver][roots] establishes this more precisely than the
[current authoring-path documentation][skills-doc]. Different same-name copies
can coexist; installer copy diagnostics inspect only explicitly supplied roots.

The [global instruction provider][global] reads the first nonempty
`AGENTS.override.md`, otherwise `AGENTS.md`, from Codex home. It reads the full
file. The [repository loader][project] applies `project_doc_max_bytes` to
repository instruction discovery; the [instruction manager][manager] combines
global instructions afterward. Do not interpret the default 32 KiB repository
budget as a demonstrated truncation limit on the suite's global pointer block.
Host/session behavior beyond this reviewed implementation remains unverified.

## What status checks

`python scripts/install_suite.py status --codex-home PATH` includes informational
`configuration_diagnostics`. Add `--profile NAME` to inspect `NAME.config.toml`
after `config.toml`, matching [modern Codex profiles][profiles]. Names follow
[upstream validation][profile-name]: nonempty ASCII letters, digits, underscores,
and hyphens. Legacy `[profiles.NAME]` tables are not merged as modern profiles.

The diagnostic reads only these user files, never writes configuration, and never
prints raw contents or parser exceptions. Linked, nonregular, unreadable,
malformed, or over-1-MiB files produce an incomplete result instead of a guessed
configuration. Python 3.10 installation remains supported; TOML diagnostics are
`unavailable` without Python 3.11+'s standard-library `tomllib`. No fallback parser
or dependency is installed.

[Native enablement rules][rules] select a canonical `SKILL.md` path or exact skill
name (trimmed), not both. Later matching rules override earlier rules, including
across the base and selected-profile User layers. Relative paths resolve against
the configuration directory. For example:

```toml
# config.toml: disable by name, then re-enable one specific installed copy.
[[skills.config]]
name = "pm-essential-skills-source-selection"
enabled = false

[[skills.config]]
path = "/absolute/codex-home/skills/pm-essential-skills-source-selection/SKILL.md"
enabled = true
```

A later selected profile can disable that name again. Session flags can override
these user rules. The native rule resolver considers User and SessionFlags layers,
not project layers. Status does **not** inspect session flags, running application
state, custom-agent configuration, or other host-provided configuration. It does
not infer which profile a running session selected.

Important JSON fields:

- `status`: `inspected`, `partial`, or `unavailable`.
- `files`: requested file paths and their inspection states. A missing file means
  no observed settings in that layer, not proof of active defaults in a session.
- `configured_disabled_skills`: receipt-installed names disabled after applying
  successfully interpreted user layers, in suite order.
- `include_instructions`: explicit user-layer value, or `null` when not observed.
- `user_layer_resolution_complete`: false when the requested inspection could not
  be fully interpreted; reported values may then be overridden by unresolved data.
- `effective_activation`: always `unknown`; `session_overrides`: `not_inspected`.
- `warnings` and `next_steps`: informational guidance, never automatic repairs.

Configuration warnings do not change status's integrity-based exit code. Missing
or modified managed installation files still produce the existing degraded status.

## Opt-outs versus pointers and reminders

`skills.include_instructions=false` suppresses the automatic skills instructions
block. `skills.bundled.enabled=false` concerns bundled system skills, not this
suite. Neither setting proves that all references to these files disappear.

The suite's managed global instructions and optional hook reminders explicitly
reference skill files. Native catalog disablement is **not a filesystem access
control** and cannot guarantee that an agent will never read a referenced file
through a general file-reading tool. Status warns about this ambiguity; it does
not rewrite intentional opt-outs, remove global guidance, or alter hook policy
based on incomplete session context. Review intentional opt-outs alongside those
pointers and reminders. Actual discovery, dispatch, selection, and adherence in
a particular session remain separate, unverified outcomes.

[roots]: https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/ext/skills/src/host_roots.rs
[skills-doc]: https://learn.chatgpt.com/docs/build-skills
[global]: https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/codex-home/src/instructions/mod.rs
[project]: https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/core/src/agents_md.rs
[manager]: https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/core/src/agents_md_manager.rs
[profiles]: https://learn.chatgpt.com/docs/config-file/config-advanced#profiles
[profile-name]: https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/protocol/src/config_types.rs
[rules]: https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/config/src/skills_config.rs
