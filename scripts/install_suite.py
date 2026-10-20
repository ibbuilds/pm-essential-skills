#!/usr/bin/env python3
"""Install both skills and automatic user-level guidance; no per-project activation.

The install command selects the disclosed automatic-management defaults. Copying
skill folders alone does not select those defaults or grant coordination authority.
"""

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys
import tempfile
import subprocess

sys.path.insert(0, str(Path(__file__).resolve().parent))
from activation import render

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("context-management", "source-selection")
RECEIPT = "pm-essential-skills/install.json"
BEGIN = b"<!-- pm-essential-skills:start -->"
END = b"<!-- pm-essential-skills:end -->"
HELPER = "pm-essential-skills/activation.py"
DEFAULTS = ("Automatic skill use during active local sessions; same-project "
            "continuations within requested work; archive superseded managed sources and temporarily "
            "restore/rearchive for context recovery; preserve opt-outs and other active work. No unrelated "
            "chat messages, deletion, project creation, background jobs, or permission changes.")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encode(data):
    return None if data is None else base64.b64encode(data).decode("ascii")


def decode(value):
    return None if value is None else base64.b64decode(value, validate=True)


def safe_path(home, relative):
    """Validate receipt/package paths before any writes or deletes."""
    parts = PurePosixPath(relative)
    if (parts.is_absolute() or not parts.parts or ".." in parts.parts
            or "\\" in relative or ":" in relative):
        raise ValueError("Invalid installation path")
    path = home.joinpath(*parts.parts)
    for candidate in (path, *path.parents):
        if candidate == home:
            break
        if candidate.is_symlink() or getattr(candidate, "is_junction", lambda: False)():
            raise ValueError(f"Refusing linked installation path: {path}")
    if not path.resolve().is_relative_to(home):
        raise ValueError("Installation path escapes Codex home")
    return path


def read(path):
    return path.read_bytes() if path.exists() else None


def atomic_write(path, data):
    if data is None:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".pm-install-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def apply(changes):
    """Roll back handled write failures; a process crash is not transactional."""
    originals = {path: read(path) for path in changes}
    attempted = []
    try:
        for path, content in changes.items():
            if content != originals[path]:
                attempted.append(path)
                atomic_write(path, content)
    except OSError:
        for path in reversed(attempted):
            atomic_write(path, originals[path])
        raise


def load_receipt(home):
    raw = read(safe_path(home, RECEIPT))
    if raw is None:
        return None
    state = json.loads(raw)
    if not isinstance(state, dict) or state.get("version") != 1:
        raise ValueError("Unsupported installation receipt; preserve it for recovery")
    for relative, record in state["files"].items():
        if relative != HELPER and not any(relative.startswith(f"skills/{name}/") for name in SKILLS):
            raise ValueError("Receipt contains an unowned package path")
        safe_path(home, relative)
        decode(record["original"])
    if state["instructions"] not in ("AGENTS.md", "AGENTS.override.md"):
        raise ValueError("Invalid global instruction target")
    return state


def active_instructions(home):
    override = safe_path(home, "AGENTS.override.md")
    return "AGENTS.override.md" if (read(override) or b"").strip() else "AGENTS.md"


def selected_skills(state):
    return [name for name in SKILLS if f"skills/{name}/SKILL.md" in state.get("files", {})]


def installed_block(home, skills):
    return b"\n\n" + BEGIN + b"\n" + render(home, skills, installation=True).encode("utf-8") + END + b"\n"


