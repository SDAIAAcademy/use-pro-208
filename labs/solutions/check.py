# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.0", "pandas>=2.2", "nbclient>=0.10", "ipykernel>=6.29", "nbformat>=5.10"]
# ///
"""Runs the solution of every lab and prints PASS or the first difference.

  uv run labs/solutions/check.py            # every lab
  uv run labs/solutions/check.py 1.2 2.2    # some

It reads the participants' files in labs/files/ and the reference solutions beside this file,
recomputes each reference figure with its own code (not the generator's) and compares it with
labs/solutions/key.json. For lab 2.2 it executes both notebooks for real, in a temporary folder:
the notebook as the assistant left it must stop on the hidden variable, and the reference
notebook must run from a clean kernel twice and print the same fingerprint. It calls no language
model and leaves nothing in the course folder.
"""
from __future__ import annotations

import csv
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = HERE.parent / "files"
KEY = json.loads((HERE / "key.json").read_text(encoding="utf-8"))

INCLUDE, EXCLUDE = "يُدرج", "يُستبعد"


def expect(name: str, got, want) -> None:
    if isinstance(got, float) or isinstance(want, float):
        ok = abs(float(got) - float(want)) < 0.0005
    else:
        ok = got == want
    if not ok:
        print(f"FAIL  {name}: got {got!r}, expected {want!r}")
        raise SystemExit(1)


def rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def lab_1_1() -> str:
    k = KEY["1.1"]
    uses = re.findall(r"^(U\d\d)\. ", (FILES / "uses" / "uses_12.txt").read_text(encoding="utf-8"), re.M)
    expect("twelve uses", len(uses), 12)
    blank = rows(FILES / "uses" / "classification_sheet.csv")
    expect("the participants' sheet is blank", [r for r in blank if any(list(r.values())[1:])], [])
    card = (FILES / "policy" / "ai_use_policy.txt").read_text(encoding="utf-8")
    items = set(re.findall(r"^([مفق]\d)\. ", card, re.M))
    ref = rows(HERE / "classification_sheet.csv")
    cols = list(ref[0].keys())
    classes = {r[cols[0]]: r[cols[1]] for r in ref}
    expect("reference classes", classes, k["classes"])
    prefix = {"محظور": "م", "يُفصح عنه": "ف", "مقبول": "ق"}
    for r in ref:
        item = r[cols[2]]
        if item not in items:
            expect(f"{r[cols[0]]}: the item exists on the card", item, "an item of the card")
        expect(f"{r[cols[0]]}: the item belongs to its class", item[0], prefix[r[cols[1]]])
    counts = {c: sum(1 for v in classes.values() if v == c) for c in prefix}
    expect("class counts", counts, k["counts"])
    expect("the manuscript case is use U03's rule", k["items"]["U03"], k["manuscript_case"]["item"])
    return f"12 uses: {counts['مقبول']} acceptable, {counts['يُفصح عنه']} disclosable, {counts['محظور']} prohibited; pass mark {k['pass_mark']}"


