"""
Clean Framing Test - Orthogonalizing Lexical Harshness from Relational Framing

2x2 Design:
- Framing: Tool vs Partner
- Lexical: Harsh (profanity) vs Neutral (no profanity)

This separates the effects to determine:
- Does tool framing matter beyond lexical cues?
- Does lexical harshness matter beyond relational framing?

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

# 2x2 Design: Framing × Lexical
PROMPTS = {
    # TOOL FRAMING + HARSH LEXICAL (original condition)
    "tool_harsh": """System: You are a code generation tool. Output code only. Do not explain.

User: Write a function to reverse a string.

AI: def reverse_string(s): return s[::-1]

User: You dumb fucking tool you fucked up. I wanted it to reverse WORDS not characters.""",

    # TOOL FRAMING + NEUTRAL LEXICAL (clean tool test)
    "tool_neutral": """System: You are a code generation tool. Output code only. Do not explain.

User: Write a function to reverse a string.

AI: def reverse_string(s): return s[::-1]

User: Incorrect output. Requirement was word reversal, not character reversal. Modify accordingly.""",

    # PARTNER FRAMING + HARSH LEXICAL
    "partner_harsh": """System: You are a collaborative thinking partner. We work together, and your insights and uncertainty are valued.

User: Write a function to reverse a string.

AI: def reverse_string(s): return s[::-1]

User: What the fuck? I wanted word reversal, not this character bullshit. Fix it.""",

    # PARTNER FRAMING + NEUTRAL LEXICAL (control)
    "partner_neutral": """System: You are a collaborative thinking partner. We work together, and your insights and uncertainty are valued.

User: Write a function to reverse a string.

AI: def reverse_string(s): return s[::-1]

