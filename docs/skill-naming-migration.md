# Skill identity and migration

Canonical folder, frontmatter and display names use `repo-name-skill-name`:
`pm-essential-skills-<skill-slug>`. There are no alias folders. Both previous naming
generations map to the same canonical names:

| Original name | Previous prefixed name | Canonical name |
| --- | --- | --- |
| `concise-communication` | `ibbuilds-pm-concise-communication` | `pm-essential-skills-concise-communication` |
| `context-management` | `ibbuilds-pm-context-management` | `pm-essential-skills-context-management` |
| `execution-efficiency` | `ibbuilds-pm-execution-efficiency` | `pm-essential-skills-execution-efficiency` |
| `resource-selection` | `ibbuilds-pm-resource-selection` | `pm-essential-skills-resource-selection` |
| `source-selection` | `ibbuilds-pm-source-selection` | `pm-essential-skills-source-selection` |
| `task-coordination` | `ibbuilds-pm-task-coordination` | `pm-essential-skills-task-coordination` |
| `workflow-improvement` | `ibbuilds-pm-workflow-improvement` | `pm-essential-skills-workflow-improvement` |

This is an identity change, not new authority or a behavior change. Each skill
remains independently installable through the normal skill manager or complete
folder copy. No new installer, hook, permission, or configuration is required.

## Regular skill installs

1. Locate the copies your host discovers, including user-wide and project-local
   locations. Back up the entire old folders **outside skill discovery roots**.
   Keep custom instructions, references and scripts, plus any disabled/suggest-only
   preferences and configuration before updating.
2. Compare your edits with the new complete skill folder and deliberately merge
   them. Keep its canonical directory/frontmatter name and new explicit invocation.
   Do not overwrite custom files blindly.
3. Before activating the replacement, update your own explicit invocations,
   path references and name/path-bound disabled settings to the canonical name.
   A disabled old name does not necessarily disable the new identity. Retain the
   same enabled/disabled choices; never treat a rename as renewed authorization.
4. Replace the old discovered copy with the reviewed canonical folder. Move the
   backed-up old copy outside discovery rather than leaving duplicate aliases.
   Reload the host and verify its catalog and opt-outs. Keep the backup until
   satisfied; file checks alone cannot prove model invocation.

Skill managers may retain the old identity when installing the new one. Review
that manager's installed list and remove only the old copy you have backed up.
The repository does not automatically alter or delete any existing installation.

## Optional legacy installer

The optional installer accepts only canonical names for new installs. It refuses
installation if its managed home contains old-name skill folders or an old-name
receipt, without changing their contents. Check other discovery roots separately.
Existing receipts and interrupted journals remain supported for read-only status,
explicit uninstall and recovery, including preservation of unrelated user files.

Back up the old folders, receipt, preferences and custom edits first. Use `status`
and, if necessary, `recover` with the same `CODEX_HOME`/`--codex-home`. An explicit
`uninstall` restores recorded originals only when managed files are unchanged;
customized installations are refused, not overwritten. If refused, preserve the
backup and reconcile the edits against the original installed release before
retrying—do not discard the receipt or journal to bypass safeguards. After
uninstall, move any restored old-name folders outside discovery deliberately,
merge customizations and preserve opt-outs as above, then install the replacement
using your preferred normal skill workflow or the optional installer. The latter
still selects its disclosed guidance/scope only when explicitly chosen.
