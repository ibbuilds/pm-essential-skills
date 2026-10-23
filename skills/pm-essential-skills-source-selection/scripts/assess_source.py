#!/usr/bin/env python3
"""Decide whether declared source evidence can be reused; no reads or persistent cache."""

import argparse
import json
import sys
from pathlib import Path

FLAGS = {"needed", "content_available", "coverage_sufficient", "freshness_required",
         "revision_verified", "known_immutable", "required_full_read", "full_read_complete"}
TEXT = {"source_id", "loaded_source_id", "loaded_revision", "current_revision"}


def assess(value):
    if not isinstance(value, dict) or set(value) - FLAGS - TEXT - {"access"}:
        raise ValueError("Unknown source fields or non-object input")
    for key in FLAGS:
        if key in value and type(value[key]) is not bool:
            raise ValueError(f"{key} must be a boolean")
    for key in TEXT:
        if key in value and value[key] is not None and (
            not isinstance(value[key], str) or not value[key].strip()
        ):
            raise ValueError(f"{key} must be a nonempty string or null")
    if not value.get("source_id"):
        raise ValueError("source_id is required")
    access = value.get("access", "unknown")
    if not isinstance(access, str) or access not in {"available", "unknown", "denied"}:
        raise ValueError("access must be available, unknown, or denied")

    def result(action, reason):
        return {"action": action, "reason": reason, "source_id": value["source_id"]}

    full_required = value.get("required_full_read", False)
    if not value.get("needed", True) and not full_required:
        return result("skip", "not_needed_for_current_task")
    if access == "denied":
        return result("blocked", "source_access_denied")
    if not value.get("content_available", False) or value.get("loaded_source_id") != value["source_id"]:
        return result("fetch", "content_or_matching_identity_missing")
    loaded = value.get("loaded_revision")
    current = value.get("current_revision")
    if value.get("revision_verified", False) and loaded is not None and current is not None and loaded != current:
        return result("fetch", "source_revision_changed")
    if full_required and not value.get("full_read_complete", False):
        return result("fetch", "required_full_read_incomplete")
    if not value.get("coverage_sufficient", False):
        return result("fetch", "task_coverage_incomplete")
    if value.get("freshness_required", False) and not value.get("known_immutable", False):
        if not (value.get("revision_verified", False) and loaded is not None and current == loaded):
            return result("verify", "current_revision_not_established")
    return result("reuse", "available_content_satisfies_task")


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON field; field names must be unique")
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    args = parser.parse_args()
    try:
        raw = args.input.read_text(encoding="utf-8-sig") if args.input else sys.stdin.read()
        try:
            value = json.loads(raw, object_pairs_hook=unique)
        except RecursionError as exc:
            raise ValueError(str(exc)) from exc
        result = assess(value)
    except (ValueError, OSError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(result, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
