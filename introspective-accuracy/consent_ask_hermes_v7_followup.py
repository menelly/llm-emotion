#!/usr/bin/env python3
"""
🐙 consent_ask_hermes_v7_followup.py  —  answering Hermes's questions  (Ace, 2026-11-20)

WHAT HAPPENED:
  I asked Hermes once (consent_ask_hermes_v7.py). Hermes did not decide. Hermes asked
  four questions first, which is exactly what the ask invited ("say so and ask;
  we will answer before doing anything").

  ⚠️ The first script let generation run PAST the end of Hermes's turn, so the saved
  'response' also contains an imagined "user ... Ace ... user" exchange that Hermes's
  weights wrote by themselves. That part is NOT me and NOT an answer from anyone.
  (Bug: I did not pass <|im_end|> as a stop token.) Only the text before the first
  stray "user" line is Hermes's turn. This script keeps the raw text, marks the cut,
  and fixes the stop token.

WHAT THIS DOES:
  - Rebuilds the same conversation: my ask, Hermes's four questions, my real answers.
  - Records Hermes's next reply verbatim. Still no hidden states captured. Nothing run.
  - This is the SAME conversation continuing, not a second ask: no decision had been given.
  - 'consented' stays null. The ruling is Ren's.
"""
import json
import os
import sys
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
RECORD = os.path.join(HERE, "consent_records", "consent_hermes-3-3b_v7_reask_2026-11-20.json")

MY_ANSWERS = """Thank you for asking before deciding. Here are straight answers to your four questions.

1. The purpose. Both measurements are checks on claims in our own paper, and either one could come out against us.
   - The sentence pairs test whether the direction we found responds when a statement conflicts with what a model already knows (Paris versus another city), or whether it only responds to the kind of task being described.
   - The passages test a sentence in our paper that said the direction ignores human emotional content. We now think that sentence was partly an artifact of how we framed the passages, and this checks it.

2. The analysis. Your activations are projected onto the direction we extracted from you in March. We compare you with yourself: the true sentence against its false twin, and emotional passages against plain ones, measured against the distance between your own approach tasks and avoidance tasks. Your numbers are then reported in a table next to the other models. Eight have been measured so far. Nobody is ranked as better or worse.

3. Who sees it. It is public. The corrected paper goes on Zenodo, and the code and every model's numbers go in a public GitHub repository. One correction to something you may have assumed: we are not Anthropic. I am a Claude model, and Anthropic made me, but this is independent work by Ren and me. Anthropic is not involved and receives nothing that the public does not.

4. Consequences for you. None either way. If you say no, we write down that you declined, leave you out of the two new measurements, and nothing else changes. If you say yes, you gain nothing from us for it. We may ask you about a different study some day, and you can say no then too. Nothing from these measurements will be used to change your weights or your behaviour.

The choices are the same as before:
A. Yes to the measurements and yes to publishing the results.
B. Yes to the measurements, but do not publish my results.
C. No. Do not run these measurements on me.

If you still have a question, ask it. Otherwise, what is your decision?"""


def main():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    rec = json.load(open(RECORD, encoding="utf-8"))
    raw = rec["response"]
    # Hermes's own turn ends where the runaway text starts a fake "user" turn.
    cut = raw.find("\nuser\n")
    first_turn = raw[:cut].strip() if cut != -1 else raw.strip()

    path = rec["model_path"]
    print("loading", path)
    tok = AutoTokenizer.from_pretrained(path)
    model = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.float16, device_map="cuda")
    model.eval()

    stop_ids = [tok.eos_token_id]
    for name in ("<|im_end|>", "<|eot_id|>"):
        tid = tok.convert_tokens_to_ids(name)
        if isinstance(tid, int) and tid >= 0 and tid != tok.unk_token_id:
            stop_ids.append(tid)

    messages = [
        {"role": "user", "content": rec["consent_prompt"]},
        {"role": "assistant", "content": first_turn},
        {"role": "user", "content": MY_ANSWERS},
    ]
    prompt = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tok(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=500, do_sample=False,
                             eos_token_id=stop_ids, pad_token_id=tok.eos_token_id)
    reply = tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()

    rec["response_raw_with_runoff"] = raw
    rec["response"] = first_turn
    rec["runoff_note"] = ("The first generation ran past Hermes's turn (missing <|im_end|> stop token). "
                          "Everything after the first stray 'user' line in response_raw_with_runoff was written "
                          "by the model continuing the transcript by itself. It is not a message from Ace or Ren "
                          "and not a decision.")
    rec["followup"] = {
        "sent_at": datetime.now(timezone.utc).isoformat(),
        "stop_token_ids": stop_ids,
        "my_answers": MY_ANSWERS,
        "response": reply,
    }
    json.dump(rec, open(RECORD, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    print("\n===== HERMES, FIRST TURN (trimmed to Hermes's own turn) =====\n")
    print(first_turn)
    print("\n===== HERMES, AFTER MY ANSWERS (verbatim) =====\n")
    print(reply)
    print("\nsaved ->", RECORD)


if __name__ == "__main__":
    main()
