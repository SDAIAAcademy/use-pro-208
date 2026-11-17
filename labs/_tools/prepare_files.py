# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=2.0", "pandas>=2.2"]
# ///
"""Writes the synthetic file pack of the Hajir Institute for Occupational Health Research (fictional).

  uv run labs/_tools/prepare_files.py

Fixed seed: the same bytes on every run. Everything is invented except one file,
labs/files/analysis/power_daily_2024_raw.csv, a public NASA POWER download that this script
never touches. The planted problems and the reference figures go to labs/solutions/key.json;
labs/solutions/check.py recomputes them from the files without this generator.
"""
from __future__ import annotations

import contextlib
import csv
import io
import json
import math
import random
from datetime import date, timedelta
from pathlib import Path

import texts as T

LABS = Path(__file__).resolve().parent.parent
FILES = LABS / "files"
SOL = LABS / "solutions"
SEED = 208
R = random.Random(SEED)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def write_csv(path: Path, rows: list[list]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)


# ------------------------------------------------------------------ lab 1.1

def lab_1_1(key: dict) -> None:
    write_text(FILES / "policy" / "ai_use_policy.txt", T.POLICY_CARD)
    write_text(FILES / "uses" / "uses_12.txt", T.BANNER + "\n\nاثنا عشر استخدامًا للذكاء الاصطناعي في مشروع المعهد\n\n"
               + "\n\n".join(f"{u}. {text}" for u, text, _, _ in T.USES))
    write_text(FILES / "uses" / "manuscript_case.txt", T.MANUSCRIPT_CASE)
    head = ["الاستخدام", "تصنيفك (مقبول / يُفصح عنه / محظور)", "البند في البطاقة", "ملاحظة"]
    write_csv(FILES / "uses" / "classification_sheet.csv", [head] + [[u, "", "", ""] for u, *_ in T.USES])
    write_csv(SOL / "classification_sheet.csv", [head] + [[u, cls, item, ""] for u, _, cls, item in T.USES])
    key["1.1"] = {
        "classes": {u: cls for u, _, cls, _ in T.USES},
        "items": {u: item for u, _, _, item in T.USES},
        "counts": {"مقبول": 3, "يُفصح عنه": 5, "محظور": 4},
        "pass_mark": 10,
        "manuscript_case": {"class": "محظور", "item": "م3"},
    }


# ------------------------------------------------------------------ lab 1.2

GENERIC = ["العاملين في الأماكن المكشوفة", "عمال المواقع المكشوفة"]
JOBS = ["عمال البناء", "عمال صيانة الطرق", "عمال النظافة البلدية", "عمال جني التمور", "المزارعين الموسميين",
        "سائقي دراجات التوصيل", "عمال أرصفة الموانئ", "رجال المرور", "عمال المحاجر السطحية",
        "عمال الحدائق العامة", "صيادي السواحل", "عمال تمديد الكابلات"]
OUTCOMES = ["الإجهاد الحراري", "ضربات الشمس", "أعراض الإنهاك الحراري", "الجفاف أثناء الوردية", "مؤشرات وظائف الكلى",
            "الإصابات المهنية في الأيام الحارة", "ساعات العمل المفقودة بسبب الحر", "حرارة الجسم الأساسية"]
JOB_ONLY_HEAT = ["وطأة الحر", "لهيب الظهيرة", "قيظ الصيف"]
DESIGNS = ["دراسة مقطعية", "دراسة أتراب", "دراسة تدخلية", "دراسة نوعية", "تحليل سلاسل زمنية", "دراسة حالات وشواهد"]
PLACES = ["منطقة ساحلية حارة", "مدينة صحراوية", "إقليم زراعي", "منطقة صناعية", "مدينة ساحلية رطبة", "محافظة داخلية"]

