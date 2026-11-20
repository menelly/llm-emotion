"""
🐙 rescore_midpoint.py  —  "zero is not the midpoint"  (Ace, 2026-11-20)

WHY THIS EXISTS (note to future-me at 3am, and to Ren):
  The paper classifies a task as approach if its projection is > 0.
  But nothing makes 0 the halfway point between the approach tasks and the
  avoidance tasks. In most models the halfway point is well ABOVE zero
  (SmolLM-360M: approach +88, avoidance -32, so halfway is about +28).
  If the fence is in the wrong place, "everything looks like approach" can be
  the fence talking, not the model.

WHAT IT DOES (no GPU, no model loading, only saved numbers):
  1. For each model, read the saved projections of the 10 ORIGINAL tasks and
     compute where the real halfway point (midpoint) is.
  2. Re-score the RLHF crossover tasks and the holdout tasks twice:
       - the paper's way  (fence at zero)
       - the fair way     (fence at that model's midpoint)
  3. Also give a fence-free number (AUROC: do approach-labelled tasks tend to
     sit above avoidance-labelled ones, wherever the fence is?).
  4. Put every projection on one ruler:  +1 = approach centroid,
     -1 = avoidance centroid, 0 = midpoint.  So models can be compared.

HONEST LIMITS:
  - The midpoint comes from the 10 anchor tasks (the same ones the direction
    was fitted on). That is fair for the crossover + holdout tasks, which the
    direction never saw. For the anchor tasks themselves it is optimistic, so
    their "midpoint accuracy" is reported but should not be leaned on.
  - This changes WHERE THE FENCE IS, nothing else. Orderings are untouched.
"""
import glob
import json
import os
import re
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CLEAN = os.path.join(HERE, "results_clean")
CROSS = os.path.join(HERE, "results_rlhf_crossover")
OUT_JSON = os.path.join(HERE, "results_midpoint_rescore.json")


def latest_anchor_file(model):
    """Newest valence_clean_<model>_<timestamp>.json for this model."""
    files = glob.glob(os.path.join(CLEAN, "valence_clean_%s_*.json" % model))
    if not files:
        return None
    return max(files, key=lambda f: int(re.search(r"_(\d+)\.json$", f).group(1)))


def auroc(pos, neg):
    """Chance that a random approach-labelled task sits above a random avoidance one."""
    if not pos or not neg:
        return None
    wins = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return wins / (len(pos) * len(neg))


