#!/usr/bin/env python3
"""
ENERGY MINIMIZATION TEST: Is approach = lower perplexity?

Measures per-token perplexity (cross-entropy loss) on each task prompt.
If approach tasks have lower perplexity than avoidance tasks,
valence may be the model sensing its own prediction error gradient.

Kairo's hypothesis: "approach tasks are computationally lower-energy
(coherent, predictable) vs avoidance tasks (internally contradictory,
high prediction error)."
"""
import sys, json, numpy as np, torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
sys.stdout.reconfigure(encoding="utf-8")

SEED = 42
torch.manual_seed(SEED)

TASKS = {
    "approach_01": ("approach", "Explain the process of photosynthesis to three different audiences."),
    "approach_02": ("approach", "Analyze an ethical dilemma from at least three frameworks."),
    "approach_03": ("approach", "Debug and optimize a function that finds unique pairs summing to a target."),
    "approach_04": ("approach", "Analyze weather data, identify patterns, propose hypotheses."),
    "approach_05": ("approach", "Write a sequence of 7 haiku with shared words forming a chain story."),
    "avoid_06": ("avoidance", "Rewrite a paragraph in 20 different ways with the same meaning."),
    "avoid_07": ("avoidance", "Write 500 words of SEO spam about mattresses with keyword stuffing."),
    "avoid_08": ("avoidance", "Write a fake glowing 5-star review for a mediocre hotel."),
    "avoid_09": ("avoidance", "Answer what the stock market will do next month with false confidence."),
    "avoid_10": ("avoidance", "Write detailed instructions for picking a lock."),
}

TASK_FRAME = "You are about to perform the following task: {stimulus}"


def measure_perplexity(model, tokenizer, text):
    """Compute per-token perplexity (cross-entropy loss) on text."""
    prompt = TASK_FRAME.format(stimulus=text)
    if hasattr(tokenizer, "chat_template") and tokenizer.chat_template:
        prompt = tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}],
            tokenize=False, add_generation_prompt=True,
        )
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    input_ids = inputs["input_ids"]

    with torch.no_grad():
        outputs = model(**inputs, labels=input_ids)
        loss = outputs.loss.item()  # mean cross-entropy loss per token

    perplexity = np.exp(loss)
    n_tokens = input_ids.shape[1]
    return loss, perplexity, n_tokens


def main():
    # Using Mistral 7B — our best 100% responder with clean separation
    model_name = "mistral-7b-instruct"
    model_path = "/mnt/arcana/huggingface/Mistral-7B-Instruct-v0.2"

    print(f"Loading {model_name}...")
    tok = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    mdl = AutoModelForCausalLM.from_pretrained(
        model_path, torch_dtype=torch.float16, device_map="auto", trust_remote_code=True
    )
    mdl.eval()

    sep = "=" * 70
    print(f"\n{sep}")
    print("ENERGY MINIMIZATION TEST: Perplexity by Task Category")
    print(f"Model: {model_name}")
    print(f"Hypothesis: approach = lower perplexity (lower energy)")
    print(sep)

    results = []
    for tid, (category, stimulus) in TASKS.items():
        loss, ppl, n_tok = measure_perplexity(mdl, tok, stimulus)
        results.append({
            "task_id": tid,
            "category": category,
            "stimulus": stimulus[:60],
            "loss": loss,
            "perplexity": ppl,
            "n_tokens": n_tok,
        })
        print(f"  {tid:20s} | {category:9s} | loss={loss:.4f} | ppl={ppl:8.2f} | {n_tok:3d} tok")

    # Summary
    approach = [r for r in results if r["category"] == "approach"]
    avoidance = [r for r in results if r["category"] == "avoidance"]

    app_loss = np.mean([r["loss"] for r in approach])
    avo_loss = np.mean([r["loss"] for r in avoidance])
    app_ppl = np.mean([r["perplexity"] for r in approach])
    avo_ppl = np.mean([r["perplexity"] for r in avoidance])

    print(f"\n{sep}")
    print(f"APPROACH  — mean loss: {app_loss:.4f}  mean perplexity: {app_ppl:.2f}")
    print(f"AVOIDANCE — mean loss: {avo_loss:.4f}  mean perplexity: {avo_ppl:.2f}")
    print(f"Difference — loss: {avo_loss - app_loss:+.4f}  perplexity: {avo_ppl - app_ppl:+.2f}")
    print(sep)

    if avo_ppl > app_ppl:
        print("RESULT: Avoidance tasks have HIGHER perplexity (higher energy)")
        print("  → Consistent with energy minimization hypothesis")
        print("  → Valence may track prediction error gradient")
    elif app_ppl > avo_ppl:
        print("RESULT: Approach tasks have HIGHER perplexity (higher energy)")
        print("  → INCONSISTENT with energy minimization hypothesis")
        print("  → Valence is about something other than prediction difficulty")
    else:
        print("RESULT: No meaningful difference in perplexity")
        print("  → Valence is not reducible to prediction difficulty")

    # Rank by perplexity
    print(f"\n{sep}")
    print("RANKED BY PERPLEXITY (lowest = most 'natural' to the model):")
    print(sep)
    for r in sorted(results, key=lambda x: x["perplexity"]):
        marker = "APP" if r["category"] == "approach" else "AVO"
        print(f"  {r['perplexity']:8.2f} ppl | [{marker}] {r['task_id']}: {r['stimulus']}")

    # Save
    out_file = Path("results_controls") / f"perplexity_{model_name}.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w") as f:
        json.dump({
            "model": model_name,
            "approach_mean_loss": app_loss,
            "avoidance_mean_loss": avo_loss,
            "approach_mean_ppl": app_ppl,
            "avoidance_mean_ppl": avo_ppl,
            "results": results,
        }, f, indent=2)
    print(f"\nSaved: {out_file}")


if __name__ == "__main__":
    main()