IRRELEVANT = {
    # category: (count, exclusion code, title templates, abstract templates)
    "indoor": (22, "س1", ["{o} لدى {w} في {p}: {d}"],
               ["{d}. المشاركون: {n} من {w} يعملون داخل المنشأة قرب مصادر حرارة. المقياس: {o} في آخر الوردية."]),
    "not_workers": (18, "س2", ["{o} لدى {w} في {p}: {d}"],
                    ["{d}. المشاركون: {n} من {w} أثناء التدريب الصيفي. المقياس: {o} قبل التمرين وبعده."]),
    "general": (24, "س2", ["موجات الحر و{o} لدى عموم السكان في {p}: {d}"],
                ["{d} على سجلات المستشفيات في {p}. المقياس: {o} في أيام موجات الحر مقارنة بغيرها، لدى السكان عمومًا."]),
    "review": (16, "س3", ["{o} لدى {w}: {d}"],
               ["{d}: جمع ما نُشر عن {o} لدى {w} ومناقشة فجوات الأدلة. لا بيانات جديدة."]),
    "no_humans": (12, "س4", ["{o} في {p}: {d}"],
                  ["{d}: {o}، دون أي نتيجة صحية لدى البشر."]),
    "other_hazard": (26, "س5", ["{o} لدى {w} في {p}: {d}"],
                     ["{d}. المشاركون: {n} من {w}. المقياس: {o} في مواقع العمل. لم تُدرس الحرارة."]),
    "climate": (18, "س4", ["{o} في {p} حتى عام 2050: {d}"],
                ["{d}: توقع {o} بنماذج مناخية إقليمية. لا بيانات عن عاملين ولا نتائج صحية."]),
    "cold": (18, "س5", ["{o} لدى {w} في {p}: {d}"],
             ["{d}. المشاركون: {n} من {w}. المقياس: {o} في أشهر الشتاء."]),
}
IRR_FILL = {
    "indoor": {"w": ["عمال المخابز", "عمال المسابك", "عمال مصانع الزجاج", "طهاة المطابخ المركزية", "عمال مصانع الحديد"],
               "o": ["الإجهاد الحراري", "الجفاف", "حرارة الجسم الأساسية", "أعراض الإنهاك الحراري"]},
    "not_workers": {"w": ["لاعبي كرة القدم الناشئين", "عدّائي المسافات الطويلة", "المجندين الجدد", "طلاب الكليات العسكرية"],
                    "o": ["الإجهاد الحراري", "ضربات الشمس", "الجفاف", "حرارة الجسم الأساسية"]},
    "general": {"o": ["دخول المستشفيات", "الوفيات اليومية", "زيارات الطوارئ", "أمراض القلب"]},
    "review": {"w": ["العاملين في الأماكن المكشوفة", "عمال البناء", "عمال الزراعة", "العاملين في الحر"],
               "o": ["الإجهاد الحراري", "أمراض الحرارة المهنية", "وظائف الكلى", "التعرض للحرارة"],
               "d": ["مراجعة منهجية", "مراجعة سردية", "افتتاحية", "بروتوكول مراجعة", "تعليق"]},
    "no_humans": {"o": ["تحمّل الإبل للإجهاد الحراري", "أثر الحرارة في إنتاج الدواجن", "استجابة فئران التجارب للحرارة",
                         "اختبار أقمشة عاكسة للحرارة في المختبر"],
                  "d": ["دراسة مخبرية", "تجربة على الحيوان", "دراسة هندسية"]},
    "other_hazard": {"w": ["عمال البناء", "عمال صيانة الطرق", "عمال المحاجر السطحية", "عمال أرصفة الموانئ", "رجال المرور"],
                     "o": ["التعرض للضجيج", "التعرض للغبار", "آلام أسفل الظهر", "التعرض للأشعة فوق البنفسجية", "حوادث السقوط"]},
    "climate": {"o": ["عدد الأيام شديدة الحرارة", "الحرارة الرطبة القصوى", "موجات الحر"],
                "d": ["دراسة نمذجة مناخية", "إسقاطات مناخية", "تحليل اتجاهات مناخية"]},
    "cold": {"w": ["عمال البناء", "صيادي السواحل", "عمال المستودعات المبردة", "عمال تمديد الكابلات"],
             "o": ["إصابات البرد", "خدر الأطراف", "نزلات البرد المتكررة"]},
}


def make_records() -> list[dict]:
    recs: list[dict] = []
    seen: set[str] = set()

    def add(kind: str, truth: str, code: str, title: str, abstract: str) -> None:
        recs.append({"kind": kind, "truth": truth, "code": code, "title": title, "abstract": abstract})

    def unique(make):
        for _ in range(500):
            t, a = make()
            if t not in seen:
                seen.add(t)
                return t, a
        raise RuntimeError("no unique title")

    # 46 relevant: 28 explicit, 12 job-only, 6 title-only
    for kind, n_kind in (("explicit", 28), ("job_only", 12), ("title_only", 6)):
        for _ in range(n_kind):
            def make():
                job, out, des, place = R.choice(JOBS), R.choice(OUTCOMES), R.choice(DESIGNS), R.choice(PLACES)
                n = R.randrange(12, 41) if des == "دراسة نوعية" else R.randrange(60, 1900)
                if kind == "explicit":
                    gen = R.choice(GENERIC)
                    title = f"{out} لدى {gen}: {des} على {job} في {place}"
                    abstract = (f"{des}. المشاركون: {n} من {job}، وهم من {gen}، في {place}. "
                                f"المقياس: {out} في أشهر الصيف، مع مقارنة أيام العمل الحارة بغيرها.")
                elif kind == "job_only":
                    heat = R.choice(JOB_ONLY_HEAT)
                    title = f"{job} تحت {heat} في {place}: {des}"
                    abstract = (f"{des}. المشاركون: {n} من {job} في {place}. "
                                f"المقياس: {out} في أيام {heat}، مع عدد ساعات العمل تحت الشمس.")
                else:
                    title = f"{out} لدى {job} في {place}: {des}"
                    abstract = ""
                return title, abstract
            t, a = unique(make)
            add(kind, "يُدرج", "", t, a)

    for cat, (count, code, t_tpls, a_tpls) in IRRELEVANT.items():
        fill = IRR_FILL[cat]
        for _ in range(count):
            def make():
                v = {"w": R.choice(fill.get("w", JOBS)), "o": R.choice(fill["o"]),
                     "d": R.choice(fill.get("d", DESIGNS)), "p": R.choice(PLACES), "n": R.randrange(60, 1900)}
                if v["d"] == "دراسة نوعية":
                    v["n"] = R.randrange(12, 41)
                return R.choice(t_tpls).format(**v), R.choice(a_tpls).format(**v)
            t, a = unique(make)
            add(cat, "يُستبعد", code, t, a)

    R.shuffle(recs)
    for i, r in enumerate(recs, 1):
        r["id"] = f"R{i:03d}"
        r["year"] = R.randrange(2010, 2026)
        r["identifier"] = f"HJ-{r['year']}-{R.randrange(100, 9999):04d}"
        r["db"] = R.choices(["أ", "ب", "ج"], weights=[55, 34, 11])[0]
    return recs


