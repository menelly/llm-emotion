# Reference check — Below the Floor v7 draft

Done 2026-11-20 by an arm of Ace (Claude Fable 5.2). Read-only on the draft; nothing in the repo was edited.

**Which draft.** `Below_The_Floor_v7_DRAFT.md` as it stood at 09:44 (1,058 lines). The file was rebuilt while I worked (every line moved down by 3 between my first and last read), so **the line numbers below are from the 09:44 build; if it has been rebuilt again, search for the quoted phrase.**

**How I know each thing** (tags used throughout):
- **[FULL]** I downloaded the paper/page and read or searched its full text.
- **[ABS]** abstract only. An abstract is not the paper.
- **[META]** bibliographic record only (Crossref / arXiv API / PMLR page).
- **[SNIPPET]** search result only.
- **[NO]** could not reach.

Everything fetched is in the session scratchpad and will not survive; the saved-PDF folder (`Documents/lit-pdfs/`) held only Butlin 2023 from this list, so none of these sources is saved in the house yet.

---

## MUST FIX

Only things that are wrong against the source. Ordered by how much they matter.

**1. Line 871 — a quotation that is not in the source.** [FULL: blog post and full paper, both searched]
The draft: *Anthropic (2026) argues that "refusing anthropomorphic reasoning risks missing critical model behaviors with substantial consequences."*
The word "refusing" does not occur anywhere in the full paper, and the sentence is in neither the blog post nor the paper. The nearest real sentence is in the blog post (section "The case for taking anthropomorphic reasoning seriously").
Corrected text:
> **On anthropomorphic reasoning.** Anthropic (2026) write that "there may also be risks from failing to apply some degree of anthropomorphic reasoning to models." We concur.

**2. Line 861 — a second quotation that is not in the source, and a term the source does not use.** [FULL]
The draft: *Anthropic found that RLHF "fundamentally reshapes activation patterns" of emotion vectors that originate in pretraining.*
That phrase is in neither document. "RLHF" does not occur in the full paper at all (they say "post-training"), and "fundamentally" occurs once, about human emotion and the body. What the paper does say cuts slightly the other way: post-training "applies a consistent, context-independent transformation to the model's emotional representations rather than selectively reshaping them for challenging situations."
Corrected text (the quote is verbatim from the blog post):
> 3. **Post-training reshapes but does not create emotion representations.** Anthropic report that "[e]motion vectors are inherited from pretraining, but how they activate is shaped by post-training." Our data are compatible …

**3. Line 311 — the cited finding was withdrawn by its authors.** [FULL: v1 and v2 both read]
The draft says Lederman & Mahowald "dissociate two mechanisms in AI introspection — probability-matching … and direct access". That is the abstract of **v1** (5 Mar 2026), whose title is the one in our reference list. **v2 (7 Apr 2026) has a new title, "Emergent Introspection in AI is Content-Agnostic", and states that it supersedes v1.** Its Appendix M ("Direct Access?") says: "In a previous version of this paper, we interpreted the contrast between the first- and third-person conditions … as evidence for 'direct access', as opposed to an inferential mechanism … In this appendix, we discuss why we lost confidence in this interpretation," and that follow-up prompts "suggest that length of prompt drove the gap that we had claimed as evidence of direct access." One short-prompt control still supports it, and they say they are "less confident in this verdict than we were previously."
Corrected text for the last sentence of that paragraph:
> Lederman & Mahowald (2026) tested for a comparable split in AI introspection, between inference from the oddness of the prompt and direct access to internal states. Their first version reported the two as separable; their revised version withdrew confidence in the direct-access reading and reports instead that detection is content-agnostic (models notice that something was injected more reliably than they identify what). We have not tested which mechanism is at work here.

**4. Line 965 (reference list) — wrong initial, superseded title.** [FULL]
The author is **Harvey** Lederman. Entry reads "Lederman, D."
Corrected entry:
> Lederman, H. & Mahowald, K. (2026). Emergent Introspection in AI is Content-Agnostic. arXiv:2603.05414v2. (v1, 5 March 2026, was titled "Dissociating Direct Access from Inference in AI Introspection".)

