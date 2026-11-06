# Concise Communication: first-reading clarity

The goal is the shortest useful answer the reader can understand on the first reading. Reducing character count by replacing explanations with acronyms or dense labels can create more questions. The skill now makes scope, common vocabulary, necessary meaning and readable format explicit, in any language. It preserves exact technical identifiers, uncertainty, requested depth, verbatim formats and complete artifacts.

## Sources and adaptation

Reviewed original sources on 6 November 2026:

| Source | Useful pattern | Adaptation |
| --- | --- | --- |
| [Anthropic internal-comms skill](https://github.com/anthropics/skills/blob/main/skills/internal-comms/SKILL.md), [FAQ guidance](https://github.com/anthropics/skills/blob/main/skills/internal-comms/examples/faq-answers.md), [general guidance](https://github.com/anthropics/skills/blob/main/skills/internal-comms/examples/general-comms.md) | Select format by the communication need, put key information first, use approachable wording and distinguish uncertain answers. | Apply those principles to agent replies. Do not import its corporate source searches, mandatory audience/tone questionnaire, or FAQ sentence limits into ordinary chat. |
| [DfE plain-language guidance](https://design.education.gov.uk/content-design/plain-language) | Use the audience's language and explain necessary technical terminology. Plain language adapts to the reader. | Prefer common words across languages; preserve a necessary term with a short practical explanation. Do not impose English readability scores or patronize an expert. |
| [Morkes and Nielsen: concise, scannable and objective writing](https://www.nngroup.com/articles/concise-scannable-and-objective-how-to-write-for-the-web/) | Readable organization, useful brevity and factual wording are separate qualities. | Use understandable bullets for multiple findings, numbered steps for sequences and tables for comparable attributes; avoid automatic walls of text or compulsory formatting. The 1997 web study is not evidence of LLM token savings or guaranteed chat comprehension. |

No source text or company template was copied into the runtime skill. Its procedure stays in one short SKILL.md; no new runtime script, second-model rewriting pass or readability service is required. Implicit invocation remains enabled. Existing global skill-selection instructions already cover matching communication tasks.

## Intended behavior

- Answer the user's question first and keep unrequested background, fixes and next-task proposals out unless essential to interpret/use the answer.
- Use common words before short obscure ones. Keep cause, consequence or a small example when needed to understand the point; do not invent an unknown cause.
- Several failures should usually be separate short bullets, not one dense paragraph or an unexplained list of technical labels.
- Match detail to the request and reader. Exact terms, code, commands, citations, uncertainty and complete requested deliverables remain intact.
- Keep status accurate: built is not deployed, pending is not successful, and unattempted is not denied.

The existing per-skill case matrix retains its original factual-blocker and exact-text controls. A separate independent application pass exercises nontechnical failure reports, a short conceptual example, verbatim multiline output, unpublished work, requested technical depth and a second non-English language. These are bounded application checks, not a measured comprehension or native activation rate. The objective is fewer clarification requests; no numeric savings claim is made without complete-task measurements.

The first six-case pass preserved exact text, truthful publication status, requested expert detail, a useful example and Portuguese wording. It also exposed an unnecessary technical label in a short Spanish failure report: the response retained “authentication token” where the user's session expiring was sufficient. The procedure was refined to explain observable behavior rather than echo diagnostic labels. This finding illustrates why brevity alone is not an adequate acceptance criterion.

In the focused follow-up, the first failure became “No se puede completar la compra porque la sesión caducó.” The agent kept separate short bullets for the duplicate charge and unknown email status, without adding fixes or losing their causes/uncertainty. This was a correction check by the same evaluator, not another blind run.