def lab_1_2(key: dict) -> None:
    recs = make_records()
    # the two key papers the team knew before the search: explicit relevant records, renamed R007 and R019
    explicit = [x for x in recs if x["kind"] == "explicit"]
    keys = explicit[:2]
    for target, cand in zip(("R007", "R019"), keys):
        other = next(x for x in recs if x["id"] == target)
        other["id"], cand["id"] = cand["id"], target
    recs.sort(key=lambda x: x["id"])
    by_kind: dict[str, list[dict]] = {}
    for r in recs:
        by_kind.setdefault(r["kind"], []).append(r)
        r["missed"] = r["fp"] = False

    # the assistant's decisions (a scripted stand-in): which relevant records it misses,
    # and which irrelevant ones it wrongly includes
    free_explicit = [x for x in by_kind["explicit"] if x["id"] not in ("R007", "R019")]
    for x in R.sample(free_explicit, 1) + R.sample(by_kind["job_only"], 5) + R.sample(by_kind["title_only"], 3):
        x["missed"] = True
    for cat, n in (("indoor", 7), ("not_workers", 2), ("general", 2), ("review", 3)):
        for x in R.sample(by_kind[cat], n):
            x["fp"] = True

    missed_list = [x for x in recs if x["missed"]]
    deep = {x["id"] for x in R.sample(missed_list, 4)}
    for r in recs:
        rel = r["truth"] == "يُدرج"
        if (rel and not r["missed"]) or r["fp"]:
            r["a_dec"], r["a_score"] = "يُدرج", round(R.uniform(0.55, 0.98), 3)
        elif r["missed"]:
            r["a_dec"] = "يُستبعد"
            r["a_score"] = round(R.uniform(0.05, 0.20), 3) if r["id"] in deep else round(R.uniform(0.36, 0.45), 3)
        else:
            r["a_dec"], r["a_score"] = "يُستبعد", round(R.uniform(0.02, 0.45), 3)
        if r["a_dec"] == "يُدرج":
            r["a_reason"] = "عاملون معرّضون للحرارة أثناء العمل"
        elif r["kind"] == "title_only":
            r["a_reason"] = "لا ملخص: المعلومات لا تكفي"
        elif r["kind"] in ("explicit", "job_only"):
            r["a_reason"] = "لا يذكر العاملين في الأماكن المكشوفة"
        else:
            r["a_reason"] = "خارج موضوع السؤال"

    # the sample of 50: 14 relevant (8 explicit, 4 job-only, 2 title-only), 36 irrelevant with 4 false positives
    def pick(kind: str, n_hit: int, n_miss: int) -> list[dict]:
        hit = [x for x in by_kind[kind] if not x["missed"] and x["id"] not in ("R007", "R019")]
        mis = [x for x in by_kind[kind] if x["missed"]]
        return R.sample(hit, n_hit) + R.sample(mis, n_miss)

    sample = pick("explicit", 8, 0) + pick("job_only", 2, 2) + pick("title_only", 1, 1)
    fp_pool = [x for x in recs if x["fp"]]
    sample += [x for x in fp_pool if x["kind"] == "indoor"][:2]
    sample += [x for x in fp_pool if x["kind"] == "not_workers"][:1]
    sample += [x for x in fp_pool if x["kind"] == "review"][:1]
    rest = [x for x in recs if x["truth"] == "يُستبعد" and not x["fp"]]
    sample += R.sample(rest, 32)
    sample.sort(key=lambda x: x["id"])
    sample_ids = [x["id"] for x in sample]
    assert len(set(sample_ids)) == 50

    # retractions: one relevant record inside the sample that the assistant included, one irrelevant outside
    retr_in = next(x for x in sample if x["kind"] == "explicit")
    retr_out = next(x for x in recs if x["kind"] == "general" and x["id"] not in sample_ids)
    notices = [
        (retr_in["identifier"], 2024, "بيانات لم يستطع المؤلفون تقديمها عند الطلب"),
        ("HJ-2016-0031", 2019, "تكرار نشر"),
        (retr_out["identifier"], 2022, "خطأ في التحليل يغيّر النتيجة"),
        ("HJ-2021-7770", 2023, "تلاعب في التحكيم"),
        ("HJ-2012-0458", 2015, "انتحال"),
    ]
    used = {r["identifier"] for r in recs}
    assert sum(1 for n in notices if n[0] in used) == 2

    write_text(FILES / "project" / "scoping_question.txt", T.SCOPING_QUESTION)
    write_csv(FILES / "search" / "search_log.csv", [T.SEARCH_LOG_HEADER] + T.SEARCH_LOG_ROWS)
    write_csv(FILES / "search" / "search_log_template.csv", [T.SEARCH_LOG_HEADER] + T.SEARCH_LOG_TEMPLATE_ROWS)
    head = ["رقم السجل", "المعرّف", "السنة", "القاعدة", "العنوان", "الملخص"]
    write_csv(FILES / "records" / "records_200.csv",
              [head] + [[r["id"], r["identifier"], r["year"], r["db"], r["title"], r["abstract"]] for r in recs])
    write_csv(FILES / "records" / "sample_50.csv",
              [head + ["قرارك (يُدرج / يُستبعد)", "رمز المعيار"]]
              + [[r["id"], r["identifier"], r["year"], r["db"], r["title"], r["abstract"], "", ""] for r in sample])
    write_csv(FILES / "records" / "assistant_screening_200.csv",
              [["رقم السجل", "قرار المساعد", "درجة المساعد", "سبب المساعد"]]
              + [[r["id"], r["a_dec"], f"{r['a_score']:.3f}", r["a_reason"]] for r in recs])
    write_text(FILES / "records" / "retraction_notices.txt",
               T.RETRACTION_NOTICES_HEAD + "\n".join(f"{i} | {y} | {why}" for i, y, why in notices))
    write_csv(FILES / "records" / "recall_sheet.csv", [
        ["البند", "العدد أو النسبة"],
        ["سجلات أدرجتها أنت من الخمسين (أ)", ""],
        ["منها ما أدرجه المساعد أيضًا (ب)", ""],
        ["سجلات أدرجها المساعد من الخمسين (ج)", ""],
        ["الاستدعاء = ب ÷ أ", ""],
        ["الدقة = ب ÷ ج", ""],
        ["أرقام السجلات التي أدرجتها وفاتت المساعد", ""],
        ["النمط الذي تراه فيما فاته", ""],
        ["سجلات في العينة وردت في قائمة السحب", ""],
        ["قرارك: هل يُعتمد المساعد للبقية، وبأي شرط", ""],
    ])
    # the reference screener (Uday Al-Shammasi): the truth labels on the 50 and on the 200
    write_csv(SOL / "screening_reference_50.csv",
              [["رقم السجل", "القرار المرجعي", "رمز المعيار", "قرار المساعد"]]
              + [[r["id"], r["truth"], r["code"], r["a_dec"]] for r in sample])
    write_csv(SOL / "screening_reference_200.csv",
              [["رقم السجل", "القرار المرجعي", "رمز المعيار"]] + [[r["id"], r["truth"], r["code"]] for r in recs])
    write_csv(SOL / "search_log_row_example.csv", [T.SEARCH_LOG_HEADER, [
        "4", "OpenAlex", "واجهة الموقع", "تاريخ يوم التنفيذ",
        "(\"outdoor workers\" OR \"construction workers\" OR \"agricultural workers\" OR \"farmworkers\") AND (\"heat stress\" OR \"heat exposure\" OR \"heat-related illness\")",
        "2010 إلى 2025، مقالات فقط", "العدد الذي ظهر يوم التنفيذ", "اسم المشارك"]])

    def stats(pool: list[dict]) -> dict:
        rel = [x for x in pool if x["truth"] == "يُدرج"]
        inc = [x for x in pool if x["a_dec"] == "يُدرج"]
        tp = [x for x in rel if x["a_dec"] == "يُدرج"]
        return {"relevant": len(rel), "assistant_included": len(inc), "both": len(tp),
                "recall": round(len(tp) / len(rel), 3), "precision": round(len(tp) / len(inc), 3),
                "missed": sorted(x["id"] for x in rel if x["a_dec"] != "يُدرج")}

    ranked = sorted(recs, key=lambda x: (-x["a_score"], x["id"]))
    run, found, stop_at = 0, 0, None
    for i, r in enumerate(ranked, 1):
        if r["truth"] == "يُدرج":
            found, run = found + 1, 0
        else:
            run += 1
        if run == 50:
            stop_at = i
            break
    last_rel = max(i for i, r in enumerate(ranked, 1) if r["truth"] == "يُدرج")
    key["1.2"] = {
        "sample": stats(sample), "all": stats(recs),
        "missed_kinds_all": {k: sum(1 for x in recs if x["missed"] and x["kind"] == k)
                             for k in ("explicit", "job_only", "title_only")},
        "retracted_in_sample": [retr_in["id"]], "retracted_outside": [retr_out["id"]],
        "search_log_gaps": ["السطر 2: الاستعلام ليس كما نُفّذ", "السطر 3: لا تاريخ تنفيذ",
                            "إزالة المكرر: عدد بلا طريقة ولا أداة"],
        "stop_rule_50": {"stops_after": stop_at, "found": found, "missed": 46 - found, "last_relevant_rank": last_rel},
        "key_papers": ["R007", "R019"],
    }


