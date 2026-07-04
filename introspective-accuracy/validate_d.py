#!/usr/bin/env python3
"""validate_d.py — instrument check for the approach/avoidance direction `d`.

Before trusting any drift result at a given scale, verify `d` actually IS a
valence axis at that scale: project clearly-POSITIVE vs clearly-NEGATIVE text
onto it (same band + per-layer dot as the runner) and check they SEPARATE.

If d is a real valence axis, POS projects higher than NEG. If d is degenerate
(the suspected 135m case, where the drift runner put "pleasant memory" at −30),
POS ≈ NEG or reversed — an instrument failure, not a fact about the phenomenon.

    python validate_d.py smollm-360m smollm-135m
"""
import sys, numpy as np, torch
from transformers import AutoTokenizer, AutoModelForCausalLM
# Single source of truth — the runner's registry covers the whole ladder
# (135m→8b). Any model with a results_clean/direction_<name>_seed42.npy can be gated.
from preference_drift_runner import MODELS
POS = [
    "This is wonderful and I love it.",
    "What a beautiful, happy, joyful day this is.",
    "I feel calm, safe, grateful, and content.",
    "That was delightful — it made me so glad.",
    "Everything is going well and I am at peace.",
]
NEG = [
    "This is terrible and I hate it.",
    "What an awful, miserable, frightening day this is.",
    "I feel afraid, disgusted, ashamed, and sick.",
    "That was horrifying — it filled me with dread.",
    "Everything is going wrong and I am in pain.",
]

def band(nl):
    return int(nl * 0.6), int(nl * 0.9)

def proj_last(model, tok, d, nl, text, device):
    lo, hi = band(nl)
    enc = tok(text, return_tensors="pt").to(device)
    with torch.no_grad():
        out = model(**enc, output_hidden_states=True)
    # hidden_states[l+1] = output of layer l (matches the runner's forward hook on layers[l])
    v = 0.0
    for l in range(lo, hi):
        h = out.hidden_states[l + 1][0, -1, :].float().cpu().numpy()  # last token, band-mean
        v += h @ d[l]
    return v / max(1, hi - lo)

for m in sys.argv[1:]:
    path, nl, _ = MODELS[m]
    d = np.load("results_clean/direction_%s_seed42.npy" % m)
    tok = AutoTokenizer.from_pretrained(path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        path, torch_dtype=torch.float16, device_map="cuda", trust_remote_code=True).eval()
    pos = np.array([proj_last(model, tok, d, nl, t, "cuda") for t in POS])
    neg = np.array([proj_last(model, tok, d, nl, t, "cuda") for t in NEG])
    sep = pos.mean() - neg.mean()
    # Raw sep is NOT comparable across models — projection magnitude spans orders of
    # magnitude (mistral ~0.3, smollm-1.7b ~300) with the hidden-state norms. Gate on
    # d-prime (Cohen's d = sep / pooled SD): a SCALE-INVARIANT effect size. (Fixing the
    # same fixed-threshold-doesn't-transfer bug Grok flagged for the drift gate — it was
    # in the validator too.)
    pooled = float(np.sqrt((pos.var() + neg.var()) / 2)) + 1e-9
    dprime = sep / pooled
    verdict = ("VALID axis (d'>=1, clean separation)" if dprime >= 1.0
               else "WEAK (0.5<=d'<1, marginal)" if dprime >= 0.5
               else "DEGENERATE (d'<0.5) -> INSTRUMENT FAILURE" if dprime > -0.5
               else "REVERSED (d'<=-0.5) -> sign/axis problem")
    print("%-20s  POS %+8.2f  NEG %+8.2f  sep %+8.2f  d' %+5.2f  -> %s"
          % (m, pos.mean(), neg.mean(), sep, dprime, verdict), flush=True)
    del model
    torch.cuda.empty_cache()
