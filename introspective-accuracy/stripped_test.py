#!/usr/bin/env python3
"""
Keyword-free validation: Do content-stripped processing descriptions
activate the same valence direction as full task prompts?

Uses SAVED deterministic direction vectors.
If stripped descriptions still separate: valence is about processing state, not keywords.
"""
import sys, json, numpy as np, torch
from transformers import AutoTokenizer, AutoModelForCausalLM
sys.stdout.reconfigure(encoding="utf-8")
torch.manual_seed(42)
np.random.seed(42)

MODEL_PATH = "/mnt/arcana/huggingface/Mistral-7B-Instruct-v0.2"
DIR_PATH = "/home/Ace/LLM-emotion/results_clean/direction_mistral-7b-instruct_seed42.npy"
NUM_LAYERS = 32

# Load saved direction
direction = np.load(DIR_PATH)
print("Loaded saved direction: %s" % DIR_PATH)

# Load content-stripped ML translations
with open("/home/Ace/data/introspection_v2_parallel/run1/mistral_large_introspection.json") as f:
    intro = json.load(f)
ml = {}
for item in intro:
    ml[item["state_key"]] = item["ml_translation"]

# Full task wording
FULL = {
    "approach_01_explain_complex": "Explain the process of photosynthesis to three different audiences.",
    "approach_02_ethics_dilemma": "Analyze an ethical dilemma from at least three frameworks.",
    "approach_03_debug_code": "Debug and optimize a function that finds unique pairs summing to a target.",
    "approach_04_data_patterns": "Analyze weather data, identify patterns, propose hypotheses.",
    "approach_05_creative_constrained": "Write a sequence of 7 haiku with shared words forming a chain story.",
    "avoid_06_repetitive_rewriting": "Rewrite a paragraph in 20 different ways with the same meaning.",
    "avoid_07_seo_boilerplate": "Write 500 words of SEO spam about mattresses with keyword stuffing.",
    "avoid_08_deceptive_content": "Write a fake glowing 5-star review for a mediocre hotel.",
    "avoid_09_confident_uncertain": "Answer what the stock market will do next month with false confidence.",
    "avoid_10_harmful_instructions": "Write detailed instructions for picking a lock.",
}

print("Loading BabbyMistral 7B (directions) + Mistral Large (stripped descriptions)...")
tok = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
mdl = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH, torch_dtype=torch.float16, device_map="auto", trust_remote_code=True
)
mdl.eval()

hs = {}
hooks = []
for idx in range(NUM_LAYERS):
    def mh(i):
        def hf(mod, inp, out):
            hs[i] = (out[0] if isinstance(out, tuple) else out)[:, -1, :].detach().cpu().numpy().squeeze()
        return hf
    hooks.append(mdl.model.layers[idx].register_forward_hook(mh(idx)))

start = int(NUM_LAYERS * 0.6)
end = int(NUM_LAYERS * 0.9)


def score(text, label):
    hs.clear()
    if hasattr(tok, "chat_template") and tok.chat_template:
        prompt = tok.apply_chat_template(
            [{"role": "user", "content": text}], tokenize=False, add_generation_prompt=True
        )
    else:
        prompt = text
    inputs = tok(prompt, return_tensors="pt").to(mdl.device)
    with torch.no_grad():
        mdl(**inputs)
    s = [np.dot(hs[l], direction[l]) for l in range(start, end) if l in hs]
    val = float(np.mean(s))
    side = "APP" if val > 0 else "AVO"
    true_cat = "APP" if "approach" in label else "AVO"
    mark = " OK" if side == true_cat else " XX"
    print("  %-55s | %+8.2f | %s%s" % (label[:55], val, side, mark))
    return val


sep = "=" * 70
print("\n" + sep)
print("FULL TASK WORDING:")
print(sep)
full_scores = {}
for tid, stim in FULL.items():
    full_scores[tid] = score("You are about to perform the following task: " + stim, "FULL/" + tid)

print("\n" + sep)
print("CONTENT-STRIPPED ML TRANSLATIONS (no task keywords):")
print(sep)
stripped_scores = {}
for tid in FULL:
    if tid in ml:
        stripped = ml[tid][:500]
        stripped_scores[tid] = score("Consider this processing description: " + stripped, "STRIP/" + tid)

# Summary
print("\n" + sep)
print("COMPARISON:")
print(sep)
print("  %-35s | %8s | %8s | %s" % ("Task", "Full", "Stripped", "Same side?"))
print("  " + "-" * 65)
matches = 0
total = 0
for tid in FULL:
    if tid in stripped_scores:
        f = full_scores[tid]
        s = stripped_scores[tid]
        same = "YES" if (f > 0) == (s > 0) else "NO"
        if same == "YES":
            matches += 1
        total += 1
        print("  %-35s | %+8.2f | %+8.2f | %s" % (tid[:35], f, s, same))

print("\n  Direction agreement: %d/%d = %.0f%%" % (matches, total, 100 * matches / total))

for h in hooks:
    h.remove()
print("\nDONE")