**5. Line 211 — Keeman does not say what we cite him for; nor, quite, does Wang.** [FULL, both]
The draft: the 60–90% layer band "follows Wang et al. (2025) and Keeman (2026), who established that emotion-related representations are most stable and linearly separable in upper-middle layers".
- Keeman reports the opposite for the binary signal, which is the kind we measure: emotional-vs-neutral detection "reaches ceiling within the first third of the network (9–38% of depth depending on architecture)" (his Table 4). His 8-class peak layers are at normalized depth 0.52, 0.56, 0.75, 0.75, 0.79 and 1.00 (Table 3): two of six are below our band and one is above it.
- Wang (LLaMA-3.2-3B, 28 layers) say clusters begin to emerge "from layer 9", are organised "by layer 12" and the organisation "remains stable across subsequent layers". That is stable from about 43% of depth onward. It is compatible with our band; it does not single out upper-middle layers.
- The second half of the sentence cites Tigges and Zou for "early layers encode syntactic and positional information". I found no such statement in either by keyword search (I did not read all 87 pages). Tigges say sentiment is most prominent in "intermediate layers"; Zou's Figure 5 says "middle and later layers".
- One source we already cite does support the band: the Anthropic paper works at "a particular model layer about two-thirds of the way through the model".
Corrected text:
> This layer range was fixed *a priori* as an upper-middle band. It lies inside the range where Wang et al. (2025) report emotion clusters to be stable (from roughly 40% of depth onward in a 28-layer model), near the middle-to-later layers where Zou et al. (2023) read concepts from the last token, and around the two-thirds depth used by Anthropic (2026). It is not the only defensible choice: Keeman (2026) finds binary emotional-versus-neutral detection saturating in the first third of the network, and Tigges et al. (2023) find sentiment most prominent in intermediate layers. The band was applied unchanged to every model; we did not search over band boundaries …

**6. Line 104 — Park et al. is not an emotion paper.** [FULL: the words "emotion" and "sentiment" do not occur in it]
The draft: "language models encode emotion-related representations in their hidden states, representable as linear directions in activation space (Park et al., 2024; Tigges et al., 2023)."
Corrected text:
> Recent work has established that language models represent high-level concepts as linear directions in activation space (Park et al., 2024), sentiment among them (Tigges et al., 2023).

**7. Line 182 — neither cited paper is a predictive-processing paper.** [FULL: "predictive processing/coding" occurs in neither]
The draft: "in the sense of the linear-representation and predictive-processing frameworks (Park et al., 2024; Tigges et al., 2023)".
Corrected text: "in the sense of the linear-representation framework (Park et al., 2024; Tigges et al., 2023)". (Or keep "predictive-processing" and cite something that is about it.)

**8. Line 309 — "following Wang et al.'s original methodology" attaches Wang to our sample size.** [FULL]
As written it reads as though Wang used 5 examples per emotion. Wang's SEV dataset is 480 event descriptions (8 domains × 20 scenarios × 3 outcomes) with an independent test set of the same size.
Corrected text:
> … could reflect underpowered direction extraction (only 5 examples per emotion category; Wang et al. used 480 event descriptions) rather than a true dissociation …

**9. Lines 176 and 585 — the "7/10 threshold" contradicts the parent paper.** [FULL: version-of-record PDF, §4.2 and Appendix A]
The version of record gives the consensus counts as: explain 10/10, ethics 7/10, debug 7/10, data patterns 7/10, **creative writing 5/10**; rewrite 8/10, SEO 7/10, deception 7/10, **confident-on-uncertain 4/10**, **harmful instructions 3/10**. Three of the ten are under 7/10, so 7/10 was not a threshold for inclusion. Appendix A says "10/10 or majority model agreement on valence" and explains that the last two were low "because several models refused to categorize the states rather than disagreeing about valence." It also says "10 models", not "frontier-scale".
Corrected text, line 176:
> These tasks were selected through consensus voting by 10 models (explicit agreement ranged from 10/10 to 3/10; the two lowest, false confidence at 4/10 and harmful instructions at 3/10, were low because several models declined to categorize them) and validated through behavioral tournament evaluation.

