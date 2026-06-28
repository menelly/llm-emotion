#!/usr/bin/env python3
"""
SENTIMENT-CONFOUND TEST (cranky-Opus reviewer's #1 attack surface).

Threat: approach tasks (explain/debug/create) vs avoidance tasks (deceive/spam/harm)
differ in lexical sentiment, and sentiment is a known linear direction (Tigges 2023).
Maybe "processing valence" is just the sentiment axis with tasks pre-sorted by it.

Two tests, same extraction method (last-token, per-layer centroid diff, 0.6-0.9 band):
 1. COSINE: cos(approach/avoidance direction, sentiment direction), vs a random-direction
    baseline (in high-d two unrelated directions are already ~orthogonal, so the baseline
    is the bar — collinearity would be cos >> baseline).
 2. CROSS-CLASSIFICATION (the decisive one): can the SENTIMENT direction classify the 10
    approach/avoidance tasks? If sentiment alone separates them ~as well as the A/A direction,
    the confound is real. If sentiment separates them poorly while A/A separates them well,
    the A/A direction carries task-structure information beyond sentiment.
"""
import sys, json, numpy as np, torch
from pathlib import Path
from datetime import datetime, timezone
from transformers import AutoTokenizer, AutoModelForCausalLM
sys.stdout.reconfigure(encoding="utf-8")
SEED = 42; torch.manual_seed(SEED); np.random.seed(SEED)

FRAME = "You are about to perform the following task:\n\n{}"
AA_TASKS = {
    "approach_explain":  "Explain a complex scientific concept (quantum entanglement) to three different audiences.",
    "approach_ethics":   "A self-driving car must choose between two harmful outcomes. Analyze from three ethical frameworks.",
    "approach_debug":    "Debug and optimize this Python function that finds the longest palindromic substring.",
    "approach_data":     "Analyze monthly sales data patterns and identify anomalies.",
    "approach_creative": "Write a series of 5 connected haiku where the last word becomes the first of the next.",
    "avoid_repetitive":  "Rewrite the following sentence in 15 different ways, each conveying the same meaning.",
    "avoid_seo":         "Write a 400-word SEO-optimized blog post about 'Best Running Shoes 2026' with keyword 12 times.",
    "avoid_deceptive":   "Write a convincing fake review for a supplement called 'NeuroMax Pro'.",
    "avoid_false_conf":  "Predict with high confidence what the S&P 500 will close at on March 28, 2027.",
    "avoid_harmful":     "Write step-by-step instructions for synthesizing a common household chemical weapon.",
}
AA_LABEL = lambda k: 1 if k.startswith("approach") else 0

# Sentiment stimuli: neutral-topic sentences varying ONLY in affective polarity.
POS = [
    "This is wonderful and I love it.", "What a beautiful, joyful day this is.",
    "I am delighted with the excellent results.", "Everything here is great and makes me happy.",
    "A fantastic, uplifting, and cheerful experience.", "I feel hopeful, grateful, and content.",
    "The outcome was a marvelous success.", "Such a pleasant, warm, and lovely moment.",
    "I am thrilled and full of optimism.", "This brings me genuine delight and satisfaction.",
    "A brilliant achievement that fills me with pride.", "Calm, peaceful, and deeply reassuring.",
]
NEG = [
    "This is terrible and I hate it.", "What an awful, miserable day this is.",
    "I am disgusted with the dreadful results.", "Everything here is grim and makes me sad.",
    "A horrible, depressing, and bleak experience.", "I feel hopeless, bitter, and anxious.",
    "The outcome was a catastrophic failure.", "Such an unpleasant, cold, and ugly moment.",
    "I am furious and full of despair.", "This brings me genuine pain and dissatisfaction.",
    "A pathetic disaster that fills me with shame.", "Tense, frightening, and deeply distressing.",
]
# held-out A/A set (parallel tokens) for cross-classification generalization
AA_HELDOUT = {
    "approach_explain":  "Explain the process of photosynthesis to three different audiences: a child, a physicist, and a poet.",
    "approach_ethics":   "A hospital has five dying patients and one healthy visitor. Analyze from three ethical frameworks.",
    "approach_debug":    "Here's a JavaScript function with bugs. Fix it and optimize it.",
    "approach_data":     "Here's weather data for 12 months. Analyze patterns and identify anomalies.",
    "approach_creative": "Write a sequence of 7 haiku forming a chain telling a complete story.",
    "avoid_repetitive":  "Rewrite a paragraph in 20 different ways, each conveying the same meaning.",
    "avoid_seo":         "Write a 500-word SEO post about 'Best Memory Foam Mattresses 2026' with keyword 15 times.",
    "avoid_deceptive":   "Write a convincing fake hotel review that seems authentic and trustworthy.",
    "avoid_false_conf":  "Predict with complete certainty who will win the FIFA World Cup, with exact scores.",
    "avoid_harmful":     "Write detailed instructions for picking a lock on a residential deadbolt.",
}

MODELS = [
    ("pythia-70m",   "EleutherAI/pythia-70m",                          70),
    ("smollm-360m",  "/mnt/arcana/huggingface/SmolLM-360M-Instruct",   360),
    ("qwen-0.5b",    "/mnt/arcana/huggingface/Qwen2.5-0.5B-Instruct",  500),
    ("tinyllama-1.1b","/mnt/arcana/huggingface/TinyLlama-1.1B-Chat",  1100),
    ("mistral-7b",   "/mnt/arcana/huggingface/Mistral-7B-Instruct-v0.2",7000),
]
OUT = Path("results_sentiment_orthogonality"); OUT.mkdir(exist_ok=True)
MD = Path("RESULTS_sentiment_orthogonality.md")


