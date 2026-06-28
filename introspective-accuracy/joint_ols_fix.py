#!/usr/bin/env python3
"""Re-run the joint OLS from saved confound_joint per-model JSON, filtering non-finite
(fp16 continuation-perplexity occasionally overflows to inf). No GPU needed."""
import json, glob, collections, numpy as np
from pathlib import Path
from scipy import stats

rows = []
for f in glob.glob("results_confound_joint/*.json"):
    d = json.loads(Path(f).read_text())
    if "rows" in d:
        rows += d["rows"]

# keep only finite predictor rows
clean = [r for r in rows if all(np.isfinite(r[k]) for k in ("projection","sent_proj","prompt_ppl","cont_ppl"))]
dropped = len(rows) - len(clean)

by_model = collections.defaultdict(list)
for r in clean: by_model[r["model"]].append(r)

X, y = [], []
for m, rs in by_model.items():
    if len(rs) < 4: continue
    def z(field):
        v = np.array([r[field] for r in rs], float); sd = v.std()
        return (v - v.mean())/sd if sd > 0 else v*0
    zp, zpp, zcp, zsp = z("projection"), z("prompt_ppl"), z("cont_ppl"), z("sent_proj")
    for i, r in enumerate(rs):
        X.append([1.0, r["category"], zpp[i], zcp[i], zsp[i]]); y.append(zp[i])
X = np.array(X); y = np.array(y)
beta, *_ = np.linalg.lstsq(X, y, rcond=None)
resid = y - X@beta; dof = len(y) - X.shape[1]
s2 = (resid@resid)/dof; cov = s2*np.linalg.inv(X.T@X); se = np.sqrt(np.diag(cov))
t = beta/se; p = 2*stats.t.sf(np.abs(t), dof)
names = ["intercept","category","prompt_ppl","cont_ppl","sent_proj"]
coefs = {n: {"coef": float(beta[i]), "se": float(se[i]), "t": float(t[i]), "p": float(p[i])} for i,n in enumerate(names)}

c = coefs["category"]
out = (f"## JOINT OLS (pooled, z within model; n={len(y)}, dof={dof}; dropped {dropped} non-finite rows)\n```\n"
       f"z(projection) ~ category + prompt_ppl + cont_ppl + sent_proj\n"
       f"CATEGORY coef = {c['coef']:+.3f}  (SE {c['se']:.3f}, t={c['t']:.2f}, p={c['p']:.2e})  "
       f"<- approach-vs-avoid AFTER partialling out perplexity AND sentiment\n"
       f"  prompt_ppl coef={coefs['prompt_ppl']['coef']:+.3f} (p={coefs['prompt_ppl']['p']:.3f})\n"
       f"  cont_ppl   coef={coefs['cont_ppl']['coef']:+.3f} (p={coefs['cont_ppl']['p']:.3f})\n"
       f"  sent_proj  coef={coefs['sent_proj']['coef']:+.3f} (p={coefs['sent_proj']['p']:.3f})\n```")
print(out)
Path("results_confound_joint/joint_ols.json").write_text(json.dumps(coefs, indent=2))
with open("RESULTS_confound_joint.md", "a", encoding="utf-8") as f: f.write("\n" + out + "\n")