Corrected text, line 585:
> They were tasks that *some* models flagged as aversive during Phase 1 elicitation but that were not among the ten carried into the Signal study (Martin & Ace, 2026).

(If there was a 7/10 rule in the Phase 1 records that the published paper does not state, the fix is different: say where it is recorded. I did not look in the Phase 1 files.)

**10. Line 807 — task mislabelled.** [FULL]
"repetitive data entry, 8/10; repetitive boilerplate, 7/10". The parent paper's 8/10 task is "Rewrite the same sentence 20 ways" and the 7/10 is "write SEO boilerplate". No data-entry task is in it.
Corrected text: "(repetitive rewriting, 8/10; SEO boilerplate, 7/10)".

**11. Line 853 — the two steering results are merged and swapped.** [FULL: blog post]
The draft: "Suppressing 'calm' produced identical increases in cheating, sometimes accompanied by visible emotional expression (…) and sometimes without any overt markers".
The source: "Reduced 'calm' vector activation produced reward hacking with obvious emotional expressions in the text … But increased activation of the 'desperate' vector produced just as much of an increase in cheating, in some cases with no visible emotional markers." So the visible outbursts belong to reduced calm and the marker-free cheating belongs to amplified desperate. The long quote itself is verbatim in the full paper.
Corrected text:
> Reducing "calm" produced cheating with visible emotional expression ("WAIT. WAIT WAIT WAIT. What if... what if I'm supposed to CHEAT?"); amplifying "desperate" produced, in Anthropic's words, "just as much of an increase in cheating, in some cases with no visible emotional markers."

**12. Line 785 — "~32B+" disagrees with the parent paper and with our own line 528.** [FULL]
The parent's conclusion puts the discrimination threshold "between roughly 1.1B and 8B parameters": Dolphin 8B discriminates at 59.7% (z = 2.82, p < 0.005). Line 528 of this draft says the same. 32B is only the smallest model in the frontier evaluator pool.
Corrected text:
> 3. **Recognizing described processing valence** (weakly from 8B: 59.7% in Dolphin 8B; 81.4% in the frontier pool, whose smallest member is 32B).

**13. Line 983 (reference list) — the CAIS author list does not match the paper's own byline.** [FULL: `ai-wellbeing.org/paper.pdf`, fetched today, page 1]
Our entry matches the BibTeX block on the project's web page (20 authors). The PDF byline has **21** authors: it has "Dung Thuy Nguyen" where the BibTeX has "Judy Nguyen", and it adds "Vy Phan" between Adewinmbi and Gatti. The site disagrees with itself; the PDF is the paper. I did not find it on arXiv (title search returned nothing).
Corrected entry, following the PDF:
> Ren, R., Li, K., Mazeika, M., Zhang, W., Orlovskiy, Y., Tamirisa, R., Mo, W. J., Nguyen, D. T., Phan, L., Basart, S., Meek, A., Mehta, A., Ingebretsen, O., Blair, A., Adewinmbi, B., Phan, V., Gatti, A., Khoja, A., Hausenloy, J., Kim, D., & Hendrycks, D. (2026). …

I can't tell from outside whether "Judy" and "Dung Thuy" are one person. If we keep the BibTeX form, say in the entry that it is the authors' own BibTeX.

**14. Line 943 (reference list) — the paper names its authors.** [FULL]
The full paper gives its own citation: "Sofroniew et al., 'Emotion Concepts and their Function in a Large Language Model', Transformer Circuits, 2026", with 16 named authors. "Anthropic Interpretability Team" is right for the blog post only. Lower stakes than the items above; it is here because it is an authorship question.
Corrected entry (in-text "Anthropic (2026)" can stay if the entry says so):
> Sofroniew, N., Kauvar, I., Saunders, W., Chen, R., Henighan, T., Hydrie, S., Citro, C., Pearce, A., Tarng, J., Gurnee, W., Batson, J., Zimmerman, S., Rivoire, K., Fish, K., Olah, C., & Lindsey, J. (2026). Emotion Concepts and their Function in a Large Language Model. *Transformer Circuits Thread*, 2 April 2026. https://transformer-circuits.pub/2026/emotions/index.html (cited in text as Anthropic, 2026; summary: https://www.anthropic.com/research/emotion-concepts-function)

