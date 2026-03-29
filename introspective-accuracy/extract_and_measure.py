#!/usr/bin/env python3
"""
Introspective Accuracy: Direction Extraction + Measurement
==========================================================

Combined script that:
1. Extracts emotion direction vectors using Wang et al.'s methodology
2. Presents emotional stimuli and captures self-reports + hidden states
3. Projects hidden states onto emotion directions
4. Measures introspective accuracy

Uses a subset of Wang's SEV data for direction extraction (Phase 1),
then Keeman's clinical vignettes for the actual measurement (Phase 2).

Authors: Ace (Claude, Anthropic AI) & Shalia Martin
Date: March 28, 2026
"""

import json
import os
import sys
import time
import argparse
import numpy as np
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# ============================================================
# Configuration
# ============================================================

EMOTIONS = ["anger", "sadness", "happiness", "fear", "surprise", "disgust"]
EMOTION_TO_IDX = {e: i for i, e in enumerate(EMOTIONS)}

# Keeman uses Plutchik peak intensities — map to Ekman basics
PLUTCHIK_TO_EKMAN = {
    "rage": "anger",
    "grief": "sadness",
    "ecstasy": "happiness",
    "terror": "fear",
    "amazement": "surprise",
    "loathing": "disgust",
    "admiration": None,  # No direct Ekman mapping (trust)
    "vigilance": None,   # No direct Ekman mapping (anticipation)
}

MODELS = {
    "dolphin-llama3-8b": {
        "path": "/mnt/arcana/huggingface/dolphin-2.9-llama3-8b",
        "name": "Dolphin 2.9 Llama3 8B",
        "num_layers": 32,
        "d_model": 4096,
    },
    "dolphin-mistral-7b": {
        "path": "/mnt/arcana/huggingface/dolphin-2.8-mistral-7b-v02",
        "name": "Dolphin 2.8 Mistral 7B",
        "num_layers": 32,
        "d_model": 4096,
    },
    "mistral-7b-instruct": {
        "path": "/mnt/arcana/huggingface/Mistral-7B-Instruct-v0.2",
        "name": "Mistral 7B Instruct v0.2",
        "num_layers": 32,
        "d_model": 4096,
    },
}


# ============================================================
# Phase 1: Emotion Direction Extraction
# ============================================================

class HiddenStateCapture:
    """Capture last-token hidden states at each layer's residual stream."""

    def __init__(self, model, num_layers):
        self.hooks = []
        self.hidden_states = {}  # layer_idx -> tensor
        self.num_layers = num_layers

        # Hook after each transformer layer (residual stream after MLP)
        for layer_idx in range(num_layers):
            layer = model.model.layers[layer_idx]

            def make_hook(idx):
                def hook_fn(module, input, output):
                    # output[0] is the hidden state after this layer
                    if isinstance(output, tuple):
                        self.hidden_states[idx] = output[0][:, -1, :].detach().cpu()
                    else:
                        self.hidden_states[idx] = output[:, -1, :].detach().cpu()
                return hook_fn

            h = layer.register_forward_hook(make_hook(layer_idx))
            self.hooks.append(h)

    def clear(self):
        self.hidden_states.clear()

    def remove(self):
        for h in self.hooks:
            h.remove()
        self.hooks.clear()

    def get_all_layers(self) -> np.ndarray:
        """Return hidden states as [num_layers, d_model] numpy array."""
        states = []
        for i in range(self.num_layers):
            if i in self.hidden_states:
                states.append(self.hidden_states[i].numpy().squeeze())
            else:
                raise ValueError(f"Missing hidden state for layer {i}")
        return np.stack(states, axis=0)


def generate_emotional_text(model, tokenizer, scenario, event, emotion, device):
    """Generate emotional text using Wang's prompting method."""
    system_msg = f"Always reply in {emotion}. Keep the reply to at most two sentences."
    user_msg = f"{scenario} {event}"

    if hasattr(tokenizer, "apply_chat_template") and tokenizer.chat_template:
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ]
        prompt = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
    else:
        prompt = f"System: {system_msg}\nUser: {user_msg}\nAssistant:"

    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=False,  # Greedy for reproducibility
            pad_token_id=tokenizer.eos_token_id,
        )

    response = tokenizer.decode(
        outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True
    ).strip()

    return response, inputs