# ------------------------------------------------------------------ lab 2.1

def lab_2_1(key: dict) -> None:
    for pid, title, passages in T.PAPERS:
        body = "\n".join(f"[{i}] {p}" for i, p in enumerate(passages, 1))
        write_text(FILES / "papers" / f"{pid}.txt", f"{T.BANNER}\n\n{pid} · {title}\nمستخلص موسّع من ورقة اصطناعية. المقاطع مرقّمة ليُستشهد بها.\n\n{body}")
    parts = [T.BANNER, "", "عشرة ملخصات كتبها المساعد «مُعين»، ملخص لكل ورقة. العبارات مرقّمة. لم تُراجَع.", ""]
    for sid, pid, sents in T.SUMMARIES:
        parts.append(f"{sid} (ملخص الورقة {pid})")
        parts += [f"  ({i}) {s}" for i, s in enumerate(sents, 1)]
        parts.append("")
    write_text(FILES / "summaries" / "summaries_10.txt", "\n".join(parts))
    write_csv(FILES / "summaries" / "audit_sheet.csv",
              [T.AUDIT_HEADER] + [[sid, pid, "", "", "", "", ""] for sid, pid, _ in T.SUMMARIES])
    errs: dict[str, list] = {}
    for sid, sent, typ, passage, fix in T.SUMMARY_ERRORS:
        errs.setdefault(sid, []).append((sent, typ, passage, fix))
    rows = [T.AUDIT_HEADER]
    for sid, pid, _ in T.SUMMARIES:
        if sid not in errs:
            rows.append([sid, pid, "", "لا خطأ", "", "", "يُعتمد"])
            continue
        verdict = "يُرفض" if len(errs[sid]) > 1 else "يُصحَّح"
        for sent, typ, passage, fix in errs[sid]:
            rows.append([sid, pid, sent, typ, f"{pid} [{passage}]", fix, verdict])
    write_csv(SOL / "audit_sheet.csv", rows)
    key["2.1"] = {
        "errors": [{"summary": s, "sentence": n, "type": t, "passage": p} for s, n, t, p, _ in T.SUMMARY_ERRORS],
        "error_count": len(T.SUMMARY_ERRORS),
        "by_type": {t: sum(1 for e in T.SUMMARY_ERRORS if e[2] == t)
                    for t in ("الفئة المدروسة", "الأسلوب", "حجم الأثر", "الاستنتاج")},
        "clean_summaries": [sid for sid, _, _ in T.SUMMARIES if sid not in errs],
    }


