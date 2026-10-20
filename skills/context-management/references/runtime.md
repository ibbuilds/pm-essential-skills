# Runtime readiness and recoverable transfers

Read on activation, material capability changes, or an actual transfer. Ordinary unchanged work requires no helper calls. These helpers have no account access and never perform a host operation; supplied observations are not authorization grants.

## Readiness

`scripts/preflight.py` reads JSON through stdin or `--input`. Supply verified observations from supported host tools and known skill locations. Missing/unknown flags do not count as success. Cache facts during the session instead of repeating discovery.

```json
{
  "membership": "project",
  "project_id": "actual-project-id",
  "source_thread_id": "actual-source-thread-id",
  "current_skill_available": true,
  "destination_skill_available": true,
  "create_thread_available": true,
  "reconcile_thread_available": true,
  "authorization_verified": true,
  "execution_mode_allows_transfer": true,
  "safe_checkpoint": true,
  "references_accessible": true,
  "settings_preserved": true
}
```

Verify destination skill availability from the same project's installed skill path or a verified personal installation on the target host. Do not assume that a skill mentioned in a prompt is installed. Preserve exact host/project identity and settings; if they cannot be established, readiness is degraded.

`transfer_ready` means the supplied gates passed, not that the script independently discovered or authorized them. Report unsupported capabilities once, with the manual fallback; never claim full automatic management is active when gates are missing. For standalone setup, flags `create_project_available`, `move_chat_available`, `verify_membership_available`, `setup_consent_verified`, and `chosen_project_name` distinguish unsupported, consent/name requirements, and readiness. They do not perform creation.

## Transfer journal

With Python 3.10+ available, use `scripts/transfer_state.py` for actual transfers. Write one journal beside its immutable brief, e.g. `.pm-context/handoffs/task-001.state.json`. Reference that journal from the small project index. Do not start a second journal for the same pending transfer to bypass an uncertain result.

Every command takes `--state PATH --event EVENT`; mutations after preparation require `--expected-revision N`. Event data comes from stdin or `--input PATH`, avoiding shell quoting and secret-bearing arguments. Output is a compact summary with ownership, revision, attempts, and brief size. A failure exits 2; stop the associated host action when the journal command fails.

| Event | Required observation/data | Next step |
| --- | --- | --- |
| `prepare` | Unique `handoff_id`, verified `project_id`, `source_thread_id`, and UTF-8 `brief_path` | Records fingerprint and prepared state; never overwrites an existing journal. |
| `request` | True gates: `authorization_verified`, `project_verified`, `destination_skill_available`, `references_accessible`, `settings_preserved`, `safe_checkpoint`, `execution_mode_allows_transfer` | Saves requesting state **before** calling the host create tool. Pause source implementation. |
| `unknown` | Empty object after lost/ambiguous creation result | Preserve uncertain state; reconcile through the host. No blind retry. |
| `failed` | `definite_failure: true` from an authoritative host outcome | Source can remain usable; one resolved retry is permitted. |
| `absent` | `definitive_absence: true` after an uncertain result | Same bounded retry path. A missing item in a partial/eventually consistent listing is not proof of absence. |
| `confirm` | Actual `destination_thread_id`, `destination_ready: true`, matching `project_id` and `handoff_id` | Destination owns implementation immediately; source must stay paused even if index writing fails. |
| `supersede` | `routing_saved: true` after updating the project index | Complete source routing; finish the source turn. |
| `cancel` | Empty object, only before dispatch or after definite failure | Retain journal and restore/keep source ownership. Cannot cancel uncertain or confirmed creation into another writer. |
| `status` | No event data needed | Read current state after restart without mutating it. |

A retry requires `failure_resolved: true` with the other request gates. A maximum of two creation attempts per transfer prevents retry loops. After exhaustion, preserve useful source work and report the failure; do not silently generate another handoff ID for the same operation.

The journal uses an exclusive lock, expected revisions, a content fingerprint, and same-directory atomic replacement. Changed briefs cannot dispatch. Confirmation and superseding are idempotent for the same destination; an existing destination cannot be replaced. Events record only bounded lifecycle metadata, not transcripts or credentials. Retain the journal to recover after interruption. These checks coordinate clients that follow this protocol; they cannot stop an unrelated host process from writing project files.

An existing `.lock` fails closed. Do not remove it automatically: another writer may still be active. On a stale lock, establish that no writer is running and reconcile host state before an authorized cleanup. Corrupt journals and storage permission errors are reported without silently resetting transfer state. Atomic replacement protects against partial writes during process interruption; it is not a guarantee against all hardware/storage failures.

## Failure between journal and host calls

A crash after `request` but before a confirmed host result leaves no active implementation owner in the journal. Reconcile first, even if the create call might never have happened. The protocol deliberately favors preserving work over duplicate execution. If creation succeeded but confirmation could not be recorded, keep the known destination and repair this journal; do not create another successor or resume the source concurrently.

If Python/storage is unavailable, use the same lifecycle in existing project notes. Clearly label it as instruction-based fallback. Preserve the source, expose capability limitations, and avoid unsupported automatic transfers rather than bypass safeguards.