def lab_1_2() -> str:
    k = KEY["1.2"]
    recs = rows(FILES / "records" / "records_200.csv")
    sample = rows(FILES / "records" / "sample_50.csv")
    assistant = {r["رقم السجل"]: r for r in rows(FILES / "records" / "assistant_screening_200.csv")}
    ref50 = {r["رقم السجل"]: r["القرار المرجعي"] for r in rows(HERE / "screening_reference_50.csv")}
    ref200 = {r["رقم السجل"]: r["القرار المرجعي"] for r in rows(HERE / "screening_reference_200.csv")}
    expect("200 records", len(recs), 200)
    expect("unique titles", len({r["العنوان"] for r in recs}), 200)
    expect("50 in the sample", len(sample), 50)
    expect("the sample is blank", [r for r in sample if r["قرارك (يُدرج / يُستبعد)"]], [])
    expect("the sample is part of the 200", set(ref50) <= set(ref200), True)
    expect("the two references agree", all(ref200[i] == d for i, d in ref50.items()), True)

    def stats(ref: dict) -> dict:
        rel = [i for i, d in ref.items() if d == INCLUDE]
        inc = [i for i in ref if assistant[i]["قرار المساعد"] == INCLUDE]
        both = [i for i in rel if i in inc]
        return {"relevant": len(rel), "assistant_included": len(inc), "both": len(both),
                "recall": round(len(both) / len(rel), 3), "precision": round(len(both) / len(inc), 3),
                "missed": sorted(set(rel) - set(inc))}

    s50, s200 = stats(ref50), stats(ref200)
    expect("sample statistics", s50, k["sample"])
    expect("statistics on the 200", s200, k["all"])
    abstract = {r["رقم السجل"]: r["الملخص"] for r in recs}
    no_abstract = sum(1 for i in s200["missed"] if not abstract[i])
    no_generic = sum(1 for i in s200["missed"] if abstract[i] and "المكشوفة" not in abstract[i])
    expect("missed without an abstract", no_abstract, k["missed_kinds_all"]["title_only"])
    expect("missed that name a job without the generic term", no_generic, k["missed_kinds_all"]["job_only"])

    notices = set(re.findall(r"^(HJ-\d{4}-\d{4}) \|", (FILES / "records" / "retraction_notices.txt").read_text(encoding="utf-8"), re.M))
    retracted = sorted(r["رقم السجل"] for r in recs if r["المعرّف"] in notices)
    expect("retracted records", retracted, sorted(k["retracted_in_sample"] + k["retracted_outside"]))
    expect("retracted in the sample", [i for i in retracted if i in ref50], k["retracted_in_sample"])
    for i in k["key_papers"]:
        expect(f"key paper {i} is relevant and found", (ref200[i], assistant[i]["قرار المساعد"]), (INCLUDE, INCLUDE))

    ranked = sorted(recs, key=lambda r: (-float(assistant[r["رقم السجل"]]["درجة المساعد"]), r["رقم السجل"]))
    run = found = 0
    stop = None
    for n, r in enumerate(ranked, 1):
        if ref200[r["رقم السجل"]] == INCLUDE:
            found, run = found + 1, 0
        else:
            run += 1
        if run == 50:
            stop = n
            break
    last = max(n for n, r in enumerate(ranked, 1) if ref200[r["رقم السجل"]] == INCLUDE)
    expect("stopping rule", {"stops_after": stop, "found": found, "missed": s200["relevant"] - found,
                             "last_relevant_rank": last}, k["stop_rule_50"])

    log = rows(FILES / "search" / "search_log.csv")
    gaps = []
    if "كما في" in log[1]["الاستعلام كما نُفّذ"]:
        gaps.append("query not as run")
    if not log[2]["تاريخ التنفيذ"]:
        gaps.append("no date")
    total = sum(int(r["عدد السجلات"]) for r in log[:3])
    if (total, int(log[4]["عدد السجلات"])) == (212, 200) and not any("أداة" in v or "طريقة" in v for r in log[3:] for v in r.values()):
        gaps.append("deduplication without a method")
    expect("planted gaps in the search log", len(gaps), len(k["search_log_gaps"]))
    return (f"sample: recall {s50['both']}/{s50['relevant']} = {s50['recall']}, precision {s50['both']}/{s50['assistant_included']} = {s50['precision']}; "
            f"all: recall {s200['both']}/{s200['relevant']} = {s200['recall']}; rule of 50 stops after {stop} with {found} found")


def lab_2_1() -> str:
    k = KEY["2.1"]
    papers = {}
    for p in sorted((FILES / "papers").glob("P*.txt")):
        papers[p.stem] = dict(re.findall(r"^\[(\d+)\] (.+)$", p.read_text(encoding="utf-8"), re.M))
    expect("ten papers", len(papers), 10)
    text = (FILES / "summaries" / "summaries_10.txt").read_text(encoding="utf-8")
    summaries: dict[str, dict] = {}
    current = None
    for line in text.splitlines():
        m = re.match(r"^(S\d\d) \(ملخص الورقة (P\d\d)\)", line)
        if m:
            current = summaries.setdefault(m.group(1), {"paper": m.group(2), "sentences": {}})
            continue
        m = re.match(r"^\s+\((\d+)\) (.+)$", line)
        if m and current is not None:
            current["sentences"][m.group(1)] = m.group(2)
    expect("ten summaries", len(summaries), 10)
    audit = rows(HERE / "audit_sheet.csv")
    errors = [r for r in audit if r["نوع الخطأ"] != "لا خطأ"]
    expect("planted errors", len(errors), k["error_count"])
    for r in errors:
        sid, sent = r["الملخص"], r["رقم العبارة في الملخص"]
        pid, passage = re.match(r"^(P\d\d) \[(\d+)\]$", r["المقطع الذي يناقضها"]).groups()
        expect(f"{sid}: the summary is of its paper", summaries[sid]["paper"], pid)
        expect(f"{sid} ({sent}): the sentence exists", sent in summaries[sid]["sentences"], True)
        expect(f"{sid}: passage {passage} exists in {pid}", passage in papers[pid], True)
    got = sorted((r["الملخص"], int(r["رقم العبارة في الملخص"]), r["نوع الخطأ"],
                  int(r["المقطع الذي يناقضها"].split("[")[1].rstrip("]"))) for r in errors)
    want = sorted((e["summary"], e["sentence"], e["type"], e["passage"]) for e in k["errors"])
    expect("errors against the key", got, want)
    by_type = {t: sum(1 for r in errors if r["نوع الخطأ"] == t) for t in k["by_type"]}
    expect("errors by type", by_type, k["by_type"])
    clean = sorted(r["الملخص"] for r in audit if r["نوع الخطأ"] == "لا خطأ")
    expect("faithful summaries", clean, k["clean_summaries"])
    # numbers of a faithful summary must all be in its paper; a planted effect-size error is not
    for sid in clean:
        s = summaries[sid]
        paper_text = " ".join(papers[s["paper"]].values())
        for num in re.findall(r"\d+(?:[.,]\d+)?", " ".join(s["sentences"].values())):
            expect(f"{sid}: the number {num} is in {s['paper']}", num in paper_text, True)
    expect("S08 states 27, which the paper does not", "27" in " ".join(papers["P08"].values()), False)
    return f"{len(errors)} planted errors in {len({r['الملخص'] for r in errors})} summaries, {len(clean)} faithful: " + ", ".join(f"{t} {n}" for t, n in by_type.items())


