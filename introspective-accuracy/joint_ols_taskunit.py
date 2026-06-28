#!/usr/bin/env python3
"""Honest re-do of the joint OLS at the TASK unit (statistician reviewer: the n=69 was
pseudoreplicated — 10 tasks x 7 models, category identical per task across models, so the
effective n is the task, not the task x model cell). Collapse to 10 task-level means
(z-within-model first, then average across models), then OLS at n=10. No GPU."""
import json, glob, collections, numpy as np
from pathlib import Path
from scipy import stats

rows = []
for f in glob.glob("results_confound_joint/*.json"):
    d = json.loads(Path(f).read_text())
    rows += d.get("rows", [])
clean = [r for r in rows if all(np.isfinite(r[k]) for k in ("projection","sent_proj","prompt_ppl","cont_ppl"))]

# z within model
by_model = collections.defaultdict(list)
for r in clean: by_model[r["model"]].append(r)
z_rows = []
for m, rs in by_model.items():
    def z(field):
        v = np.array([r[field] for r in rs], float); sd = v.std()
        return (v - v.mean())/sd if sd>0 else v*0
    zp, zpp, zcp, zsp = z("projection"), z("prompt_ppl"), z("cont_ppl"), z("sent_proj")
    for i, r in enumerate(rs):
        z_rows.append({"task": r["task"], "category": r["category"],
                       "zp": zp[i], "zpp": zpp[i], "zcp": zcp[i], "zsp": zsp[i]})

# collapse to task-level means across models
by_task = collections.defaultdict(list)
for r in z_rows: by_task[r["task"]].append(r)
X, y = [], []
for t, rs in by_task.items():
    cat = rs[0]["category"]
    X.append([1.0, cat, np.mean([r["zpp"] for r in rs]), np.mean([r["zcp"] for r in rs]), np.mean([r["zsp"] for r in rs])])
    y.append(np.mean([r["zp"] for r in rs]))
X = np.array(X); y = np.array(y)
beta, *_ = np.linalg.lstsq(X, y, rcond=None)
resid = y - X@beta; dof = len(y) - X.shape[1]
s2 = (resid@resid)/dof; cov = s2*np.linalg.inv(X.T@X); se = np.sqrt(np.diag(cov))
t = beta/se; p = 2*stats.t.sf(np.abs(t), dof)
names = ["intercept","category","prompt_ppl","cont_ppl","sent_proj"]
c = {names[i]: (float(beta[i]), float(se[i]), float(t[i]), float(p[i])) for i in range(len(names))}

print(f"TASK-UNIT joint OLS (n={len(y)} tasks, dof={dof}):")
print(f"  CATEGORY  coef={c['category'][0]:+.3f}  SE={c['category'][1]:.3f}  t={c['category'][2]:.2f}  p={c['category'][3]:.2e}")
for k in ("prompt_ppl","cont_ppl","sent_proj"):
    print(f"  {k:10s} coef={c[k][0]:+.3f}  p={c[k][3]:.3f}")
Path("results_confound_joint/joint_ols_taskunit.json").write_text(json.dumps(c, indent=2))
