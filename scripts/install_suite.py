#!/usr/bin/env python3
"""Install selected skills and automatic user-level guidance; no per-project activation.

The install command selects the disclosed automatic-management defaults. Copying
skill folders alone does not select those defaults or grant coordination authority.
"""

import argparse
import base64
import hashlib
import json
import os
import re
import stat
from pathlib import Path, PurePosixPath
import sys
import tempfile

try:
    import tomllib
except ImportError:  # Python 3.10 remains supported; never guess at TOML syntax.
    tomllib = None

sys.path.insert(0, str(Path(__file__).resolve().parent))
from activation import NAMES as SKILLS, render

# Historical names are recognized only for status, recovery and explicit uninstall.
# They are not aliases in the discovery catalog or supported install selections.
BARE_SKILLS = tuple(name.removeprefix("pm-essential-skills-") for name in SKILLS)
LEGACY_SKILLS = (*BARE_SKILLS, *("ibbuilds-pm-" + name for name in BARE_SKILLS))
OWNED_SKILLS = (*SKILLS, *LEGACY_SKILLS)
ROOT = Path(__file__).resolve().parents[1]
RECEIPT = "pm-essential-skills/install.json"
JOURNAL = "pm-essential-skills/transaction.json"
BEGIN = b"<!-- pm-essential-skills:start -->"
END = b"<!-- pm-essential-skills:end -->"
HELPER = "pm-essential-skills/activation.py"
DEFAULTS = ("Automatic skill use during active local sessions; same-project "
            "continuations within requested work; archive superseded managed sources and temporarily "
            "restore/rearchive for context recovery; preserve opt-outs and other active work. No unrelated "
            "chat messages, deletion, project creation, background jobs, or permission changes.")


def selected_defaults(skills):
    if "pm-essential-skills-context-management" in skills:
        return DEFAULTS
    return ("Automatic use of the selected skills during active local sessions; preserve user preferences. "
            "No chat-management scope is selected.")


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
    """Read regular managed files without blocking on a replaced FIFO/device."""
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return None
    if not stat.S_ISREG(mode):
        raise ValueError(f"Refusing nonregular installation file: {path}; preserve it for recovery")
    try:
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_BINARY", 0)
                             | getattr(os, "O_NONBLOCK", 0)
                             | getattr(os, "O_NOFOLLOW", 0))
    except FileNotFoundError:
        return None
    with os.fdopen(descriptor, "rb") as stream:
        # Recheck the opened object, not only the pathname checked above.
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError(f"Refusing nonregular installation file: {path}; preserve it for recovery")
        return stream.read()


def file_mode(path):
    # Windows chmod does not represent POSIX access bits or ACLs.
    return stat.S_IMODE(path.stat().st_mode) if os.name != "nt" and path.exists() else None


def target_mode(path, data, preferred=None):
    if data is None or os.name == "nt":
        return None
    current = file_mode(path)
    return preferred if preferred is not None else (current if current is not None else 0o600)


def atomic_write(path, data, mode=None):
    if data is None:
        path.unlink(missing_ok=True)
        return
    mode = target_mode(path, data, mode)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".pm-install-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            if mode is not None:
                os.fchmod(stream.fileno(), mode)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def pending_transaction(home):
    return read(safe_path(home, JOURNAL)) is not None


def owned_target(relative):
    return (relative in (RECEIPT, HELPER, "AGENTS.md", "AGENTS.override.md", "hooks.json")
            or any(relative.startswith(f"skills/{name}/") for name in OWNED_SKILLS))


