---
name: research
description: 'Fact research. Use when the user says "research", "look up", "find out", "is it still true" or "what''s the latest", or the answer depends on versions, prices, limits, APIs or anything that may have changed since training, even when you are fairly sure you remember the answer.'
metadata:
  type: technique
---

# Research

**Research** answers from sources opened in this session, not from memory, and leaves a trail the user can check. Name each source and the date you checked it in your answer.

When the user asked you to research or write something up, also save the findings:

<research-note path="research/{topic}.md">
# {question}
Checked: {today's date}
## Answer
{the answer, and the version or context it holds for}
## Sources
- {title}: {URL or file path} ({its publication or release date})
## Conflicts and confidence
{what disagreed, which source won and why}. Confidence: {high, medium or low}.
</research-note>
