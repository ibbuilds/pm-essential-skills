# Bounded local reads with revision-aware reuse

Use only when a local regular UTF-8 file needs a substantial or repeated read and this helper is available. Directories, devices, and named pipes are rejected; the byte limit is not a universal filesystem I/O deadline. Native read/search tools remain appropriate. Known answers need no tool; remote sources retain their native permissions, revision checks, and pagination. Do not create a persistent cache, install a server, or copy remote content merely to use this reader.

`scripts/read_source.py` takes JSON through stdin or `--input`. It reads a local snapshot, hashes its bytes, and emits only a bounded content page plus provenance. It creates no files. Example:

```json
{"path":"/actual/source.txt","start_line":20,"end_line":60,"max_chars":12000}
```

Paths must identify authorized task sources. Line bounds are one-based and inclusive, using physical LF-delimited lines like `rg` (not every Unicode line separator). CRLF is retained verbatim; bare CR, form feed, and Unicode separators remain content within a line. Character offsets and content hashes preserve the original decoded text and raw bytes respectively. Omitted bounds mean the entire file. `max_chars` limits emitted text characters, not tokens or JSON encoding overhead; default 12,000, maximum 100,000. Only UTF-8 text up to 16 MiB is supported. Use a streaming or format-specific reader for other files; a rejected read does not mean the source is absent.

The response supplies canonical `source_id`, a SHA-256 `revision`, `content` pieces, `coverage_spans`, `coverage_sufficient`, `full_read_complete`, and, for incomplete reads, `next_cursor`. Spans are zero-based character offsets `[start, end)` in decoded text. Long lines paginate without dropping characters. The hash describes the bytes read, not a guarantee that another process will not subsequently change the file.

For reuse, pass the previous source identity/revision/spans as `loaded_source_id`, `loaded_revision`, and `loaded_spans`, with `content_available: true` **only while the matching content is actually accessible in working context**. The helper rechecks the current hash. It returns `reuse` with no duplicate text for sufficient unchanged coverage, or emits only missing requested spans. Changed content, changed identity, or lost context invalidates reuse. A remembered hash without available content is not a cache hit.

For the next page, retain the same requested line bounds and pass `cursor: next_cursor`, `expected_revision: revision`, and all available matching coverage. The cursor cannot skip unread material. A revision change returns `restart` without content; restart coverage at the new version rather than combine pages from different versions. Reuse decisions still rely on truthful declarations of model-visible context.

`required_full_read: true` overrides narrowed line bounds. Continue until full coverage is established; do not claim a complete review from an incomplete page. `force_read: true` honors an explicit reread request despite available prior content. For a forced sequence, follow its pagination even when old content was complete. The response adds `reread_spans`, independent of old `coverage_spans`; carry these back on every forced continuation, along with the usual matching source/revision and available-content declarations. Only include coverage emitted during this forced pass. Starting without a cursor resets the forced-pass coverage. Older callers that pass a forced cursor without `reread_spans` must be updated; skipped prefixes now fail validation rather than using old coverage as proof of a reread. Stop only when the actual requested coverage is sufficient. No helper can certify that the assistant understood the source or included every material exception.

## Safe tool-output reduction

For output filtering and optional command capture, read [safe tool-output reduction](output-reduction.md).

### Optional command capture

See [optional command capture](output-reduction.md#optional-command-capture).
