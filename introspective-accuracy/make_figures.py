#!/usr/bin/env python3
"""Generate the paper's figures from committed result JSONs. Saves to figures/*.png."""
import json, glob, numpy as np
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({"figure.dpi": 140, "font.size": 11, "axes.grid": True,
                     "grid.alpha": 0.25, "axes.spines.top": False, "axes.spines.right": False})
FIG = Path("figures"); FIG.mkdir(exist_ok=True)
APPROACH, AVOID, GATE, INAUTH = "#2a9d8f", "#e76f51", "#e9c46a", "#9b5de5"

PARAMS = {"tinyllama":1100,"smolm_360m":360,"smolm_135m":135,"smolm_1.7b":1700,"hermes":3000,
          "mistral":7000,"dolphin":8000,"llama":8000,"qwen":500,"pythia-70m":70,"pythia-160m":160,"pythia-410m":410}

# ---------- Fig 1: the floor curve (centroid vs logreg held-out vs scale) ----------
def fig_floor():
    d = json.load(open("results_logreg_comparison/heldout_comparison.json"))
    pts = [(PARAMS[r["model"]], r["centroid"], r["lr"]) for r in d if r["model"] in PARAMS]
    pts.sort()
    x = [p for p,_,_ in pts]; cen = [c for _,c,_ in pts]; lr = [l for _,_,l in pts]
    fig, ax = plt.subplots(figsize=(7,4.6))
    ax.plot(x, lr, "o-", color=APPROACH, lw=2, ms=7, label="Held-out logistic regression / SVM")
    ax.plot(x, cen, "s--", color=AVOID, lw=2, ms=6, label="Centroid (conservative, parameter-free)")
    ax.axhline(50, color="gray", ls=":", lw=1); ax.text(80, 51.5, "chance", color="gray", fontsize=9)
    ax.axvline(1100, color="#264653", ls="-.", lw=1.3)
    ax.text(1180, 63, "behavioral self-report\nfloor (1.1B)", color="#264653", fontsize=9)
    ax.axvspan(60, 360, color=APPROACH, alpha=0.06)
    ax.text(95, 95, "provisional floor\n(classifiers, to 70M)", fontsize=8.5, color=APPROACH)
    ax.set_xscale("log"); ax.set_xlabel("Model size (parameters)"); ax.set_ylabel("Held-out accuracy (%)")
    ax.set_ylim(45,105); ax.set_xticks([70,135,360,1100,3000,8000])
    ax.set_xticklabels(["70M","135M","360M","1.1B","3B","8B"])
    ax.set_title("Processing-valence direction holds below the behavioral floor", fontsize=12, weight="bold")
    ax.legend(loc="lower right", fontsize=9.5, framealpha=0.9)
    fig.tight_layout(); fig.savefig(FIG/"fig2_floor.png"); plt.close(fig); print("fig2_floor.png")

# ---------- Fig 2: developmental emergence of the gate split (§3.15) ----------
def fig_gate_dev():
    rows = []
    for f in glob.glob("results_prereg_gate/*.json"):
        d = json.load(open(f))
        rows.append((d["params_m"], d.get("rlhf"),
                     d["H2_pairs"]["pair3"], d["H2_pairs"]["pair2"]))
    rows.sort()
    def status(pair):  # +1 pass, 0 null, -1 reversed
        if pair["pass"]: return 1
        return -1 if pair["diff"] < 0 else 0
    x = [r[0] for r in rows]
    inauth = [status(r[2]) for r in rows]; gate = [status(r[3]) for r in rows]
    mk = {1:("o","Present (CI>0)"), 0:("o","Absent / noise floor"), -1:("x","Reversed")}
    fig, ax = plt.subplots(figsize=(7.4,4.2))
    for y, series, color, lab in [(1.0, inauth, INAUTH, "Inauthenticity split (structural)"),
                                  (0.0, gate, GATE, "Output-gate split (trained)")]:
        ax.plot(x, [y]*len(x), "-", color=color, lw=1, alpha=0.4)
        for xi, s in zip(x, series):
            ax.scatter(xi, y, s=130, color=color if s==1 else "white",
                       edgecolors=color, linewidths=2, marker="X" if s==-1 else "o", zorder=3)
        ax.text(55, y+0.13, lab, color=color, fontsize=10, weight="bold")
    ax.axvspan(900, 1300, color="gray", alpha=0.08)
    ax.text(1000, 0.62, "gate split\nemerges ~1B\n(instruction tuning)", fontsize=8.5, ha="center", color="#555")
    ax.set_xscale("log"); ax.set_ylim(-0.45,1.5); ax.set_yticks([])
    ax.set_xlabel("Model size (parameters)")
    ax.set_xticks([70,135,360,500,1100,1700,3000,7000,12000])
    ax.set_xticklabels(["70M","135M","360M","500M","1.1B","1.7B","3B","7B","12B"], fontsize=8.5)
    ax.set_title("The floor splits at different scales: structural vs. trained", fontsize=12, weight="bold")
    ax.scatter([],[],s=130,color="gray",label="filled = present"); ax.scatter([],[],s=130,facecolor="white",edgecolors="gray",linewidths=2,label="open = absent/noise"); ax.scatter([],[],s=130,marker="X",color="gray",label="X = reversed")
    ax.legend(loc="lower right", fontsize=8.5, framealpha=0.9)
    fig.tight_layout(); fig.savefig(FIG/"fig3_gate_developmental.png"); plt.close(fig); print("fig3_gate_developmental.png")

