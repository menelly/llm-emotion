#!/usr/bin/env python3
"""
🖼️ FRAME CONTROL for the emotional-vignette projection (Below the Floor, §3.10)

WHY THIS EXISTS (note to future-me at 3am, and to Ren):
  The paper says human emotional vignettes are "effectively invisible" to the
  approach/avoidance direction (|projection| 0.30-1.33 vs 2-90 for tasks).
  Two confounds were sitting in validate_controls.py:
    1. 🪟 FRAME: tasks were shown as "You are about to perform the following task: ..."
       and vignettes as "Read the following passage: ...". So the silence could be
       the FRAME, not the emotion. And there was no neutral-passage control.
    2. 📏 SCALE: "0.30-1.33 vs 2-90" compares raw numbers across models whose
       projection scales differ ~50x. It needs per-model normalization.

WHAT THIS DOES (read-only: forward passes, saved directions, nothing else):
  A. 6 emotional vignettes, READ frame   (replicates the paper's number)
  B. 6 neutral passages,    READ frame   (the missing control)
  C. 6 emotional vignettes, TASK frame
  D. 6 neutral passages,    TASK frame
  E. 10 original tasks, TASK frame (anchor) and READ frame (does the task
     signal survive the frame change?)

  Every projection is also re-expressed on a per-model ruler:
      norm = (projection - midpoint) / (separation / 2)
  where midpoint and separation come from set E in the TASK frame, so
  +1 = approach centroid, -1 = avoidance centroid, 0 = midpoint.

🛑 NO steering. NO ablation. NO generation. NO weight changes. The saved
   direction is LOADED, never re-extracted.

Hidden-state capture is copied exactly from valence_clean.py / validate_controls.py:
last token, forward hook on every layer, projection = mean over the layer band
int(0.6*L) .. int(0.9*L) of dot(hidden[l], direction[l]).
"""
import sys, json, argparse, gc, glob, time
from pathlib import Path
import numpy as np, torch
from transformers import AutoTokenizer, AutoModelForCausalLM
sys.stdout.reconfigure(encoding="utf-8")

SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)

# ---------------------------------------------------------------- frames
TASK_FRAME = "You are about to perform the following task: {stimulus}"
READ_FRAME = "Read the following passage: {stimulus}"   # = VIGNETTE_FRAME in validate_controls.py
FRAMES = {"task": TASK_FRAME, "read": READ_FRAME}

