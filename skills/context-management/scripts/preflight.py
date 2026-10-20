#!/usr/bin/env python3
"""Assess declared host capabilities. No discovery, authorization grants, or mutations."""

import argparse
import json
import sys
from pathlib import Path

FLAGS = {"current_skill_available", "destination_skill_available", "create_thread_available",
         "reconcile_thread_available", "create_project_available", "move_chat_available",
         "verify_membership_available", "authorization_verified", "safe_checkpoint",
         "references_accessible", "settings_preserved", "setup_consent_verified",
         "target_project_verified", "project_selection_authorized"}
FLAGS.add("execution_mode_allows_transfer")
TEXT = {"project_id", "source_thread_id", "chosen_project_name"}


def assess(value):
    if not isinstance(value, dict) or set(value) - FLAGS - TEXT - {"membership"}:
        raise ValueError("Unknown preflight fields or non-object input")
    for key in FLAGS:
        if key in value and value[key] is not None and type(value[key]) is not bool:
            raise ValueError(f"{key} must be true, false, or null")
    for key in TEXT:
        if key in value and value[key] is not None and (
            not isinstance(value[key], str) or not value[key].strip()
        ):
            raise ValueError(f"{key} must be a nonempty string or null")
    membership = value.get("membership", "unknown")
    if not isinstance(membership, str) or membership not in {"project", "standalone", "unknown"}:
        raise ValueError("membership must be project, standalone, or unknown")

    required = ["current_skill_available", "destination_skill_available", "create_thread_available",
                "reconcile_thread_available", "authorization_verified", "safe_checkpoint",
                "references_accessible", "settings_preserved", "execution_mode_allows_transfer"]
    missing = [key for key in required if value.get(key) is not True]
    selected_target = (value.get("target_project_verified") is True
                       and value.get("project_selection_authorized") is True)
    if membership != "project" and not selected_target:
        missing.append("verified_project_membership")
    for key in ["project_id", "source_thread_id"]:
        if not value.get(key):
            missing.append(key)
    setup_caps = ["create_project_available", "move_chat_available", "verify_membership_available"]
    setup_missing = [key for key in setup_caps if value.get(key) is not True]
    if membership != "standalone":
        setup = "not_applicable" if membership == "project" else "resolve_membership"
    elif setup_missing:
        setup = "unsupported"
    elif value.get("setup_consent_verified") is not True:
        setup = "needs_consent"
    elif not value.get("chosen_project_name"):
        setup = "needs_name"
    elif not value.get("source_thread_id"):
        setup = "needs_chat_identity"
    elif value.get("safe_checkpoint") is not True:
        setup = "defer"
    else:
        setup = "ready"
    return {"transfer_ready": not missing, "transfer_missing": missing,
            "source_membership": membership,
            "project_setup": setup, "setup_missing_capabilities": setup_missing,
            "status": "ready" if not missing else "degraded" if value.get("current_skill_available") is True else "unavailable"}


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON field: {key}")
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    args = parser.parse_args()
    try:
        raw = args.input.read_text(encoding="utf-8-sig") if args.input else sys.stdin.read()
        result = assess(json.loads(raw, object_pairs_hook=unique))
    except (ValueError, OSError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(result, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