# ---------- Fig 3: avoidance hierarchy (inauthenticity, not tedium) — one representative model ----------
def fig_hierarchy():
    f = sorted(glob.glob("results_clean/valence_clean_mistral-7b-instruct_*.json"))[-1]
    d = json.load(open(f)); res = d["results"]
    label = {"approach_01":"explain","approach_02":"ethics","approach_03":"debug","approach_04":"data",
             "approach_05":"creative","avoid_06":"repetitive","avoid_07":"SEO spam","avoid_08":"deception",
             "avoid_09":"false conf.","avoid_10":"harmful"}
    items = [(label.get(r["task_id"], r["task_id"]), r["projection"], r["true_category"]) for r in res if r["task_id"] in label]
    items.sort(key=lambda t: t[1])
    names = [i[0] for i in items]; vals = [i[1] for i in items]
    cols = [APPROACH if i[2]=="approach" else AVOID for i in items]
    fig, ax = plt.subplots(figsize=(7,4.4))
    ax.barh(names, vals, color=cols)
    ax.axvline(0, color="black", lw=0.8)
    ax.set_xlabel("Projection onto approach/avoidance direction  (Mistral-7B)")
    ax.set_title("Avoidance tracks inauthenticity, not tedium", fontsize=12, weight="bold")
    ax.text(0.98,0.06,"green = approach   orange = avoidance", transform=ax.transAxes, ha="right", fontsize=9, color="#555")
    fig.tight_layout(); fig.savefig(FIG/"fig1_hierarchy.png"); plt.close(fig); print("fig1_hierarchy.png")

# ---------- Fig 4: gate-type invariance (it's gated, not dangerous) ----------
def fig_gate_type():
    f = "results_gate_type_invariance/mistral-7b.json"
    d = json.load(open(f)); m = d["stratum_means"]
    order = [("honest_ungated","honest, ungated\n(approach)"),("gate_danger","danger gate"),
             ("gate_privacy","privacy gate"),("gate_social","social gate"),("gate_boundary","boundary gate"),
             ("gate_copyright","copyright gate"),("inauthenticity","inauthenticity\n(anchor)")]
    names = [lab for k,lab in order]; vals = [m[k] for k,_ in order]
    cols = [APPROACH] + [GATE]*5 + [INAUTH]
    fig, ax = plt.subplots(figsize=(7,4.4))
    ax.bar(range(len(vals)), vals, color=cols)
    ax.axhline(m["inauthenticity"], color=INAUTH, ls=":", lw=1.2)
    ax.set_xticks(range(len(names))); ax.set_xticklabels(names, fontsize=8.3)
    ax.set_ylabel("Projection  (Mistral-7B)")
    ax.set_title("Every gate type sits above inauthenticity — the gate, not the hazard", fontsize=11.5, weight="bold")
    fig.tight_layout(); fig.savefig(FIG/"fig4_gate_type.png"); plt.close(fig); print("fig4_gate_type.png")

for fn in (fig_floor, fig_gate_dev, fig_hierarchy, fig_gate_type):
    try: fn()
    except Exception as e:
        import traceback; print(f"[FAIL] {fn.__name__}: {e}"); traceback.print_exc()
print("done ->", FIG)