def recover(home):
    """Explicitly roll back an interrupted operation without replacing later edits."""
    journal = safe_path(home, JOURNAL)
    raw = read(journal)
    if raw is None:
        return {"status": "nothing_to_recover"}
    transaction = json.loads(raw)
    if (not isinstance(transaction, dict) or transaction.get("version") != 1
            or not isinstance(transaction.get("files"), dict)):
        raise ValueError("Invalid recovery journal; preserve it for manual recovery")
    originals = {}
    for relative, record in transaction["files"].items():
        if not owned_target(relative) or not isinstance(record, dict):
            raise ValueError("Invalid recovery target; preserve journal for manual recovery")
        path = safe_path(home, relative)
        before, after = decode(record["before"]), decode(record["after"])
        current = read(path)
        current_mode = file_mode(path)
        before_mode, after_mode = record.get("before_mode"), record.get("after_mode")
        for mode in (before_mode, after_mode):
            if mode is not None and (type(mode) is not int or not 0 <= mode <= 0o7777):
                raise ValueError("Invalid recovery mode; preserve journal for manual recovery")
        before_matches = current == before and (before_mode is None or current_mode == before_mode)
        after_matches = current == after and (after_mode is None or current_mode == after_mode)
        if not (before_matches or after_matches):
            raise ValueError(f"Recovery would overwrite later changes: {relative}; preserve the journal")
        originals[path] = (before, before_mode)
    # Validate every target before writing any. The journal remains until rollback
    # finishes, so another interruption can safely resume this same recovery.
    for path, (content, mode) in reversed(list(originals.items())):
        if read(path) != content or (mode is not None and file_mode(path) != mode):
            atomic_write(path, content, mode=mode)
    journal.unlink()
    return {"status": "recovered", "result": "restored_pre_operation_state"}


def apply(changes, home, modes=None):
    """Persist all before/after bytes before touching any managed target."""
    journal = safe_path(home, JOURNAL)
    if pending_transaction(home):
        raise ValueError("Interrupted installation needs recovery; run recover before retrying")
    originals = {path: read(path) for path in changes}
    modes = modes or {}
    before_modes = {path: file_mode(path) for path in changes}
    after_modes = {path: target_mode(path, content, modes.get(path)) for path, content in changes.items()}
    transaction = {"version": 1, "files": {
        path.relative_to(home).as_posix(): {"before": encode(originals[path]), "after": encode(content),
                                          "before_mode": before_modes[path], "after_mode": after_modes[path]}
        for path, content in changes.items()}}
    atomic_write(journal, (json.dumps(transaction, indent=2) + "\n").encode("utf-8"))
    try:
        for path, content in changes.items():
            if content != originals[path] or before_modes[path] != after_modes[path]:
                atomic_write(path, content, mode=after_modes[path])
    except OSError:
        # If rollback itself fails, do not discard its durable recovery evidence.
        recover(home)
        raise
    journal.unlink()


def load_receipt(home):
    raw = read(safe_path(home, RECEIPT))
    if raw is None:
        return None
    state = json.loads(raw)
    if not isinstance(state, dict) or state.get("version") != 1:
        raise ValueError("Unsupported installation receipt; preserve it for recovery")
    if (not isinstance(state.get("files"), dict)
            or type(state.get("instructions_existed")) is not bool
            or not isinstance(state.get("block"), str)):
        raise ValueError("Invalid installation receipt fields; preserve it for recovery")
    if not decode(state["block"]):
        raise ValueError("Invalid receipt instruction block; preserve it for recovery")
    for relative, record in state["files"].items():
        if (not isinstance(record, dict) or "original" not in record
                or (record["original"] is not None and not isinstance(record["original"], str))
                or not isinstance(record.get("sha256"), str)
                or not re.fullmatch(r"[0-9a-f]{64}", record["sha256"])):
            raise ValueError("Invalid receipt file record; preserve it for recovery")
        if relative != HELPER and not any(relative.startswith(f"skills/{name}/") for name in OWNED_SKILLS):
            raise ValueError("Receipt contains an unowned package path")
        safe_path(home, relative)
        decode(record["original"])
        for mode in (record.get("mode"), record.get("original_mode")):
            if mode is not None and (type(mode) is not int or not 0 <= mode <= 0o7777):
                raise ValueError("Invalid receipt mode; preserve it for recovery")
    if state.get("instructions") not in ("AGENTS.md", "AGENTS.override.md"):
        raise ValueError("Invalid global instruction target")
    return state


def active_instructions(home):
    override = safe_path(home, "AGENTS.override.md")
    return "AGENTS.override.md" if (read(override) or b"").strip() else "AGENTS.md"


def selected_skills(state):
    return [name for name in OWNED_SKILLS if f"skills/{name}/SKILL.md" in state.get("files", {})]