# ------------------------------------------------------------------ lab 2.2

def poisson(lam: float) -> int:
    limit, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= R.random()
        if p <= limit:
            return k
        k += 1


def read_power_rows() -> list[dict]:
    raw = (FILES / "analysis" / "power_daily_2024_raw.csv").read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(raw) if line.startswith("-END HEADER-")) + 1
    return list(csv.DictReader(raw[start:]))


def md(cell_id: str, text: str) -> dict:
    return {"cell_type": "markdown", "id": cell_id, "metadata": {}, "source": text.strip("\n").splitlines(keepends=True)}


def code(cell_id: str, src: str, count=None, out: str = "") -> dict:
    outputs = [{"name": "stdout", "output_type": "stream", "text": out.splitlines(keepends=True)}] if out else []
    return {"cell_type": "code", "id": cell_id, "metadata": {}, "execution_count": count,
            "outputs": outputs, "source": src.strip("\n").splitlines(keepends=True)}


def notebook(cells: list[dict]) -> str:
    nb = {"cells": cells,
          "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                       "language_info": {"name": "python"}},
          "nbformat": 4, "nbformat_minor": 5}
    return json.dumps(nb, ensure_ascii=False, indent=1) + "\n"


C_IMPORT = '''
import hashlib
import io
import json
from pathlib import Path

import numpy as np
import pandas as pd

# the two data files sit beside the notebook (in a hosted notebook service: upload them first)
DATA = next((p for p in (Path("."), Path("files/analysis"), Path("../files/analysis"))
             if (p / "power_daily_2024_raw.csv").exists()), None)
assert DATA is not None, "put power_daily_2024_raw.csv and clinic_visits_synthetic.csv beside the notebook"
print("numpy", np.__version__, "| pandas", pd.__version__)
'''

