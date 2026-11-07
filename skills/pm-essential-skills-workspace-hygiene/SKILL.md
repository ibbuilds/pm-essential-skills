---
name: pm-essential-skills-workspace-hygiene
description: "Use during work that creates backups, captures, exports or temporary artifacts, when storage grows unexpectedly, or when retiring superseded files. Small edits generating no files need no scan."
---

# PM Essential Skills / Workspace Hygiene

Keep the workspace limited to useful work, deliverables and justified recovery material. Prevent accumulation during the active task instead of waiting for a cleanup request. This skill installs no monitor or schedule.

## Prevent unnecessary copies

Use established scratch/output directories. Give generated material a purpose, owner and retirement condition; reuse a suitable existing result. As iterations succeed, retire superseded task-owned intermediates after their replacement is verified and consumers no longer need them. Preserve requested variants and needed source material. No artifact manifest is required by default.

Prefer existing version control for recoverable versioned work. Check that it actually contains the needed content before relying on it: a repository does not preserve every uncommitted, untracked or ignored file. Do not create a full-project backup before ordinary edits or commit/stash user changes merely to make cleanup possible. A scoped copy is justified only for a real recovery gap within authority.

Before bulk capture, export, download or backup, identify destination, expected growth and any known capacity/retention limit. Use permitted batches and retire verified intermediates when needed to fit; otherwise pause that generation. Unrelated material is not disposable capacity. Do not invent universal size or age limits.

A full-project backup needs a concrete recovery reason, bounded contents and a retirement condition. Place it outside its source; exclude earlier backups, dependencies and reproducible output unless recovery specifically requires them. Never nest a backup in itself or multiply prior backups.

## Inspect the relevant growth

Reuse current size evidence or inspect the affected destination for bulk/uncertain growth, unexpected growth and after bulk work. Broaden only for unresolved growth or the requested coverage; recheck changed areas while evidence remains applicable. A single small output of known size needs no project inventory or cleanup report.

Use native tools or the optional read-only helper: `python scripts/inventory_workspace.py PROJECT --top 10` from this skill's folder; on Windows, `py -3.11` can replace `python`. It skips observed links/reparse points, writes nothing and never deletes files. It reports logical bytes, not guaranteed reclaimable disk space. Exit 1 means incomplete coverage; inspect limits, errors and skipped links before claiming completeness.

Classify candidates by current use, ownership and recoverability: active work, required deliverables/recovery, unique user data, reproducible artifacts/caches or uncertain legacy material. Names, age, size, ignore rules and apparent duplicates do not establish deletion safety. Ignoring a directory does not free its disk space.

Check consumers and supported versions before treating legacy material as obsolete. Retiring product functionality requires its own accepted scope, not a storage-cleanup shortcut. Preserve `.git`, user edits, databases, credentials, source assets and active/shared work unless their specific removal is authorized. Read [recovery and retention](references/recovery-and-retention.md) when recovery, legacy use or inventory limits are uncertain.

## Retire what is demonstrably dispensable

Remove unneeded task-owned, regenerable scratch within existing authority, during work and at completion. Reuse explicit retention requirements and preserve still-needed recovery points. Consider regeneration needs before clearing useful caches or dependencies; do not clear them reflexively. Keep unknown/shared candidates intact, explain the specific uncertainty and ask only the necessary destructive choice while continuing safe work.

Before removal, resolve each exact target inside the intended workspace or explicitly authorized destination; check links, junctions and concurrent changes. Use native literal-path operations. Never use a broad wildcard wipe, `git clean`, or a shell pipeline that reconstructs deletion commands. Relocating material on the same volume does not reclaim its storage.

Verify selected removals and surviving deliverables, source and recovery material. Report material growth, removals/retentions, measured logical bytes when available and remaining coverage/ownership limits. Do not label partial coverage a clean workspace or logical totals physical space recovered. Stop when retained material has a justified purpose and lifecycle.
