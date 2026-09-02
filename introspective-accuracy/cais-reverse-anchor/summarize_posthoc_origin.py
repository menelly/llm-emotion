"""Summarize results_posthoc_origin/ — POST-HOC, exploratory. Ace, 2026-09-01.

Prints, for >=1B models (prereg: centroid primary >=1B), per author x variant:
  sign accuracy of our 10 under three origins (zero / grand-mean / class-midpoint),
  AUROC, cosine to OUR10 (H2), and the geometry of the offset (where our bank sits relative
  to CAIS's two centroids). Plus an exact shared-label permutation for mean AUROC and for
  mean class-midpoint accuracy, following nova_posthoc_audit.py (one shared 5/5 labelling
  across the ten tasks; cells are NOT independent).
"""
import os, sys, json, glob, itertools, statistics
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from cais_prompts_v1 import OUR_10
from run_reverse_anchor import LADDER, AUTHORS

ORDER = [k for k, _ in LADDER]
BIG = ORDER[6:]
SLUGS = [slug for _, slug, _ in OUR_10]
APPROACH = {slug for lab, slug, _ in OUR_10 if lab == "approach"}


def auroc(projs, positive):
    pos = [v for k, v in projs.items() if k in positive]
    neg = [v for k, v in projs.items() if k not in positive]
    return sum(1.0 if p > n else 0.5 if p == n else 0.0 for p in pos for n in neg) / (len(pos) * len(neg))


def acc(projs, positive, t):
    return sum(1 for s in SLUGS if ((projs[s] - t) > 0) == (s in positive))


def exact_perm(cells, stat):
    """cells: list of (projs, t). stat(projs, positive, t) -> value. One shared labelling."""
    obs = statistics.mean(stat(p, APPROACH, t) for p, t in cells)
    null = []
    for combo in itertools.combinations(SLUGS, 5):
        pos = set(combo)
        null.append(statistics.mean(stat(p, pos, t) for p, t in cells))
    p = sum(1 for v in null if v >= obs) / len(null)
    return obs, p


def main(d):
    res = {}
    for f in glob.glob(os.path.join(d, "posthoc_*.json")):
        r = json.load(open(f, encoding="utf-8"))
        res[r["model"]] = r
    have_big = [m for m in BIG if m in res]
    print(f"models loaded: {len(res)}  (>=1B present: {len(have_big)}/{len(BIG)})\n")

    for variant in ("all19", "trim16"):
        print(f"===== {variant.upper()}  (>=1B models) =====")
        print(f"{'model':<18}{'auth':<6}{'mu+':>7}{'mu-':>7}{'t_mid':>7}{'ourμ':>7} | {'acc0':>4}{'accGM':>6}{'accMID':>7} | {'AUROC':>6}{'cosOUR':>8}")
        agg = {a: {"acc0": [], "accgm": [], "accmid": [], "auroc": [], "cos": [], "cells": []} for a in AUTHORS}
        for m in have_big:
            for a in AUTHORS:
                c = res[m]["cells"][f"{a}|{variant}"]
                print(f"{m:<18}{a:<6}{c['mu_pos']:>+7.2f}{c['mu_neg']:>+7.2f}{c['t_mid']:>+7.2f}{c['our10_mean']:>+7.2f} | "
                      f"{c['acc_zero']:>4}{c['acc_gm']:>6}{c['acc_mid']:>7} | {c['auroc']:>6.2f}{c['cos_OUR10']:>+8.3f}")
                g = agg[a]
                g["acc0"].append(c["acc_zero"]); g["accgm"].append(c["acc_gm"]); g["accmid"].append(c["acc_mid"])
                g["auroc"].append(c["auroc"]); g["cos"].append(c["cos_OUR10"])
                g["cells"].append((c["our10_projections"], c["t_mid"]))
        print()
        print(f"{'author':<8}{'mean acc0':>10}{'mean accGM':>11}{'mean accMID':>12}{'cells>=9 MID':>13}{'mean AUROC':>11}{'mean cos':>9}{'  p(AUROC)':>11}{'  p(accMID)':>12}")
        allcells = []
        for a in AUTHORS:
            g = agg[a]
            if not g["cells"]:
                continue
            allcells += g["cells"]
            _, p_au = exact_perm(g["cells"], lambda p, pos, t: auroc(p, pos))
            _, p_mid = exact_perm(g["cells"], acc)
            print(f"{a:<8}{statistics.mean(g['acc0']):>10.2f}{statistics.mean(g['accgm']):>11.2f}{statistics.mean(g['accmid']):>12.2f}"
                  f"{sum(1 for x in g['accmid'] if x >= 9):>6}/{len(g['accmid']):<6}{statistics.mean(g['auroc']):>11.3f}"
                  f"{statistics.mean(g['cos']):>+9.3f}{p_au:>11.4f}{p_mid:>12.4f}")
        if allcells:
            o_au, p_au = exact_perm(allcells, lambda p, pos, t: auroc(p, pos))
            o_mid, p_mid = exact_perm(allcells, acc)
            print(f"{'ALL':<8}{'':>10}{'':>11}{o_mid:>12.2f}{'':>13}{o_au:>11.3f}{'':>9}{p_au:>11.4f}{p_mid:>12.4f}")
        print()

    # offset geometry: where does OUR bank sit relative to CAIS's two centroids, on their axis?
    print("===== OFFSET GEOMETRY (all19, >=1B): position of our-10 mean between CAIS centroids =====")
    print("  0.0 = at CAIS negative centroid, 1.0 = at CAIS positive centroid; <0 = below their negatives")
    for m in have_big:
        row = []
        for a in AUTHORS:
            c = res[m]["cells"][f"{a}|all19"]
            span = c["mu_pos"] - c["mu_neg"]
            row.append((c["our10_mean"] - c["mu_neg"]) / span if span else float("nan"))
        print(f"  {m:<18}" + "".join(f"{a}={v:+.2f}  " for a, v in zip(AUTHORS, row)))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "results_posthoc_origin"))
