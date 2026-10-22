#!/usr/bin/env python3
"""No-dependency Agent Skills frontmatter/link preflight.

This is an additional repository-specific check, not a replacement for the
canonical `skills-ref validate` utility from agentskills/agentskills.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
SKILLS = [ROOT, ROOT / "chapters/gravity-physics", ROOT / "chapters/fluid-physics"]
ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def check_skill(folder: Path) -> list[str]:
    errors: list[str] = []
    path = folder / "SKILL.md"
    if not path.exists():
        return [f"missing {path}"]
    raw = path.read_text(encoding="utf8")
    parts = raw.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        return [f"{path}: invalid frontmatter fences"]
    front = parts[1].strip().splitlines()
    vals = {}
    for ln in front:
        if not ln.strip() or ln.startswith(" ") or ln.startswith("\t"):
            continue  # nested metadata
        if ":" not in ln:
            errors.append(f"{path}: malformed YAML top-level field: {ln}")
            continue
        key, value = ln.split(":", 1)
        if key not in ALLOWED_KEYS:
            errors.append(f"{path}: unexpected field {key}")
        vals[key] = value.strip().strip('"\'')
    name = vals.get("name", "")
    description = vals.get("description", "")
    if name != folder.name or not SKILL_NAME.fullmatch(name) or len(name) > 64:
        errors.append(f"{path}: invalid name/folder mismatch: {name}")
    if not 1 <= len(description) <= 1024:
        errors.append(f"{path}: description length invalid")
    if len(raw.splitlines()) >= 500:
        errors.append(f"{path}: >500 lines: split into references")
    if not parts[2].strip():
        errors.append(f"{path}: no instructions")
    for link in MARKDOWN_LINK.findall(raw):
        if link.startswith(("http://", "https://", "#", "mailto:")):
            continue
        linkpath = link.split("#", 1)[0]
        if not linkpath:
            continue
        if not (folder / linkpath).resolve().is_file():
            errors.append(f"{path}: missing local link {link}")
    return errors


def main() -> int:
    errors = [e for folder in SKILLS for e in check_skill(folder)]
    for folder in SKILLS:
        for ref in folder.rglob("*.md"):
            if ref.name == "SKILL.md":
                continue
            for link in MARKDOWN_LINK.findall(ref.read_text(encoding="utf8")):
                if link.startswith(("https://", "http://", "#", "mailto:")):
                    continue
                file = (ref.parent / link.split("#", 1)[0]).resolve()
                if not file.is_file():
                    errors.append(f"{ref}: missing local link {link}")
    if errors:
        print("\n".join("FAIL: " + e for e in errors))
        return 1
    print("PASS: 3 skill manifests, local links and instructions validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
