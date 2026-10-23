# Freshness-aware reuse

Read when deciding whether previously retrieved content can support the current task. No persistent cache, collection scan, or content database is needed. Reuse known facts in working context; the optional `scripts/assess_source.py` makes ambiguous decisions repeatable without fetching anything itself.

The helper takes JSON through stdin or `--input`:

```json
{
  "source_id": "stable-document-or-file-identity",
  "loaded_source_id": "stable-document-or-file-identity",
  "content_available": true,
  "coverage_sufficient": true,
  "freshness_required": true,
  "loaded_revision": "v1",
  "current_revision": "v1",
  "revision_verified": true,
  "access": "available"
}
```

Use actual IDs, revisions, hashes, ETags, or version markers when available. `revision_verified` means the current marker was established through a supported fresh read or trusted change information, not copied from the old record. Equivalent revision labels on different sources do not establish identity. A modification time is a hint; it is not a content fingerprint unless the source system guarantees its meaning.

| Action | Meaning |
| --- | --- |
| `reuse` | Available matching content covers the task, with required freshness established or legitimately unnecessary. |
| `verify` | A current fact needs revalidation. Prefer a lightweight revision check before reloading the whole source. |
| `fetch` | Content/identity/coverage is missing, a required full read is incomplete, or the verified revision changed. Fetch only the sufficient unit unless full coverage is required. |
| `skip` | Source is not needed for this task and no full-read requirement applies. |
| `blocked` | Access is denied. Do not retry repeatedly or treat the denial as a negative finding. |

`needed` defaults to true; other booleans default to false. `required_full_read: true` overrides an attempted `needed: false` optimization. Set `full_read_complete` only for the current relevant source version. A known changed revision requires a fresh read even when the old version was previously reviewed completely.

Use `known_immutable: true` only when the identity denotes an immutable source/version. New drafts, live project files, and a convenient old timestamp do not establish immutability. If a historical version is the intended authority, identify that version explicitly rather than claim it is current.

Unchanged bytes and provenance establish identity, not continued applicability: an immutable approved April plan may be superseded by an accepted May decision. When a known relevant update changes the governing evidence, invalidate dependent conclusions and reassess only affected claims; no universal supersession scan is needed. The April plan remains appropriate for a question about April. Fresh facts never override explicit user permissions or preferences.

The helper validates declared observations, not their truth. It does not hash files, obtain permissions, or infer token savings. Do not call it for every source when the reuse decision is already obvious.

For local UTF-8 sources, the optional [bounded reader](bounded-reading.md) performs a current content-hash check and emits only missing, bounded coverage. It uses the same assessment logic without a persistent cache. For remote sources, use their existing tool's revision/range support; this helper cannot intercept or cache arbitrary connectors.
