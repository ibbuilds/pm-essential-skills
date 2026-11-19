#!/usr/bin/env node
// PreCompact hook. Tells the compaction summary to keep what a fresh continuation needs
// (the same fields as the pause handoff). Never blocks compaction.
//
// The docs do not say whether hook stdout replaces or adds to the user's `/compact <text>`,
// so the user's text is echoed first, as their priority, and is never lost either way.
import { readFileSync } from "node:fs";

const INSTRUCTIONS =
  "When writing the summary, keep what a fresh continuation needs: " +
  "the goal in the user's terms; decisions and their reasons; dead ends (what was tried, why it failed); " +
  "verified state (files changed, the last check command and its exact result); files to read first; " +
  "the next action; open questions for the user. " +
  "Drop raw tool output, file dumps and exploration that led nowhere, except as one-line dead ends. " +
  "Never copy secret values; name where they live.";

function readStdin() {
  try {
    return JSON.parse(readFileSync(0, "utf8"));
  } catch {
    return {};
  }
}

export function compactInstructions(input) {
  const custom = typeof input?.custom_instructions === "string" ? input.custom_instructions.trim() : "";
  if (!custom) return INSTRUCTIONS;
  return `The user's instructions for this summary, which take priority over everything below:\n${custom.slice(0, 8_000)}\n\n${INSTRUCTIONS}`;
}

function main() {
  const input = readStdin();
  if (!input || typeof input !== "object" || input.agent_id) return;
  if (input.trigger !== "manual" && input.trigger !== "auto") return;
  process.stdout.write(compactInstructions(input));
}

if (process.argv[1] && process.argv[1].endsWith("pre-compact.mjs")) main();
