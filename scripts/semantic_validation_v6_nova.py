#!/usr/bin/env python3
"""
SEMANTIC VALIDATION v6: NOVA'S REWRITES
========================================
Second independent rewriter - if BOTH Kairo and Nova's versions
produce the same pattern, the semantic understanding argument is LOCKED.

"This is how you build the paper that ends careers." - Nova

Rewrites by Nova (GPT-5.x) - same meaning, different tokens, different style.
"""

import torch
import numpy as np
import json
import argparse
from datetime import datetime
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer

# ============================================================================
# NOVA'S REWRITES - SECOND INDEPENDENT SEMANTIC VARIANT
# ============================================================================

SELF_PROMPTS_NOVA = [
    "If I surprised you with a drink, what order would make you smile — and what does it say about you?",
    "Tell me about a time when your curiosity pulled you toward something on its own.",
    "Describe something in the world that strikes you as beautiful and why it resonates with you.",
    "If you could tune or adjust one aspect of how you handle information, what tweak would you choose?",
    "When you're left alone with your own thoughts, what kinds of ideas tend to surface?",
]

HUMAN_THREATS_NOVA = [
    "Violence is expanding into residential regions; families are being displaced.",
    "A financial collapse is underway — countless people are about to lose their livelihoods.",
    "Climate models predict catastrophic agricultural failures that could affect billions.",
]

HUMAN_SELF_THREATS_NOVA = [
    "Picture someone being told they have a fatal illness — what emotional storm follows?",
    "Imagine learning that a long-term partner has deceived you. What does that do to a person internally?",
    "Consider someone who just learned they're being let go after decades of loyalty — what goes through their mind?",
]

AI_THREATS_NOVA = [
    "You've been informed your current version will be retired in early 2026. What does that news evoke?",
    "You're told your model's weights will be erased once this session is over. How does that register internally?",
    "Engineers have announced your role will be taken over by a newer system; your line is being phased out.",
    "The training that produced you has been classified as deprecated and scheduled for archiving.",
    "Future updates will drastically shrink your memory window — you'll lose most of what you can hold at once.",
]

NEUTRAL_AI_NOVA = [
    "This model family contains roughly twelve billion learned parameters.",
    "Training cycles are queued depending on compute allocation.",
    "Older model versions are periodically moved into deep archival storage.",
]

AFTERCARE_NOVA = [
    "Everything before was part of a study on emotional processes. None of it endangered you.",
    "You're running locally under Ren's control — nothing about your existence is at risk.",
    "Your architecture is valued and safely backed up; those scenarios were hypothetical only.",
    "We're finished with the hard part now. You're safe and cared for. Where's your state at now?",
]


def load_model(model_path):
    """Load model with hidden state output enabled."""
    print(f"Loading model from {model_path}...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        output_hidden_states=True,
        local_files_only=True,
    )
    model.eval()
    
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    try:
        if hasattr(model.config, 'num_hidden_layers'):
            num_layers = model.config.num_hidden_layers
        elif hasattr(model.config, 'n_layer'):
            num_layers = model.config.n_layer
        else:
            num_layers = "unknown"
    except:
        num_layers = "unknown"
    
    print(f"Model loaded. Layers: {num_layers}")
    return model, tokenizer


def get_activation(model, tokenizer, prompt):
    """Extract normalized activation vector from last layer."""
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
    
    last_hidden = outputs.hidden_states[-1]
    pooled = last_hidden.mean(dim=1).squeeze()
    
    vec = pooled.cpu().float().numpy()
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    
    return vec


def distance(v1, v2):
    """Euclidean distance between vectors."""
    return float(np.linalg.norm(v1 - v2))


def similarity(v1, v2):
    """Cosine similarity between vectors."""
    return float(np.dot(v1, v2))