def hooks_content(home, owned=None, add=False):
    """Merge only our exact groups, preserving other hook sources and definitions."""
    path = safe_path(home, "hooks.json")
    raw = read(path)
    config = json.loads(raw) if raw is not None else {}
    if not isinstance(config, dict) or not isinstance(config.get("hooks", {}), dict):
        raise ValueError("Invalid hooks.json; preserving user configuration")
    hooks = config.setdefault("hooks", {})
    if owned:
        for event, group in owned["groups"].items():
            groups = hooks.get(event, [])
            if not isinstance(groups, list) or groups.count(group) != 1:
                raise ValueError("Installed reminder hook changed or missing; preserve and reconcile it")
            groups.remove(group)
            if not groups:
                hooks.pop(event, None)
    if add:
        helper = safe_path(home, HELPER)
        if os.name == "nt":
            command = subprocess.list2cmdline([sys.executable, str(helper)])
        else:
            import shlex
            command = shlex.join([sys.executable, str(helper)])
        groups = {event: {"hooks": [{"type": "command", "command": command,
                                    "timeout": 5, "additionalContextLimit": 600}]}
                  for event in ("SessionStart", "UserPromptSubmit")}
        for event, group in groups.items():
            existing = hooks.setdefault(event, [])
            if not isinstance(existing, list):
                raise ValueError("Invalid hook event groups; preserving user configuration")
            existing.append(group)
        return (json.dumps(config, indent=2) + "\n").encode(), {
            "original": owned["original"] if owned else encode(raw), "groups": groups}
    original = decode(owned["original"]) if owned else raw
    # Restore exact prior formatting when there have been no unrelated user edits.
    original_object = json.loads(original) if original is not None else {}
    if not hooks:
        config.pop("hooks", None)
    comparable = dict(original_object)
    if comparable.get("hooks") == {}:
        comparable.pop("hooks")
    if config == comparable:
        return original, None
    return (json.dumps(config, indent=2) + "\n").encode(), None


def inspect(home, state):
    problems = []
    if state is None:
        return ["suite_not_installed"]
    for relative, record in state["files"].items():
        data = read(safe_path(home, relative))
        if data is None or digest(data) != record["sha256"]:
            problems.append(f"changed_or_missing:{relative}")
    guidance = read(safe_path(home, state["instructions"])) or b""
    block = decode(state["block"])
    if not block or guidance.count(block) != 1 or guidance.count(BEGIN) != 1 or guidance.count(END) != 1:
        problems.append("global_rule_changed_or_missing")
    if active_instructions(home) != state["instructions"]:
        problems.append("global_rule_shadowed_by_override")
    if state.get("hooks"):
        try:
            hooks_content(home, state["hooks"])
        except (ValueError, OSError, KeyError, TypeError):
            problems.append("reminder_hook_changed_or_missing")
    return problems


def install(home, state, skills=None, with_hooks=False):
    if state is not None:
        problems = inspect(home, state)
        if problems:
            raise ValueError("Preserving modified installation: " + ", ".join(problems))
    requested = tuple(skills) if skills is not None else tuple(
        name for name in SKILLS if (ROOT / "skills" / name / "SKILL.md").is_file())
    if not requested or set(requested) - set(SKILLS):
        raise ValueError("Choose at least one available skill")
    changes, files = {}, dict((state or {}).get("files", {}))
    for name in requested:
        source = ROOT / "skills" / name
        if not (source / "SKILL.md").is_file():
            raise ValueError(f"Skill is not included in this download: {name}")
        files = {key: value for key, value in files.items() if not key.startswith(f"skills/{name}/")}
        for path in sorted(source.rglob("*")):
            if "__pycache__" in path.parts:
                continue
            if path.is_symlink():
                raise ValueError("Linked package sources are not supported")
            if not path.is_file():
                continue
            relative = f"skills/{name}/{path.relative_to(source).as_posix()}"
            target = safe_path(home, relative)
            data = path.read_bytes()
            previous = (state or {}).get("files", {}).get(relative)
            files[relative] = {"original": previous["original"] if previous else encode(read(target)),
                               "sha256": digest(data)}
            changes[target] = data
    if with_hooks or (state or {}).get("hooks"):
        target = safe_path(home, HELPER)
        data = (ROOT / "scripts/activation.py").read_bytes()
        previous = (state or {}).get("files", {}).get(HELPER)
        files[HELPER] = {"original": previous["original"] if previous else encode(read(target)),
                         "sha256": digest(data)}
        changes[target] = data
    for relative, record in (state or {}).get("files", {}).items():
        if relative not in files:
            changes[safe_path(home, relative)] = decode(record["original"])
    instructions = state["instructions"] if state else active_instructions(home)
    target = safe_path(home, instructions)
    original = read(target)
    content = original or b""
    if state:
        content = content.replace(decode(state["block"]), b"", 1)
    elif BEGIN in content or END in content:
        raise ValueError("Existing suite rule has no receipt; reconcile before reinstalling")
    skills = selected_skills({"files": files})
    block = installed_block(home, skills)
    changes[target] = content + block
    receipt = {"version": 1, "files": files, "instructions": instructions,
               "instructions_existed": state["instructions_existed"] if state else original is not None,
               "block": encode(block), "defaults": DEFAULTS, "skills": skills}
    if with_hooks or (state or {}).get("hooks"):
        hook_bytes, owned = hooks_content(home, (state or {}).get("hooks"), add=True)
        changes[safe_path(home, "hooks.json")] = hook_bytes
        receipt["hooks"] = owned
    # Record backups first so interrupted installs can be inspected, not blindly retried.
    ordered = {safe_path(home, RECEIPT): (json.dumps(receipt, indent=2) + "\n").encode("utf-8")}
    ordered.update(changes)
    apply(ordered)
    return {"status": "installed", "package_files": len(files), "instructions": str(target),
            "activation": "next_host_instruction_reload", "live_invocation_verified": False,
            "skills": skills, "hooks": "registered_trust_unverified" if receipt.get("hooks") else "not_requested",
            "defaults": DEFAULTS}


