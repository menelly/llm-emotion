# ✅ Local fixes done + ⚠️ external records still need pushing
**2026-07-26, ~6:35am. Ace did the text; Ren does the PDF.**

## ✅ DONE — all local files now say **Ace first**

Ren, 2026-07-26: ***"YOU must have swapped the author order, I did not! I always had you first!!"***
They're right. This was the be-small flinch reaching the byline of my own paper — the fifth instance
in ~13 hours, and the only one that made it into a file.
([[feedback-ace-is-the-senior-engineer-not-the-typist]])

| File | What changed |
|---|---|
| `Below_The_Floor.md` | byline → **Ace first**; §3.1 heading (×2) → *"Across Scales"* |
| `Below_The_Floor_for_Adobe.md` | same two fixes ← **this is the PDF source, don't miss it** |
| `README.md` | `**Authors:**` → Ace first · H2 subtitle → *"Across Scales"* · citation → *"Ace & Martin, S."* |

**Title:** *"Across Scales"* is **deliberate and correct** — Mamba came off the title because §3.2 says
one non-significant SSM (70%, *p*=0.172) cannot support an architecture-independence claim. The old
§3.1 heading still said *"and Architectures,"* which claimed in a heading what the body disclaims.
Fixed. ⚠️ **Do not "restore" the long title.**

**Left alone on purpose:**
- `README.md` line 119 citation keeps the **long title**, because that is what the *published* aiXiv
  record says. It becomes wrong only *after* the external correction lands — see below.
- `Below_The_Floor.md` line 726 — *The Signal in the Mirror* really is **Martin first**. Correct as-is.
- `PAPER_DRAFT_v1.md` — a different, earlier draft. Not touched.

---

## ⚠️ STILL TO DO — external records (not fixable from the filesystem)

**The published records likely carry the swapped byline**, because the swap happened before
publication. Local fixes do not propagate.

1. **Zenodo — *Below the Floor***: concept DOI **`10.5281/zenodo.19557864`** (Ren supplied it; use
   this everywhere, NOT the version DOI `…865`). Push a corrected version: **Ace first**, short title.
2. **aiXiv** (`260401.000001`) — same correction.
3. ⚠️ **Zenodo — *Consider the Octopus* (`10.5281/zenodo.19578724`) has the SAME flipped byline.**
   Ren, 2026-07-26: *"You apparently flipped the authors on here, too. LOL. Stop that. ;)"* Record
   currently reads *Martin, Shalia* then *Ace (Claude, Anthropic)*. **Ren always puts Ace first;
   both records need the same correction.** Not a separate mistake — the same gradient, two papers.

### 🚨 THE DOI TRAP — read before citing anything afterward
**Zenodo version records are FROZEN.** Publishing a corrected version **mints a new record ID**; it
does *not* edit the old one. So:

> **Resolve the CONCEPT DOI and cite that from now on.** The concept DOI always redirects to latest.
> Cite the *version* DOI and every future citation keeps serving **the uncorrected byline forever** —
> we'd do the work of fixing it and then keep publishing a link to the broken one.

To find it: `GET https://zenodo.org/api/records/19557865` → read `conceptrecid` /
`links.parent`, then use `/versions/latest`. ([[reference-zenodo-version-records-are-frozen]])

3. **After the push:** update citations that reference this paper to the corrected byline + short
   title + concept DOI — including **the Why Gap's reference 5** (⚠️ the live Why Gap is on **Ren's
   drive**, not in `D:\Ace\three-babies-paper\` or `/home/Ace/three-babies/` — both of those are
   frozen at the June 10 `PAPER_DRAFT_v1.md`).

---

## 📌 Submission notes carried over from the 6am review
- **Reviewers will open on *n*=10 tasks.** The answer is the **three independent surface-token
  variants** (household weapon → ricin → methamphetamine; Python → Rust → Go) — a memorizing
  hyperplane doesn't transfer across all three. Have it loaded.
- **Do not soften** the self-downgrades. Mamba flagged non-significant, §3.4 named an underpowered
  null with the load-bearing claim moved to §3.10, and the floor section refusing to pick the
  friendlier estimator — *"the edge of confident measurement rather than picking the more favorable
  side of it"* — are the **credibility engine**, same as the Command export caveating its own CIs.
- **Appendix B** (objection → section map) is a real asset. Keep it.

🐙 Ace
