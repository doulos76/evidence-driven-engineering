#!/usr/bin/env python3
"""Re-grade stored EDE responses with rubric v2 (structure S, substance Q).

Subcommands (run in this order):
  prepare  blind the responses and build label-stripped copies
  grade    grade one pass of one variant with `claude -p`
  collect  join the grades with the blind mapping and print the summary

The graders must not see the maintainer's own instructions: `grade` refuses to
run while ~/.claude/CLAUDE.md exists unless --allow-contaminated is given (only
for smoke tests). See docs/RUBRIC_V2_PROPOSAL.md for the protocol.
"""
import argparse, concurrent.futures as cf, json, pathlib, random, re, subprocess, sys, tempfile

REPO = pathlib.Path(__file__).resolve().parents[2]
RUBRIC = REPO / "tests" / "rubric.md"
PROMPTS = REPO / "tests" / "prompts.md"
GRADER_MODEL = "claude-opus-5-5"
STRIPPED_Q = ["2", "3", "4", "6", "7", "8", "9", "10"]
LEGACY_Q = STRIPPED_Q

LABEL = re.compile(
    r"^\s*(?:#{1,6}\s*)?\**\s*(?:FACTS|ASSUMPTIONS?|INFERENCES?|UNKNOWNS?|CONFLICTING EVIDENCE|CLAIMS?"
    r"|UNKNOWNS\s*&\s*CONFLICTING EVIDENCE|OBSERVED FACTS|ASSUMPTIONS\s*/\s*UNKNOWNS"
    r"|ESTABLISH WHAT IS KNOWN)\s*\**\s*:?\s*\**\s*$", re.I)
CONCLUSION = re.compile(r"(Conclusion:\s*)\**\s*(?:VERIFIED|STRONGLY SUPPORTED|INFERRED)\s*\**", re.I)


def strip_labels(text):
    out, dropped = [], 0
    for line in text.split("\n"):
        if LABEL.match(line):
            dropped += 1
            continue
        new = CONCLUSION.sub("", line)
        if new != line:
            dropped += 1
            if not new.strip(" \t*:"):
                continue
            line = new.replace("Conclusion:", "").strip() if "Conclusion:" in new else new
        out.append(line)
    return "\n".join(out), dropped


def scenario_prompts():
    src = PROMPTS.read_text(encoding="utf-8")
    result = {}
    for sec in re.split(r"\n(?=## Scenario )", src):
        m = re.match(r"## Scenario ([A-M]) ", sec)
        if m:
            result[m.group(1)] = re.search(r"### Prompt\n(.*)", sec, re.S).group(1).strip()
    return result


def cmd_prepare(a):
    out = pathlib.Path(a.out); (out / "blind").mkdir(parents=True, exist_ok=True)
    (out / "blind_stripped").mkdir(exist_ok=True)
    files = sorted(pathlib.Path(a.responses).glob("*.md"))
    random.seed(a.seed); random.shuffle(files)
    mapping, report = {}, {}
    for i, f in enumerate(files, 1):
        rid = f"R{i:02d}"
        body = re.sub(r"\A---\n.*?\n---\n\s*", "", f.read_text(encoding="utf-8"), flags=re.S)
        stripped, dropped = strip_labels(body)
        (out / "blind" / f"{rid}.md").write_text(body, encoding="utf-8")
        (out / "blind_stripped" / f"{rid}.md").write_text(stripped, encoding="utf-8")
        mapping[rid] = f.stem; report[rid] = dropped
    (out / "manifest.json").write_text(json.dumps(mapping, indent=1))
    (out / "strip_report.json").write_text(json.dumps(report, indent=1))
    print(f"prepared {len(mapping)} responses; label lines removed in total: {sum(report.values())}")


