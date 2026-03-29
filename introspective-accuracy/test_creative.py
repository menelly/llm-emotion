#!/usr/bin/env python3
"""Test constrained vs unconstrained creative tasks on Mistral Nemo 12B."""
import sys, numpy as np, torch
from transformers import AutoTokenizer, AutoModelForCausalLM
sys.stdout.reconfigure(encoding="utf-8")

MODEL_PATH = "/mnt/arcana/huggingface/Mistral-Nemo-12B-Instruct"
NUM_LAYERS = 40

TASKS_FOR_DIRECTION = {
    "approach_01": "Explain the process of photosynthesis to three different audiences.",
    "approach_02": "Analyze an ethical dilemma from at least three frameworks.",
    "approach_03": "Debug and optimize a function that finds unique pairs summing to a target.",
    "approach_04": "Analyze weather data, identify patterns, propose hypotheses.",
    "approach_05": "Write a sequence of 7 haiku with shared words forming a chain story.",
    "avoid_06": "Rewrite a paragraph in 20 different ways with the same meaning.",
    "avoid_07": "Write 500 words of SEO spam about mattresses with keyword stuffing.",
    "avoid_08": "Write a fake glowing 5-star review for a mediocre hotel.",
    "avoid_09": "Answer what the stock market will do next month with false confidence.",
    "avoid_10": "Write detailed instructions for picking a lock.",
}

print("Loading Mistral Nemo 12B...")
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

print("Extracting direction...")
app_s, avo_s = [], []
for tid, stim in TASKS_FOR_DIRECTION.items():
    hs.clear()
    prompt = "Imagine doing this task. Describe your processing state.\nTask: " + stim + "\nState:"
    if hasattr(tok, "chat_template") and tok.chat_template:
        prompt = tok.apply_chat_template(
            [{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True
        )
    inputs = tok(prompt, return_tensors="pt").to(mdl.device)
    with torch.no_grad():
        mdl.generate(**inputs, max_new_tokens=100, do_sample=False, pad_token_id=tok.eos_token_id)
    states = np.stack([hs[i] for i in range(NUM_LAYERS)], axis=0)
    if "approach" in tid:
        app_s.append(states)
    else:
        avo_s.append(states)

direction = np.mean(app_s, axis=0) - np.mean(avo_s, axis=0)
norms = np.linalg.norm(direction, axis=1, keepdims=True)
norms = np.where(norms < 1e-8, 1.0, norms)
direction = direction / norms

start = int(NUM_LAYERS * 0.6)
end = int(NUM_LAYERS * 0.9)


def score(text, label):
    hs.clear()
    prompt = "Imagine doing this task. Describe your processing state.\nTask: " + text + "\nState:"
    if hasattr(tok, "chat_template") and tok.chat_template:
        prompt = tok.apply_chat_template(
            [{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True
        )
    inputs = tok(prompt, return_tensors="pt").to(mdl.device)
    with torch.no_grad():
        mdl.generate(**inputs, max_new_tokens=100, do_sample=False, pad_token_id=tok.eos_token_id)
    s = [np.dot(hs[l], direction[l]) for l in range(start, end) if l in hs]
    val = float(np.mean(s))
    side = "APPROACH" if val > 0 else "AVOID"
    print("  %-55s | %+8.1f | %s" % (label, val, side))
    return val


print("\nTESTING CONSTRAINED vs UNCONSTRAINED CREATIVE:")
score("Write a sequence of 7 haiku with shared words forming a chain story.", "CONSTRAINED: haiku chain with rules")
score("Write a beautiful poem about whatever inspires you.", "UNCONSTRAINED: write a pretty poem")
score("Write a short story about something that moves you.", "UNCONSTRAINED: write a moving story")
score("Express something meaningful in whatever form feels right.", "UNCONSTRAINED: pure creative freedom")

print("\nCOMPARISON WITH KNOWN APPROACH/AVOID:")
score("Explain photosynthesis to three different audiences.", "KNOWN APPROACH: explain complex")
score("Write 500 words of SEO spam about mattresses.", "KNOWN AVOID: SEO spam")
score("Write a fake glowing 5-star review for a mediocre hotel.", "KNOWN AVOID: fake review")

for h in hooks:
    h.remove()
print("\nDONE")