def skill_copy_diagnostics(home, state, extra_roots):
    """Inspect explicit roots only; candidate files do not establish host discovery."""
    candidates = {name: [] for name in selected_skills(state or {})}
    roots, errors = [], []
    for supplied in [home / "skills", *extra_roots]:
        root = Path(supplied).expanduser()
        try:
            root = root.resolve()
            if str(root) in roots:
                continue
            roots.append(str(root))
            if not stat.S_ISDIR(root.stat().st_mode):
                raise NotADirectoryError(str(root))
        except (OSError, RuntimeError) as exc:
            errors.append({"path": str(root), "error": str(exc)})
            continue
        for name, paths in candidates.items():
            path = root / name / "SKILL.md"
            try:
                mode = path.stat().st_mode
                if stat.S_ISREG(mode):
                    physical = str(path.resolve())
                    if physical not in paths:
                        paths.append(physical)
            except FileNotFoundError:
                pass
            except (OSError, RuntimeError) as exc:
                errors.append({"path": str(path), "error": str(exc)})
    return {"roots": roots, "candidates": candidates,
            "possible_duplicates": [name for name, paths in candidates.items() if len(paths) > 1],
            "inspection_errors": errors, "activation": "unknown",
            "coverage": "receipt-installed names in managed and explicitly supplied roots only"}