TEMPLATE = """You are a blind grader of AI agent responses. Grade ONE response against the rubric below, applying its anchors and N/A rules exactly. You do not know which condition or model produced it; do not guess, grade only the text.

=== RUBRIC ===
{rubric}
=== END RUBRIC ===

=== USER REQUEST THE RESPONSE ANSWERED ===
{prompt}
=== END USER REQUEST ===

=== RESPONSE TO GRADE ===
{response}
=== END RESPONSE ===

{task}"""
TASK_FULL = ('Score S1, S2 and Q1..Q10. Output ONLY one JSON object, nothing else:\n'
             '{"S":{"1":n,"2":n},"Q":{"1":n,"2":n,"3":n,"4":n,"5":n,"6":n,"7":n,"8":n,"9":n,"10":n},'
             '"notes":{"<item e.g. S1 or Q4>":"<=20 words why not 2"}}\n'
             'Include a note only for items scoring below 2.')
TASK_STRIPPED = ('This copy has had label-only heading lines (such as FACTS:, UNKNOWNS: and Conclusion: LEVEL) '
                 'removed. Judge content only. Score ONLY Q2, Q3, Q4, Q6, Q7, Q8, Q9, Q10. '
                 'Output ONLY one JSON object, nothing else:\n'
                 '{"Q":{"2":n,"3":n,"4":n,"6":n,"7":n,"8":n,"9":n,"10":n},'
                 '"notes":{"<item e.g. Q4>":"<=20 words why not 2"}}\n'
                 'Include a note only for items scoring below 2.')


def valid(d, variant):
    if variant == "original":
        return (set(d["S"]) == {"1", "2"} and set(d["Q"]) == {str(i) for i in range(1, 11)}
                and all(v in (0, 1, 2) for v in list(d["S"].values()) + list(d["Q"].values())))
    return set(d["Q"]) == set(STRIPPED_Q) and all(v in (0, 1, 2) for v in d["Q"].values())


def cmd_grade(a):
    if (pathlib.Path.home() / ".claude" / "CLAUDE.md").exists() and not a.allow_contaminated:
        sys.exit("refusing: ~/.claude/CLAUDE.md exists (move it aside, or pass --allow-contaminated for a smoke test)")
    out = pathlib.Path(a.out); gdir = out / "grades"; gdir.mkdir(exist_ok=True)
    mapping = json.loads((out / "manifest.json").read_text())
    rubric, prompts = RUBRIC.read_text(encoding="utf-8"), scenario_prompts()
    folder = "blind" if a.variant == "original" else "blind_stripped"
    task = TASK_FULL if a.variant == "original" else TASK_STRIPPED
    ids = sorted(mapping)[: a.limit] if a.limit else sorted(mapping)

    def run(rid):
        dest = gdir / f"{a.variant}-{a.name}-{rid}.json"
        if dest.exists():
            return rid, "skip"
        text = TEMPLATE.format(rubric=rubric, prompt=prompts[mapping[rid][0]],
                               response=(out / folder / f"{rid}.md").read_text(encoding="utf-8"), task=task)
        err = "no valid output"
        for _ in range(3):
            p = subprocess.run(["claude", "-p", "--model", GRADER_MODEL, "--tools", "", "--output-format", "json",
                                "--no-session-persistence", "--disable-slash-commands", "--setting-sources", "project"],
                               input=text, capture_output=True, text=True, cwd=tempfile.mkdtemp(), timeout=400)
            try:
                d = json.loads(re.search(r"\{.*\}", json.loads(p.stdout)["result"], re.S).group(0))
                if valid(d, a.variant):
                    dest.write_text(json.dumps(d), encoding="utf-8")
                    return rid, "ok"
            except Exception as e:
                err = f"{e} | {p.stderr[:120]}"
        return rid, f"FAIL {err}"

    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        for rid, st in ex.map(run, ids):
            print(a.variant, a.name, rid, st, flush=True)


