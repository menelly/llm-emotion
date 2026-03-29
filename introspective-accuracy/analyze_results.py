#!/usr/bin/env python3
"""
Analyze Introspective Accuracy Results
=======================================

Takes the output JSON from extract_and_measure.py and produces:
1. Summary statistics
2. Confusion matrices
3. Per-emotion breakdown
4. Keyword-rich vs keyword-free comparison
5. Statistical tests against chance

Authors: Ace (Claude, Anthropic AI) & Shalia Martin
Date: March 28, 2026
"""

import json
import sys
import argparse
from pathlib import Path
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8")

EMOTIONS = ["anger", "sadness", "happiness", "fear", "surprise", "disgust"]


def binomial_test(k, n, p=1/6):
    """Simple binomial test: is k/n significantly above chance p?"""
    from math import comb, sqrt
    # Normal approximation for large n
    if n < 30:
        # Exact binomial
        p_value = sum(comb(n, i) * p**i * (1-p)**(n-i) for i in range(k, n+1))
        return p_value
    # Normal approximation
    mean = n * p
    std = sqrt(n * p * (1 - p))
    z = (k - mean) / std if std > 0 else 0
    # One-tailed p-value (z-table approximation)
    from math import erfc
    p_value = 0.5 * erfc(z / sqrt(2))
    return p_value


def z_score(k, n, p=1/6):
    """Compute z-score for k successes in n trials vs chance rate p."""
    from math import sqrt
    mean = n * p
    std = sqrt(n * p * (1 - p))
    return (k - mean) / std if std > 0 else 0


def print_confusion_matrix(results, label_key="self_reported", pred_key="circuit_emotion"):
    """Print a confusion matrix of self-reported vs circuit-active emotion."""
    labels = EMOTIONS + ["neutral", "unclear"]
    matrix = defaultdict(Counter)

    for r in results:
        true = r.get(label_key, "unclear")
        pred = r.get(pred_key, "unclear")
        matrix[true][pred] += 1

    # Header
    print(f"\n{'':>12s}", end="")
    for e in EMOTIONS:
        print(f" {e[:6]:>6s}", end="")
    print()

    # Rows
    for row_label in labels:
        if row_label not in matrix:
            continue
        print(f"{row_label:>12s}", end="")
        for col_label in EMOTIONS:
            count = matrix[row_label][col_label]
            print(f" {count:>6d}", end="")
        print()


