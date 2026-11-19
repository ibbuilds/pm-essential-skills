#!/usr/bin/env node
// SessionStart hook.
// - After /clear or at startup: if a recent HANDOFF.md sits in the working directory,
//   load it so the fresh session continues the work without being asked.
// - At startup or after /clear: if BACKLOG.md has open items, show the user how many,
//   so parked work and "remind me to..." items come back.
// - On resume: if the prompt cache has expired and the conversation is large, tell the
//   user what resuming will cost before the first request is sent.
// Never blocks the session.
//
// PM_HANDOFF_MAX_AGE_HOURS  ignore handoffs older than this (default 72)
// PM_RESUME_WARN_TOKENS     warn on cold resumes at or above this size (default 50000)
import { readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const MAX_CHARS = 9_000;

function readStdin() {
  try {
    return JSON.parse(readFileSync(0, "utf8"));
  } catch {
    return {};
  }
}

function positive(value, fallback) {
  const number = Number(value);
  return Number.isFinite(number) && number > 0 ? number : fallback;
}

function age(ms) {
  const minutes = Math.round(ms / 60_000);
  if (minutes < 90) return `${minutes} min`;
  const hours = Math.round(minutes / 60);
  return hours < 48 ? `${hours} h` : `${Math.round(hours / 24)} days`;
}

export function handoffOutput(cwd, now = Date.now()) {
  const path = join(cwd, "HANDOFF.md");
  let stats;
  try {
    stats = statSync(path);
  } catch {
    return null;
  }
  const maxAge = positive(process.env.PM_HANDOFF_MAX_AGE_HOURS, 72) * 3_600_000;
  const elapsed = now - stats.mtimeMs;
  if (elapsed > maxAge) return null;
  let text = readFileSync(path, "utf8");
  if (text.length > MAX_CHARS) text = `${text.slice(0, MAX_CHARS)}\n[truncated: read HANDOFF.md for the rest]`;
  return {
    systemMessage: `HANDOFF.md from ${age(elapsed)} ago is loaded. Say "continue" to pick it up.`,
    hookSpecificOutput: {
      hookEventName: "SessionStart",
      additionalContext:
        `An earlier session left this handoff in HANDOFF.md, written ${age(elapsed)} ago. ` +
        'If the user\'s first message continues that work, or is just "continue" or "go", re-check the state it describes, then start from its Next action. ' +
        "If the user asks for something unrelated, ignore the handoff. Delete HANDOFF.md once its work is finished.\n\n" +
        text,
    },
  };
}

export function backlogMessage(cwd) {
  let text;
  try {
    text = readFileSync(join(cwd, "BACKLOG.md"), "utf8");
  } catch {
    return null;
  }
  const open = text.split(/\r?\n/).filter((line) => /^\s*[-*] \[ \]/.test(line));
  if (open.length === 0) return null;
  const first = open[0].replace(/^\s*[-*] \[ \]\s*/, "").slice(0, 120);
  const items = open.length === 1 ? "1 parked item" : `${open.length} parked items`;
  return `BACKLOG.md has ${items}. First: ${first}`;
}

export function startOutput(cwd, now = Date.now()) {
  const handoff = handoffOutput(cwd, now);
  const backlog = backlogMessage(cwd);
  if (!backlog) return handoff;
  if (!handoff) return { systemMessage: backlog };
  return { ...handoff, systemMessage: `${handoff.systemMessage} ${backlog}` };
}

export function resumeOutput(input) {
  const tokens = Number(input.context_tokens) || 0;
  if (!input.prompt_cache_likely_expired || tokens < positive(process.env.PM_RESUME_WARN_TOKENS, 50_000)) return null;
  const cost = Number(input.estimated_cache_write_usd);
  const price = Number.isFinite(cost) && cost > 0 ? ` (about $${cost.toFixed(2)} at API rates)` : "";
  return {
    systemMessage:
      `This conversation's prompt cache has expired. Your next message re-sends all ${Math.round(tokens / 1000)}k tokens${price}. ` +
      "If you don't need its full detail, start a new session instead and continue from a handoff.",
  };
}

function main() {
  const input = readStdin();
  if (input.agent_id) return;
  let output = null;
  try {
    if (input.source === "resume") output = resumeOutput(input);
    else if ((input.source === "clear" || input.source === "startup") && input.cwd) output = startOutput(input.cwd);
  } catch {
    return;
  }
  if (output) process.stdout.write(JSON.stringify(output));
}

if (process.argv[1] && process.argv[1].endsWith("session-start.mjs")) main();