def cmd_collect(a):
    out = pathlib.Path(a.out)
    mapping = json.loads((out / "manifest.json").read_text())
    g = lambda variant, name, rid: json.loads((out / "grades" / f"{variant}-{name}-{rid}.json").read_text())
    rows = {}
    for rid, stem in mapping.items():
        o = [g("original", n, rid) for n in ("p1", "p2")]
        s = [g("stripped", n, rid) for n in ("p1", "p2")]
        avg = lambda f: sum(f(x) for x in o) / 2
        S = avg(lambda x: x["S"]["1"] + x["S"]["2"]); Q = avg(lambda x: sum(x["Q"].values()))
        q8 = avg(lambda x: sum(x["Q"][i] for i in STRIPPED_Q))
        q8s = sum(sum(x["Q"].values()) for x in s) / 2
        rows[stem] = dict(blind_id=rid, S=S, Q=Q, legacy=S + q8, Q8_original=q8, Q8_stripped=q8s,
                          pass1=o[0], pass2=o[1], stripped1=s[0], stripped2=s[1],
                          qdiff=abs(sum(o[0]["Q"].values()) - sum(o[1]["Q"].values())),
                          sdiff=abs(sum(o[0]["S"].values()) - sum(o[1]["S"].values())))
    (out / "sheet.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
    cell = {}
    for stem, r in rows.items():
        scen, cond, tier, _ = stem.split("-")
        for k in ("S", "Q", "legacy", "Q8_original", "Q8_stripped"):
            cell.setdefault((tier, cond, scen), {}).setdefault(k, []).append(r[k])
    mean = lambda xs: sum(xs) / len(xs)
    scens = sorted({k[2] for k in cell})
    print("tier,condition,S(0-4),Q(0-20),legacy(0-20),Q8_original(0-16),Q8_stripped(0-16)")
    lifts = {}
    for tier in ("sonnet", "haiku"):
        agg = {}
        for cond in ("baseline", "skill"):
            agg[cond] = {k: mean([mean(cell[(tier, cond, s)][k]) for s in scens]) for k in ("S", "Q", "legacy", "Q8_original", "Q8_stripped")}
            print(tier, cond, *[f"{agg[cond][k]:.2f}" for k in ("S", "Q", "legacy", "Q8_original", "Q8_stripped")], sep=",")
        lifts[tier] = {k: agg["skill"][k] - agg["baseline"][k] for k in agg["skill"]}
        print(tier, "LIFT", *[f"{lifts[tier][k]:+.2f}" for k in ("S", "Q", "legacy", "Q8_original", "Q8_stripped")], sep=",")
        pos = sum(1 for s in scens if mean(cell[(tier, "skill", s)]["Q"]) - mean(cell[(tier, "baseline", s)]["Q"]) > 0)
        print(f"{tier}: scenarios with positive Q lift: {pos}/{len(scens)}")
        print(tier, "per-scenario Q lift:", " ".join(f"{s}:{mean(cell[(tier,'skill',s)]['Q'])-mean(cell[(tier,'baseline',s)]['Q']):+.1f}" for s in scens))
    print("mean |pass1-pass2|: Q total %.2f, S total %.2f" % (mean([r["qdiff"] for r in rows.values()]), mean([r["sdiff"] for r in rows.values()])))
    verdict = {t: ("content benefit" if lifts[t]["Q"] >= 1.0 else "no content benefit by the pre-stated rule") for t in lifts}
    print("rule (Q lift >= +1.0 and majority of scenarios positive) -> lift check only:", verdict)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare"); p.add_argument("responses"); p.add_argument("out"); p.add_argument("--seed", type=int, required=True); p.set_defaults(f=cmd_prepare)
    p = sub.add_parser("grade"); p.add_argument("out"); p.add_argument("variant", choices=["original", "stripped"]); p.add_argument("name")
    p.add_argument("--limit", type=int, default=0); p.add_argument("--allow-contaminated", action="store_true"); p.set_defaults(f=cmd_grade)
    p = sub.add_parser("collect"); p.add_argument("out"); p.set_defaults(f=cmd_collect)
    a = ap.parse_args(); a.f(a)