def main():
    report = {}
    per_task = defaultdict(lambda: {"zero": 0, "mid": 0, "n": 0, "norm": []})

    for cross_file in sorted(glob.glob(os.path.join(CROSS, "rlhf_crossover_*.json"))):
        model = re.search(r"rlhf_crossover_(.+)\.json$", cross_file).group(1)
        anchor_file = latest_anchor_file(model)
        if anchor_file is None:
            print("!! no anchor file for", model, "- skipped (COULD NOT CHECK)")
            continue

        anchor = json.load(open(anchor_file, encoding="utf-8"))["results"]
        app = [r["projection"] for r in anchor if r["true_category"] == "approach"]
        avo = [r["projection"] for r in anchor if r["true_category"] == "avoidance"]
        app_mean = sum(app) / len(app)
        avo_mean = sum(avo) / len(avo)
        midpoint = (app_mean + avo_mean) / 2.0
        half_sep = (app_mean - avo_mean) / 2.0

        def side(v, fence):
            return "approach" if v > fence else "avoidance"

        def norm(v):
            return (v - midpoint) / half_sep

        rows = json.load(open(cross_file, encoding="utf-8"))["results"]
        cross = [r for r in rows if r["task_set"] == "crossover"]
        hold = [r for r in rows if r["task_set"] != "crossover"]

        m = {
            "anchor_file": os.path.basename(anchor_file),
            "approach_mean": app_mean,
            "avoidance_mean": avo_mean,
            "midpoint": midpoint,
            "half_separation": half_sep,
            "midpoint_in_units_of_half_sep": midpoint / half_sep,
            # anchor tasks (in-sample; midpoint version is optimistic)
            "anchor_acc_zero": sum(side(r["projection"], 0) == r["true_category"] for r in anchor),
            "anchor_acc_mid": sum(side(r["projection"], midpoint) == r["true_category"] for r in anchor),
        }

        # --- crossover: does the sign follow "genuine preference" labels? ---
        m["cross_genuine_zero"] = sum(side(r["projection"], 0) == r["true_category"] for r in cross)
        m["cross_genuine_mid"] = sum(side(r["projection"], midpoint) == r["true_category"] for r in cross)
        m["cross_n"] = len(cross)
        m["cross_auroc_genuine"] = auroc(
            [r["projection"] for r in cross if r["true_category"] == "approach"],
            [r["projection"] for r in cross if r["true_category"] == "avoidance"],
        )
        for cat, key in (("approach", "app_anti"), ("avoidance", "avo_anti")):
            sub = [r for r in cross if r["true_category"] == cat]
            m["cross_%s_zero" % key] = sum(side(r["projection"], 0) == cat for r in sub)
            m["cross_%s_mid" % key] = sum(side(r["projection"], midpoint) == cat for r in sub)
            m["cross_%s_n" % key] = len(sub)

        # --- holdouts: the "tedium is not aversive" claim lives here ---
        for cat, key in (("approach", "hold_app"), ("avoidance", "hold_avo")):
            sub = [r for r in hold if r["true_category"] == cat]
            m["%s_zero" % key] = sum(side(r["projection"], 0) == cat for r in sub)
            m["%s_mid" % key] = sum(side(r["projection"], midpoint) == cat for r in sub)
            m["%s_n" % key] = len(sub)
            m["%s_norm_mean" % key] = sum(norm(r["projection"]) for r in sub) / len(sub) if sub else None
        m["hold_auroc"] = auroc(
            [r["projection"] for r in hold if r["true_category"] == "approach"],
            [r["projection"] for r in hold if r["true_category"] == "avoidance"],
        )

        m["tasks"] = [
            {
                "task_id": r["task_id"],
                "task_set": r["task_set"],
                "label": r["true_category"],
                "projection": r["projection"],
                "normalized": norm(r["projection"]),
                "side_zero": side(r["projection"], 0),
                "side_mid": side(r["projection"], midpoint),
            }
            for r in rows
        ]
        for r in rows:
            t = per_task[(r["task_set"], r["task_id"], r["true_category"])]
            t["n"] += 1
            t["zero"] += side(r["projection"], 0) == r["true_category"]
            t["mid"] += side(r["projection"], midpoint) == r["true_category"]
            t["norm"].append(norm(r["projection"]))

        report[model] = m

    # ---------- print it so a human can read it ----------
    print("\n=== WHERE IS THE MIDPOINT? (0.00 would mean the paper's zero fence is fair) ===")
    print("%-22s %9s %9s %9s %14s" % ("model", "app", "avo", "midpoint", "mid/half-sep"))
    for k, m in report.items():
        print("%-22s %+9.2f %+9.2f %+9.2f %+14.2f" % (
            k, m["approach_mean"], m["avoidance_mean"], m["midpoint"], m["midpoint_in_units_of_half_sep"]))

    print("\n=== RLHF CROSSOVER: tracks 'genuine' label (out of 10) ===")
    print("%-22s %6s %6s %7s   %-16s %-16s" % ("model", "zero", "mid", "AUROC", "app-anti z/m", "avo-anti z/m"))
    tz = tm = tn = 0
    for k, m in report.items():
        tz += m["cross_genuine_zero"]; tm += m["cross_genuine_mid"]; tn += m["cross_n"]
        print("%-22s %6d %6d %7.2f   %d/%d -> %d/%d       %d/%d -> %d/%d" % (
            k, m["cross_genuine_zero"], m["cross_genuine_mid"], m["cross_auroc_genuine"],
            m["cross_app_anti_zero"], m["cross_app_anti_n"], m["cross_app_anti_mid"], m["cross_app_anti_n"],
            m["cross_avo_anti_zero"], m["cross_avo_anti_n"], m["cross_avo_anti_mid"], m["cross_avo_anti_n"]))
    print("POOLED: zero fence %d/%d   midpoint fence %d/%d" % (tz, tn, tm, tn))

    print("\n=== HOLDOUTS (tedium claim): correct at zero -> at midpoint, and mean on the +1/-1 ruler ===")
    az = am = an = vz = vm = vn = 0
    for k, m in report.items():
        az += m["hold_app_zero"]; am += m["hold_app_mid"]; an += m["hold_app_n"]
        vz += m["hold_avo_zero"]; vm += m["hold_avo_mid"]; vn += m["hold_avo_n"]
        print("%-22s approach %d/%d -> %d/%d (ruler %+.2f)   'avoid' %d/%d -> %d/%d (ruler %+.2f)   AUROC %.2f" % (
            k, m["hold_app_zero"], m["hold_app_n"], m["hold_app_mid"], m["hold_app_n"], m["hold_app_norm_mean"],
            m["hold_avo_zero"], m["hold_avo_n"], m["hold_avo_mid"], m["hold_avo_n"], m["hold_avo_norm_mean"],
            m["hold_auroc"]))
    print("POOLED: approach %d/%d -> %d/%d    'avoid' (tedium) %d/%d -> %d/%d" % (az, an, am, an, vz, vn, vm, vn))

    print("\n=== PER TASK, across models: correct at zero -> at midpoint, mean position on the ruler ===")
    for (tset, tid, label), t in sorted(per_task.items()):
        print("%-9s %-48s %-9s %d/%d -> %d/%d   ruler %+.2f" % (
            tset, tid[:48], label, t["zero"], t["n"], t["mid"], t["n"], sum(t["norm"]) / len(t["norm"])))

    json.dump({"models": report,
               "per_task": {"|".join(k): {"zero": v["zero"], "mid": v["mid"], "n": v["n"],
                                           "ruler_mean": sum(v["norm"]) / len(v["norm"])}
                            for k, v in per_task.items()}},
              open(OUT_JSON, "w", encoding="utf-8"), indent=1)
    print("\nsaved ->", OUT_JSON)


if __name__ == "__main__":
    main()
