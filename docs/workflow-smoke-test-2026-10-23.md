# Workflow smoke test: 2026-10-23

## Question and task

Can supplied skills help complete an already-authorized, fully specified task without making the user repeat context or perform setup? Two fresh Codex tasks proposed status-documentation changes for these actual repositories. Both received the same source snapshots and evidence. The second additionally received PM Concise Communication and SWE Software Verification bodies. These were explicitly supplied, not automatically selected.

The acceptance checks were: an applicable minimal patch for both READMEs; normal installation and independent use preserved; no invented test/publication/usage result; no claim of suite superiority or uselessness; and unvalidated user experience clearly distinguished from observed maintenance.

## Observations

- Both returned applicable unified diffs. `git apply --check --verbose` passed against the supplied snapshots.
- Neither asked the user a question, requested setup, or required another user message to produce the artifact.
- The baseline sent one unnecessary intent-only preamble; the supplied-skill task did not. Both final completion notes contained 27 whitespace-separated words, excluding the requested diff. This is a communication observation, not token measurement.
- Both preserved the substantive evidence and installation instructions. The supplied-skill patch included a direct PR reference and was selected for application.
- Neither exposed supported complete-task usage. No token delta, efficiency percentage, or elapsed-time advantage is established.

## Interpretation and limits

This is one-turn artifact preparation with rich supplied context, not an end-to-end user journey. There was no observed question/setup burden in either arm, so it cannot show a reduction in those costs. It did not exercise ambiguous requests, interruptions, repeated failures, context handoffs, source discovery, or automatic skill selection. Native global skill exposure and effective model/effort were not independently isolated. One pair does not establish causality or broad quality parity.

The earlier code-review pair also found the same two PM defects in both arms. Neither comparison proves the suites achieve their main goals: lower complete-task token use and less user effort at preserved quality. Small smoke checks must not substitute for representative multi-step workflow evaluation. Preserve negative and inconclusive results rather than relabeling them as success.

A future evaluation needs observable task completion, preserved constraints, avoidable user questions, repeated explanations, unnecessary work, recovery/rework, and complete comparable usage including the skills' own overhead. Missing telemetry remains unknown. Do not launch more model runs simply to obtain a favorable result.
