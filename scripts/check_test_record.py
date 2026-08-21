#!/usr/bin/env python3
"""Warn (non-fatal) if a PR touches SKILL.md but adds no new file under
tests/results/, per the rule in CONTRIBUTING.md ("Skill content changes").

Usage: check_test_record.py <base-ref> <head-ref>
"""

import subprocess
import sys


def changed_files(base_ref, head_ref):
    result = subprocess.run(
        ["git", "diff", "--name-status", f"{base_ref}...{head_ref}"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.splitlines()


def main():
    if len(sys.argv) != 3:
        print("usage: check_test_record.py <base-ref> <head-ref>")
        sys.exit(2)

    base_ref, head_ref = sys.argv[1], sys.argv[2]
    lines = changed_files(base_ref, head_ref)

    skill_changed = any(
        line.split("\t")[-1] == "SKILL.md" and not line.startswith("D")
        for line in lines
    )
    if not skill_changed:
        print("SKILL.md not changed in this PR — nothing to check.")
        return

    new_test_result = any(
        line.startswith("A") and line.split("\t")[-1].startswith("tests/results/")
        for line in lines
    )

    if new_test_result:
        print("OK: SKILL.md changed and a new file was added under tests/results/.")
        return

    print(
        "::warning::This PR changes SKILL.md but does not add a new file under "
        "tests/results/. Per CONTRIBUTING.md, non-trivial SKILL.md changes should "
        "have a with-skill vs. baseline scenario run recorded. If this change is "
        "trivial (typo, formatting) or the existing test results still apply, "
        "no action is needed — this is a reminder, not a blocker."
    )


if __name__ == "__main__":
    main()