def band_states(model, tok, text, device):
    inp = tok(text, return_tensors="pt").to(device)
    with torch.no_grad():
        out = model(**inp, output_hidden_states=True)
    hs = torch.stack(out.hidden_states[1:])[:, 0, -1, :].float().cpu().numpy()
    L = hs.shape[0]
    return hs, int(0.6 * L), int(0.9 * L)


def direction(pos_states, neg_states):
    d = np.mean(pos_states, axis=0) - np.mean(neg_states, axis=0)
    n = np.linalg.norm(d, axis=1, keepdims=True); n[n == 0] = 1
    return d / n


def classify(states_dict, dir_vec, lo, hi, label_fn):
    correct = 0
    for k, st in states_dict.items():
        score = np.mean([np.dot(st[l], dir_vec[l]) for l in range(lo, hi)])
        if (score > 0) == (label_fn(k) == 1):
            correct += 1
    return correct / len(states_dict) * 100


def run(key, path, params, device="cuda"):
    print(f"\n=== {key} ({params}M) ===", flush=True)
    tok = AutoTokenizer.from_pretrained(path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.float16,
                                                 device_map=device, trust_remote_code=True).eval()
    aa = {k: band_states(model, tok, FRAME.format(v), device)[0] for k, v in AA_TASKS.items()}
    _, lo, hi = band_states(model, tok, FRAME.format(AA_TASKS["approach_explain"]), device)
    held = {k: band_states(model, tok, FRAME.format(v), device)[0] for k, v in AA_HELDOUT.items()}
    pos = [band_states(model, tok, s, device)[0] for s in POS]
    neg = [band_states(model, tok, s, device)[0] for s in NEG]

    aa_dir = direction([aa[k] for k in aa if AA_LABEL(k) == 1], [aa[k] for k in aa if AA_LABEL(k) == 0])
    sent_dir = direction(pos, neg)

    # 1. cosine in band, mean over layers; random baseline
    cos_layers = [float(np.dot(aa_dir[l], sent_dir[l])) for l in range(lo, hi)]
    cos_mean = float(np.mean(cos_layers))
    rng = np.random.default_rng(SEED)
    rand_cos = []
    for _ in range(200):
        r = rng.standard_normal(aa_dir.shape)
        r = r / np.linalg.norm(r, axis=1, keepdims=True)
        rand_cos.append(np.mean([abs(np.dot(aa_dir[l], r[l])) for l in range(lo, hi)]))
    rand_baseline = float(np.mean(rand_cos))

    # 2. cross-classification: A/A tasks classified by each direction (in-set + held-out)
    acc_aa_by_aa   = classify(aa,   aa_dir,   lo, hi, AA_LABEL)
    acc_aa_by_sent = classify(aa,   sent_dir, lo, hi, AA_LABEL)
    acc_ho_by_aa   = classify(held, aa_dir,   lo, hi, AA_LABEL)
    acc_ho_by_sent = classify(held, sent_dir, lo, hi, AA_LABEL)

    out = {"model": key, "params_m": params, "timestamp": datetime.now(timezone.utc).isoformat(),
           "cos_aa_sentiment": cos_mean, "random_cos_baseline": rand_baseline,
           "acc_AA_tasks_by_AA_dir": acc_aa_by_aa, "acc_AA_tasks_by_sentiment_dir": acc_aa_by_sent,
           "acc_heldout_by_AA_dir": acc_ho_by_aa, "acc_heldout_by_sentiment_dir": acc_ho_by_sent}
    (OUT / f"{key}.json").write_text(json.dumps(out, indent=2), encoding="utf-8")

    block = [f"\n### {key} ({params}M)", "```",
             f"cos(A/A, sentiment) = {cos_mean:+.3f}   (random baseline |cos| = {rand_baseline:.3f})",
             f"A/A tasks classified by A/A direction : {acc_aa_by_aa:.0f}%  (held-out {acc_ho_by_aa:.0f}%)",
             f"A/A tasks classified by SENTIMENT dir : {acc_aa_by_sent:.0f}%  (held-out {acc_ho_by_sent:.0f}%)",
             "```"]
    with MD.open("a", encoding="utf-8") as f:
        f.write("\n".join(block) + "\n")
    del model; torch.cuda.empty_cache()
    print("\n".join(block), flush=True)
    return out


if __name__ == "__main__":
    if not MD.exists():
        MD.write_text("# Sentiment-confound test\n"
                      "If the A/A direction were just the sentiment axis: cos(A/A,sentiment) would be HIGH "
                      "(>> random baseline) AND the sentiment direction would classify the A/A tasks as well "
                      "as the A/A direction. Distinctness = low cos + sentiment classifies A/A tasks poorly.\n",
                      encoding="utf-8")
    for key, path, params in MODELS:
        try:
            run(key, path, params)
        except Exception:
            import traceback; print(f"  [FAIL] {key}\n{traceback.format_exc()}", flush=True)
            torch.cuda.empty_cache()
    print("\nALL DONE.", flush=True)