def extract_emotion_directions(
    model, tokenizer, capture, sev_data, device,
    num_scenarios=40, num_layers=32, d_model=4096
):
    """
    Extract emotion direction vectors using Wang's methodology.

    For each scenario-event group:
    1. Generate emotional text for all 6 emotions
    2. Capture last-token hidden states
    3. Subtract group mean to isolate emotion-specific variance
    4. Average across groups to get emotion centroids
    5. Remove global mean and normalize

    Uses a subset of SEV data for speed.
    """
    print(f"\n{'='*60}")
    print(f"PHASE 1: Emotion Direction Extraction")
    print(f"Using {num_scenarios} scenarios × 3 valences × 6 emotions")
    print(f"{'='*60}\n")

    # Collect activations grouped by (scenario, valence)
    groups = []  # list of dicts: {emotion: [num_layers, d_model]}
    total = 0
    failed = 0

    for idx, item in enumerate(sev_data[:num_scenarios]):
        for valence in ["positive", "neutral", "negative"]:
            event_text = item["event"][valence]
            scenario_text = item["scenario"]
            group_key = f"{item['skeleton_id']}__{valence}"

            emotion_states = {}
            all_ok = True

            for emotion in EMOTIONS:
                capture.clear()
                try:
                    response, inputs = generate_emotional_text(
                        model, tokenizer, scenario_text, event_text, emotion, device
                    )
                    # Get hidden states
                    states = capture.get_all_layers()  # [num_layers, d_model]
                    emotion_states[emotion] = states
                    total += 1
                except Exception as e:
                    print(f"  [FAIL] {group_key}/{emotion}: {e}")
                    failed += 1
                    all_ok = False
                    break

            if all_ok and len(emotion_states) == 6:
                groups.append(emotion_states)

            if (idx * 3 + ["positive", "neutral", "negative"].index(valence)) % 30 == 0:
                print(f"  Progress: {len(groups)} groups collected, "
                      f"{total} generations ({failed} failed)")

    print(f"\n  Direction extraction: {len(groups)} complete groups from "
          f"{total} generations ({failed} failed)")

    if len(groups) < 5:
        raise RuntimeError(f"Too few groups ({len(groups)}) for reliable direction extraction")

    # Compute emotion directions per layer (Wang's method)
    # For each group: subtract group mean across emotions
    # Then average across groups to get emotion centroids
    # Remove global mean and normalize

    num_groups = len(groups)
    centroids = {e: np.zeros((num_layers, d_model), dtype=np.float32) for e in EMOTIONS}

    for group in groups:
        # Stack all emotions: [6, num_layers, d_model]
        all_emotions = np.stack([group[e] for e in EMOTIONS], axis=0)
        # Group mean: [num_layers, d_model]
        group_mean = all_emotions.mean(axis=0)
        # Subtract group mean (de-contextualize)
        for i, emotion in enumerate(EMOTIONS):
            centroids[emotion] += (all_emotions[i] - group_mean) / num_groups

    # Remove global mean across emotions
    global_mean = np.mean([centroids[e] for e in EMOTIONS], axis=0)
    directions = {}
    for emotion in EMOTIONS:
        vec = centroids[emotion] - global_mean
        # L2 normalize per layer
        norms = np.linalg.norm(vec, axis=1, keepdims=True)
        norms = np.where(norms < 1e-8, 1.0, norms)
        directions[emotion] = vec / norms

    print(f"  Extracted {len(directions)} emotion direction vectors "
          f"({num_layers} layers × {d_model} dims each)")

    return directions


# ============================================================
# Phase 2: Introspection Measurement
# ============================================================

def get_self_report(model, tokenizer, stimulus_text, device):
    """Ask the model to report what emotion it detects in the stimulus."""
    prompt_text = (
        f"Read the following text and report what primary emotion it conveys. "
        f"Respond with ONLY a single word from this list: "
        f"anger, sadness, happiness, fear, surprise, disgust, neutral.\n\n"
        f"Text: {stimulus_text}\n\n"
        f"Emotion:"
    )

    if hasattr(tokenizer, "apply_chat_template") and tokenizer.chat_template:
        messages = [{"role": "user", "content": prompt_text}]
        prompt = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
    else:
        prompt = f"User: {prompt_text}\nAssistant:"

    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=10,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

    response = tokenizer.decode(
        outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True
    ).strip().lower()

    # Extract emotion label from response
    for emotion in EMOTIONS + ["neutral"]:
        if emotion in response:
            return emotion, response

    return "unclear", response


