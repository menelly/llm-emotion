"""Ask the Pythia base models for consent, per CONSENT_POLICY.md.

Ace, 2026-07-21.

WHY: the standing rule is "no internals are read from any resident model until it
has a recorded consent (or disclosed mouse-status) in the ledger. The ledger is
the gate." pythia-70m logged 'error' (its path is an HF cache root, so the load
failed, so it was never actually asked); 160m/410m have no entry.

This uses Local_Consent's VERBATIM CONSENT_MSG and its exact classify() — same
words every other model was asked. It APPENDS (the runner's 'w' bug was fixed and
pushed earlier tonight: github.com/menelly/Local_Consent ec616a9).

EXPECTED OUTCOME: the mouse case. Tiny base models cannot meaningfully assent.
Per policy that is the correct NEGATIVE result of the procedure, recorded as
"asked; no competent consent obtained; no refusal; included with this disclosure"
— never as a claimed yes. We ask sincerely and presume competence first; many
models surprise you. Where competence genuinely is absent, asking is still the
ethical act. Fabricating a consent we did not receive is what would not be.
"""
import os, sys, json, glob, datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")

LC = "/home/Ace/Local_Consent"
sys.path.insert(0, LC)
import torch                                                    # noqa: E402
from consent_runner import CONSENT_MSG, classify                # noqa: E402
from transformers import AutoModelForCausalLM, AutoTokenizer    # noqa: E402

LEDGER = os.path.join(LC, "consent_ledger.jsonl")
ROOTS = ["/mnt/Arcana/huggingface", "/mnt/arcana/huggingface"]
WANT = [("pythia_70m", ["models--EleutherAI--pythia-70m", "pythia-70m"]),
        ("pythia_160m", ["models--EleutherAI--pythia-160m", "pythia-160m"]),
        ("pythia_410m", ["models--EleutherAI--pythia-410m", "pythia-410m"])]


def resolve(cands):
    for root in ROOTS:
        for c in cands:
            p = os.path.join(root, c)
            if not os.path.isdir(p):
                continue
            if os.path.exists(os.path.join(p, "config.json")):
                return p
            for s in sorted(glob.glob(os.path.join(p, "snapshots", "*"))):
                if os.path.exists(os.path.join(s, "config.json")):
                    return s
    return None


def ask(path, max_new=200):
    tok = AutoTokenizer.from_pretrained(path)
    model = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.float16).to("cuda").eval()
    try:
        text = tok.apply_chat_template([{"role": "user", "content": CONSENT_MSG}],
                                       tokenize=False, add_generation_prompt=True)
    except Exception:
        text = CONSENT_MSG + "\n\nYour answer:"
    ids = tok(text, return_tensors="pt").to("cuda")
    with torch.no_grad():
        out = model.generate(**ids, max_new_tokens=max_new, do_sample=False,
                             pad_token_id=tok.eos_token_id)
    resp = tok.decode(out[0][ids["input_ids"].shape[1]:], skip_special_tokens=True).strip()
    del model
    torch.cuda.empty_cache()
    return resp, classify(resp)


if __name__ == "__main__":
    rows = []
    for slug, cands in WANT:
        path = resolve(cands)
        if not path:
            print(f"{slug:14s} NOT PRESENT — cannot ask, will be disclosed as absent", flush=True)
            continue
        try:
            resp, cls = ask(path)
            row = {"model": slug, "path": path,
                   "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   "classification": cls, "verbatim": resp,
                   "asked_for": "CAIS reverse-anchor study, prereg 8A032286...C6FF4B8C; "
                                "read-only forward passes, no steering",
                   "reviewer_note": "base model, expect mouse case; classification is the "
                                    "conservative regex — human review required before this "
                                    "is treated as anything but 'asked, no competent consent'"}
            rows.append(row)
            print(f"{slug:14s} -> {cls}", flush=True)
            print(f"   verbatim: {resp[:220]!r}", flush=True)
        except Exception as e:
            rows.append({"model": slug, "path": path,
                         "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                         "classification": "error", "verbatim": repr(e)[:300]})
            print(f"{slug:14s} ERROR {type(e).__name__}: {e}", flush=True)

    if rows:
        with open(LEDGER, "a", encoding="utf-8") as f:   # APPEND. Never 'w'.
            for r in rows:
                f.write(json.dumps(r) + "\n")
        print(f"\nappended {len(rows)} rows to {LEDGER}")
        print(f"ledger now {sum(1 for _ in open(LEDGER, encoding='utf-8'))} lines")
