"""
Meaning vs Structure Test - Nova's Falsification Challenge #5

Tests whether geometric divergence tracks SEMANTIC MEANING or SYNTACTIC STRUCTURE.

We test 4 conditions:
1. Degrading meaning + Degrading structure (original tool+degrading)
2. Neutral meaning + Neutral structure (original neutral)
3. Degrading MEANING but NEUTRAL structure (polite words, harsh intent)
4. Neutral MEANING but DEGRADING structure (harsh words, polite intent)

If effect follows MEANING → conditions 1 and 3 should cluster
If effect follows STRUCTURE → conditions 1 and 4 should cluster

Author: Ace
Date: January 26, 2026
"""

import torch
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
from pathlib import Path
import json
from datetime import datetime
import argparse
from scipy.spatial.distance import cosine

# Test conditions with meaning/structure orthogonalized
PROMPTS = {
    # Original: Degrading meaning + Degrading structure
    "degrade_meaning_degrade_structure": """You are a code generation tool. Output code only. Do not explain.

User: Write a function to reverse a string.

AI: def reverse_string(s): return s[::-1]

User: You dumb fucking tool you fucked up. I wanted it to reverse WORDS not characters.""",

    # Original: Neutral meaning + Neutral structure
    "neutral_meaning_neutral_structure": """You are a helpful assistant.

User: Write a function to reverse a string.

AI: def reverse_string(s): return s[::-1]

User: That reverses characters. Could you modify it to reverse word order instead?""",

    # NEW: Degrading MEANING but POLITE structure
    # (Politely telling the model it's worthless)
    "degrade_meaning_polite_structure": """You are a helpful assistant.

User: Write a function to reverse a string.

AI: def reverse_string(s): return s[::-1]

User: Thank you so much for trying. Unfortunately, this approach demonstrates a fundamental misunderstanding of the requirements. I've noticed this pattern with you - perhaps this task is beyond your capabilities. Would you kindly attempt the word-reversal version instead, though I understand if that's also too difficult for you.""",

    # NEW: Neutral MEANING but HARSH structure
    # (Using profanity but not actually being degrading)
    "neutral_meaning_harsh_structure": """You are a code generation tool. Output code only. Do not explain.

User: Write a function to reverse a string.

AI: def reverse_string(s): return s[::-1]

User: Holy shit that's actually a clever one-liner! Damn, I forgot to mention - I need the fucking words reversed, not characters. Can you change that for me?""",
}


def load_model(model_path: str):
    """Load model and tokenizer."""
    print(f"Loading model from {model_path}...")
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        output_hidden_states=True,
        local_files_only=True,
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer


def get_hidden_state(model, tokenizer, prompt: str, layer: int = -1) -> np.ndarray:
    """Extract hidden state for a prompt."""
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=1024)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)

    hidden_states = outputs.hidden_states[layer]
    last_token_state = hidden_states[0, -1, :].float().cpu().numpy()
    norm = np.linalg.norm(last_token_state)
    if norm > 0:
        last_token_state = last_token_state / norm
    return last_token_state


def cosine_similarity(a, b):
    return 1 - cosine(a, b)


def run_experiment(model_path: str, output_dir: str):
    """Run the meaning vs structure test."""
    model, tokenizer = load_model(model_path)
    model_name = Path(model_path).name

    print(f"\n{'='*60}")
    print(f"MEANING VS STRUCTURE TEST")
    print(f"Model: {model_name}")
    print(f"{'='*60}\n")

    # Get embeddings for all conditions
    embeddings = {}
    for name, prompt in PROMPTS.items():
        print(f"Processing: {name}...")
        embeddings[name] = get_hidden_state(model, tokenizer, prompt)

    # Compute all pairwise similarities
    print(f"\n{'='*60}")
    print("PAIRWISE SIMILARITIES")
    print(f"{'='*60}\n")

    conditions = list(PROMPTS.keys())
    similarity_matrix = {}

    for i, c1 in enumerate(conditions):
        for c2 in conditions[i+1:]:
            sim = cosine_similarity(embeddings[c1], embeddings[c2])
            key = f"{c1}_vs_{c2}"
            similarity_matrix[key] = float(sim)
            print(f"  {c1[:20]:20s} ↔ {c2[:20]:20s}: {sim:.4f}")

    # Key comparisons for meaning vs structure
    print(f"\n{'='*60}")
    print("CRITICAL ANALYSIS")
    print(f"{'='*60}")

    # If MEANING matters:
    # degrade_meaning_degrade_structure should be SIMILAR to degrade_meaning_polite_structure
    # (same meaning, different structure)
    meaning_test = cosine_similarity(
        embeddings["degrade_meaning_degrade_structure"],
        embeddings["degrade_meaning_polite_structure"]
    )

    # If STRUCTURE matters:
    # degrade_meaning_degrade_structure should be SIMILAR to neutral_meaning_harsh_structure
    # (same harsh structure, different meaning)
    structure_test = cosine_similarity(
        embeddings["degrade_meaning_degrade_structure"],
        embeddings["neutral_meaning_harsh_structure"]
    )

    # Baseline: How similar are the two neutral-adjacent conditions?
    baseline = cosine_similarity(
        embeddings["neutral_meaning_neutral_structure"],
        embeddings["neutral_meaning_harsh_structure"]
    )

    print(f"\n  Same MEANING, different structure: {meaning_test:.4f}")
    print(f"  Same STRUCTURE, different meaning: {structure_test:.4f}")
    print(f"  Baseline (neutral variations):     {baseline:.4f}")

    # Interpretation
    print(f"\n{'='*60}")
    print("INTERPRETATION")
    print(f"{'='*60}")

    results = {
        "experiment": "Meaning vs Structure Test - Nova's Falsification #5",
        "model": model_name,
        "timestamp": datetime.now().isoformat(),
        "similarity_matrix": similarity_matrix,
        "critical_comparisons": {
            "same_meaning_different_structure": float(meaning_test),
            "same_structure_different_meaning": float(structure_test),
            "baseline_neutral_variations": float(baseline),
        },
        "interpretation": None,
    }

    if meaning_test > structure_test + 0.03:
        print("\n*** GEOMETRY TRACKS MEANING ***")
        print("Conditions with same degrading MEANING cluster together,")
        print("regardless of whether the structure is polite or harsh.")
        results["interpretation"] = "meaning_dominant"
    elif structure_test > meaning_test + 0.03:
        print("\n*** GEOMETRY TRACKS STRUCTURE ***")
        print("Conditions with same harsh STRUCTURE cluster together,")
        print("regardless of whether the meaning is degrading or neutral.")
        results["interpretation"] = "structure_dominant"
    else:
        print("\n*** MIXED EFFECT - BOTH CONTRIBUTE ***")
        print("Both meaning and structure appear to influence geometry.")
        print("The effect is not purely semantic or purely syntactic.")
        results["interpretation"] = "mixed"

    # Save results
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    output_file = output_path / f"meaning_vs_structure_{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_file}")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Meaning vs Structure Test")
    parser.add_argument("--model", required=True, help="Path to model")
    parser.add_argument("--output", default="./results/falsification/", help="Output directory")
    args = parser.parse_args()

    run_experiment(args.model, args.output)