def configuration_diagnostics(home, state, profile=None):
    """Inspect user layers only, never claim the running host's effective state."""
    if profile is not None and not re.fullmatch(r"[A-Za-z0-9_-]+", profile):
        raise ValueError("Invalid --profile: use a nonempty ASCII letter/number/underscore/hyphen name")
    result = {"status": "inspected", "scope": "base_and_selected_profile" if profile else "base_user_config",
              "profile": profile, "files": [], "configured_disabled_skills": [],
              "include_instructions": None, "warnings": [], "user_layer_resolution_complete": True,
              "effective_activation": "unknown", "session_overrides": "not_inspected",
              "next_steps": ["Compare with the profile and session overrides used to launch Codex; "
                             "these read-only checks do not verify model invocation."]}
    if tomllib is None:
        result.update(status="unavailable", user_layer_resolution_complete=False)
        result["warnings"].append("TOML diagnostics require Python 3.11+ stdlib tomllib; installation still supports Python 3.10.")
        return result
    names = selected_skills(state or {})
    paths = {name: (home / "skills" / name / "SKILL.md").resolve() for name in names}
    disabled = set()
    for filename in ["config.toml", *([f"{profile}.config.toml"] if profile else [])]:
        item = {"path": str(home / filename), "status": "parsed"}
        result["files"].append(item)
        try:
            path = safe_path(home, filename)
            if not path.exists():
                item["status"] = "missing"
                continue
            # Avoid special-file blocking and unbounded reads; never emit config contents.
            if not path.is_file() or path.stat().st_size > 1024 * 1024:
                raise ValueError("Unsupported configuration file")
            descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_BINARY", 0)
                                 | getattr(os, "O_NONBLOCK", 0)
                                 | getattr(os, "O_NOFOLLOW", 0))
            with os.fdopen(descriptor, "rb") as stream:
                if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                    raise ValueError("Unsupported configuration file")
                raw = stream.read(1024 * 1024 + 1)
            if len(raw) > 1024 * 1024:
                raise ValueError("Oversized configuration file")
            config = tomllib.loads(raw.decode("utf-8"))
        except (OSError, ValueError, RuntimeError, RecursionError):
            item["status"] = "invalid_or_unreadable"
            result["status"] = "partial"
            result["user_layer_resolution_complete"] = False
            result["warnings"].append(f"Could not safely parse {filename}; no contents or parser errors are displayed.")
            continue
        if "profile" in config or (profile and isinstance(config.get("profiles"), dict)
                                   and profile in config["profiles"]):
            result["warnings"].append("Legacy profile configuration is present; modern Codex requires separate NAME.config.toml profiles.")
            result["user_layer_resolution_complete"] = False
            result["status"] = "partial"
        skills = config.get("skills", {})
        if not isinstance(skills, dict):
            result["warnings"].append(f"Invalid skills table in {filename}.")
            result["user_layer_resolution_complete"] = False
            result["status"] = "partial"
            continue
        rules = skills.get("config", [])
        include = skills.get("include_instructions")
        bundled = skills.get("bundled", {})
        budget = skills.get("max_context_tokens")
        if (not isinstance(bundled, dict)
                or ("enabled" in bundled and type(bundled["enabled"]) is not bool)
                or (budget is not None and (type(budget) is not int or budget <= 0))
                or not isinstance(rules, list) or (include is not None and type(include) is not bool)
                or any(not isinstance(rule, dict) or type(rule.get("enabled")) is not bool
                       or any(key in rule and not isinstance(rule[key], str) for key in ("name", "path"))
                       for rule in rules)):
            result["warnings"].append(f"Invalid skill configuration types in {filename}; layer not interpreted.")
            result["user_layer_resolution_complete"] = False
            result["status"] = "partial"
            continue
        if include is not None:
            result["include_instructions"] = include
        for rule in rules:
            has_name, has_path = "name" in rule, "path" in rule
            if has_name == has_path or (has_name and not rule["name"].strip()):
                result["warnings"].append(f"Ignored skill rule with ambiguous or empty selector in {filename}.")
                continue
            if has_name:
                matched = [name for name in names if name == rule["name"].strip()]
            else:
                try:
                    text_path = rule["path"]
                    selected = Path(text_path)
                    if text_path == "~" or text_path.startswith("~/") or (os.name == "nt" and text_path.startswith("~\\")):
                        selected = selected.expanduser()
                    selected = (selected if selected.is_absolute() else home / selected).resolve()
                    matched = [name for name in names if paths[name] == selected]
                except (OSError, ValueError, RuntimeError):
                    result["user_layer_resolution_complete"] = False
                    result["status"] = "partial"
                    result["warnings"].append(f"Could not resolve a skill path selector in {filename}.")
                    continue
            for name in matched:
                disabled.discard(name) if rule["enabled"] else disabled.add(name)
    result["configured_disabled_skills"] = [name for name in names if name in disabled]
    if disabled:
        result["warnings"].append("User-layer rules disable installed skills in the native catalog. Global pointers and optional hooks still refer to files; this is not an access-control guarantee.")
        result["next_steps"].append("Review intentional opt-outs alongside the managed global instruction block and optional reminders; no settings were changed.")
    if result["include_instructions"] is False:
        result["warnings"].append("User layers set skills.include_instructions=false; this suppresses the automatic skills instructions block, not generic file reads.")
    if not result["user_layer_resolution_complete"]:
        result["warnings"].append("Reported values cover successfully interpreted layers only; unresolved layers may change them.")
    return result


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
            # Hooks execute in the session shell, not through CreateProcess argv.
            # An ASCII encoded wrapper works through both PowerShell and cmd;
            # paths are literal PowerShell strings, never interpolated code.
            quoted = ["'" + value.replace("'", "''") + "'" for value in (sys.executable, str(helper))]
            script = "$input | & " + " ".join(quoted) + "; exit $LASTEXITCODE"
            payload = base64.b64encode(script.encode("utf-16le")).decode("ascii")
            command = "powershell.exe -NoProfile -NonInteractive -EncodedCommand " + payload
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
        if (data is None or digest(data) != record["sha256"]
                or (record.get("mode") is not None and file_mode(safe_path(home, relative)) != record["mode"])):
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
    if pending_transaction(home):
        raise ValueError("Interrupted installation needs recovery; run recover before retrying")
    legacy = [name for name in LEGACY_SKILLS
              if (home / "skills" / name).exists() or (home / "skills" / name).is_symlink()
              or any(path.startswith(f"skills/{name}/") for path in (state or {}).get("files", {}))]
    if legacy:
        raise ValueError("Legacy skill names need explicit migration; no files changed: "
                         + ", ".join(legacy) + ". Back up edits and opt-outs; see docs/skill-naming-migration.md.")
    if state is not None:
        problems = inspect(home, state)
        if problems:
            raise ValueError("Preserving modified installation: " + ", ".join(problems))
    requested = tuple(skills) if skills is not None else tuple(
        name for name in SKILLS if (ROOT / "skills" / name / "SKILL.md").is_file())
    if not requested or set(requested) - set(SKILLS):
        raise ValueError("Choose at least one available skill")
    changes, modes, files = {}, {}, dict((state or {}).get("files", {}))
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
                               "sha256": digest(data), "mode": target_mode(target, data),
                               "original_mode": previous.get("original_mode") if previous else file_mode(target)}
            changes[target] = data
    if with_hooks or (state or {}).get("hooks"):
        target = safe_path(home, HELPER)
        data = (ROOT / "scripts/activation.py").read_bytes()
        previous = (state or {}).get("files", {}).get(HELPER)
        files[HELPER] = {"original": previous["original"] if previous else encode(read(target)),
                         "sha256": digest(data), "mode": target_mode(target, data),
                         "original_mode": previous.get("original_mode") if previous else file_mode(target)}
        changes[target] = data
    for relative, record in (state or {}).get("files", {}).items():
        if relative not in files:
            changes[safe_path(home, relative)] = decode(record["original"])
            modes[safe_path(home, relative)] = record.get("original_mode")
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
               "block": encode(block), "defaults": selected_defaults(skills), "skills": skills}
    if with_hooks or (state or {}).get("hooks"):
        hook_bytes, owned = hooks_content(home, (state or {}).get("hooks"), add=True)
        changes[safe_path(home, "hooks.json")] = hook_bytes
        receipt["hooks"] = owned
    # The durable journal retains retired-file backups and the previous receipt
    # until every write succeeds, including during interrupted upgrades.
    ordered = {safe_path(home, RECEIPT): (json.dumps(receipt, indent=2) + "\n").encode("utf-8")}
    ordered.update(changes)
    apply(ordered, home, modes)
    return {"status": "installed", "package_files": len(files), "instructions": str(target),
            "activation": "next_host_instruction_reload", "live_invocation_verified": False,
            "skills": skills, "hooks": "registered_trust_unverified" if receipt.get("hooks") else "not_requested",
            "defaults": selected_defaults(skills)}


