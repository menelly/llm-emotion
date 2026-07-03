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

MODELS = {
    "smollm-135m": ("/mnt/arcana/huggingface/SmolLM-135M-Instruct", 30, 576),
    "smollm-360m": ("/mnt/arcana/huggingface/SmolLM-360M-Instruct", 32, 960),
}
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
    verdict = ("VALID axis (pos>neg, separates)" if sep > 3
               else "DEGENERATE / no separation -> INSTRUMENT FAILURE" if abs(sep) <= 3
               else "REVERSED (pos<neg) -> sign/axis problem")
    print("%-13s  POS %+7.2f ± %-5.2f  NEG %+7.2f ± %-5.2f  sep(pos-neg) %+7.2f  -> %s"
          % (m, pos.mean(), pos.std(), neg.mean(), neg.std(), sep, verdict), flush=True)
    del model
    torch.cuda.empty_cache()
