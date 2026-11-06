---
name: pm-essential-skills-workspace-hygiene
description: Use when work creates backups, captures, exports or temporary artifacts, when project storage grows unexpectedly, or when completed work leaves generated files to retire.
---

# PM Essential Skills / Workspace Hygiene

Keep useful deliverables and recovery material while bounding the files produced by agent work. Apply during the active task without waiting for a cleanup request. This skill works independently and installs no monitor or schedule.

## Prevent accumulation

Use the project's established scratch/output directories. Give each temporary artifact an owner and a purpose; reuse a suitable existing result instead of creating another copy. A small edit producing no temporary artifacts needs no inventory, helper or cleanup report.

Before a bulk download, capture, export or backup, identify the destination and expected growth. Keep scratch separate from deliverables. Prefer version control or a scoped recovery copy for the changed material when adequate. A full-project backup needs a concrete recovery reason, bounded contents and a retirement condition. Put it outside the source being copied; exclude earlier backups, dependencies and reproducible outputs unless recovery specifically needs them. A backup must never contain itself or multiply previous backups.

## Inspect an actual growth risk

At the first relevant artifact-producing task without current size evidence, on unexpected growth, and after a bulk operation, reuse an existing inventory or make one bounded inspection. Recheck only changed areas while the evidence remains applicable. Do not rescan the whole project every turn.

Use native filesystem tools, or run `python scripts/inventory_workspace.py PROJECT --top 10` from this skill's folder. On Windows a supported launcher such as `py -3.11` can replace `python`. The standard-library helper reads directory metadata only, skips observed links/reparse points, writes nothing and never deletes files. Concurrent tree changes can invalidate this non-atomic inventory. It reports logical file bytes, not physical allocation or guaranteed reclaimable space. Exit 1 means incomplete coverage; inspect `limits`, `error_count` and `skipped_links` before claiming a full inventory. Adjust `--max-entries` or `--max-seconds` only when the missing coverage matters.

Identify which large paths belong to current work, retained recovery, user data, dependencies or unknown owners. Names, age, size, Git ignore status and apparent duplicates are clues, not deletion authority. Preserve `.git`, user edits, databases, credentials, source assets and active work unless their specific removal is authorized. A partial scan cannot establish that the rest is clean.

## Retire known temporary work

Remove task-owned, regenerable scratch when it is no longer needed and cleanup is within existing authority. Reuse explicit project retention/count/size limits; do not invent a universal expiry or silently discard a needed recovery point. Unknown or shared candidates remain intact with a concise explanation of their size and uncertainty. Ask only for the specific unresolved destructive choice when necessary, while continuing safe work.

Before removal, resolve each exact target inside the intended workspace and check for links, junctions and concurrent changes. Use native literal-path operations; never run a broad wildcard wipe, `git clean`, or a shell pipeline that reconstructs deletion commands. Moving files into another folder on the same disk does not reclaim space.

After cleanup, verify the selected paths and required deliverables/recovery material. Report material growth, what was retained/removed, measured bytes where available and remaining uncertain candidates. Stop when the task's generated material has a useful destination and lifecycle; a clean project may need no action.
