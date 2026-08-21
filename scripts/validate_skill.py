#!/usr/bin/env python3
"""Validate SKILL.md's YAML frontmatter for the Agent Skills format.

Checks:
- the file starts with a `---` delimited frontmatter block
- the frontmatter is valid YAML
- required fields (name, description) are present and non-empty
- name matches the skill's directory name (the repo root)
"""

import pathlib
import sys

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL_PATH = REPO_ROOT / "SKILL.md"
REQUIRED_FIELDS = ("name", "description")


def fail(message):
    print(f"FAIL: {message}")
    sys.exit(1)


def main():
    if not SKILL_PATH.exists():
        fail(f"{SKILL_PATH} does not exist")

    text = SKILL_PATH.read_text(encoding="utf-8")

    if not text.startswith("---\n"):
        fail("SKILL.md must start with a '---' YAML frontmatter delimiter")

    parts = text.split("---\n", 2)
    if len(parts) < 3:
        fail("SKILL.md frontmatter block is not closed with a second '---'")

    frontmatter_raw = parts[1]

    try:
        frontmatter = yaml.safe_load(frontmatter_raw)
    except yaml.YAMLError as exc:
        fail(f"frontmatter is not valid YAML: {exc}")

    if not isinstance(frontmatter, dict):
        fail("frontmatter must be a YAML mapping (key: value pairs)")

    for field in REQUIRED_FIELDS:
        value = frontmatter.get(field)
        if not value or not str(value).strip():
            fail(f"frontmatter is missing required non-empty field '{field}'")

    expected_name = REPO_ROOT.name
    actual_name = frontmatter["name"]
    if actual_name != expected_name:
        fail(
            f"frontmatter name '{actual_name}' does not match "
            f"repository directory name '{expected_name}'"
        )

    body = parts[2]
    if not body.strip():
        fail("SKILL.md has no content after the frontmatter block")

    print("OK: SKILL.md frontmatter is valid")
    print(f"  name: {frontmatter['name']}")
    print(f"  description: {frontmatter['description'][:80]}...")


if __name__ == "__main__":
    main()