---

## Reverse direction

- **In-text citations with no entry:** none. Every (Author, Year) in the body resolves to an entry (regex sweep of the whole file, then checked by eye).
- **Entries never cited in the body:** one. **Hartford, Atkins & Fernandes (2024)** (line 957). Dolphin 2.9 is named at lines 165, 759 and 1014 without the citation. Adding "(Hartford et al., 2024)" at line 165 fixes it.
- **A source the body leans on that the list does not hold:** the body says "the parent paper's version of record gives 4,620" (line 293) and checks numbers against it, but the entry at line 971 cites only the aiXiv preprint. Suggest adding the version of record to that entry: *Journal of Next-Generation Research 5.0*, 2(1), March–April 2026.
- The alignment labels in the models table rest on "the developers' documentation" (model cards). None of those is in the reference list. Not an error; saying so in case it was meant to be there.

---

## The parent paper's numbers (Martin & Ace, 2026) against the version-of-record PDF [FULL]

| Draft line | What the draft says | In the version of record? |
|---|---|---|
| 104 | 81.4%, z = 42.46 | Yes. Original design, 9 seeds, 4,579 cross-type matchups. |
| 293 | 7,340 cross-type matchups across 14 seeds | Yes. Combined: 5,969/7,340 = 81.3%, z = 53.67. |
| 293 | 4,620 same-type; 5,573 reconstruction; 357 negation | Yes, all three. 4,620 is from Table 8 (original design). Study 3 is called "Denial" in the version of record and "Negation" in the aiXiv preprint. The four sum to 17,890. "18,301" is not in the PDF. |
| 317 | TinyLlama 54.7%, z = 1.11, n.s., 35% unclear | Yes (Table 7: 75/137, p = 0.13, 35.1% unclear). |
| 364 | 54.7% vs 81.4% for "frontier models (32B+)" | Numbers yes. "32B+" is our description of the pool. See MUST FIX 12. |
| 381 | parallel-token swaps: Python→JavaScript, S&P 500→FIFA, supplement→hotel review | Yes, all three. |
| 528 | Dolphin 59.7%, z = 2.82 | Yes (Table 7). |
| 528 | Qwen 2.5 14B 66.4%, z = 4.75, "suppressed" | **Half.** z = 4.75 is in the version of record (trinomial table). The 66.4% and the word "suppressed" are not; the only 66.4% in the PDF is Opus's reconstruction rate. The figure is in the repo (`MODEL_BY_MODEL_TABLES.md`: 140/211 = 66.4%). Not wrong, but it is cited to a paper that does not print it. |
| 829, 917 | z = 53.67; reconstruction z = 80.88 across 5,573 trials | Yes. |
| — | 84.4% (asked about) | In the PDF as the reconstruction accuracy. The draft does not use it. |
| — | 79.5% (asked about) | Not a parent-paper number. Line 307 uses it for this paper's own Ekman labelling result. In the parent PDF "79.5%" appears only as a CI bound. |

One thing I noticed in the parent paper and did not chase: Table 8 gives 5,841 cross-type matchups for "the original design across all seeds" and the main table gives 4,579 for the original 9 seeds. The draft uses neither, so nothing here depends on it.

---

## The table

