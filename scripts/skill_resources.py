"""Check that a skill's linked local resources ship with that skill alone.

Used only by maintainer validation and archive builders; no runtime hooks.
"""

from pathlib import Path
import re
from urllib.parse import unquote


def resource_errors(folder):
    folder = Path(folder).resolve()
    errors = []
    for path in sorted(folder.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"^(`{3,}|~{3,}).*?^\1\s*$", "", text,
                      flags=re.MULTILINE | re.DOTALL)
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            target = target.strip()
            if re.match(r"^[A-Za-z]:[/\\]", target) or target.lower().startswith("file:"):
                errors.append(f"Resource outside independent skill: {path.relative_to(folder)}: {target}")
                continue
            if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target) or target.startswith("#"):
                continue
            local = unquote(target.split("#", 1)[0].strip("<>"))
            resolved = (path.parent / local).resolve()
            label = f"{path.relative_to(folder)}: {target}"
            if not resolved.is_relative_to(folder):
                errors.append(f"Resource outside independent skill: {label}")
            elif not resolved.exists():
                errors.append(f"Missing skill resource: {label}")
    return errors