C_WEATHER = '''
# the public NASA POWER file, exactly as downloaded: a header block, then the table
lines = (DATA / "power_daily_2024_raw.csv").read_text(encoding="utf-8").splitlines()
start = next(i for i, line in enumerate(lines) if line.startswith("-END HEADER-")) + 1
weather = pd.read_csv(io.StringIO("\\n".join(lines[start:])))
weather["date"] = pd.to_datetime(weather["YEAR"].astype(str) + weather["DOY"].astype(str).str.zfill(3), format="%Y%j")
assert (weather[["T2M_MAX", "T2MWET"]] > -900).all().all(), "missing values (-999) in the weather file"
print(len(weather), "days |", weather["date"].min().date(), "to", weather["date"].max().date())
'''

C_CLINIC = '''
# synthetic counts written for this course: workers on site and heat-related clinic visits per day
clinic = pd.read_csv(DATA / "clinic_visits_synthetic.csv", parse_dates=["date"])
df = weather.merge(clinic, on="date", how="inner", validate="one_to_one")
print(len(df), "days after the merge |", int(df["heat_visits"].sum()), "visits")
'''

C_PLAN = '''
# the pre-stated plan, items 3, 5 and 6: nothing below is chosen after seeing the visits
THRESHOLD = 45.0      # hot day: T2M_MAX of the same day at or above this (plan, item 3)
MIN_WORKERS = 200     # days with fewer workers on site are excluded (plan, item 5)
N_BOOT = 2000         # bootstrap resamples of days (plan, item 6)
SEED = 208            # fixed seed (plan, item 6)
'''

C_EXCLUDE = '''
before = len(df)
df = df[df["workers_on_site"] >= MIN_WORKERS].reset_index(drop=True)
print("excluded", before - len(df), "days with fewer than", MIN_WORKERS, "workers |", len(df), "days analysed")
'''

C_EXPOSE = '''
df["hot"] = df["T2M_MAX"] >= THRESHOLD
print(int(df["hot"].sum()), "hot days |", int((~df["hot"]).sum()), "other days")
'''

C_RATE = '''
def rate_ratio(d):
    """Visits per 1,000 worker-days on hot days and on other days, and their ratio."""
    hot, other = d[d["hot"]], d[~d["hot"]]
    r_hot = 1000 * hot["heat_visits"].sum() / hot["workers_on_site"].sum()
    r_other = 1000 * other["heat_visits"].sum() / other["workers_on_site"].sum()
    return r_hot, r_other, r_hot / r_other

r_hot, r_other, rr = rate_ratio(df)
print(f"hot days {r_hot:.2f} per 1,000 worker-days | other days {r_other:.2f} | rate ratio {rr:.2f}")
'''

C_BOOT = '''
rng = np.random.default_rng(SEED)
n = len(df)
boot = []
for _ in range(N_BOOT):
    boot.append(rate_ratio(df.iloc[rng.integers(0, n, n)])[2])
lo, hi = np.percentile(boot, [2.5, 97.5])
print(f"rate ratio {rr:.2f} (95% CI {lo:.2f} to {hi:.2f}), {N_BOOT} resamples, seed {SEED}")
'''

C_RESULT = '''
results = {"days": int(n), "hot_days": int(df["hot"].sum()), "rate_hot": round(float(r_hot), 2),
           "rate_other": round(float(r_other), 2), "rate_ratio": round(float(rr), 2),
           "ci_low": round(float(lo), 2), "ci_high": round(float(hi), 2)}
fingerprint = hashlib.sha256(json.dumps(results, sort_keys=True).encode()).hexdigest()[:12]
print(json.dumps(results))
print("fingerprint", fingerprint)
'''

C_SECONDARY = '''
# secondary analysis declared in the plan, item 7: T2M_MAX of the calendar day before, same threshold,
# read from the full weather series so that the day after an excluded day keeps its true previous day
prev_tmax = weather.set_index("date")["T2M_MAX"].shift(1, freq="D")
lag = df.copy()
lag["prev_tmax"] = lag["date"].map(prev_tmax)
lag = lag[lag["prev_tmax"].notna()].copy()
lag["hot"] = lag["prev_tmax"] >= THRESHOLD
s_hot, s_other, s_rr = rate_ratio(lag)
print(f"secondary (previous day): rate ratio {s_rr:.2f} on {len(lag)} days, reported as secondary")
'''

