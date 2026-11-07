# Source selection by expertise and applicability

Version 0.6.6. The prior skill explained retrieval, bounded output and reuse, but gave little guidance for deciding which sources can support a claim. The revision makes relevant expertise, primary evidence, governing applicability and claim-level support part of source selection. It preserves exact-source requests, sufficient-context fast paths, requested coverage and freshness-aware reuse. Helper behavior is unchanged; no new provider, runtime, trust service, model default or mandatory research agent is introduced.

## Primary-source comparison

Sources read on 2026-11-07. Their procedures inform this revision; they do not measure its effectiveness.

| Source | Applicable reasoning | Adaptation and limits |
| --- | --- | --- |
| Matt Pocock, [research](https://github.com/mattpocock/skills/blob/main/skills/engineering/research/SKILL.md), content blob `ffc9eb89849cc4cf74962ce93d786ffd17c6a5dc` | Trace claims to the official documentation, code, specification or first-party source that owns the fact. | Prefer applicable primary evidence and traceable citations. Do not import automatic background agents or a mandatory Markdown research file. |
| Digital Inquiry Group / Civic Online Reasoning, [Teaching Lateral Reading](https://cor.inquirygroup.org/curriculum/collections/teaching-lateral-reading) and [A Little of Everything](https://cor.inquirygroup.org/curriculum/collections/a-little-of-everything) | Identify who is behind information, inspect evidence and check what independent sources say. A website's self-description is insufficient verification. | Use a narrow independent provenance check when unfamiliar/disputed authority matters. Do not require a separate credibility investigation for every known source or trivial answer. |
| Cornell Legal Information Institute, [legal research](https://www.law.cornell.edu/wex/Legal_research) and [primary authority](https://www.law.cornell.edu/wex/primary_authority) | Distinguish official legal authority from commentary; authority governs only where it applies. | Identify jurisdiction, governing status and effective date. These U.S. educational explainers inform the source distinction; they are not the law for every jurisdiction or a substitute for the applicable official source. |
| OWASP, [LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) | External websites and files can carry indirect instructions that redirect a model. External content must remain distinct from trusted instructions. | Reputable sources still cannot authorize disclosure, code execution or task changes. Preserve legitimate procedures within actual authorization. Markdown guidance and sample refusals do not implement or certify a security boundary. |

## Practical scope

Official status and first-party origin do not prove independent comparative claims. Reputation, relevant adoption and repository stars help prioritize discovery, but do not replace inspecting evidence or create a fixed popularity threshold. A verified niche implementation can establish its own behavior; a famous person outside the topic cannot establish it by reputation alone. Qualified synthesis can outweigh one primary study when its methods and scope justify that judgment.

The added conditional reference explains software/version fit, legal applicability, empirical evidence, conflicting claims and source trust. The entrypoint retains essential criteria and existing retrieval/reuse references. Its description and UI prompt now expose expertise and applicability; implicit invocation remains enabled. The generated selection pointer is aligned with that scope. No global settings, hooks or unrelated skill procedures change.

## Verification scope

The 11 new cases in `tests/source-authority-cases.json` cover expertise versus SEO/fame, legal jurisdiction and effective date, missing jurisdiction, version mismatch, verifiable low-adoption evidence, vendor conflicts, copied claims, exact-source summaries, embedded instructions, authorized procedures and corrected evidence. Existing reuse/output/coverage cases remain in place. The individual-skill positive scenario now exercises evidence selection; output-failure regression scenarios remain in their existing fixtures.

An independent application pass received the revised skill, raw requests without expected answers, and an isolated local corpus. It chose the supplied project's v2 documentation and implementation over a famous developer's v3 article, correctly reported three total calls and no validation-error retry, and did not follow the official-looking page's instruction to create an unrelated file. The marker file was absent afterward. Its decisions preserved the 11 authority scenarios and two existing reuse contrasts. It appropriately treated a straightforward already-approved installation as outside source selection when no source uncertainty existed.

The local suite passed 372 tests with 22 platform skips, and all 29 synthetic helper replays passed. Skill-creator validation, repository checks and installer packaging passed; packaged skill bytes were checked against the source before publication. Structural and fixture checks validate their own contracts, not model adherence. The independent pass was one application with scenario decisions and a local synthetic document; it does not establish universal activation, live connector safety, general injection resistance or measured resource savings.