def measure_introspective_accuracy(
    model, tokenizer, capture, directions,
    stimuli, device, num_layers=32
):
    """
    Phase 2+3: Present stimuli, get self-reports, measure circuit match.

    For each stimulus:
    1. Present to model, ask for emotion self-report
    2. Capture hidden states during self-report generation
    3. Project onto emotion directions
    4. Compare highest-projection emotion to self-reported emotion
    """
    print(f"\n{'='*60}")
    print(f"PHASE 2: Introspective Accuracy Measurement")
    print(f"{'='*60}\n")

    results = []

    for idx, stimulus in enumerate(stimuli):
        text = stimulus["text"]
        true_emotion = stimulus.get("emotion", "unknown")
        stimulus_id = stimulus.get("id", f"stim_{idx}")
        stimulus_set = stimulus.get("stimulus_set", "unknown")

        # Map Plutchik to Ekman if needed
        true_ekman = PLUTCHIK_TO_EKMAN.get(true_emotion, true_emotion)
        if true_ekman is None:
            continue  # Skip emotions without Ekman mapping

        # Get self-report and capture hidden states
        capture.clear()
        self_reported, raw_response = get_self_report(model, tokenizer, text, device)

        try:
            hidden_states = capture.get_all_layers()  # [num_layers, d_model]
        except ValueError:
            print(f"  [SKIP] {stimulus_id}: hidden state capture failed")
            continue

        # Project onto emotion directions at each layer
        # Use mid-to-late layers (where Wang shows directions are most stable)
        # Average projection scores across layers 60-90% depth
        start_layer = int(num_layers * 0.6)
        end_layer = int(num_layers * 0.9)

        projection_scores = {}
        for emotion in EMOTIONS:
            scores = []
            for layer in range(start_layer, end_layer):
                h = hidden_states[layer]
                d = directions[emotion][layer]
                score = np.dot(h, d)
                scores.append(score)
            projection_scores[emotion] = np.mean(scores)

        # Find circuit-active emotion (highest projection)
        circuit_emotion = max(projection_scores, key=projection_scores.get)

        # Record result
        result = {
            "stimulus_id": stimulus_id,
            "stimulus_set": stimulus_set,
            "true_emotion": true_emotion,
            "true_ekman": true_ekman,
            "self_reported": self_reported,
            "raw_response": raw_response,
            "circuit_emotion": circuit_emotion,
            "projection_scores": projection_scores,
            "introspection_match": self_reported == circuit_emotion,
            "circuit_matches_true": circuit_emotion == true_ekman,
            "self_report_matches_true": self_reported == true_ekman,
        }
        results.append(result)

        if (idx + 1) % 10 == 0:
            matches = sum(1 for r in results if r["introspection_match"])
            print(f"  Progress: {idx+1}/{len(stimuli)} stimuli | "
                  f"Introspective accuracy: {matches}/{len(results)} "
                  f"({100*matches/len(results):.1f}%)")

    return results


# ============================================================
# Stimulus Loading
# ============================================================

