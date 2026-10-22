# Concise communication design

The skill responds to the product requirement for brief, specific, plain-language
replies across domains. It reduces unnecessary generation at composition time,
not through a second compression pass or a host-specific display layer.

The [community stretchtext report](https://www.reddit.com/r/ClaudeCode/comments/1x688sx/turning_a_crazy_idea_from_1967_into_a_claude_code/)
and its [public implementation](https://github.com/pro-vi/cc-stretch), checked
2026-10-22, distinguish collapsed text from the full generated reply. The author's
reported 83% reduction concerns initially visible words in their sample, not
verified token or subscription savings for this suite. That mechanism depends on
specific renderers and may conceal details until expanded.

We adopt a concise default, not the plugin or its measured percentage. Essential
information remains visible; explicit depth requests and complete artifacts take
precedence. There is no expansion widget, mandatory follow-up offer, second model,
extra tool call, or assumption that omitted content was read. Semantic cases cover
ordinary answers, truthful status, blockers, requested depth, and full artifacts.

The four new capability owners complete previously unassigned PM responsibilities:
Task Coordination owns the whole accepted outcome; Resource Selection owns
available execution choices; Workflow Improvement owns selective toolkit and
knowledge maintenance; Concise Communication owns how results are conveyed.
The [scope coverage map](pm-scope-coverage.md) records their boundaries rather than
treating the number of existing skills as the product scope.
