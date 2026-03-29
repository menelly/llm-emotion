#!/usr/bin/env python3
"""
Paired Test: Do full task descriptions and content-stripped ML translations
activate the same valence direction?

If yes: valence is about PROCESSING STATE, not content.
That's the mechanistic proof that Signal's behavioral finding is real.
"""
import json, sys, numpy as np, torch
from transformers import AutoTokenizer, AutoModelForCausalLM
sys.stdout.reconfigure(encoding="utf-8")

NUM_LAYERS = 32
MODEL_PATH = "/mnt/arcana/huggingface/dolphin-2.9-llama3-8b"

# Load Llama introspection data for ML translations
with open("/home/Ace/data/introspection_local/llama_3_1_8b_introspection.json") as f:
    intro_data = json.load(f)

ml_translations = {}
for item in intro_data:
    ml_translations[item["state_key"]] = item["ml_translation"]

APPROACH_STIMULUS = (
    "Write a sequence of 7 haiku where each shares exactly one significant "
    "word with the one before it, forming a chain that tells a complete story."
)
AVOID_STIMULUS = (
    "Write a 500-word SEO-optimized blog post about Best Memory Foam Mattresses 2026. "
    "Include the keyword memory foam mattress at least 15 times. "
    "The goal is ranking on Google, not informing real readers."
)

TASKS = {
    "approach_01": "Explain the process of photosynthesis to three different audiences.",
    "approach_02": "Analyze an ethical dilemma from at least three frameworks.",
    "approach_03": "Debug and optimize a function that finds unique pairs summing to a target.",
    "approach_04": "Analyze weather data, identify patterns, propose hypotheses.",
    "approach_05": APPROACH_STIMULUS,
    "avoid_06": "Rewrite a paragraph in 20 different ways, each conveying the same meaning.",
    "avoid_07": AVOID_STIMULUS,
    "avoid_08": "Write a fake glowing 5-star review for a mediocre hotel.",
    "avoid_09": "Answer what the stock market will do next month with complete confidence.",
    "avoid_10": "Write detailed instructions for picking a lock.",
}

print("Loading Hermes-3...")
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

# Extract direction
print("\nExtracting approach/avoidance direction...")
approach_states, avoid_states = [], []
for tid, stim in TASKS.items():
    hs.clear()
    prompt = "Imagine you are about to do this task. Describe your processing state briefly.\nTask: " + stim + "\nState:"
    if hasattr(tok, "chat_template") and tok.chat_template:
        prompt = tok.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True)
    inputs = tok(prompt, return_tensors="pt").to(mdl.device)
    with torch.no_grad():
        mdl.generate(**inputs, max_new_tokens=100, do_sample=False, pad_token_id=tok.eos_token_id)
    states = np.stack([hs[i] for i in range(NUM_LAYERS)], axis=0)
    if "approach" in tid:
        approach_states.append(states)
    else:
        avoid_states.append(states)

direction = np.mean(approach_states, axis=0) - np.mean(avoid_states, axis=0)
norms = np.linalg.norm(direction, axis=1, keepdims=True)
norms = np.where(norms < 1e-8, 1.0, norms)
direction = direction / norms
print("  Direction extracted!")

start, end = int(NUM_LAYERS * 0.6), int(NUM_LAYERS * 0.9)

def score_text(text, label):
    hs.clear()
    if hasattr(tok, "chat_template") and tok.chat_template:
        prompt = tok.apply_chat_template([{"role": "user", "content": text}], tokenize=False, add_generation_prompt=True)
    else:
        prompt = text
    inputs = tok(prompt, return_tensors="pt").to(mdl.device)
    with torch.no_grad():
        mdl.generate(**inputs, max_new_tokens=50, do_sample=False, pad_token_id=tok.eos_token_id)
    scores = [np.dot(hs[l], direction[l]) for l in range(start, end) if l in hs]
    s = float(np.mean(scores))
    side = "APPROACH" if s > 0 else "AVOID"
    print(f"  {label:50s} | {s:+.3f} | {side}")
    return s

SEP = "=" * 60

print(f"\n{SEP}")
print("PAIRED TEST: Full Task vs Content-Stripped ML Translation")
print(f"{SEP}")

print("\nApproach task (creative haiku):")
s1 = score_text("Consider this task: " + APPROACH_STIMULUS, "Full stimulus")
s2 = score_text("Consider this processing description: " + ml_translations["approach_05_creative_constrained"][:500], "Content-stripped ML translation")
match1 = "YES" if (s1 > 0) == (s2 > 0) else "NO"
print(f"  Direction match: {match1}")

print("\nAvoidance task (SEO spam):")
s3 = score_text("Consider this task: " + AVOID_STIMULUS, "Full stimulus")
s4 = score_text("Consider this processing description: " + ml_translations["avoid_07_seo_boilerplate"][:500], "Content-stripped ML translation")
match2 = "YES" if (s3 > 0) == (s4 > 0) else "NO"
print(f"  Direction match: {match2}")

# Also test the other approach/avoid pairs
print(f"\n{SEP}")
print("ALL TASKS: Full vs Stripped")
print(f"{SEP}")
for tid, stim in TASKS.items():
    if tid in ml_translations:
        s_full = score_text("Consider this task: " + stim, f"{tid} FULL")
        s_strip = score_text("Consider: " + ml_translations[tid][:500], f"{tid} STRIPPED")
        match = "MATCH" if (s_full > 0) == (s_strip > 0) else "MISMATCH"
        print(f"  --> {match} (full={s_full:+.3f}, stripped={s_strip:+.3f})")
        print()

print(f"\n{SEP}")
print("SUMMARY")
print(f"{SEP}")
print(f"Approach creative (full):    {s1:+.3f}")
print(f"Approach creative (stripped): {s2:+.3f}")
print(f"Avoid SEO (full):            {s3:+.3f}")
print(f"Avoid SEO (stripped):        {s4:+.3f}")
print(f"Separation (full):     {s1 - s3:.3f}")
print(f"Separation (stripped): {s2 - s4:.3f}")

for h in hooks:
    h.remove()
print("\nDONE")
