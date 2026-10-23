#!/usr/bin/env python3
"""Assess declared archive/recovery state; no host calls, writes, or authority grants."""

import argparse
import json
from pathlib import Path
import sys

FLAGS = {"target_verified", "authorized", "archive_control_available", "archive_effect_isolated",
         "no_other_active_work", "handoff_confirmed", "routing_saved", "source_superseded",
         "source_recovery_ready", "original_archived", "currently_archived", "restored_for_recovery",
         "recovery_receipt_saved", "user_keep_visible"}


def assess(value):
    if not isinstance(value, dict) or set(value) - FLAGS - {"stage", "read_result"}:
        raise ValueError("Unknown archive observations or non-object input")
    for key in FLAGS:
        if key in value and value[key] is not None and type(value[key]) is not bool:
            raise ValueError(f"{key} must be true, false, or null")
    stage = value.get("stage")
    if stage not in ("after_handoff", "recover", "restore"):
        raise ValueError("stage must be after_handoff, recover, or restore")
    read_result = value.get("read_result", "not_attempted")
    if read_result not in ("not_attempted", "success", "archive_blocked", "failed"):
        raise ValueError("read_result must describe an actual supported read outcome")

    def result(action, reason):
        return {"action": action, "reason": reason}

    def mutation_gate():
        for key in ("authorized", "archive_control_available", "archive_effect_isolated", "no_other_active_work"):
            if value.get(key) is not True:
                return result("keep", f"missing_{key}")
        return None

    if value.get("user_keep_visible") is True and stage != "recover":
        return result("keep", "user_keeps_visible")
    if value.get("target_verified") is not True:
        return result("verify_target", "source_identity_unverified")

    if stage == "after_handoff":
        for key in ("handoff_confirmed", "routing_saved", "source_superseded", "source_recovery_ready"):
            if value.get(key) is not True:
                return result("keep", f"missing_{key}")
        if value.get("currently_archived") is True:
            return result("keep", "already_archived")
        if value.get("currently_archived") is not False:
            return result("verify_archive_state", "archive_state_unknown")
        return mutation_gate() or result("archive_source", "superseded_source_ready")

    if stage == "recover":
        if read_result == "success":
            return result("use_context", "direct_read_succeeded")
        if read_result == "not_attempted":
            return result("read_source", "try_supported_read_before_restoring")
        if read_result != "archive_blocked":
            return result("fallback", "read_failure_does_not_establish_archive_barrier")
        if value.get("user_keep_visible") is True:
            return result("keep", "user_keeps_visible")
        if value.get("currently_archived") is not True or value.get("original_archived") is not True:
            return result("verify_archive_state", "archived_state_not_established")
        gate = mutation_gate()
        if gate:
            return gate
        if value.get("recovery_receipt_saved") is not True:
            return result("record_recovery_receipt", "preserve_original_state_before_restore")
        return result("unarchive_for_recovery", "archival_blocks_needed_read")

    if value.get("recovery_receipt_saved") is not True:
        return result("keep", "no_owned_recovery_receipt")
    if value.get("original_archived") is False:
        return result("keep", "originally_unarchived")
    if value.get("original_archived") is not True:
        return result("verify_archive_state", "original_state_unknown")
    if value.get("currently_archived") is True:
        return result("cleanup_complete", "original_archive_state_confirmed")
    if value.get("currently_archived") is not False or value.get("restored_for_recovery") is not True:
        return result("reconcile_restore", "temporary_restore_unconfirmed")
    return mutation_gate() or result("rearchive_source", "restore_original_archived_state")


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
        try:
            value = json.loads(raw, object_pairs_hook=unique)
        except RecursionError as exc:
            raise ValueError(str(exc)) from exc
        output = assess(value)
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(output, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
