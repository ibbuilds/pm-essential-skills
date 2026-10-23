#!/usr/bin/env python3
"""Local transfer journal. Never creates a chat or grants tool authorization."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
from pathlib import Path

PHASES = {"prepared", "requesting", "uncertain", "confirmed", "superseded", "cancelled", "failed"}
EVENTS = {"prepare", "request", "unknown", "failed", "confirm", "supersede", "cancel", "absent", "status"}
SCHEMA = {"version", "revision", "phase", "handoff_id", "project_id", "source_thread_id",
          "destination_thread_id", "brief_path", "brief_sha256", "brief_bytes", "attempts", "events"}
GATES = {"authorization_verified", "project_verified", "destination_skill_available",
         "references_accessible", "source_recovery_ready", "settings_preserved", "safe_checkpoint", "execution_mode_allows_transfer"}


def text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a nonempty string")
    return value


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON field; field names must be unique")
        result[key] = value
    return result


def read_regular_bytes(path, *, journal=False):
    # Durable state/briefs cannot be streams. Check before open and again on the
    # descriptor; a FIFO substituted between those checks must not block open.
    if not path.is_file():
        raise ValueError("Durable transfer source requires a regular file")
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NONBLOCK", 0)
    if journal:
        flags |= getattr(os, "O_NOFOLLOW", 0)
    with os.fdopen(os.open(path, flags), "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError("Durable transfer source requires a regular file")
        return stream.read()


def parse_json(raw):
    try:
        return json.loads(raw, object_pairs_hook=unique)
    except RecursionError as exc:
        # Normalize decoder limits only, not recursion in lifecycle logic.
        raise ValueError("JSON nesting exceeds decoder limit") from exc


def read_json(path, *, journal=False):
    # Event payloads (--input) retain their ordinary stream-compatible behavior.
    raw = (read_regular_bytes(path, journal=True).decode("utf-8-sig") if journal
           else path.read_text(encoding="utf-8-sig"))
    return parse_json(raw)


def digest(path, source_thread_id=None):
    raw = read_regular_bytes(path)
    if not raw.strip():
        raise ValueError("Continuation brief is empty")
    content = raw.decode("utf-8-sig")
    if source_thread_id is not None and not re.search(
            r"(?<![\w-])" + re.escape(text(source_thread_id, "source_thread_id")) + r"(?![\w-])", content):
        raise ValueError("Continuation brief must include the verified source_thread_id")
    return hashlib.sha256(raw).hexdigest(), len(raw)


def validate(state):
    if not isinstance(state, dict) or set(state) != SCHEMA:
        raise ValueError("Invalid transfer journal schema")
    if type(state["version"]) is not int or state["version"] != 1:
        raise ValueError("Unsupported transfer journal version")
    for key in ["revision", "brief_bytes", "attempts"]:
        if type(state[key]) is not int or state[key] < 0:
            raise ValueError(f"Invalid {key}")
    if state["attempts"] > 2:
        raise ValueError("Transfer attempts exceed the bounded retry limit")
    if not isinstance(state["phase"], str) or state["phase"] not in PHASES:
        raise ValueError("Invalid transfer phase")
    if state["phase"] in {"requesting", "uncertain", "confirmed", "superseded"} and not state["attempts"]:
        raise ValueError("In-flight/confirmed transfers require a recorded creation attempt")
    if state["phase"] == "failed" and state["attempts"] != 2:
        raise ValueError("Failed terminal state requires exhausted attempts")
    if state["phase"] == "prepared" and state["attempts"] >= 2:
        raise ValueError("Prepared state cannot exceed the retry limit")
    events = state["events"]
    if not isinstance(events, list) or not 1 <= len(events) <= 12:
        raise ValueError("Invalid bounded event history")
    for index, entry in enumerate(events):
        if (not isinstance(entry, dict) or set(entry) != {"event", "phase", "revision"}
                or not isinstance(entry["event"], str) or entry["event"] not in EVENTS - {"status"}
                or not isinstance(entry["phase"], str) or entry["phase"] not in PHASES
                or type(entry["revision"]) is not int or entry["revision"] != index):
            raise ValueError("Invalid transfer event")
    if events[-1]["revision"] != state["revision"] or events[-1]["phase"] != state["phase"]:
        raise ValueError("Journal state disagrees with event history")
    # Version 1 retains the complete history; the writer never prunes events or
    # appends idempotent no-ops. Check consistency, not host outcomes/permission.
    if events[0]["event"] != "prepare" or events[0]["phase"] != "prepared":
        raise ValueError("Transfer history must start with prepare/prepared")
    phase, attempts = "prepared", 0
    for entry in events[1:]:
        event = entry["event"]
        allowed = {
            "request": ({"prepared"}, "requesting"),
            "unknown": ({"requesting"}, "uncertain"),
            "failed": ({"requesting", "uncertain"}, "prepared" if attempts < 2 else "failed"),
            "absent": ({"uncertain"}, "prepared" if attempts < 2 else "failed"),
            "confirm": ({"requesting", "uncertain"}, "confirmed"),
            "supersede": ({"confirmed"}, "superseded"),
            "cancel": ({"prepared", "failed"}, "cancelled"),
        }
        if event not in allowed or phase not in allowed[event][0]:
            raise ValueError("Invalid lifecycle transition in transfer history")
        phase = allowed[event][1]
        if event == "request":
            attempts += 1
        if attempts > 2 or entry["phase"] != phase:
            raise ValueError("Transfer history phase or retry limit is inconsistent")
    if state["attempts"] != attempts:
        raise ValueError("Transfer attempts disagree with request event history")
    for key in ["handoff_id", "project_id", "source_thread_id", "brief_path"]:
        text(state[key], key)
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,79}", state["handoff_id"]):
        raise ValueError("handoff_id must be a filesystem-safe lowercase ID")
    if not isinstance(state["brief_sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", state["brief_sha256"]):
        raise ValueError("Invalid continuation brief digest")
    destination = state["destination_thread_id"]
    if state["phase"] in {"confirmed", "superseded"}:
        text(destination, "destination_thread_id")
        if destination == state["source_thread_id"]:
            raise ValueError("Destination cannot equal source")
    elif destination is not None:
        raise ValueError("Unconfirmed phase cannot have a destination")
    return state


def transition(state, event, data):
    """Pure lifecycle change; caller supplies observed results, never inferred success."""
    validate(state)
    if not isinstance(data, dict):
        raise ValueError("Event data must be an object")
    next_state = dict(state)
    phase = state["phase"]
    allowed = {
        "request": GATES | {"failure_resolved"}, "unknown": set(),
        "failed": {"definite_failure"}, "absent": {"definitive_absence"},
        "confirm": {"destination_thread_id", "destination_ready", "project_id", "handoff_id"},
        "supersede": {"routing_saved"}, "cancel": set(),
    }
    if event not in allowed:
        raise ValueError("Unknown transition event. Supported events: " + ", ".join(sorted(allowed)))
    if set(data) - allowed[event]:
        # Report only fixed schema names, never untrusted payload keys/values.
        fields = ", ".join(sorted(allowed[event])) or "(none; use an empty object)"
        raise ValueError(f"Unknown event-data field. Allowed fields for {event}: {fields}")
    if event == "request":
        if phase != "prepared" or state["attempts"] >= 2:
            raise ValueError("Creation is allowed only from prepared, within the retry limit")
        if any(data.get(key) is not True for key in GATES):
            raise ValueError("Verified transfer gates are required before creation")
        if state["attempts"] and data.get("failure_resolved") is not True:
            raise ValueError("Resolve the prior definite failure before retrying")
        next_state.update(phase="requesting", attempts=state["attempts"] + 1)
    elif event == "unknown":
        if phase != "requesting":
            raise ValueError("Only an in-flight creation can become uncertain")
        next_state["phase"] = "uncertain"
    elif event in {"failed", "absent"}:
        gate = "definite_failure" if event == "failed" else "definitive_absence"
        phases = {"requesting", "uncertain"} if event == "failed" else {"uncertain"}
        if phase not in phases or data.get(gate) is not True:
            raise ValueError("A definitive host outcome is required before retry")
        next_state["phase"] = "prepared" if state["attempts"] < 2 else "failed"
    elif event == "confirm":
        if phase not in {"requesting", "uncertain", "confirmed", "superseded"}:
            raise ValueError("No creation to confirm")
        destination = text(data.get("destination_thread_id"), "destination_thread_id")
        if (data.get("destination_ready") is not True or data.get("project_id") != state["project_id"]
                or data.get("handoff_id") != state["handoff_id"] or destination == state["source_thread_id"]):
            raise ValueError("Ready destination must match this project/handoff and differ from source")
        if phase in {"confirmed", "superseded"}:
            if destination != state["destination_thread_id"]:
                raise ValueError("Cannot replace an already confirmed destination")
            return next_state
        next_state.update(phase="confirmed", destination_thread_id=destination)
    elif event == "supersede":
        if phase not in {"confirmed", "superseded"} or data.get("routing_saved") is not True:
            raise ValueError("Save confirmed routing before superseding the source")
        if phase == "superseded":
            return next_state
        next_state["phase"] = "superseded"
    elif event == "cancel":
        if phase not in {"prepared", "failed", "cancelled"}:
            raise ValueError("Cannot cancel an in-flight or confirmed creation into a source writer")
        if phase == "cancelled":
            return next_state
        next_state["phase"] = "cancelled"
    next_state["revision"] += 1
    next_state["events"] = state["events"] + [
        dict(event=event, phase=next_state["phase"], revision=next_state["revision"])
    ]
    return validate(next_state)


def write_atomic(path, state):
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(state, stream, separators=(",", ":"))
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def update(path, event, data, expected_revision=None):
    if event not in EVENTS:
        raise ValueError("Unknown transfer event. Supported events: " + ", ".join(sorted(EVENTS)))
    path = Path(path)
    if path.is_symlink():
        raise ValueError("Journal cannot be a symbolic link")
    path = path.resolve()
    if event == "status":
        return validate(read_json(path, journal=True))
    if not isinstance(data, dict):
        raise ValueError("Event data must be an object")
    if event != "prepare" and (type(expected_revision) is not int or expected_revision < 0):
        raise ValueError("An expected revision is required for mutation")
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_name(path.name + ".lock")
    # Never auto-remove an existing lock: it may belong to a live writer.
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        os.close(fd)
        if event == "prepare":
            if path.exists():
                raise ValueError("Journal already exists; read and reconcile it instead of overwriting")
            if set(data) != {"handoff_id", "project_id", "source_thread_id", "brief_path"}:
                raise ValueError("Preparation needs handoff_id, project_id, source_thread_id, brief_path")
            brief = Path(text(data["brief_path"], "brief_path")).resolve()
            fingerprint, size = digest(brief, data["source_thread_id"])
            state = validate(dict(version=1, revision=0, phase="prepared", **data,
                                  destination_thread_id=None, brief_sha256=fingerprint,
                                  brief_bytes=size, attempts=0,
                                  events=[dict(event="prepare", phase="prepared", revision=0)]))
            state["brief_path"] = str(brief)
        else:
            state = validate(read_json(path, journal=True))
            if expected_revision != state["revision"]:
                raise ValueError("Stale revision; read current state before retrying")
            if event == "request" and digest(Path(state["brief_path"]), state["source_thread_id"])[0] != state["brief_sha256"]:
                raise ValueError("Brief changed after preparation; do not dispatch altered context")
            previous = state
            state = transition(state, event, data)
            if state == previous:
                return state
        write_atomic(path, state)
        return state
    finally:
        lock.unlink()


def summary(state):
    phase = state["phase"]
    owner = state["destination_thread_id"] if phase in {"confirmed", "superseded"} else (
        None if phase in {"requesting", "uncertain"} else state["source_thread_id"])
    fields = ["revision", "phase", "handoff_id", "destination_thread_id", "attempts", "brief_bytes"]
    return {key: state[key] for key in fields} | {
        "active_writer": owner,
        "must_pause_source": phase in {"requesting", "uncertain", "confirmed", "superseded"},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", required=True, type=Path)
    parser.add_argument("--event", required=True, choices=sorted(EVENTS))
    parser.add_argument("--input", type=Path)
    parser.add_argument("--expected-revision", type=int)
    args = parser.parse_args()
    try:
        if args.event == "status":
            data = {}
        else:
            data = read_json(args.input) if args.input else parse_json(sys.stdin.read())
        result = summary(update(args.state, args.event, data, args.expected_revision))
    except (ValueError, OSError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(result, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
