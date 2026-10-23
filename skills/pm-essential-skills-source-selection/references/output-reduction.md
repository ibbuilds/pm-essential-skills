# Safe tool-output reduction

When a command or tool would return a large result, use its existing structured output, field selection, or a deterministic filter before returning text to the model. Summarizing an already-ingested dump does not avoid that ingestion. No new hook, wrapper, or dependency is required.

Keep the original producer's exit status separate from filter status. Preserve relevant totals (including failures/skips when supplied), the selected scope, and whether output was truncated or paginated. Do not invent unavailable counts. Retain a supported run ID or accessible raw-log path for recovery; use an existing artifact where available, or a task-scoped temporary capture when necessary and authorized. Avoid collecting unrelated sensitive output.

For example, a test command can exit nonzero before printing any line matching a failure regex. Report its actual status and inspect the raw diagnostic, rather than treating zero matches as a pass. A successful final `head` or parser does not establish that the producer succeeded; a pipeline may also interrupt the producer. Prefer the tool's structured result or explicit status capture, not a blind `command | grep | head` recipe.

Filtering selects evidence; it does not establish exhaustive coverage. If a requested full review, unexpected status, missing totals, or unexplained empty result leaves a material gap, retrieve the needed raw context or remaining pages. If raw recovery is unavailable, disclose that limit rather than claiming complete verification. Do not rerun an externally mutating command merely to recover output.

### Optional command capture

For one **already-authorized, noninteractive foreground command** whose native tool cannot bound output while retaining raw logs, `scripts/capture_command.py` runs its argv once with `shell=False`. It streams stdout/stderr directly to separate files, then returns a compact JSON head/tail preview and SHA-256 hashes. Prefer native structured results; short output usually costs **more** with this envelope. Opt in only for expected noisy output, not every command; this is not a required wrapper or permission check.

```sh
# Use an existing, authorized task-scoped directory; argv follows --.
python /path/to/pm-essential-skills-source-selection/scripts/capture_command.py \
  --output-dir /existing/task/artifacts --preview-bytes 1024 -- \
  python -m unittest discover -s tests
```

The helper inherits cwd, environment, and stdin. It creates a fresh private `capture-*` subdirectory with `stdout.bin`, `stderr.bin`, and `summary.json`; no output files are overwritten and no command is retried. The JSON includes actual signed `exit_code` (negative for a POSIX signal), each raw path/byte count/hash, selected preview byte count, and truncation. The helper exits with the producer code, or `128 + signal` for signal termination. Invalid options, launch failures, and capture failures are errors, not empty successful results; a capture error after a failed producer retains its nonzero exit. `status: completed` means the producer terminated, **not** that it succeeded. A launch error has no producer exit code.

`--preview-bytes` is a per-stream raw byte budget, default 1,024, maximum 65,536; zero returns metadata only. Long streams use head and tail, potentially omitting the decisive middle diagnostic. UTF-8 decoding replaces invalid/split characters only in previews; raw bytes remain intact. JSON escaping and metadata add overhead, so this is not a token budget or proof of token savings. Hashing reads fixed-size chunks; raw artifact disk use is unbounded. Inspect raw files with suitable bounded/binary tools when the status, truncation, or requested coverage requires it. Keep them until recovery is no longer needed; cleanup is the caller's responsibility.

This helper does **not** redact secrets, interpret test totals, order interleaved stdout/stderr, sandbox commands, or manage timeouts/background descendants. Raw artifacts may contain sensitive data. Use existing host cancellation/process controls and storage limits. Do not use it for daemons or commands that leave writers running after the foreground process exits: hashes describe only the bytes inspected. Do not run a command solely to summarize an existing artifact, or rerun a mutation to recover its output. An interruption may leave raw files without a summary; inspect the retained directory and producer state before any retry.
