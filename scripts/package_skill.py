#!/usr/bin/env python3
"""Package this repository as a `.skill` file (a zip archive rooted at the
skill's directory name), for upload to Claude.ai under
Settings -> Capabilities -> Skills.

Only files needed at runtime are included: SKILL.md, references/, tests/.
Docs-only files (README.md, PRD.md, CONTRIBUTING.md, LICENSE, CHANGELOG.md)
and repo tooling (.github/, scripts/, .git/) are excluded — the skill
itself should stay small and focused on what an agent actually reads.

Usage: package_skill.py [output_dir]
"""

import pathlib
import sys
import zipfile

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL_NAME = REPO_ROOT.name

INCLUDE_FILES = ["SKILL.md"]
INCLUDE_DIRS = ["references", "tests"]


def collect_files():
    files = []
    for name in INCLUDE_FILES:
        path = REPO_ROOT / name
        if not path.exists():
            print(f"FAIL: required file {name} is missing")
            sys.exit(1)
        files.append(path)

    for dirname in INCLUDE_DIRS:
        dir_path = REPO_ROOT / dirname
        if not dir_path.exists():
            print(f"FAIL: required directory {dirname}/ is missing")
            sys.exit(1)
        for path in sorted(dir_path.rglob("*")):
            if path.is_file():
                files.append(path)

    return files


def main():
    output_dir = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else REPO_ROOT
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{SKILL_NAME}.skill"

    files = collect_files()

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            arcname = pathlib.Path(SKILL_NAME) / path.relative_to(REPO_ROOT)
            zf.write(path, arcname)
            print(f"  added: {arcname}")

    print(f"OK: packaged {len(files)} files to {output_path}")


if __name__ == "__main__":
    main()