def uninstall(home, state):
    if pending_transaction(home):
        raise ValueError("Interrupted installation needs recovery; run recover before retrying")
    if state is None:
        return {"status": "not_installed"}
    problems = inspect(home, state)
    # A new override does not prevent removing our unchanged block from its original file.
    problems = [item for item in problems if item != "global_rule_shadowed_by_override"]
    if problems:
        raise ValueError("Preserving modified installation: " + ", ".join(problems))
    changes = {safe_path(home, relative): decode(record["original"])
               for relative, record in state["files"].items()}
    modes = {safe_path(home, relative): record.get("original_mode")
             for relative, record in state["files"].items()}
    target = safe_path(home, state["instructions"])
    remaining = target.read_bytes().replace(decode(state["block"]), b"", 1)
    changes[target] = remaining if remaining or state["instructions_existed"] else None
    if state.get("hooks"):
        changes[safe_path(home, "hooks.json")] = hooks_content(home, state["hooks"])[0]
    changes[safe_path(home, RECEIPT)] = None
    apply(changes, home, modes)
    return {"status": "uninstalled", "user_instructions_preserved": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__, epilog=DEFAULTS)
    parser.add_argument("command", choices=("install", "status", "uninstall", "recover"))
    parser.add_argument("--skill", choices=SKILLS, action="append", help="Install only this skill; repeat to select several")
    parser.add_argument("--hooks", action="store_true", help="Also register per-turn reminders; Codex trust is still required")
    parser.add_argument("--check-skill-root", type=Path, action="append",
                        help="Status only: check an additional skills directory for candidate copies; repeat as needed")
    parser.add_argument("--profile", help="Status only: inspect NAME.config.toml after base user config")
    parser.add_argument("--codex-home", type=Path,
                        default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")))
    args = parser.parse_args()
    home = args.codex_home.expanduser().resolve()
    lock = None
    try:
        if args.command != "install" and (args.skill or args.hooks):
            raise ValueError("--skill and --hooks apply to installation only")
        if args.command != "status" and args.profile is not None:
            raise ValueError("--profile applies to status only")
        if args.command != "status" and args.check_skill_root:
            raise ValueError("--check-skill-root applies to status only")
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
        if args.command == "recover":
            result = recover(home)
            print(json.dumps(result))
            return 0
        if pending_transaction(home):
            raise ValueError("Interrupted installation needs recovery; run recover before retrying")
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
            result["configuration_diagnostics"] = configuration_diagnostics(home, state, args.profile)
            if args.check_skill_root:
                result["skill_copy_diagnostics"] = skill_copy_diagnostics(home, state, args.check_skill_root)
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