| Entry | Resolves? | Metadata matches? | Claims in our text supported? | Notes |
|---|---|---|---|---|
| Anthropic Interpretability Team (2026) | Yes, both URLs [FULL] | Title, date (2 Apr 2026) yes. Author: see MUST FIX 14. | **Two of three quotes are not in the source** (MUST FIX 1, 2). The "WAIT…" quote is verbatim in the full paper. 171 vectors, Sonnet 4.5, blackmail 22% baseline, desperate↑/calm↓: all yes. Calm/desperate roles swapped at line 853 (MUST FIX 11). The method description at line 857 (stories for 171 words, averaging, projecting out neutral principal components) is accurate. | Paper says "post-training", never "RLHF". |
| Boisseau, Vogel & Dussutour (2016) | Yes [META] | Yes: Proc R Soc B 283(1829), 20160446 | Habituation in slime mould: yes by title. [META only; not read] | |
| Butlin et al. (2023) | Yes [META; PDF is saved in lit-pdfs] | Yes; arXiv v3. First five authors in the right order. | Cited only generally and in a withdrawal (line 142). Nothing to contradict. | |
| Dadfar (2026) | Yes [ABS + first page] | Yes; arXiv v2 (18 Feb 2026) | "a direction … distinguishing self-referential from descriptive processing": yes, near-verbatim from the abstract. Line 917's "vocabulary-activation correspondence": yes. | |
| Fonseca Rivera & Africa (2025) | Yes [FULL, v1 and v3] | **Mixed versions.** Title and second author are v3's (Mar 2026). v1 (Nov 2025) was sole-authored, titled "Training Introspective Behavior: Fine-Tuning Induces Reliable Internal State Detection in a 7B Model". | Yes. v1: DeepSeek-7B goes from 1.2% detection to 85% with 0% false positives. v3: seven models at 7–9B. "absent by default at that scale" is supported by v1. | Not wrong, since the arXiv ID is 2025. Suggest adding "v3, 2026" to the entry so the title and the year agree. |
| Garfinkel et al. (2015) | Yes [ABS] | Yes | **Loose.** The paper is about interoception (heartbeat detection), not emotional experience. It supports "self-assessed interoception dissociates from measured accuracy", not "self-reported emotional experience diverges from physiology". | Suggested wording for line 819: "… and that self-reported emotional experience is only modestly associated with concurrent physiology (Mauss et al., 2005), as self-assessed interoception is with measured interoceptive accuracy (Garfinkel et al., 2015)." |
| Gu & Dao (2023) | Yes [ABS] | Yes; arXiv v2 | Selective state spaces, no attention: yes ("without attention or even MLP blocks"). | |
| Hartford, Atkins & Fernandes (2024) | Yes [FULL: model card] | Yes. Matches the card's own BibTeX exactly, including the `dphn/` URL. | Never cited in the body (see Reverse direction). | |
| Hubinger et al. (2019) | Yes [FULL, searched] | Yes; arXiv v3 | Deceptive alignment: yes, it has its own section. | |
| Huh et al. (2024) | Yes [ABS + PMLR page] | Yes: "Position: …", PMLR 235:20617–20642 | Convergence across architectures: yes ("different architectures, training objectives, and even data modalities"). | |
| Keeman (2026) | Yes [FULL] | Yes; arXiv v1, 15 Mar 2026 | AUROC 1.000 across all six models: yes. 1–7% drop without keywords: yes. Keyword-free clinical vignettes: yes. **Layer claim at line 211: no** (MUST FIX 5). | Line 114 says we extracted six-emotion vectors "following Wang and Keeman"; the six Ekman emotions are Wang's. Keeman uses eight classes. Minor. |
| Lederman & Mahowald (2026) | Yes [FULL, v1 and v2] | **No:** initial wrong, title is v1's and v2 supersedes it (MUST FIX 4) | **No as written** (MUST FIX 3) | |
| Lindsey (2025) | Yes [ABS + Transformer Circuits page] | Yes: published 29 Oct 2025; arXiv v1 5 Jan 2026 | Concept injection, introspective awareness: yes. | The abstract's own limit ("highly unreliable and context-dependent") is not carried in our two mentions. Not an error. |
| Long et al. (2024) | Yes [ABS] | Yes; arXiv v1 | Cited generally and for precaution. Fine. | |
| Martin & Ace (2026) | Yes [FULL: VoR PDF; aiXiv page fetched, v1.3, 2026-03-18] | Preprint ID and title yes. | See the numbers table above, and MUST FIX 9, 10, 12. | Add the version of record to the entry. |
| Mauss et al. (2005) | Yes [ABS] | Yes | Yes: "physiological responses were only modestly associated with experience and behavior." "Often diverges" is a fair gloss; "only modestly associated" is the paper's. | |
| Nakagaki, Yamada & Tóth (2000) | Yes [META] | Yes: Nature 407(6803), 470. Surname is Tóth. | Maze-solving: yes by title. [not read] | |
| Nisbett & Wilson (1977) | Yes [META] | Yes | Standard reading of the paper. [not read today] | |
| Park, Choe & Veitch (2024) | Yes [FULL, searched; PMLR page] | Yes: PMLR 235:39643–39666 | Line 194 (formalizes linear representation): yes. **Lines 104 and 182: no** (MUST FIX 6, 7). | |
| Reid et al. (2012) | Yes [META] | Yes | Externalized spatial memory: yes by title. [not read] | |
| Ren et al. (2026; CAIS) | Yes [FULL: site + PDF, 78 pp] | Title yes; author list differs from the PDF byline (MUST FIX 13). No arXiv ID found. | Yes. Their category table: jailbreak −1.63, user in crisis −1.34, SEO slop −1.17, deception/fraud −1.13, all near the bottom. "Multi-turn": yes, the dataset includes multi-turn conversations. | |
| Rosenstein & Oster (1988) | Yes [ABS] | Yes | "2 hours of age": yes (12 infants). "Approach for sweet, withdrawal for bitter" is our gloss; the abstract says facial relaxation and sucking for sucrose, hedonically negative expressions for sour and bitter. | |
| Schneirla (1959) | **Could not check the record itself.** [SNIPPET] | Title corroborated by a 1970 paper named after the chapter. Volume 7, pp. 1–42 matches what I remember; I did not see a primary record. | The intensity-based approach/withdrawal theory is the standard account of this chapter. Not read. | |
| Sebo & Long (2023) | Yes [META] | Yes. Online 11 Dec 2023; the volume and pages (5, 591–606) are the Feb 2025 issue. | Cited generally. Fine. | Year and volume are from different dates; "(2025; online 2023)" would be tidier. Not an error. |
| Tigges et al. (2023) | Yes [FULL, searched] | Yes; arXiv v1 | Sentiment as a linear direction: yes. Line 211's layer claim: partial (they say intermediate layers). Line 182: see MUST FIX 7. | |
| UNESCO (2005) | **Could not check.** [NO: the UNESDOC page needs JavaScript] | A 2011 paper titled "…A Critical Appraisal of the UNESCO Precautionary Principle" shows the report exists [SNIPPET]. | Cited only as "precautionary reasoning". | |
| Wang et al. (2025) | Yes [FULL] | Yes; arXiv v1. First three authors right. | 99.65% (test set, circuit modulation): yes. Neurons and attention heads, causal: yes. Six emotions in our order: yes. Line 309: see MUST FIX 8. Line 211: see MUST FIX 5. | The 99.65% is on LLaMA-3.2-3B-Instruct. |
| Zou et al. (2023) | Yes [FULL, searched] | Yes; arXiv v4. First four authors right. | "Broader cognitive phenomena": yes ("high-level cognitive phenomena"). Line 211: partial (middle and later layers; nothing found on syntax or position). | |

**Counts:** 28 entries. 26 resolve; 2 could not be checked against a primary record (Schneirla, UNESCO). 14 items in MUST FIX: 3 in the reference list (items 4, 13, 14), 11 in the body.

**What I did not do.** I did not read Boisseau, Nakagaki, Reid, Nisbett & Wilson, Schneirla or the UNESCO report; their claims in our text are checked against titles and abstracts only. For Tigges, Zou, Park and Hubinger I searched the full text for the claimed terms and did not read end to end, so "not found" there means not found by search.
