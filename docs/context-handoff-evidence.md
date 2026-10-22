# Context handoffs: evidence and decision policy

Reviewed 22 October 2026. The objective is less total work at the same quality,
not the shortest possible thread or the largest number of warnings.

## What the research supports

- [OpenAI's current best practices](https://learn.chatgpt.com/guides/best-practices)
  favor a coherent unit of work per chat and retaining the same chat when that
  preserves useful reasoning. This is guidance, not a numerical cost threshold.
- [Claude Code's cost guidance](https://code.claude.com/docs/en/costs) distinguishes
  repeated context, cache misses and background requests. It recommends clearing
  unrelated work and using native compaction. A visible message count does not
  measure any of these costs.
- [Anthropic's cost experiments](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)
  report different results for short and long triage runs. Context editing made
  the short run more expensive; pruning and compaction helped the longer run.
  These are small, provider-specific billing experiments, not Codex allowance
  measurements or proof that frequent new chats save tokens.
- [CliffCompaction, September 2026](https://arxiv.org/html/2609.26779v1) tests
  absolute context budgets and a specialized truncation method. Very small
  budgets harm some results, and summarization can cost more than full context.
  Its results do not establish a fresh-thread restart percentage.
- [Parallel Context Compaction, May 2026](https://arxiv.org/html/2605.23296v1)
  measures QA/dialogue serving, not coding handoffs. Frequent summarization can
  dominate latency; using 75% of a window in one experiment does not establish
  that percentage as optimal.
- [AutoCompact, October 2026](https://arxiv.org/html/2610.02163v1) studies a trained
  coding/compaction policy. Its results cannot be assumed for ordinary prompted
  skills without that training.

None of these sources establishes a universal message count, occupancy percentage
or user-interruption threshold that minimizes total usage without quality loss.
Native compaction, context editing and a fresh-thread handoff are different
operations. Prefer a suitable existing host feature over adding another mechanism.

## Operational meaning of “too much”

At useful checkpoints, reuse observations already available: sizeable resolved
logs, superseded decisions, completed investigations, current constraints and the
next requested work. Assess whether a short accurate brief can replace substantial
history without losing needed detail. Do not fetch old transcripts or make a model
call solely to score a thread. Keep routine assessment quiet; tell the user only
when there is an actionable recommendation, material risk or necessary choice.

When comparable costs are available, compare the same remaining requested work:

- Continue: future input and output in this thread, including applicable ongoing
  context overhead and native compaction when actually accounted for.
- Handoff: summary/transfer, destination startup, reconstruction, **and execution
  of the remaining work in the destination**. Do not double-count components.

Omitting destination execution creates a misleadingly cheap alternative. Unknown
components remain unknown. A partial lower bound can disprove a saving when it
already exceeds continuing, but cannot prove a saving when it is smaller.
Estimates must remain labeled estimates; a small difference within their
uncertainty is not a convincing reason to interrupt. Token volume, cached-token
billing and subscription allowance are not interchangeable.

Without comparable numbers, use concrete replaceable-history evidence and
handoff readiness, not invented savings. Large outputs can warrant assessment
earlier than many short exchanges. Near completion, or when reconstruction would
repeat the investigation, staying may be better. A vague goal label is not the
decision criterion.

## Implementation and limits

The [skill's policy](../skills/ibbuilds-pm-context-management/references/policy.md) owns the
actual decision rules. Existing numerical defaults remain tunable compatibility
backstops, not research-proven economic optima. Neither a message-count cap nor
a percentage alone establishes savings.

Substantial replaceable history already supports earlier review without waiting
for those backstops. Complete favorable cost evidence can support early review;
known nonbeneficial costs or repeated reconstruction should not cause a new
pressure-only interruption. Existing human answers, pending questions, explicit
boundaries, critical policy, authorization and transfer readiness retain their
documented precedence. The helper validates observations, not their factual truth.

Local regressions establish routing behavior only. No live user-host evaluation,
quality-equivalence result, measured saving or automatic host activation is claimed.
