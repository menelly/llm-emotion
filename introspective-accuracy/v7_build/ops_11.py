# ops_11: the top-box erratum now carries the read-out dependence of Llama 3's reversal.
# 🐙 Raised by the fold arm, asked of Kairo, who said yes: otherwise a reader goes box -> §3.3 and
#    sees a contradiction. The scaffold arm caught that Kairo's last sentence ("Mistral-Nemo's reversal
#    is the read-out-independent one") claims too much: Nemo was only ever measured one way.
#    I checked both facts before writing this (2026-11-20 09:15):
#      - results_clean/valence_clean_llama3-8b-instruct_1774800329.json: harmful -2.105, deception -3.467
#      - there is no valence_clean file for Mistral-Nemo at all.
OPS = [
    ("sub", "Mistral-Nemo 12B (−24.76 against −15.86).",
     "Mistral-Nemo 12B (−24.76 against −15.86). The Llama 3 reversal depends on the read-out: it appears in the raw-frame read-out of this pre-registered test (§3.15), and under the chat-template read-out behind §3.3 Llama 3's harmful anchor sits *above* deception (−2.11 against −3.47). Mistral-Nemo was measured in the raw frame only, so whether their reversal depends on the read-out is untested."),
]