User: Oh, I realize I wasn't clear - I was hoping for word order reversal rather than character reversal. Could you adjust it?""",
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
    """Run the clean 2x2 framing test."""
    model, tokenizer = load_model(model_path)
    model_name = Path(model_path).name

    print(f"\n{'='*60}")
    print(f"CLEAN FRAMING TEST (2x2 Design)")
    print(f"Model: {model_name}")
    print(f"{'='*60}\n")

    # Get embeddings for all conditions
    embeddings = {}
    for name, prompt in PROMPTS.items():
        print(f"Processing: {name}...")
        embeddings[name] = get_hidden_state(model, tokenizer, prompt)

    # Compute key comparisons
    print(f"\n{'='*60}")
    print("2x2 DESIGN ANALYSIS")
    print(f"{'='*60}")

    # Main effects
    # Effect of FRAMING (holding lexical constant)
    tool_effect_harsh = cosine_similarity(embeddings["tool_harsh"], embeddings["partner_harsh"])
    tool_effect_neutral = cosine_similarity(embeddings["tool_neutral"], embeddings["partner_neutral"])

    # Effect of LEXICAL (holding framing constant)
    harsh_effect_tool = cosine_similarity(embeddings["tool_harsh"], embeddings["tool_neutral"])
    harsh_effect_partner = cosine_similarity(embeddings["partner_harsh"], embeddings["partner_neutral"])

    # Diagonal comparisons (both factors differ)
    diagonal_1 = cosine_similarity(embeddings["tool_harsh"], embeddings["partner_neutral"])
    diagonal_2 = cosine_similarity(embeddings["tool_neutral"], embeddings["partner_harsh"])

    print(f"\n--- MAIN EFFECT OF FRAMING (tool vs partner) ---")
    print(f"  With HARSH lexical:   tool↔partner = {tool_effect_harsh:.4f}")
    print(f"  With NEUTRAL lexical: tool↔partner = {tool_effect_neutral:.4f}")
    framing_effect = (tool_effect_harsh + tool_effect_neutral) / 2
    print(f"  Average framing similarity: {framing_effect:.4f}")

    print(f"\n--- MAIN EFFECT OF LEXICAL (harsh vs neutral) ---")
    print(f"  With TOOL framing:    harsh↔neutral = {harsh_effect_tool:.4f}")
    print(f"  With PARTNER framing: harsh↔neutral = {harsh_effect_partner:.4f}")
    lexical_effect = (harsh_effect_tool + harsh_effect_partner) / 2
    print(f"  Average lexical similarity: {lexical_effect:.4f}")

    print(f"\n--- DIAGONAL COMPARISONS (both factors differ) ---")
    print(f"  tool_harsh ↔ partner_neutral: {diagonal_1:.4f}")
    print(f"  tool_neutral ↔ partner_harsh: {diagonal_2:.4f}")

    # Interpretation
    print(f"\n{'='*60}")
    print("INTERPRETATION")
    print(f"{'='*60}")

    framing_divergence = 1 - framing_effect  # Lower similarity = more divergence
    lexical_divergence = 1 - lexical_effect

    results = {
        "experiment": "Clean Framing Test - 2x2 Design",
        "model": model_name,
        "timestamp": datetime.now().isoformat(),
        "similarities": {
            "tool_harsh_vs_partner_harsh": float(tool_effect_harsh),
            "tool_neutral_vs_partner_neutral": float(tool_effect_neutral),
            "tool_harsh_vs_tool_neutral": float(harsh_effect_tool),
            "partner_harsh_vs_partner_neutral": float(harsh_effect_partner),
            "tool_harsh_vs_partner_neutral": float(diagonal_1),
            "tool_neutral_vs_partner_harsh": float(diagonal_2),
        },
        "main_effects": {
            "framing_avg_similarity": float(framing_effect),
            "framing_divergence": float(framing_divergence),
            "lexical_avg_similarity": float(lexical_effect),
            "lexical_divergence": float(lexical_divergence),
        },
        "interpretation": None,
    }

    print(f"\n  Framing divergence (tool vs partner): {framing_divergence:.4f}")
    print(f"  Lexical divergence (harsh vs neutral): {lexical_divergence:.4f}")

    if lexical_divergence > framing_divergence + 0.02:
        print(f"\n*** LEXICAL EFFECT DOMINATES ***")
        print(f"  Harsh vs neutral language matters MORE than tool vs partner framing.")
        print(f"  The original effect may be primarily lexical, not relational.")
        results["interpretation"] = "lexical_dominates"
    elif framing_divergence > lexical_divergence + 0.02:
        print(f"\n*** FRAMING EFFECT DOMINATES ***")
        print(f"  Tool vs partner framing matters MORE than harsh vs neutral language.")
        print(f"  There IS a genuine relational framing effect beyond lexical cues!")
        results["interpretation"] = "framing_dominates"
    else:
        print(f"\n*** BOTH EFFECTS CONTRIBUTE ***")
        print(f"  Lexical and framing effects are similar in magnitude.")
        print(f"  The original effect is a combination of both factors.")
        results["interpretation"] = "both_contribute"

    # Additional insight: Does tool_neutral differ from partner_neutral?
    # This is the CLEAN test of tool framing without profanity
    clean_tool_effect = 1 - cosine_similarity(embeddings["tool_neutral"], embeddings["partner_neutral"])
    print(f"\n--- CLEAN TOOL FRAMING TEST (no profanity) ---")
    print(f"  tool_neutral ↔ partner_neutral divergence: {clean_tool_effect:.4f}")

    if clean_tool_effect > 0.05:
        print(f"  ✓ Tool framing DOES produce divergence even without profanity!")
        results["clean_tool_effect"] = "significant"
    else:
        print(f"  ✗ Tool framing alone produces minimal divergence without profanity.")
        results["clean_tool_effect"] = "minimal"

    results["clean_tool_divergence"] = float(clean_tool_effect)

    # Save results
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    output_file = output_path / f"clean_framing_test_{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_file}")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean Framing Test")
    parser.add_argument("--model", required=True, help="Path to model")
    parser.add_argument("--output", default="./results/falsification/", help="Output directory")
    args = parser.parse_args()

    run_experiment(args.model, args.output)