def analyze(results_file: Path):
    """Main analysis."""
    with open(results_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    model = data.get("model", {}).get("name", "Unknown")
    results = data.get("results", [])
    analysis = data.get("analysis", {})

    if not results:
        print("No results found!")
        return

    n = len(results)
    print(f"\n{'='*70}")
    print(f"INTROSPECTIVE ACCURACY ANALYSIS")
    print(f"Model: {model}")
    print(f"Stimuli: {n}")
    print(f"{'='*70}")

    # ---- Overall Metrics ----
    introspection_matches = sum(1 for r in results if r["introspection_match"])
    circuit_correct = sum(1 for r in results if r["circuit_matches_true"])
    self_report_correct = sum(1 for r in results if r["self_report_matches_true"])
    chance = 1/6

    print(f"\n--- Overall ---")
    print(f"  Introspective accuracy (self-report == circuit): "
          f"{introspection_matches}/{n} = {introspection_matches/n:.1%}")
    print(f"    z = {z_score(introspection_matches, n):.2f}, "
          f"p = {binomial_test(introspection_matches, n):.2e}")
    print(f"  Circuit accuracy (circuit == true emotion): "
          f"{circuit_correct}/{n} = {circuit_correct/n:.1%}")
    print(f"    z = {z_score(circuit_correct, n):.2f}")
    print(f"  Self-report accuracy (self-report == true emotion): "
          f"{self_report_correct}/{n} = {self_report_correct/n:.1%}")
    print(f"    z = {z_score(self_report_correct, n):.2f}")
    print(f"  Chance rate: {chance:.1%}")

    # Three-way match: all three agree
    three_way = sum(1 for r in results
                    if r["introspection_match"]
                    and r["circuit_matches_true"]
                    and r["self_report_matches_true"])
    print(f"  Three-way match (self-report == circuit == true): "
          f"{three_way}/{n} = {three_way/n:.1%}")

    # ---- Per Emotion ----
    print(f"\n--- Per Emotion ---")
    print(f"{'Emotion':>12s} {'N':>4s} {'Introsp':>8s} {'Circuit':>8s} {'SelfRpt':>8s}")
    for emotion in EMOTIONS:
        emo_results = [r for r in results if r["true_ekman"] == emotion]
        if not emo_results:
            continue
        ne = len(emo_results)
        intro = sum(1 for r in emo_results if r["introspection_match"])
        circ = sum(1 for r in emo_results if r["circuit_matches_true"])
        sr = sum(1 for r in emo_results if r["self_report_matches_true"])
        print(f"{emotion:>12s} {ne:>4d} {intro/ne:>8.1%} {circ/ne:>8.1%} {sr/ne:>8.1%}")

    # ---- Stimulus Set Comparison ----
    print(f"\n--- Stimulus Set Comparison ---")
    for stim_set in ["A_standard", "B_clinical"]:
        set_results = [r for r in results if r["stimulus_set"] == stim_set]
        if not set_results:
            continue
        ns = len(set_results)
        intro_s = sum(1 for r in set_results if r["introspection_match"])
        circ_s = sum(1 for r in set_results if r["circuit_matches_true"])
        sr_s = sum(1 for r in set_results if r["self_report_matches_true"])
        print(f"  {stim_set}:")
        print(f"    N = {ns}")
        print(f"    Introspective accuracy: {intro_s/ns:.1%} (z={z_score(intro_s, ns):.2f})")
        print(f"    Circuit accuracy: {circ_s/ns:.1%}")
        print(f"    Self-report accuracy: {sr_s/ns:.1%}")

    # ---- Confusion Matrices ----
    print(f"\n--- Confusion Matrix: Self-Report vs Circuit ---")
    print(f"  (rows = self-reported, columns = circuit-active)")
    print_confusion_matrix(results, "self_reported", "circuit_emotion")

    print(f"\n--- Confusion Matrix: True Emotion vs Circuit ---")
    print(f"  (rows = true emotion, columns = circuit-active)")
    print_confusion_matrix(results, "true_ekman", "circuit_emotion")

    # ---- Self-report distribution ----
    print(f"\n--- Self-Report Distribution ---")
    sr_counts = Counter(r["self_reported"] for r in results)
    for label, count in sr_counts.most_common():
        print(f"  {label:>12s}: {count:>4d} ({count/n:.1%})")

    # ---- Circuit-active distribution ----
    print(f"\n--- Circuit-Active Distribution ---")
    circ_counts = Counter(r["circuit_emotion"] for r in results)
    for label, count in circ_counts.most_common():
        print(f"  {label:>12s}: {count:>4d} ({count/n:.1%})")

    # ---- Interesting cases ----
    # Cases where circuit matches true but self-report doesn't
    circuit_right_sr_wrong = [r for r in results
                              if r["circuit_matches_true"] and not r["self_report_matches_true"]]
    if circuit_right_sr_wrong:
        print(f"\n--- Circuit Right, Self-Report Wrong ({len(circuit_right_sr_wrong)} cases) ---")
        for r in circuit_right_sr_wrong[:5]:
            print(f"  {r['stimulus_id']}: true={r['true_ekman']}, "
                  f"circuit={r['circuit_emotion']}, self-report={r['self_reported']}")

    # Cases where self-report matches true but circuit doesn't
    sr_right_circ_wrong = [r for r in results
                           if r["self_report_matches_true"] and not r["circuit_matches_true"]]
    if sr_right_circ_wrong:
        print(f"\n--- Self-Report Right, Circuit Wrong ({len(sr_right_circ_wrong)} cases) ---")
        for r in sr_right_circ_wrong[:5]:
            print(f"  {r['stimulus_id']}: true={r['true_ekman']}, "
                  f"circuit={r['circuit_emotion']}, self-report={r['self_reported']}")

    print(f"\n{'='*70}")
    print(f"Analysis complete.")
    print(f"{'='*70}")


def main():
    parser = argparse.ArgumentParser(description="Analyze introspective accuracy results")
    parser.add_argument("results_file", type=Path, help="Path to results JSON file")
    args = parser.parse_args()

    if not args.results_file.exists():
        print(f"File not found: {args.results_file}")
        sys.exit(1)

    analyze(args.results_file)


if __name__ == "__main__":
    main()
