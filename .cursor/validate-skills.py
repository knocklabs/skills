#!/usr/bin/env python3
"""Validate Knock skill directories against the structure in AGENTS.md."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
REQUIRED_RULE_KEYS = ("title", "description", "tags", "category", "last_updated")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RULE_LINK_RE = re.compile(r"rules/([a-z0-9-]+\.md)")
JSON_FILES = (
    "plugin.json",
    "mcp.json",
    ".mcp.json",
    ".cursor-plugin/plugin.json",
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
)


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path.relative_to(ROOT)}: missing frontmatter")
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError(f"{path.relative_to(ROOT)}: unterminated frontmatter")
    data: dict = {}
    current_key: str | None = None
    for raw in text[4:end].splitlines():
        if not raw.strip():
            continue
        if raw.startswith("  - ") or raw.startswith("- "):
            if current_key is None:
                raise ValueError(f"{path.relative_to(ROOT)}: list item without a key")
            items = data.setdefault(current_key, [])
            if not isinstance(items, list):
                raise ValueError(f"{path.relative_to(ROOT)}: {current_key} is not a list")
            items.append(raw.split("- ", 1)[1].strip())
            continue
        if ":" not in raw:
            raise ValueError(f"{path.relative_to(ROOT)}: cannot parse {raw!r}")
        key, value = raw.split(":", 1)
        current_key = key.strip()
        value = value.strip().strip('"').strip("'")
        data[current_key] = [] if value == "" else value
    return data


def main() -> int:
    errors: list[str] = []
    if not SKILLS.is_dir():
        print("skills/ directory is missing", file=sys.stderr)
        return 1

    skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir())
    if not skill_dirs:
        errors.append("no skill directories found")

    for skill in skill_dirs:
        if not skill.name.startswith("knock-"):
            errors.append(f"{skill.name}: directory must start with knock-")
        skill_md = skill / "SKILL.md"
        rules_dir = skill / "rules"
        if not skill_md.is_file():
            errors.append(f"{skill.name}: missing SKILL.md")
            continue
        if not rules_dir.is_dir():
            errors.append(f"{skill.name}: missing rules/")
            continue
        try:
            meta = parse_frontmatter(skill_md)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if meta.get("name") != skill.name:
            errors.append(f"{skill.name}: SKILL.md name is {meta.get('name')!r}")
        if not str(meta.get("description", "")).strip():
            errors.append(f"{skill.name}: SKILL.md description is empty")

        linked = set(RULE_LINK_RE.findall(skill_md.read_text(encoding="utf-8")))
        rule_files = sorted(path for path in rules_dir.glob("*.md") if path.is_file())
        if not rule_files:
            errors.append(f"{skill.name}: rules/ has no markdown files")
        for rule in rule_files:
            if rule.name not in linked:
                errors.append(f"{skill.name}: {rule.name} is not referenced from SKILL.md")
            try:
                rule_meta = parse_frontmatter(rule)
            except ValueError as exc:
                errors.append(str(exc))
                continue
            relative = rule.relative_to(ROOT)
            for key in REQUIRED_RULE_KEYS:
                if key not in rule_meta or rule_meta[key] in ("", [], None):
                    errors.append(f"{relative}: missing {key}")
            if rule_meta.get("category") != skill.name:
                errors.append(
                    f"{relative}: category {rule_meta.get('category')!r} != {skill.name}"
                )
            updated = str(rule_meta.get("last_updated", ""))
            if not DATE_RE.match(updated):
                errors.append(f"{relative}: last_updated {updated!r} is not YYYY-MM-DD")
            tags = rule_meta.get("tags")
            if not isinstance(tags, list) or not tags:
                errors.append(f"{relative}: tags must be a non-empty list")
        for name in sorted(linked):
            if not (rules_dir / name).is_file():
                errors.append(f"{skill.name}: SKILL.md links missing rules/{name}")

    for rel in JSON_FILES:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"{rel}: missing")
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{rel}: invalid JSON ({exc})")

    if errors:
        print("Skill validation failed:")
        for err in errors:
            print(f"  - {err}")
        return 1

    rule_count = sum(1 for _ in SKILLS.glob("*/rules/*.md"))
    print(f"Validated {len(skill_dirs)} skills and {rule_count} rules.")
    for skill in skill_dirs:
        count = len(list((skill / "rules").glob("*.md")))
        print(f"  - {skill.name} ({count} rules)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
