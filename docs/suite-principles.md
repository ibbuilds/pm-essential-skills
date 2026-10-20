# Suite purpose and skill boundaries

## Objective

Reduce avoidable AI work while preserving task quality, continuity, and user control. Measure the complete task, including the suite's own instructions, tool calls, handoffs, startup, retries, and reconstruction. A smaller prompt or more chats alone does not prove an improvement.

The suite manages the supporting workflow across any project type. Domain work remains with the user's instructions and appropriate execution skills. It does not enforce coding processes, design methods, research methodologies, branch policies, or a particular project-management service.

## Admission criteria for a skill

Before adding a skill, establish:

1. A recurring, observable source of avoidable work.
2. One distinct responsibility with a useful trigger and an explicit no-op case.
3. A lighter execution path than repeatedly solving the same management problem.
4. Preservation of user scope, source coverage, tools, and decision authority.
5. Tests or realistic evaluation cases that expose both benefits and failure costs.

Do not create a skill merely to rename behavior already owned elsewhere. A candidate stays deferred if its benefit or boundary is unclear. The 700-word entrypoint limit is a maintenance ceiling, not a writing target; conditional references are loaded only when needed.

## Current ownership

| Responsibility | Owner |
| --- | --- |
| Continue this chat, offer project setup, or perform a handoff | Context Management |
| Decide which sources to locate/read/revalidate for the current task | Source Selection |
| Preserve binding decisions and remaining work during a thread transfer | Context Management |
| Preserve provenance and unresolved source conflicts in the current result | Source Selection |
| Decide what the project should prioritize or what the user should build | User or another explicitly requested planning workflow |
| Execute domain work and its required verification | Appropriate execution skill or the assistant's normal task workflow |

Source Selection does not create a parallel project-memory system. Context Management may carry the relevant evidence references in a handoff without copying an entire retrieval history. Skills can cooperate without loading each other's full instructions by default.

## Non-intrusive behavior

- Useful same-task work proceeds without a new management call, message, or file when current state is sufficient.
- Plugin and individual skill installs use normal implicit selection without per-project activation prompts. Each skill remains independent; optional host activation adapters strengthen discovery without becoming prerequisites. Installation receipts and project notes are not authorization grants.
- Unknown measurements stay unknown. No skill attributes waste or claims savings from chat age, account percentages, or word counts.
- Notices explain a substantiated issue and an actionable next step. Avoid repeated warnings, user blame, and unnecessary confirmation.
- Respect explicit exhaustive coverage, full-document reads, required tools, output standards, and the user's choice to stay in a chat. Optimization cannot silently reduce the assignment.
- Use existing project structure. Add state only when a real continuation need justifies it; never create generic management scaffolding as an installation side effect.
- Do not change models, permissions, integrations, Git state, or external settings merely to optimize usage. Existing user authorization still applies when such changes are explicitly requested.
- Support partial capability honestly. A missing adapter is not permission to fabricate success, move unrelated data, or force a new service on the user.

## Optional integrations

Tools are adapters, not prerequisites. A checkpoint can reference ordinary files, a document, or a Git revision when the project already uses one. A source may live locally or in a connected system. The skill uses the existing tool with the appropriate access and scope.

Skills whose primary function is managing branches, commits, pull requests, deployments, or another specialized workflow belong outside this general suite. This repository itself uses Git and GitHub for development and distribution; consumers do not need those services for ordinary skill execution.

## Candidate work

The next improvement should follow observed pilot friction. Possible concerns include repeated task clarification or stale progress records, but these are not additional skills until their need and separation from the current two are demonstrated. Do not build a mandatory orchestrator or universal workflow merely to grow the suite.

## Evaluation

For matched tasks, compare completion quality, source coverage, important decisions lost, repeated reads/investigations, user interventions, latency, and total usage when the host exposes it. Keep model/effort and task conditions comparable. Include failed transfers and retrieval attempts in the totals. If metrics are unavailable, report observable behavior instead of inventing saved tokens.

Unit tests certify deterministic helper behavior. Structural checks certify packaging and references. Live tool behavior and net usage effects require separate pilots. No release is described as flawless solely because the unit tests pass.
