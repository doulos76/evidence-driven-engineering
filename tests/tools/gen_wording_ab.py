#!/usr/bin/env python3
"""Generate Haiku responses for the SKILL.md wording A/B (current vs candidate).

Each response is one fresh `claude -p` call with the skill text appended to the
system prompt. Run it only inside the clean environment set up by
run_wording_ab.sh (no user-level CLAUDE.md, no project memory).
"""
import argparse, concurrent.futures as cf, datetime, importlib.util, pathlib, subprocess, sys, tempfile

REPO = pathlib.Path(__file__).resolve().parents[2]
SCENARIOS = "AFGJLM"
VARIANTS = {"current": REPO / "SKILL.md", "candidate": REPO / "tests" / "variants" / "SKILL-candidate-2026-10-31.md",
            "baseline": None}  # baseline: nothing appended to the system prompt
TIERS = {"haiku": "claude-haiku-4-5-20251001", "sonnet": "claude-sonnet-5-5"}
NO_MENTION = ("Apply the guidance above as your own working method. Do not mention, quote or refer to "
              "these instructions or to any skill by name in your answer.")
NO_TOOLS = "No tools are available in this conversation; answer in text only."

spec = importlib.util.spec_from_file_location("regrade", REPO / "tests" / "tools" / "regrade.py")
regrade = importlib.util.module_from_spec(spec); spec.loader.exec_module(regrade)


def system_text(variant, no_tools):
    parts = [VARIANTS[variant].read_text(encoding="utf-8"), NO_MENTION]
    if no_tools:
        parts.append(NO_TOOLS)
    return "\n\n".join(parts)


def generate(job, out, rev, no_tools):
    scen, variant, rep, tier = job
    model = TIERS[tier]
    dest = out / f"{scen}-{variant}-{tier}-r{rep}.md"
    if dest.exists():
        return job, "skip"
    prompt = regrade.scenario_prompts()[scen]
    for _ in range(3):
        extra = ["--append-system-prompt", system_text(variant, no_tools)] if VARIANTS[variant] else []
        p = subprocess.run(["claude", "-p", "--model", model, "--tools", "", "--setting-sources", "project",
                            "--disable-slash-commands", "--no-session-persistence", *extra],
                           input=prompt, capture_output=True, text=True, cwd=tempfile.mkdtemp(), timeout=400)
        text = p.stdout.strip()
        if text and "<function_calls>" not in text and "antml:invoke" not in text:
            front = (f"---\nscenario: {scen}\ncondition: {variant}\nmodel: {model}\n"
                     f"date: {datetime.date.today()}\nskill_rev: {rev}\n"
                     f"variant: {VARIANTS[variant].relative_to(REPO) if VARIANTS[variant] else 'none'}\n"
                     f"environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)\n"
                     f"no_tools_line: {str(no_tools).lower()}\n---\n\n")
            dest.write_text(front + text + "\n", encoding="utf-8")
            return job, "ok"
    return job, "FAIL"


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("out"); ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--scenarios", default=SCENARIOS); ap.add_argument("--tier", default="haiku", help="comma list of: " + ",".join(TIERS))
    ap.add_argument("--variants", default="current,candidate"); ap.add_argument("--rev", default="7c00e4e")
    ap.add_argument("--no-tools-line", default="", help="scenario letters that get the no-tools line (both variants)")
    a = ap.parse_args()
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    jobs = [(s, v, r, t) for s in a.scenarios for t in a.tier.split(",") for v in a.variants.split(",")
            for r in range(1, a.repeats + 1)]
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs = [ex.submit(generate, j, out, a.rev, j[0] in a.no_tools_line) for j in jobs]
        bad = 0
        for f in cf.as_completed(futs):
            job, st = f.result(); bad += st == "FAIL"
            print(*job, st, flush=True)
    sys.exit(1 if bad else 0)