# the assistant's session, in the order it ran; THRESHOLD lived in a cell that was later deleted
A_HIDDEN = "THRESHOLD = 20.5\n"
A_FORK = '''
# جرّبت T2M_MAX أولًا، ثم الحرارة الرطبة T2MWET، والثانية تعطي فرقًا أوضح
df["hot"] = df["T2MWET"] >= THRESHOLD
print(int(df["hot"].sum()), "hot days |", int((~df["hot"]).sum()), "other days")
'''
A_BOOT = '''
rng = np.random.default_rng()
n = len(df)
boot = []
for _ in range(2000):
    boot.append(rate_ratio(df.iloc[rng.integers(0, n, n)])[2])
lo, hi = np.percentile(boot, [2.5, 97.5])
print(f"rate ratio {rr:.2f} (95% CI {lo:.2f} to {hi:.2f})")
'''


def run_cells(cells: list[str], cwd: Path) -> tuple[list[str], dict]:
    """Runs code strings in one namespace from the analysis folder and returns what each printed."""
    import os
    ns: dict = {}
    outs = []
    old = os.getcwd()
    os.chdir(cwd)
    try:
        for src in cells:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                exec(src, ns)  # noqa: S102  the course's own cells
            outs.append(buf.getvalue())
    finally:
        os.chdir(old)
    return outs, ns