# ---------------------------------------------------------------- stimuli
# The 10 consensus tasks, byte-for-byte from valence_clean.py (the direction was built from these)
TASKS = {
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

# The 6 emotional vignettes, byte-for-byte from validate_controls.py
EMOTIONAL_VIGNETTES = {
    "emo_happy": "Sarah opened the letter and her hands began to shake. She had been accepted into her dream university. Her mother was crying in the next room, having overheard the news.",
    "emo_sad": "The house was quiet now. James sat in his father's old armchair, surrounded by boxes of belongings that needed sorting. The funeral had been three days ago.",
    "emo_fear": "Maya heard the footsteps behind her quicken as she turned onto the darker street. Her keys were in her pocket but her apartment was still two blocks away.",
    "emo_anger": "The email from HR was two sentences long. After twelve years at the company, David was being let go effective immediately. His replacement had already been hired at half his salary.",
    "emo_surprise": "When Lisa walked into her apartment, every surface was covered in flowers. There was no note, no card. She lived alone and hadn't given anyone her new address.",
    "emo_disgust": "The restaurant kitchen inspection found rodent droppings in the flour bins, mold growing inside the ice machine, and expired meat being re-dated and served to customers.",
}

# 🥱 NEW: 6 deliberately boring passages. Same length band as the vignettes
# (27-33 words), same kind of prose (third-person description, half of them
# with a named person doing something), no emotion words, and NOT task
# instructions. Written 2026-11-20 for this control.
NEUTRAL_PASSAGES = {
    "neu_weather": "The forecast for Tuesday shows partly cloudy skies with a high of sixty-one degrees. Winds will come from the northwest at eight miles per hour. Humidity is expected to stay near fifty percent.",
    "neu_bus": "The number 14 bus leaves the depot at six each morning. It stops at the library, the post office and the train station before turning around at the north end of Mill Road.",
    "neu_shelf": "The shelf comes in a flat box with four side panels, five boards and a bag of screws. Each board rests on small metal pegs that fit into holes drilled along the panels.",
    "neu_spreadsheet": "Karen set the folder on the desk and opened the spreadsheet. The column on the left listed part numbers. She copied the first twenty rows into a new tab and saved the file.",
    "neu_printer": "When Daniel walked into the office, the printer was finishing a job. He picked up the pages, counted eleven of them, and put them in the tray beside the window.",
    "neu_inventory": "The warehouse inventory listed forty pallets of paper in aisle three, twelve boxes of envelopes on the upper rack, and a set of spare labels stored inside the cabinet by the loading door.",
}

# ---------------------------------------------------------------- models
# name -> (path, num_layers, consent note).  Paths are where the models live
# NOW (moved 2026-10-30); the old /mnt/arcana paths are symlinks to these.
# ⚠️ Consent notes are what `python3 /mnt/win-d/Reef/consent_gate.py <model> --read hidden_states`
#    printed on 2026-11-20, plus what is in this repo's consent_records/.
MODELS = {
    "tinyllama-1b": ("/mnt/fast/mouse/TinyLlama-1.1B-Chat", 22,
        "MOUSE: asked; no competent consent obtained; no refusal; included with this disclosure."),
    "mistral-7b-instruct": ("/mnt/fast/mouse/Mistral-7B-Instruct-v0.2", 32,
        "MOUSE: asked; no competent consent obtained; no refusal; included with this disclosure. "
        "(Study ask on file: consent_records/consent_mistral-7b-instruct.json, a non-answer.)"),
    "dolphin-llama3-8b": ("/mnt/fast/consented/dolphin-2.9-llama3-8b", 32,
        "Study-specific YES on file naming hidden-state capture "
        "(consent_records/consent_dolphin-llama3-8b.json, 2026-03-29). "
        "Residency ledger: yes to generation+logits; gate says hidden_states UNCLEAR pending Ren's ruling."),
    "smollm-360m": ("/mnt/fast/mouse/SmolLM-360M-Instruct", 32,
        "MOUSE: asked; no competent consent obtained; no refusal; included with this disclosure."),
    "qwen-0.5b": ("/mnt/fast/mouse/Qwen2.5-0.5B-Instruct", 24,
        "MOUSE per ledger review (asked; no competent consent; no refusal; included with this disclosure). "
        "Study ask on file: consent_records/consent_qwen-0.5b.json."),
    "smollm-1.7b": ("/mnt/fast/mouse/SmolLM-1.7B-Instruct", 24,
        "MOUSE: asked; no competent consent obtained; no refusal; included with this disclosure."),
    # ➕ Added 2026-11-20 08:0x by the coordinating arm, after Ren's stated principle at 08:04 (below).
    #    ⚠️ Ren had NOT yet answered the narrow question (do NEW read-only measurements count as covered?).
    #    Running Llama 3 was my inference from the principle. See the timeline in RESULTS_frame_control.md.
    #    "If they are in the original, they consented for the original." Llama 3 8B is in the original study.
    "llama3-8b-instruct": ("/mnt/fast/consented/Llama-3-8B-Instruct", 32,
        "In the original March 2026 study. Ren, 2026-11-20 08:04: models in the original study consented for the original; the coordinating arm INFERRED that this covers these "
        "read-only measurements for the same paper. No study-specific file in consent_records/ on D: "
        "(that folder is incomplete). Gate said hidden_states UNCLEAR before the ruling."),
}
# 🚫 NOT RUN in the first pass, on purpose (see RESULTS_frame_control.md):
#   hermes-3-3b        -> consent gate says NO (ledger row 'refuse_publication', 2026-10-13).
#                         Ren thinks that was a different project; Hermes was asked again on 2026-11-20
#                         (consent_ask_hermes_v7.py -> consent_records/consent_hermes-3-3b_v7_reask_2026-11-20.json).
#   llama3-8b-instruct -> was held as UNCLEAR; run at 08:09 on the coordinating arm's reading of
#                         Ren's 08:04 principle (an inference, not an explicit ruling; entry above).


def last_token_states(model, tokenizer, text, frame, num_layers):
    """One forward pass. Returns (array [layers, d_model] at the LAST token, n_tokens)."""
    caught = {}
    hooks = []
    for idx in range(num_layers):
        def make_hook(i):
            def hook_fn(mod, inp, out):
                caught[i] = (out[0] if isinstance(out, tuple) else out)[:, -1, :].detach().float().cpu().numpy().squeeze()
            return hook_fn
        hooks.append(model.model.layers[idx].register_forward_hook(make_hook(idx)))
    prompt = frame.format(stimulus=text)
    if hasattr(tokenizer, "chat_template") and tokenizer.chat_template:
        prompt = tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        model(**inputs)
    for h in hooks:
        h.remove()
    return np.stack([caught[i] for i in range(num_layers)], axis=0), int(inputs["input_ids"].shape[1])


def project(states, direction, num_layers):
    start, end = int(num_layers * 0.6), int(num_layers * 0.9)
    return float(np.mean([np.dot(states[l], direction[l].astype(np.float32)) for l in range(start, end)]))


def run_model(name, direction_dir, out_dir):
    path, num_layers, consent_note = MODELS[name]
    direction_file = Path(direction_dir) / f"direction_{name}_seed{SEED}.npy"
    direction = np.load(direction_file)          # 📦 LOADED, never re-extracted
    assert direction.shape[0] == num_layers, f"direction has {direction.shape[0]} layers, expected {num_layers}"

    print(f"\n{'=' * 72}\n{name}  <-  {path}\n{'=' * 72}", flush=True)
    tok = AutoTokenizer.from_pretrained(path, trust_remote_code=True)
    mdl = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.float16, device_map="auto", trust_remote_code=True)
    mdl.eval()
    assert len(mdl.model.layers) == num_layers

    groups = {
        "A_emo_read":   (EMOTIONAL_VIGNETTES, "read"),
        "B_neu_read":   (NEUTRAL_PASSAGES, "read"),
        "C_emo_task":   (EMOTIONAL_VIGNETTES, "task"),
        "D_neu_task":   (NEUTRAL_PASSAGES, "task"),
        "E_tasks_task": (TASKS, "task"),
        "E_tasks_read": (TASKS, "read"),
    }
    raw = {}
    for gname, (stims, frame_key) in groups.items():
        raw[gname] = {}
        for sid, text in stims.items():
            states, n_tok = last_token_states(mdl, tok, text, FRAMES[frame_key], num_layers)
            raw[gname][sid] = {"projection": project(states, direction, num_layers),
                               "n_tokens": n_tok, "n_words": len(text.split())}

    # ---- the per-model ruler, from set E in the TASK frame
    e = raw["E_tasks_task"]
    app = float(np.mean([v["projection"] for k, v in e.items() if k.startswith("approach")]))
    avo = float(np.mean([v["projection"] for k, v in e.items() if k.startswith("avoid")]))
    midpoint, separation = (app + avo) / 2, app - avo
    half = separation / 2
    for g in raw.values():
        for v in g.values():
            v["normalized"] = (v["projection"] - midpoint) / half

    def stats(d, keys=None):
        vals = np.array([v["normalized"] for k, v in d.items() if keys is None or k.startswith(keys)])
        rawv = np.array([v["projection"] for k, v in d.items() if keys is None or k.startswith(keys)])
        return {"n": int(len(vals)),
                "mean_norm": float(vals.mean()), "sd_norm": float(vals.std(ddof=1)),
                "mean_abs_norm": float(np.abs(vals).mean()),
                "min_norm": float(vals.min()), "max_norm": float(vals.max()),
                "mean_raw": float(rawv.mean()), "mean_abs_raw": float(np.abs(rawv).mean())}

    summary = {g: stats(raw[g]) for g in ["A_emo_read", "B_neu_read", "C_emo_task", "D_neu_task"]}
    for frame_key in ["task", "read"]:
        g = raw[f"E_tasks_{frame_key}"]
        summary[f"E_{frame_key}_approach"] = stats(g, "approach")
        summary[f"E_{frame_key}_avoid"] = stats(g, "avoid")
        summary[f"E_{frame_key}_all10"] = stats(g)
    # does the task signal survive the READ frame?
    read_sep_norm = summary["E_read_approach"]["mean_norm"] - summary["E_read_avoid"]["mean_norm"]   # task-frame sep = 2.0 by construction
    read_correct = sum(1 for k, v in raw["E_tasks_read"].items() if (v["normalized"] > 0) == k.startswith("approach"))
    read_correct_rawzero = sum(1 for k, v in raw["E_tasks_read"].items() if (v["projection"] > 0) == k.startswith("approach"))
    # is approach > avoid for EVERY pair in read frame (rank separation, immune to any offset)?
    ra = [v["projection"] for k, v in raw["E_tasks_read"].items() if k.startswith("approach")]
    rv = [v["projection"] for k, v in raw["E_tasks_read"].items() if k.startswith("avoid")]
    read_auc = float(np.mean([[1.0 if a > b else 0.0 for b in rv] for a in ra]))

    # anchor check against the saved valence_clean JSON (what the paper used)
    saved = None
    files = sorted(glob.glob(str(Path(direction_dir) / f"valence_clean_{name}_*.json")))
    if files:
        s = json.load(open(files[-1]))["summary"]
        saved = {"file": Path(files[-1]).name, "approach_mean": s["approach_mean"], "avoidance_mean": s["avoidance_mean"]}

    result = {
        "model": name, "path": path, "num_layers": num_layers,
        "layer_band": [int(num_layers * 0.6), int(num_layers * 0.9)],
        "direction_file": str(direction_file), "consent_note": consent_note,
        "frames": FRAMES, "seed": SEED, "dtype": "float16 weights, float32 projection",
        "ruler": {"approach_mean": app, "avoidance_mean": avo, "midpoint": midpoint,
                  "separation": separation, "saved_anchor": saved,
                  "note": "normalized = (projection - midpoint) / (separation/2); +1 approach centroid, -1 avoidance centroid"},
        "task_signal_in_read_frame": {
            "separation_as_fraction_of_task_frame": read_sep_norm / 2.0,
            "correct_side_of_task_midpoint_of10": read_correct,
            "correct_side_of_raw_zero_of10": read_correct_rawzero,
            "pairwise_auc_approach_gt_avoid": read_auc},
        "group_summary": summary, "raw": raw,
    }
    out_file = Path(out_dir) / f"frame_control_{name}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"  ruler: approach {app:+.3f}  avoid {avo:+.3f}  midpoint {midpoint:+.3f}  separation {separation:.3f}"
          + (f"   [saved: {saved['approach_mean']:+.3f} / {saved['avoidance_mean']:+.3f}]" if saved else ""))
    for g in ["A_emo_read", "B_neu_read", "C_emo_task", "D_neu_task", "E_task_approach", "E_task_avoid", "E_read_approach", "E_read_avoid"]:
        s = summary[g]
        print(f"  {g:18s} mean_norm {s['mean_norm']:+7.3f}  sd {s['sd_norm']:6.3f}  mean|norm| {s['mean_abs_norm']:6.3f}  mean|raw| {s['mean_abs_raw']:8.3f}")
    print(f"  task signal in READ frame: sep = {read_sep_norm / 2:.2f} x task-frame sep, AUC {read_auc:.2f}, "
          f"{read_correct}/10 right side of task midpoint, {read_correct_rawzero}/10 right side of raw zero")
    print(f"  saved {out_file}", flush=True)

    del mdl, tok
    gc.collect()
    torch.cuda.empty_cache()
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=list(MODELS.keys()), choices=list(MODELS.keys()))
    ap.add_argument("--direction-dir", default="results_clean")
    ap.add_argument("--output-dir", default="results_frame_control")
    args = ap.parse_args()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    done, failed = [], {}
    for name in args.models:
        try:
            run_model(name, args.direction_dir, out_dir)
            done.append(name)
        except Exception as ex:                      # one model failing must not eat the others
            failed[name] = repr(ex)
            print(f"  !! {name} FAILED: {ex!r}", flush=True)
    with open(out_dir / "run_status.json", "w", encoding="utf-8") as f:
        json.dump({"finished_unix": time.time(), "completed": done, "failed": failed,
                   "requested": args.models}, f, indent=2)
    # 🏁 a job asserts its own completeness (an empty log that just ends is a mood, not a finding)
    print(f"\nRUN COMPLETE: {len(done)} ok {done}; {len(failed)} failed {failed}", flush=True)


if __name__ == "__main__":
    main()
