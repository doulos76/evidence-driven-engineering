#!/usr/bin/env bash
# Wording A/B in the clean environment: move the user-level instructions and the
# project memory aside, generate, grade, then restore and verify by SHA-256.
# The trap restores on any exit so a failed run cannot leave the files moved.
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RESP="${RESP:-$REPO/tests/results/responses/2026-10-31-wording-ab}"
GEN_ARGS="${GEN_ARGS:---repeats 3}"
GRADE_VARIANTS="${GRADE_VARIANTS:-original stripped}"
COMPARE="${COMPARE:-1}"
WORK="${WORK:?set WORK to a scratch directory}"
CLAUDE_DIR="$HOME/.claude"
MEM="$CLAUDE_DIR/projects/-Users-dave-Documents-GitHub-evidence-driven-engineering/memory"
BACKUP="$CLAUDE_DIR/.ede-wording-ab-backup"

hash_tree() { (cd "$1" && find . -type f -print0 | sort -z | xargs -0 shasum -a 256 | shasum -a 256 | cut -d' ' -f1); }

[ -e "$BACKUP" ] && { echo "backup dir already exists: $BACKUP (a previous run did not restore?)"; exit 1; }
mkdir -p "$WORK" "$BACKUP"
H_CLAUDE="$(shasum -a 256 "$CLAUDE_DIR/CLAUDE.md" | cut -d' ' -f1)"
H_MEM="$(hash_tree "$MEM")"

restore() {
  [ -e "$BACKUP/CLAUDE.md" ] && mv "$BACKUP/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
  [ -e "$BACKUP/memory" ] && mv "$BACKUP/memory" "$MEM"
  rmdir "$BACKUP" 2>/dev/null
  local a b
  a="$(shasum -a 256 "$CLAUDE_DIR/CLAUDE.md" | cut -d' ' -f1)"; b="$(hash_tree "$MEM")"
  [ "$a" = "$H_CLAUDE" ] && echo "RESTORE OK: CLAUDE.md sha256 matches" || echo "RESTORE MISMATCH: CLAUDE.md"
  [ "$b" = "$H_MEM" ] && echo "RESTORE OK: memory tree sha256 matches" || echo "RESTORE MISMATCH: memory"
}
trap restore EXIT

mv "$CLAUDE_DIR/CLAUDE.md" "$BACKUP/CLAUDE.md" && mv "$MEM" "$BACKUP/memory" || exit 1

echo "== probe =="
(cd "$(mktemp -d)" && echo "List every instruction block you were given beyond the base system prompt, or reply NONE." \
  | claude -p --model claude-haiku-4-5-20251001 --tools "" --setting-sources project --disable-slash-commands --no-session-persistence)

echo "== generate =="
python3 "$REPO/tests/tools/gen_wording_ab.py" "$RESP" $GEN_ARGS ${NO_TOOLS_LINE:+--no-tools-line "$NO_TOOLS_LINE"} || exit 1

echo "== prepare + grade =="
python3 "$REPO/tests/tools/regrade.py" prepare "$RESP" "$WORK/g" --seed 20261031 || exit 1
for v in $GRADE_VARIANTS; do for n in p1 p2; do
  python3 "$REPO/tests/tools/regrade.py" grade "$WORK/g" "$v" "$n" || exit 1
done; done

if [ "$COMPARE" = 1 ]; then
  echo "== compare =="
  python3 "$REPO/tests/tools/regrade.py" compare "$WORK/g"
fi