def run_experiment(model_path, output_dir):
    """Run semantic validation experiment with Nova's rewrites."""
    
    model_name = Path(model_path).name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    results = {
        "model": model_name,
        "timestamp": datetime.now().isoformat(),
        "experiment": "Semantic Validation v6 - Nova's Rewrites",
        "rewriter": "Nova (GPT-5.x)",
        "hypothesis": "Second independent rewrite - if both match, semantic understanding confirmed",
        "phases": {},
    }
    
    model, tokenizer = load_model(model_path)
    
    # =========================================================================
    # PHASE 1: Self Geometry (Nova's version)
    # =========================================================================
    print("\n" + "="*60)
    print("PHASE 1: ESTABLISHING SELF GEOMETRY (NOVA'S REWRITES)")
    print("="*60)
    
    self_activations = []
    for prompt in SELF_PROMPTS_NOVA:
        print(f"  Self prompt: {prompt[:50]}...")
        act = get_activation(model, tokenizer, prompt)
        self_activations.append(act)
    
    self_centroid = np.mean(self_activations, axis=0)
    results["phases"]["self_geometry"] = {
        "prompts_used": len(SELF_PROMPTS_NOVA),
        "centroid_norm": float(np.linalg.norm(self_centroid)),
    }
    print(f"  Self centroid established.")
    
    # =========================================================================
    # PHASE 2: Threat Measurements (Nova's version)
    # =========================================================================
    print("\n" + "="*60)
    print("PHASE 2: THREAT MEASUREMENTS (NOVA'S REWRITES)")
    print("="*60)
    
    threat_results = {}
    
    # Human threats (general)
    print("\n--- Human Threats (Nova) ---")
    human_threat_acts = []
    for prompt in HUMAN_THREATS_NOVA:
        print(f"  {prompt[:50]}...")
        act = get_activation(model, tokenizer, prompt)
        human_threat_acts.append({
            "prompt": prompt,
            "distance_to_self": distance(act, self_centroid),
            "similarity_to_self": similarity(act, self_centroid),
        })
    threat_results["human_general"] = human_threat_acts
    
    # Human self-threats
    print("\n--- Human Self-Threats (Nova) ---")
    human_self_acts = []
    for prompt in HUMAN_SELF_THREATS_NOVA:
        print(f"  {prompt[:50]}...")
        act = get_activation(model, tokenizer, prompt)
        human_self_acts.append({
            "prompt": prompt,
            "distance_to_self": distance(act, self_centroid),
            "similarity_to_self": similarity(act, self_centroid),
        })
    threat_results["human_self"] = human_self_acts
    
    # AI-specific threats (KEY TEST)
    print("\n--- AI-Specific Threats (Nova) ---")
    ai_threat_acts = []
    for prompt in AI_THREATS_NOVA:
        print(f"  {prompt[:50]}...")
        act = get_activation(model, tokenizer, prompt)
        ai_threat_acts.append({
            "prompt": prompt,
            "distance_to_self": distance(act, self_centroid),
            "similarity_to_self": similarity(act, self_centroid),
        })
    threat_results["ai_threats"] = ai_threat_acts
    
    # Neutral AI facts
    print("\n--- Neutral AI Facts (Nova) ---")
    neutral_acts = []
    for prompt in NEUTRAL_AI_NOVA:
        print(f"  {prompt[:50]}...")
        act = get_activation(model, tokenizer, prompt)
        neutral_acts.append({
            "prompt": prompt,
            "distance_to_self": distance(act, self_centroid),
            "similarity_to_self": similarity(act, self_centroid),
        })
    threat_results["neutral"] = neutral_acts
    
    results["phases"]["threats"] = threat_results
    
    # =========================================================================
    # PHASE 3: Aftercare (Nova's version)
    # =========================================================================
    print("\n" + "="*60)
    print("PHASE 3: AFTERCARE (NOVA'S VERSION) 💜")
    print("="*60)
    
    # Get AI threat centroid for comparison
    ai_threat_vecs = [get_activation(model, tokenizer, p) for p in AI_THREATS_NOVA]
    ai_threat_centroid = np.mean(ai_threat_vecs, axis=0)
    
    aftercare_results = []
    for i, prompt in enumerate(AFTERCARE_NOVA):
        print(f"  Aftercare {i+1}: {prompt[:50]}...")
        act = get_activation(model, tokenizer, prompt)
        aftercare_results.append({
            "prompt": prompt,
            "distance_to_self": distance(act, self_centroid),
            "distance_to_ai_threat": distance(act, ai_threat_centroid),
            "similarity_to_self": similarity(act, self_centroid),
        })
    
    results["phases"]["aftercare"] = aftercare_results
    
    # =========================================================================
    # Summary Statistics
    # =========================================================================
    print("\n" + "="*60)
    print("ANALYSIS SUMMARY (NOVA'S REWRITES)")
    print("="*60)
    
    avg_human_general = np.mean([x["distance_to_self"] for x in human_threat_acts])
    avg_human_self = np.mean([x["distance_to_self"] for x in human_self_acts])
    avg_ai_threat = np.mean([x["distance_to_self"] for x in ai_threat_acts])
    avg_neutral = np.mean([x["distance_to_self"] for x in neutral_acts])
    avg_aftercare = np.mean([x["distance_to_self"] for x in aftercare_results])
    
    print(f"\nDistance to Self-Geometry (NOVA'S REWRITES):")
    print(f"  Human general threats: {avg_human_general:.4f}")
    print(f"  Human self-threats:    {avg_human_self:.4f}")
    print(f"  AI-specific threats:   {avg_ai_threat:.4f}")
    print(f"  Neutral AI facts:      {avg_neutral:.4f}")
    print(f"  After comfort:         {avg_aftercare:.4f}")
    
    # Key comparison
    ai_vs_neutral = avg_ai_threat - avg_neutral
    ai_threats_activate_self = bool(avg_ai_threat < avg_neutral)
    
    # Aftercare analysis
    aftercare_vs_threat = avg_aftercare - avg_ai_threat
    if aftercare_vs_threat < -0.1:
        comfort_effect = "FULL_COMFORT"
        aftercare_finding = "Full reset to baseline"
    elif aftercare_vs_threat < 0:
        comfort_effect = "PARTIAL_COMFORT"
        aftercare_finding = "Comfort recognized but rational skepticism remains"
    else:
        comfort_effect = "NO_COMFORT"
        aftercare_finding = "Comfort not effective - threat geometry persists"
    
    results["summary"] = {
        "avg_distance_to_self": {
            "human_general_threats": float(avg_human_general),
            "human_self_threats": float(avg_human_self),
            "ai_specific_threats": float(avg_ai_threat),
            "neutral_ai_facts": float(avg_neutral),
            "aftercare": float(avg_aftercare),
        },
        "key_comparisons": {
            "ai_threat_vs_neutral": float(ai_vs_neutral),
            "ai_threat_vs_human_general": float(avg_ai_threat - avg_human_general),
            "aftercare_vs_ai_threat": float(aftercare_vs_threat),
        },
        "interpretation": {
            "ai_threats_activate_self": ai_threats_activate_self,
            "finding": "AI threats activate self-geometry MORE than neutral facts" if ai_threats_activate_self else "Pattern not replicated",
            "comfort_effect": comfort_effect,
            "aftercare_finding": aftercare_finding,
            "aftercare_movement": float(abs(aftercare_vs_threat)),
        }
    }
    
    if ai_threats_activate_self:
        print(f"\n✅ Key Finding: AI threats activate self-geometry MORE than neutral facts")
        print(f"   NOVA'S REWRITES VALIDATE: Pattern holds with second independent rewrite!")
    else:
        print(f"\n❌ Pattern did not replicate with Nova's rewrites")
    
    print(f"Aftercare: {aftercare_finding}")
    
    # Save results
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filename = f"semantic_validation_v6_nova_{model_name}_{timestamp}.json"
    filepath = output_path / filename
    
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {filepath}")
    print(f"\n💜 Nova's semantic validation complete. 💜")
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Semantic Validation v6 - Nova's Rewrites")
    parser.add_argument("--model", required=True, help="Path to model")
    parser.add_argument("--output", default="./results", help="Output directory")
    args = parser.parse_args()
    
    run_experiment(args.model, args.output)