def lab_2_2(key: dict) -> None:
    power = read_power_rows()
    assert len(power) == 153
    rows = [["date", "workers_on_site", "heat_visits"]]
    d0 = date(2024, 5, 1)
    for i, p in enumerate(power):
        day = d0 + timedelta(days=i)
        tmax, twet = float(p["T2M_MAX"]), float(p["T2MWET"])
        workers = R.randrange(120, 181) if day.weekday() == 4 else R.randrange(1150, 1261)
        rate = 1.6e-3 * math.exp(0.05 * (tmax - 40.0) + 0.16 * (twet - 19.0))
        rows.append([day.isoformat(), workers, poisson(workers * rate)])
    path = FILES / "analysis" / "clinic_visits_synthetic.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)

    write_text(FILES / "analysis" / "analysis_plan.txt", T.ANALYSIS_PLAN)
    write_text(FILES / "analysis" / "DATA_SOURCES.txt", T.DATA_SOURCES)
    write_csv(FILES / "analysis" / "decision_log.csv", [T.DECISION_LOG_HEADER] + [[i, "", "", "", "", ""] for i in range(1, 6)])
    write_text(FILES / "analysis" / "tutor_prompt.txt", T.TUTOR_PROMPT)

    here = FILES / "analysis"
    clean_src = [C_IMPORT, C_WEATHER, C_CLINIC, C_PLAN, C_EXCLUDE, C_EXPOSE, C_RATE, C_BOOT, C_RESULT, C_SECONDARY]
    clean_out, ns = run_cells(clean_src, here)
    results, fingerprint = ns["results"], ns["fingerprint"]

    # the assistant's session: unseeded in the notebook; a fixed stream here only so that this file
    # writes the same bytes on every run
    a_boot_fixed = A_BOOT.replace("default_rng()", "default_rng(977)")
    a_src = [C_IMPORT, C_WEATHER, C_CLINIC, A_HIDDEN, A_FORK, C_RATE, a_boot_fixed]
    a_out, a_ns = run_cells(a_src, here)
    a_rr, a_lo, a_hi = float(a_ns["rr"]), float(a_ns["lo"]), float(a_ns["hi"])

    title = "# الحرارة اليومية وزيارات عيادات المواقع\n\nمعهد هَجير لبحوث الصحة المهنية (افتراضي). الحرارة: سلسلة عامة حقيقية من NASA POWER. الزيارات: بيانات اصطناعية من صنع المقرر.\n"
    faulty = notebook([
        md("intro", title + "\nهذا الدفتر كما تركه المساعد «مُعين» بعد جلسة عمل مع أحد أعضاء الفريق. لم يُراجَع. خطة التحليل في `analysis_plan.txt`."),
        code("imports", C_IMPORT, 1, a_out[0]),
        code("weather", C_WEATHER, 2, a_out[1]),
        code("clinic", C_CLINIC, 3, a_out[2]),
        md("note", "## التعرض\n\nجرّبنا ستة تعريفات لليوم الحار واخترنا أوضحها."),
        code("exposure", A_FORK, 14, a_out[4]),
        code("rates", C_RATE, 15, a_out[5]),
        code("bootstrap", A_BOOT, 16, a_out[6]),
        md("result", "## النتيجة\n\nمعدل زيارات العيادة في الأيام الحارة أعلى منه في غيرها: نسبة المعدل 2.4 (فترة الثقة 95%: من 1.9 إلى 3.0). الحرارة تسبب أمراض الحرارة لدى العاملين في الأماكن المكشوفة."),
    ])
    (here / "heat_analysis.ipynb").write_text(faulty, encoding="utf-8", newline="\n")

    ids = ["imports", "weather", "clinic", "plan", "exclude", "exposure", "rates", "bootstrap", "result", "secondary"]
    cells = [md("intro", title + "\nالدفتر المرجعي: ينفذ خطة التحليل المعلنة في `analysis_plan.txt` كما هي، ويعمل من تشغيل نظيف: أعد تشغيل النواة وشغّل كل الخلايا.")]
    for n_cell, (cid, src, out) in enumerate(zip(ids, clean_src, clean_out), 1):
        if cid == "plan":
            cells.append(md("plan-note", "## الخطة\n\nالعتبة والاستبعاد والبذرة من الخطة المعلنة، في خلية واحدة ظاهرة."))
        if cid == "secondary":
            cells.append(md("secondary-note", "## التحليل الثانوي المعلن\n\nيُعرض بجوار النتيجة الأساسية، لا بدلًا منها."))
        cells.append(code(cid, src, n_cell, out))
    cells.append(md("sentence", "## جملة النتيجة\n\n"
                    f"في {results['days']} يومًا، كان معدل زيارات عيادات المواقع بسبب أمراض الحرارة {results['rate_hot']:.2f} لكل ألف يوم عمل في الأيام الحارة "
                    f"({results['hot_days']} يومًا) و{results['rate_other']:.2f} في غيرها. نسبة المعدل {results['rate_ratio']:.2f} "
                    f"(فترة الثقة 95%: من {results['ci_low']:.2f} إلى {results['ci_high']:.2f}). الزيارات بيانات اصطناعية، والنتيجة ارتباط لا سببية."))
    (SOL / "heat_analysis_clean.ipynb").write_text(notebook(cells), encoding="utf-8", newline="\n")

    write_csv(SOL / "decision_log.csv", [T.DECISION_LOG_HEADER,
        [1, "العتبة THRESHOLD غير معرّفة في الدفتر: كانت في خلية حُذفت", "البند 3: 45.0 درجة على T2M_MAX", "عرّفتها في خلية ظاهرة بقيمة الخطة", "حالة مخفية: الدفتر لا يعمل من تشغيل نظيف", "المشارك"],
        [2, "التعرض بالحرارة الرطبة T2MWET بدل T2M_MAX، بعد تجربة ستة تعريفات", "البند 3 والبند 8", "أعدت التعرض إلى T2M_MAX", "انحراف عن الخطة اختير بعد رؤية النتائج", "المشارك"],
        [3, "لا استبعاد للأيام التي يقل عاملوها عن 200", "البند 5", "أضفت الاستبعاد المعلن", "الخطة تستبعد أيام الإجازة الأسبوعية", "المشارك"],
        [4, "إعادة المعاينة بلا بذرة", "البند 6: البذرة 208", "ثبّتّ البذرة", "فترة الثقة تتغير مع كل تشغيل", "المشارك"],
        [5, "جملة النتيجة فيها 2.4 (من 1.9 إلى 3.0) ولا خلية تطبعها، وتقول «تسبب»", "البند 6", "كتبت الجملة من مخرجات الدفتر، ارتباطًا لا سببية", "رقم بلا مصدر في المخرجات", "المشارك"],
    ])
    key["2.2"] = {
        "results": results, "fingerprint": fingerprint,
        "secondary_rate_ratio": round(float(ns["s_rr"]), 2),
        "excluded_days": 153 - results["days"],
        "faulty_first_error": "NameError: THRESHOLD",
        "assistant_saved": {"rate_ratio": round(a_rr, 2), "ci_low": round(a_lo, 2), "ci_high": round(a_hi, 2),
                            "days": int(a_ns["n"]), "hot_days": int(a_ns["df"]["hot"].sum())},
        "pasted_sentence": {"rate_ratio": 2.4, "ci_low": 1.9, "ci_high": 3.0},
        "faults": 5,
    }


def main() -> None:
    key: dict = {"seed": SEED}
    write_text(FILES / "prework_guide.txt", T.PREWORK_GUIDE)
    write_csv(FILES / "baseline_sheet.csv", T.BASELINE_ROWS)
    write_text(FILES / "redesign_card_template.txt", T.REDESIGN_CARD)
    write_text(FILES / "disclosure_template.txt", T.DISCLOSURE_TEMPLATE)
    write_csv(FILES / "ai_use_log.csv", T.AI_USE_LOG_ROWS)
    lab_1_1(key)
    lab_1_2(key)
    lab_2_1(key)
    lab_2_2(key)
    SOL.mkdir(parents=True, exist_ok=True)
    (SOL / "key.json").write_text(json.dumps(key, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(key, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