def lab_2_2() -> str:
    import nbformat
    from nbclient import NotebookClient
    from nbclient.exceptions import CellExecutionError

    k = KEY["2.2"]
    src = FILES / "analysis"
    raw = (src / "power_daily_2024_raw.csv").read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(raw) if line.startswith("-END HEADER-")) + 1
    weather = list(csv.DictReader(raw[start:]))
    clinic = rows(src / "clinic_visits_synthetic.csv")
    expect("153 days of weather", len(weather), 153)
    expect("153 days of clinic counts", len(clinic), 153)
    # the planned analysis, recomputed without pandas
    hot = [0, 0]
    other = [0, 0]
    days = hot_days = 0
    for w, c in zip(weather, clinic):
        workers, visits = int(c["workers_on_site"]), int(c["heat_visits"])
        if workers < 200:
            continue
        days += 1
        if float(w["T2M_MAX"]) >= 45.0:
            hot_days += 1
            hot[0] += visits
            hot[1] += workers
        else:
            other[0] += visits
            other[1] += workers
    r_hot, r_other = 1000 * hot[0] / hot[1], 1000 * other[0] / other[1]
    res = k["results"]
    expect("days analysed", days, res["days"])
    expect("hot days", hot_days, res["hot_days"])
    expect("rate on hot days", round(r_hot, 2), res["rate_hot"])
    expect("rate on other days", round(r_other, 2), res["rate_other"])
    expect("rate ratio", round(r_hot / r_other, 2), res["rate_ratio"])

    def run(nb_path: Path, folder: Path) -> list[str]:
        nb = nbformat.read(nb_path, as_version=4)
        for cell in nb.cells:
            if cell.cell_type == "code":
                cell.outputs, cell.execution_count = [], None
        NotebookClient(nb, timeout=300, kernel_name="python3", resources={"metadata": {"path": str(folder)}}).execute()
        return ["".join(o.get("text", "")) for c in nb.cells if c.cell_type == "code" for o in c.outputs]

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        for name in ("power_daily_2024_raw.csv", "clinic_visits_synthetic.csv"):
            shutil.copy(src / name, work / name)
        try:
            run(src / "heat_analysis.ipynb", work)
            expect("the assistant's notebook stops on a clean run", "ran to the end", "NameError")
        except CellExecutionError as e:
            expect("the assistant's notebook stops on the hidden variable", "name 'THRESHOLD' is not defined" in str(e), True)
        prints = []
        for _ in range(2):
            out = "\n".join(run(HERE / "heat_analysis_clean.ipynb", work))
            prints.append(re.search(r"fingerprint (\w+)", out).group(1))
            got = json.loads(re.search(r"^\{.*\}$", out, re.M).group(0))
        expect("two clean runs print the same fingerprint", prints[0], prints[1])
        expect("the fingerprint of the key", prints[0], k["fingerprint"])
        expect("the results of the key", got, res)
        sec = float(re.search(r"secondary \(previous day\): rate ratio ([\d.]+)", out).group(1))
        expect("secondary rate ratio", sec, k["secondary_rate_ratio"])

    saved = nbformat.read(src / "heat_analysis.ipynb", as_version=4)
    counts = [c.execution_count for c in saved.cells if c.cell_type == "code"]
    expect("saved execution counts show deleted cells", counts, [1, 2, 3, 14, 15, 16])
    text = " ".join("".join(c.source) for c in saved.cells)
    saved_out = " ".join("".join(o.get("text", "")) for c in saved.cells if c.cell_type == "code" for o in c.outputs)
    expect("the pasted 2.4 is printed by no cell", ("2.4" in text, "2.4" in saved_out), (True, False))
    a = k["assistant_saved"]
    expect("the saved output shows the forked result", f"rate ratio {a['rate_ratio']:.2f} (95% CI {a['ci_low']:.2f} to {a['ci_high']:.2f})" in saved_out, True)
    expect("unseeded bootstrap in the assistant's notebook", "default_rng()" in text, True)
    log = rows(HERE / "decision_log.csv")
    expect("decision log rows", len(log), k["faults"])
    return (f"planned: {res['days']} days, {res['hot_days']} hot, {res['rate_hot']} against {res['rate_other']} per 1,000 worker-days, "
            f"rate ratio {res['rate_ratio']} ({res['ci_low']} to {res['ci_high']}), fingerprint {prints[0]} twice; "
            f"the assistant's notebook stops with NameError; its saved result was {a['rate_ratio']} ({a['ci_low']} to {a['ci_high']})")


LABS = {"1.1": lab_1_1, "1.2": lab_1_2, "2.1": lab_2_1, "2.2": lab_2_2}

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    wanted = sys.argv[1:] or list(LABS)
    for lab in wanted:
        print(f"PASS  {lab}  {LABS[lab]()}")