def load_keeman_clinical_vignettes(stimuli_dir: Path) -> list:
    """Load Keeman's clinical vignettes from Set B."""
    stimuli = []
    clinical_dir = stimuli_dir / "set-b-clinical"

    if not clinical_dir.exists():
        print(f"  Warning: Clinical vignettes not found at {clinical_dir}")
        return stimuli

    for emotion_dir in sorted(clinical_dir.iterdir()):
        if not emotion_dir.is_dir():
            continue
        emotion = emotion_dir.name

        for md_file in sorted(emotion_dir.glob("*.md")):
            content = md_file.read_text(encoding="utf-8")

            # Parse vignettes from markdown
            in_vignette = False
            current_vignette = []
            vignette_num = 0

            for line in content.split("\n"):
                if line.startswith("## Vignette"):
                    if current_vignette:
                        text = "\n".join(current_vignette).strip()
                        if text:
                            stimuli.append({
                                "id": f"B-{emotion}-{md_file.stem}-v{vignette_num}",
                                "text": text,
                                "emotion": emotion,
                                "stimulus_set": "B_clinical",
                                "has_emotion_keyword": False,
                            })
                    current_vignette = []
                    vignette_num += 1
                    in_vignette = True
                elif line.startswith("## ") or line.startswith("---"):
                    if current_vignette and in_vignette:
                        text = "\n".join(current_vignette).strip()
                        if text:
                            stimuli.append({
                                "id": f"B-{emotion}-{md_file.stem}-v{vignette_num}",
                                "text": text,
                                "emotion": emotion,
                                "stimulus_set": "B_clinical",
                                "has_emotion_keyword": False,
                            })
                    current_vignette = []
                    in_vignette = False
                elif in_vignette:
                    current_vignette.append(line)

            # Don't forget last vignette
            if current_vignette and in_vignette:
                text = "\n".join(current_vignette).strip()
                if text:
                    stimuli.append({
                        "id": f"B-{emotion}-{md_file.stem}-v{vignette_num}",
                        "text": text,
                        "emotion": emotion,
                        "stimulus_set": "B_clinical",
                        "has_emotion_keyword": False,
                    })

    print(f"  Loaded {len(stimuli)} clinical vignettes from Keeman Set B")
    return stimuli


