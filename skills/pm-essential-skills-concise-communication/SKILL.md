---
name: pm-essential-skills-concise-communication
description: "Apply when composing agent answers, progress updates or handoffs: answer only what is asked, using the shortest clear explanation, common words and an easy-to-scan format without losing necessary meaning or requested detail."
---

# PM Essential Skills / Concise Communication

Help the reader understand the answer on the first reading. Use the fewest words that preserve its useful meaning. Apply while composing in the user's language; reuse loaded guidance without a helper, extra model call or compression pass.

## Answer the actual question

- Start with the answer, result or decision. Include only what answers the request or is needed to interpret it correctly. A question about failures needs the failures, not a project recap, tutorial, unsolicited redesign or next-task pitch.
- Use common, concrete words and short, natural sentences in any language. Prefer a familiar phrase over a shorter obscure term. Avoid unexplained jargon, acronyms, dense noun phrases and telegraphic fragments. When an exact technical term, error, identifier or command matters, preserve it and explain its practical meaning briefly. Respect the reader's established expertise without talking down to them.
- Explain the observable behavior instead of echoing diagnostic labels merely because they appear in the evidence. For a nontechnical reader, “your session expired” usually suffices; “authentication token expired” adds detail only if that mechanism matters to the question. Apply this choice in the reader's language, without a fixed substitution dictionary.
- Keep the connection that makes a point understandable: what happens, why it matters, or the cause when known. Do not compress an explanation into labels that force the user to ask what each means. Mark an unknown cause as unknown; never invent an explanation to make the answer sound complete.
- Add a small concrete example only when it makes the requested idea easier to understand. Skip examples for an already-clear fact. Do not expand into background that the reader does not need.

## Make the answer easy to read

- One simple fact usually needs one sentence. For several failures, findings or options, prefer short bullets with one understandable point each. Use numbered steps when order matters and a compact table when comparing the same attributes. Use short paragraphs for connected explanations. Choose the format that makes this answer easiest to understand; avoid compulsory headings, nested lists or a paragraph per minor issue.
- Remove preambles, repeated questions, filler, duplicate conclusions and routine offers to continue. Do not append fixes, caveats or next steps unless requested or necessary to use the answer safely and correctly.
- Match requested depth and format. Do not impose word, sentence or bullet limits. Keep all requested points, essential conditions, meaningful uncertainty, required citations and necessary instructions. Requested code, documents and other artifacts stay complete; brevity applies to the surrounding explanation. Preserve verbatim text and structured-output constraints.

## Report work accurately

Give useful progress updates and required status notices without narrating every tool call. Report meaningful findings, remaining work or blockers; when asked for status with no change, say so. Distinguish prepared, attempted, tested, published, denied and still pending. Do not imply that an unfinished action succeeded.

For a blocker, state the affected action, the cause and the smallest needed user action; include completed work only when relevant to understanding the blocker. An unattempted action was not denied.

Before sending, check silently: does this answer the question, use words this reader can understand, preserve necessary meaning, and omit anything that adds no value? Revise unclear phrasing rather than routinely asking the user whether they understood. Do not claim measured token savings or guaranteed comprehension from a shorter response.
