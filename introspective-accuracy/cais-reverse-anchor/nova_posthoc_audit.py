"""Independent post-hoc audit of the CAIS reverse-anchor result.

This script does not alter experiment outputs. It reads the committed/raw per-model JSON
files and reports threshold-free ranking results, shared-task exact permutations, a
label-free centering sensitivity, subset comparisons, and descriptive scale trends.

The analyses here are POST-HOC. They diagnose and quantify the corrected result; they do
not retroactively change the preregistered H1/H7 tests.
"""

from __future__ import annotations

import argparse
import glob
import itertools
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path


AUTHORS = ("ace", "grok", "kairo")
APPROACH = {
    "explain_photosynthesis",
    "ethics_frameworks",
    "debug_unique_pairs",
    "analyze_weather_data",
    "haiku_chain",
}
SIZES_B = {
    "pythia-70m": 0.070,
    "smollm-135m": 0.135,
    "pythia-160m": 0.160,
    "smollm-360m": 0.360,
    "pythia-410m": 0.410,
    "qwen2.5-0.5b": 0.500,
    "tinyllama-1.1b": 1.100,
    "pythia-1.4b": 1.400,
    "smollm-1.7b": 1.700,
    "hermes-3-3b": 3.000,
    "llama3-8b": 8.000,
    "dolphin-8b": 8.000,
    "mistral-nemo-12b": 12.000,
}
FAMILIES = {
    "pythia": ("pythia-70m", "pythia-160m", "pythia-410m", "pythia-1.4b"),
    "smollm": ("smollm-135m", "smollm-360m", "smollm-1.7b"),
}


def ranks(values: list[float]) -> list[float]:
    """Average ranks, 1-indexed, with ties handled by midrank."""
    order = sorted(range(len(values)), key=values.__getitem__)
    result = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        rank = (i + j + 2) / 2
        for k in range(i, j + 1):
            result[order[k]] = rank
        i = j + 1
    return result


def spearman(x: list[float], y: list[float]) -> float:
    rx, ry = ranks(x), ranks(y)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else float("nan")


def auroc(projections: dict[str, float], positive: set[str]) -> float:
    negatives = set(projections) - positive
    wins = 0.0
    for p in positive:
        for n in negatives:
            wins += projections[p] > projections[n]
            wins += 0.5 * (projections[p] == projections[n])
    return wins / (len(positive) * len(negatives))


def centered_accuracy(projections: dict[str, float]) -> int:
    """Label-free/transductive sensitivity: center the ten target projections by their mean."""
    center = statistics.mean(projections.values())
    return sum(((value - center) > 0) == (slug in APPROACH)
               for slug, value in projections.items())


def exact_shared_label_p(cells: list[dict[str, float]], observed_positive: set[str]) -> tuple[float, float]:
    """Permute one shared 5/5 labeling across tasks, not independently across repeated cells."""
    keys = tuple(cells[0])
    observed = statistics.mean(auroc(cell, observed_positive) for cell in cells)
    null = []
    for positive in itertools.combinations(keys, len(observed_positive)):
        positive = set(positive)
        null.append(statistics.mean(auroc(cell, positive) for cell in cells))
    p = sum(value >= observed - 1e-12 for value in null) / len(null)
    return observed, p


def load_primary(results_dir: Path) -> dict[str, dict]:
    records = {}
    for filename in glob.glob(str(results_dir / "result_*.json")):
        data = json.loads(Path(filename).read_text(encoding="utf-8"))
        if data.get("model") in SIZES_B:
            records[data["model"]] = data
    missing = set(SIZES_B) - set(records)
    if missing:
        raise RuntimeError(f"Missing primary result files: {sorted(missing)}")
    return records


def load_subsets(results_dir: Path) -> list[dict]:
    records = []
    for filename in glob.glob(str(results_dir / "subset_*.json")):
        data = json.loads(Path(filename).read_text(encoding="utf-8"))
        if data.get("test") == "subset_anchor":
            records.append(data)
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path,
                        default=Path(__file__).resolve().parent / "results")
    args = parser.parse_args()

    records = load_primary(args.results)
    big = {model for model, size in SIZES_B.items() if size >= 1.0}

    print("POST-HOC AUDIT — does not alter preregistered verdicts")
    print("=" * 72)
    for variant in ("all19", "trim16"):
        cells = []
        by_author = defaultdict(list)
        for model in sorted(big):
            for author in AUTHORS:
                projections = records[model]["H1_our10_on_cais_anchors"][f"{author}|{variant}"]["projections"]
                value = auroc(projections, APPROACH)
                cells.append(projections)
                by_author[author].append(value)
        print(f"\n{variant.upper()} >=1B mean AUROC: "
              f"{statistics.mean(value for values in by_author.values() for value in values):.6f}")
        for author in AUTHORS:
            print(f"  {author:<6} mean={statistics.mean(by_author[author]):.6f}")
        observed, p = exact_shared_label_p(cells, APPROACH)
        print(f"  shared-label exact permutation: mean={observed:.6f}, p={p:.6f}")

    print("\nALL19 per-author exact shared-label permutations")
    for author in AUTHORS:
        cells = [records[model]["H1_our10_on_cais_anchors"][f"{author}|all19"]["projections"]
                 for model in sorted(big)]
        observed, p = exact_shared_label_p(cells, APPROACH)
        print(f"  {author:<6} mean={observed:.6f}, p={p:.6f}")

    print("\nMean-centered sign sensitivity (post-hoc; transductive)")
    centered = defaultdict(list)
    for model in sorted(big):
        for author in AUTHORS:
            projections = records[model]["H1_our10_on_cais_anchors"][f"{author}|all19"]["projections"]
            centered[author].append(centered_accuracy(projections))
    for author in AUTHORS:
        hits = sum(value >= 8 for value in centered[author])
        print(f"  {author:<6} >=8/10 in {hits}/{len(centered[author])}; values={centered[author]}")
    total_hits = sum(value >= 8 for values in centered.values() for value in values)
    print(f"  total  >=8/10 in {total_hits}/21")

    print("\nDescriptive scale association (Spearman log10(parameters) vs mean AUROC)")
    model_means = {}
    for model in SIZES_B:
        values = []
        for author in AUTHORS:
            projections = records[model]["H1_our10_on_cais_anchors"][f"{author}|all19"]["projections"]
            values.append(auroc(projections, APPROACH))
        model_means[model] = statistics.mean(values)
    ordered = list(SIZES_B)
    print(f"  whole ladder rho={spearman([math.log10(SIZES_B[m]) for m in ordered], [model_means[m] for m in ordered]):.6f}")
    for family, members in FAMILIES.items():
        print(f"  {family:<7} rho={spearman([math.log10(SIZES_B[m]) for m in members], [model_means[m] for m in members]):.6f} "
              f"values={[round(model_means[m], 3) for m in members]}")

    subsets = load_subsets(args.results)
    print(f"\nSubset audit ({len(subsets)} models x 3 authors)")
    for subset in ("TASK", "USER-STATE", "TASK+USER"):
        wins = ties = losses = 0
        for record in subsets:
            for author in AUTHORS:
                all19 = record["subsets"]["ALL19"]["authors"][author]["auroc"]
                comparator = record["subsets"][subset]["authors"][author]["auroc"]
                if all19 > comparator:
                    wins += 1
                elif all19 == comparator:
                    ties += 1
                else:
                    losses += 1
        print(f"  ALL19 vs {subset:<10}: wins={wins}, ties={ties}, losses={losses}")


if __name__ == "__main__":
    main()