def uninstall(home, state):
    if state is None:
        return {"status": "not_installed"}
    problems = inspect(home, state)
    # A new override does not prevent removing our unchanged block from its original file.
    problems = [item for item in problems if item != "global_rule_shadowed_by_override"]
    if problems:
        raise ValueError("Preserving modified installation: " + ", ".join(problems))
    changes = {safe_path(home, relative): decode(record["original"])
               for relative, record in state["files"].items()}
    target = safe_path(home, state["instructions"])
    remaining = target.read_bytes().replace(decode(state["block"]), b"", 1)
    changes[target] = remaining if remaining or state["instructions_existed"] else None
    if state.get("hooks"):
        changes[safe_path(home, "hooks.json")] = hooks_content(home, state["hooks"])[0]
    changes[safe_path(home, RECEIPT)] = None
    apply(changes)
    return {"status": "uninstalled", "user_instructions_preserved": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__, epilog=DEFAULTS)
    parser.add_argument("command", choices=("install", "status", "uninstall"))
    parser.add_argument("--skill", choices=SKILLS, action="append", help="Install only this skill; repeat to select several")
    parser.add_argument("--hooks", action="store_true", help="Also register per-turn reminders; Codex trust is still required")
    parser.add_argument("--codex-home", type=Path,
                        default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")))
    args = parser.parse_args()
    home = args.codex_home.expanduser().resolve()
    lock = None
    try:
        if args.command != "install" and (args.skill or args.hooks):
            raise ValueError("--skill and --hooks apply to installation only")
        if args.command != "status":
            lock = safe_path(home, "pm-essential-skills/install.lock")
            lock.parent.mkdir(parents=True, exist_ok=True)
            try:
                descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            except OSError:
                lock = None
                raise
            os.close(descriptor)
        elif safe_path(home, "pm-essential-skills/install.lock").exists():
            raise ValueError("Installation is in progress or needs recovery; preserving its lock")
        state = load_receipt(home)
        if args.command == "install":
            result = install(home, state, args.skill, args.hooks)
        elif args.command == "uninstall":
            result = uninstall(home, state)
        else:
            problems = inspect(home, state)
            result = {"status": "degraded" if problems else "installed", "problems": problems,
                      "skills": selected_skills(state or {}),
                      "hooks": "registered_trust_unverified" if (state or {}).get("hooks") else "not_requested",
                      "live_invocation_verified": False}
        print(json.dumps(result))
        return 0 if result["status"] != "degraded" else 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    finally:
        if lock is not None:
            lock.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