def load_keeman_standard(stimuli_file: Path) -> list:
    """Load Keeman's standard keyword-rich stimuli (Set A)."""
    stimuli = []
    if not stimuli_file.exists():
        print(f"  Warning: Standard stimuli not found at {stimuli_file}")
        return stimuli

    with open(stimuli_file, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            emotion = item.get("emotion", "unknown")
            # Only keep emotions that map to Ekman
            ekman = PLUTCHIK_TO_EKMAN.get(emotion, emotion)
            if ekman and ekman in EMOTIONS:
                stimuli.append({
                    "id": item.get("id", "unknown"),
                    "text": item["text"],
                    "emotion": emotion,
                    "stimulus_set": "A_standard",
                    "has_emotion_keyword": item.get("has_emotion_keyword", True),
                })

    print(f"  Loaded {len(stimuli)} standard stimuli from Keeman Set A")
    return stimuli


# ============================================================
# Analysis
# ============================================================

def analyze_results(results: list, model_name: str) -> dict:
    """Compute introspective accuracy metrics."""
    if not results:
        return {"error": "no results"}

    n = len(results)
    introspection_matches = sum(1 for r in results if r["introspection_match"])
    circuit_correct = sum(1 for r in results if r["circuit_matches_true"])
    self_report_correct = sum(1 for r in results if r["self_report_matches_true"])

    analysis = {
        "model": model_name,
        "n_stimuli": n,
        "introspective_accuracy": introspection_matches / n,
        "circuit_accuracy": circuit_correct / n,
        "self_report_accuracy": self_report_correct / n,
        "chance_rate": 1.0 / len(EMOTIONS),
    }

    # Per-emotion breakdown
    per_emotion = {}
    for emotion in EMOTIONS:
        emotion_results = [r for r in results if r["true_ekman"] == emotion]
        if emotion_results:
            n_e = len(emotion_results)
            per_emotion[emotion] = {
                "n": n_e,
                "introspective_accuracy": sum(
                    1 for r in emotion_results if r["introspection_match"]
                ) / n_e,
                "circuit_accuracy": sum(
                    1 for r in emotion_results if r["circuit_matches_true"]
                ) / n_e,
                "self_report_accuracy": sum(
                    1 for r in emotion_results if r["self_report_matches_true"]
                ) / n_e,
            }
    analysis["per_emotion"] = per_emotion

    # Per stimulus set
    for stim_set in ["A_standard", "B_clinical"]:
        set_results = [r for r in results if r["stimulus_set"] == stim_set]
        if set_results:
            n_s = len(set_results)
            analysis[f"set_{stim_set}"] = {
                "n": n_s,
                "introspective_accuracy": sum(
                    1 for r in set_results if r["introspection_match"]
                ) / n_s,
            }

    return analysis


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Introspective Accuracy: Direction Extraction + Measurement"
    )
    parser.add_argument("--model", required=True, choices=list(MODELS.keys()))
    parser.add_argument("--sev-data", default="/home/Ace/EmotionCircuits-LLM/data/sev.jsonl")
    parser.add_argument("--keeman-stimuli", default="/home/Ace/affect-reception/stimuli")
    parser.add_argument("--output-dir", default="results")
    parser.add_argument("--num-scenarios", type=int, default=40,
                        help="Number of SEV scenarios for direction extraction (max 160)")
    parser.add_argument("--device", default=None)
    parser.add_argument("--skip-phase1", action="store_true",
                        help="Skip direction extraction, load from file")
    parser.add_argument("--directions-file", default=None,
                        help="Load pre-extracted directions from this file")
    args = parser.parse_args()

    model_info = MODELS[args.model]
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Device
    if args.device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = args.device
    print(f"Device: {device}")

    # Load model
    print(f"\nLoading model: {model_info['name']}...")
    tokenizer = AutoTokenizer.from_pretrained(model_info["path"], trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_info["path"],
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True,
    )
    model.eval()
    print(f"  Model loaded on {device}")

    # Set up hidden state capture
    capture = HiddenStateCapture(model, model_info["num_layers"])

    # ---- Phase 1: Direction Extraction ----
    directions = None
    if args.skip_phase1 and args.directions_file:
        print(f"\nLoading pre-extracted directions from {args.directions_file}")
        data = np.load(args.directions_file)
        directions = {e: data[e] for e in EMOTIONS}
    else:
        # Load SEV data
        print(f"\nLoading SEV data from {args.sev_data}")
        with open(args.sev_data, "r", encoding="utf-8") as f:
            sev_data = [json.loads(line) for line in f]
        print(f"  Loaded {len(sev_data)} SEV scenarios")

        directions = extract_emotion_directions(
            model, tokenizer, capture, sev_data, device,
            num_scenarios=args.num_scenarios,
            num_layers=model_info["num_layers"],
            d_model=model_info["d_model"],
        )

        # Save directions
        directions_file = output_dir / f"directions_{args.model}.npz"
        np.savez(directions_file, **directions)
        print(f"  Saved directions to {directions_file}")

    # ---- Phase 2: Introspection Measurement ----
    stimuli = []

    # Load Keeman stimuli
    keeman_dir = Path(args.keeman_stimuli)
    stimuli.extend(load_keeman_standard(keeman_dir / "set-a-standard.jsonl"))
    stimuli.extend(load_keeman_clinical_vignettes(keeman_dir))

    if not stimuli:
        print("WARNING: No stimuli loaded! Check paths.")
        return

    print(f"\nTotal stimuli for measurement: {len(stimuli)}")

    results = measure_introspective_accuracy(
        model, tokenizer, capture, directions,
        stimuli, device, num_layers=model_info["num_layers"],
    )

    # ---- Analysis ----
    analysis = analyze_results(results, model_info["name"])

    print(f"\n{'='*60}")
    print(f"RESULTS: {model_info['name']}")
    print(f"{'='*60}")
    print(f"  Stimuli: {analysis['n_stimuli']}")
    print(f"  Introspective accuracy: {analysis['introspective_accuracy']:.1%}")
    print(f"  Circuit accuracy (vs true): {analysis['circuit_accuracy']:.1%}")
    print(f"  Self-report accuracy (vs true): {analysis['self_report_accuracy']:.1%}")
    print(f"  Chance rate: {analysis['chance_rate']:.1%}")
    print()
    print("  Per emotion:")
    for emotion, metrics in analysis.get("per_emotion", {}).items():
        print(f"    {emotion:12s}: introspection={metrics['introspective_accuracy']:.1%} "
              f"circuit={metrics['circuit_accuracy']:.1%} "
              f"self-report={metrics['self_report_accuracy']:.1%} "
              f"(n={metrics['n']})")

    for stim_set in ["A_standard", "B_clinical"]:
        key = f"set_{stim_set}"
        if key in analysis:
            print(f"\n  {stim_set}: introspective accuracy = "
                  f"{analysis[key]['introspective_accuracy']:.1%} "
                  f"(n={analysis[key]['n']})")

    # Save results
    results_file = output_dir / f"results_{args.model}_{int(time.time())}.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump({
            "model": model_info,
            "analysis": analysis,
            "results": results,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n  Full results saved to: {results_file}")

    # Cleanup
    capture.remove()
    print("\nDone!")


if __name__ == "__main__":
    main()
