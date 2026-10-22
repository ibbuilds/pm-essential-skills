# Bounded local reads with revision-aware reuse

Use only when a local UTF-8 file needs a substantial or repeated read and this helper is available. Native read/search tools remain appropriate. Known answers need no tool; remote sources retain their native permissions, revision checks, and pagination. Do not create a persistent cache, install a server, or copy remote content merely to use this reader.

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

When a command or tool would return a large result, use its existing structured output, field selection, or a deterministic filter before returning text to the model. Summarizing an already-ingested dump does not avoid that ingestion. No new hook, wrapper, or dependency is required.

Keep the original producer's exit status separate from filter status. Preserve relevant totals (including failures/skips when supplied), the selected scope, and whether output was truncated or paginated. Do not invent unavailable counts. Retain a supported run ID or accessible raw-log path for recovery; use an existing artifact where available, or a task-scoped temporary capture when necessary and authorized. Avoid collecting unrelated sensitive output.

For example, a test command can exit nonzero before printing any line matching a failure regex. Report its actual status and inspect the raw diagnostic, rather than treating zero matches as a pass. A successful final `head` or parser does not establish that the producer succeeded; a pipeline may also interrupt the producer. Prefer the tool's structured result or explicit status capture, not a blind `command | grep | head` recipe.

Filtering selects evidence; it does not establish exhaustive coverage. If a requested full review, unexpected status, missing totals, or unexplained empty result leaves a material gap, retrieve the needed raw context or remaining pages. If raw recovery is unavailable, disclose that limit rather than claiming complete verification. Do not rerun an externally mutating command merely to recover output.

### Optional command capture

For one **already-authorized, noninteractive foreground command** whose native tool cannot bound output while retaining raw logs, `scripts/capture_command.py` runs its argv once with `shell=False`. It streams stdout/stderr directly to separate files, then returns a compact JSON head/tail preview and SHA-256 hashes. Prefer native structured results; short output usually costs **more** with this envelope. Opt in only for expected noisy output, not every command; this is not a required wrapper or permission check.

```sh
# Use an existing, authorized task-scoped directory; argv follows --.
python /path/to/source-selection/scripts/capture_command.py \
  --output-dir /existing/task/artifacts --preview-bytes 1024 -- \
  python -m unittest discover -s tests
```

The helper inherits cwd, environment, and stdin. It creates a fresh private `capture-*` subdirectory with `stdout.bin`, `stderr.bin`, and `summary.json`; no output files are overwritten and no command is retried. The JSON includes actual signed `exit_code` (negative for a POSIX signal), each raw path/byte count/hash, selected preview byte count, and truncation. The helper exits with the producer code, or `128 + signal` for signal termination. Invalid options, launch failures, and capture failures are errors, not empty successful results; a capture error after a failed producer retains its nonzero exit. `status: completed` means the producer terminated, **not** that it succeeded. A launch error has no producer exit code.

`--preview-bytes` is a per-stream raw byte budget, default 1,024, maximum 65,536; zero returns metadata only. Long streams use head and tail, potentially omitting the decisive middle diagnostic. UTF-8 decoding replaces invalid/split characters only in previews; raw bytes remain intact. JSON escaping and metadata add overhead, so this is not a token budget or proof of token savings. Hashing reads fixed-size chunks; raw artifact disk use is unbounded. Inspect raw files with suitable bounded/binary tools when the status, truncation, or requested coverage requires it. Keep them until recovery is no longer needed; cleanup is the caller's responsibility.

This helper does **not** redact secrets, interpret test totals, order interleaved stdout/stderr, sandbox commands, or manage timeouts/background descendants. Raw artifacts may contain sensitive data. Use existing host cancellation/process controls and storage limits. Do not use it for daemons or commands that leave writers running after the foreground process exits: hashes describe only the bytes inspected. Do not run a command solely to summarize an existing artifact, or rerun a mutation to recover its output. An interruption may leave raw files without a summary; inspect the retained directory and producer state before any retry.
