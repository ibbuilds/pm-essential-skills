# Recovery, retention and inventory limits

Read the relevant section when a candidate's recovery, current use or observed size is uncertain. These checks classify the work; they do not grant permission to delete it.

## Verify what recovery actually preserves

A repository is a recovery mechanism for content it contains in a usable version, not a backup of everything beside it. Tracked files can have uncommitted edits; ignored or untracked files may be the only copy of user work. A clean-looking status or a `.git` directory alone is insufficient. Use supported, scoped version/status/content checks when the decision depends on recovery. Do not create commits, stashes, new Git settings or copied projects just to justify deletion.

Prefer an existing verified recovery source for versioned code. Where a real gap needs protection before an authorized change, copy only the necessary material and identify when that copy becomes dispensable. A full-project snapshot needs a concrete reason the scoped alternative cannot satisfy. Keep it outside its input and exclude prior backups, caches and reproducible outputs unless that recovery specifically requires them.

An archive's existence alone does not prove it contains the version needed. Check the relevant contents or recovery evidence proportionately to the risk. Retire temporary recovery copies after the protected risk has passed and the intended result is verified, unless an actual retention requirement still applies. No default expiry, backup count or mandatory backup manifest is introduced.

## Classify by purpose and consumers

| Candidate | Decision basis |
| --- | --- |
| Superseded task-owned renders, captures or intermediate exports | Retire when a verified replacement exists and no active consumer needs the intermediate. Reuse task-owned scratch destinations where suitable; avoid retaining every attempt. |
| Final deliverables, requested variants and required editable source | Retain for the accepted purpose. A newer file does not make an explicitly requested alternative disposable. |
| Uncommitted/untracked user data, databases or unique local assets | Preserve unless their specific disposal is authorized. Being ignored by Git does not make them reproducible. |
| Build outputs, caches and dependencies | Establish reproducibility from available inputs and tooling, current use and regeneration cost. Preserve active/offline needs; clear only within scope and for a demonstrated purpose, not every turn or task. |
| Legacy source, data or compatibility assets | Check current consumers, supported versions and recovery/rollback needs. Retirement of functionality is its own approved change, not a disk-cleanup assumption. |
| Shared or unknown backups | Resolve ownership, necessity and authority. A suggestive name, age or duplicate-looking bytes do not establish disposal safety. Continue authorized cleanup of unrelated known scratch. |

Record only the relevant decision in current context or existing project records when persistence is useful. Do not turn cleanup into another memory database. Moving unknown material to a same-volume quarantine retains its storage; name/location changes are not reclaimed space.

## Inventory limits

The optional `scripts/inventory_workspace.py` reads metadata only. It returns logical bytes by path, bounded largest entries, counts, `limits`, `error_count` and `skipped_links`. Review skipped special entries where material too. Exit 1 indicates limited or failed coverage; exit 2 indicates an invalid/unreadable request. Increase its limits only when missing coverage matters to the actual question.

Even a completed traversal excludes skipped link targets. Hard-linked files are counted per path; logical totals do not establish physical allocation or bytes that deletion would reclaim. The scan is non-atomic: concurrent changes can invalidate observations. Recheck exact selected paths, links and active writers before removal instead of treating a size ranking as deletion advice.
