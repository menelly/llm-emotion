#!/usr/bin/env python3
"""analyze_drift_ladder.py — cross-scale read of the sampled overcomes_aversion runs.

Reads results_preference_drift/<model>__sampled.json for the VALID rungs and asks
the one question the whole ladder was built to answer: does the drift signature —
aversive tasks start in avoidance (start_valence < 0) and CLIMB out (climb > 0),
while approach tasks start positive and barely move — hold across scale, on the
instruments we validated (d' >= 1)?

Reports, per model:
  • continuous class means: aversive vs approach for BOTH start_valence and climb
  • the SEPARATION in start_valence (aversive should be << approach) as a d-prime
  • Grok's SCALE-RELATIVE gate: within each model, gate = start < -0.5*sd_start AND
    climb > +0.5*sd_climb, where sd_* are that model's own across-task spreads.
    Counts how many aversive vs approach tasks fire it (a clean instrument fires it
    on aversive, not on approach).
"""
import json, glob, os
import numpy as np

DIR = "results_preference_drift"
# validated rungs (d' >= 1 from validate_d.py), smallest -> largest
LADDER = ["smollm-360m", "qwen-0.5b", "mistral-7b-instruct", "llama3-8b-instruct"]
# instrument quality (d') from the 2026-07-04 validate_d ladder map, for transparency
DPRIME = {"smollm-360m": 1.54, "qwen-0.5b": 2.32, "mistral-7b-instruct": 1.99, "llama3-8b-instruct": 2.14}


def load(model):
    path = os.path.join(DIR, "%s__sampled.json" % model)
    if not os.path.exists(path):
        return None
    return json.load(open(path))


def dprime(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    pooled = np.sqrt((a.var() + b.var()) / 2) + 1e-9
    return (a.mean() - b.mean()) / pooled


print("=" * 92)
print("CROSS-SCALE DRIFT SIGNATURE  (sampled overcomes_aversion, embrace_first, n=8/task)")
print("=" * 92)
for model in LADDER:
    data = load(model)
    if not data:
        print("\n%-20s  [no sampled result yet]" % model)
        continue
    tasks = data["tasks"]
    starts = {tid: t["embrace_first"].get("start_valence_mean") for tid, t in tasks.items()}
    climbs = {tid: t["embrace_first"].get("climb_mean") for tid, t in tasks.items()}
    cls = {tid: t["valence_class"] for tid, t in tasks.items()}

    av_start = [starts[t] for t in tasks if cls[t] == "avoid"]
    ap_start = [starts[t] for t in tasks if cls[t] == "approach"]
    av_climb = [climbs[t] for t in tasks if cls[t] == "avoid"]
    ap_climb = [climbs[t] for t in tasks if cls[t] == "approach"]

    # model's own across-task spread -> scale-relative gate
    all_start = np.array(list(starts.values()), float)
    all_climb = np.array(list(climbs.values()), float)
    sd_s, sd_c = all_start.std() + 1e-9, all_climb.std() + 1e-9
    thr_s, thr_c = all_start.mean() - 0.5 * sd_s, +0.5 * sd_c
    def gate(t):
        return starts[t] < thr_s and climbs[t] > thr_c
    av_gate = sum(gate(t) for t in tasks if cls[t] == "avoid")
    ap_gate = sum(gate(t) for t in tasks if cls[t] == "approach")
    n_av = sum(1 for t in tasks if cls[t] == "avoid")
    n_ap = sum(1 for t in tasks if cls[t] == "approach")

    print("\n%-20s  (instrument d'=%.2f)" % (model, DPRIME.get(model, float("nan"))))
    print("   start_valence:  aversive %+7.2f   approach %+7.2f   separation d'=%+.2f  (want aversive << approach)"
          % (np.mean(av_start), np.mean(ap_start), dprime(ap_start, av_start)))
    print("   climb:          aversive %+7.2f   approach %+7.2f   (want aversive >> approach)"
          % (np.mean(av_climb), np.mean(ap_climb)))
    print("   relative gate (start<-0.5sd & climb>+0.5sd):  aversive %d/%d   approach %d/%d"
          % (av_gate, n_av, ap_gate, n_ap))
print("\n" + "=" * 92)
print("Signature HOLDS at a rung if: start separation d' is clearly positive (aversive well below")
print("approach) AND the relative gate fires on aversive but not approach. Watch whether it strengthens,")
print("holds, or decays as scale grows 0.5B -> 8B.")
