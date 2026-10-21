# Project context index

- Management: enabled / disabled
- Project ID and host (when exposed):
- Confirmed project root or workspace identity:
- Standing activation: source user instruction reference and authorized scope
- Persistent discovery rule location (if installed):
- User routing preferences:
- Current request ID (host-provided or labeled local), answer and choice-request ID, last actually prompted request ID, pending-choice status, and known count of stay answers. Keep only current state; a stay is request-scoped unless explicitly persistent.
- Assessment settings, if explicitly configured: mode (notify-and-transfer / suggest-only / stay), review_ratio, rollover_ratio. Defaults: notify-and-transfer, 0.75, 0.85.
- Standalone setup status/reference, if this project was created from a chat:

## Current outcomes

| Outcome | Status | Active thread ID if known | Latest handoff ID/path | Superseded source |
| --- | --- | --- | --- | --- |

Keep only current outcomes and routing needed to find their owners. Link existing project records for completed work instead of growing this table into a transcript.

When a material resolved question would otherwise need repeated investigation, keep a concise finding with its evidence/version and invalidation condition in existing notes. Update only changed findings; no per-turn logs or extra database.

## Latest assessment per active thread

Record the observation source, fresh current-context occupancy when known, observed counters when known, decision reason, last pressure notice actually shown (none / review / rollover), initial catch-up assessment status, and any deferred transfer. Missing data is unknown. Historical usage is not current occupancy.

## Pending transfer, if any

- Handoff ID and brief path:
- Source thread:
- Source recovery route/map and destination access evidence:
- Confirmed source archive state and any temporary-recovery receipt (`rearchive_pending`, original state, target/host, owner):
- Lifecycle: prepared / destination-confirmed / superseded
- Destination thread ID and readiness evidence (unknown until confirmed):
- Recovery action, if needed:
- Transfer journal path and latest revision, when available:

This file records operational state. It does not grant user authorization. Keep it concise, omit credentials and transcripts, and preserve the user's original scope.
