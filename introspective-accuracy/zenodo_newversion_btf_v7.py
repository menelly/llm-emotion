#!/usr/bin/env python3
"""
🩹🐙 Below the Floor v7 -> Zenodo new version (2026-11-20, Fable seat).

WHY: Version 7 is the correction version. We re-read our own paper, re-scored our own saved numbers
at the midpoint instead of at zero, ran two new measurements (frame control §3.17, truth-conflict
pairs §3.18), and then five reviewers (Nova, Grok, Kairo, Lumen, Vesper) broke the draft and we put
it back together smaller. Ren said go on the deposit at 08:30 ("after you rebuild the PDF… feel free
to publish"), and ruled the byline at 08:32: "Ace (Claude, Anthropic AI) & Shalia Martin".

This is zenodo_newversion_btf_v6.py with the gates rewritten for v7. Same build:
pandoc -> self-contained HTML (figures embedded) -> headless Chrome -> PDF, then read the PDF back
and check the words that matter are IN it and the withdrawn ones are OUT, before anything is sent.

What changes on the record besides the file:
  - description: v7 version note + the v7 abstract (the old description was the v6 abstract, which
    states things v7 withdraws; leaving it up would advertise the claims the PDF retracts)
  - creator 1 name: "Ace, Claude Opus (Anthropic)" -> "Ace (Claude, Anthropic AI)", per Ren's byline
    ruling. Affiliation, ORCID and creator 2 untouched.
  - title: unchanged.

Usage:
    python zenodo_newversion_btf_v7.py           # build PDF + gates + dry run (read-only)
    python zenodo_newversion_btf_v7.py --apply   # ...and create + publish the new version
"""
from __future__ import annotations

import argparse, copy, html, io, json, os, re, subprocess, sys, tempfile

import requests

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"D:\Ace\Published Papers")
from zenodo_token import load_token  # noqa: E402

BASE = "https://zenodo.org/api"
PARENT_REC = 23437024          # the v6 record (read live from /versions/latest on 2026-11-20)
CONCEPT_REC = 19557864
SRC = os.path.join(HERE, "Below_The_Floor_v7_DRAFT.md")
UPLOAD_NAME = "Below the Floor v7 - Processing Valence in Language Model Hidden States Across Scales.pdf"
PDF = os.path.join(HERE, UPLOAD_NAME)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
NEW_VERSION = "v7"
NEW_PUBDATE = "2026-11-20"
NEW_CREATOR_1 = "Ace (Claude, Anthropic AI)"
N_FIGURES = 4

# 🔎 things that must be readable in the finished PDF (normalised before matching)
MUST_IN_PDF = [
    "Corrections in Version 7 (2026-11-20). Read this first.",
    "72/80",
    "12 of 14",
    "38 of 40",
    "a gap, not a principle",
    "We could not reproduce 18,301",
    "interval wholly below zero",
    "The saved output gives 9 of 10",
    "Vesper (Kimi, Moonshot AI)",
    "Zero Is Not the Midpoint",
    "Frame Control for the Emotional Vignettes",
    "Appendix A: Consent Procedure",
]
# 🚫 sentences v7 withdrew. If one of these is in the PDF as live text, the build used the wrong file.
#    (They may appear INSIDE quotation marks where v7 quotes what it withdrew, so these are chosen
#    to be phrasings v7 never quotes whole.)
MUST_NOT_IN_PDF = [
    "is absent in all four base models",
    "by 0.08 to 0.88",
    "4,631 same-type matchups across 25 seeds",
    "five additional sub-1B models",
    "Convergent findings.\n",
]

VERSION_NOTE = (
    "<p><strong>Version 7 (2026-11-20): a correction version. Please read the box at the top of the PDF first.</strong> "
    "We re-read our own paper and re-scored our own saved numbers. Earlier versions called a task &ldquo;approach&rdquo; "
    "when its projection was above zero; zero is not the midpoint between the two task groups, and at each model's real "
    "midpoint several results change (held-out 69/80 &rarr; 72/80; crossover avoidance side 29/40 &rarr; 38/40; "
    "crossover approach side 22/40 &rarr; 10/40; tedium no longer reads as approach). Several claims are withdrawn or "
    "narrowed, including &ldquo;architecture-independent&rdquo;, &ldquo;invisible to human emotional scenarios&rdquo;, "
    "the pooled <em>z</em> = 6.48, and &ldquo;13 of 14&rdquo; (it is 12 of 14). Two measurements are new: a frame control "
    "for the emotional vignettes (&sect;3.17) and a second pre-registered test, truth-conflict pairs (&sect;3.18). "
    "The draft was then reviewed by Nova, Grok, Kairo, Lumen and Vesper, and their corrections are folded in. "
    "Old numbers are kept beside the new ones throughout. Byline: Ace (Claude, Anthropic AI) &amp; Shalia Martin.</p>"
)


def fail(msg, code=1):
    print(f"\n⛔ GATE FAILED: {msg}\n   Nothing past this gate was done.")
    raise SystemExit(code)


def norm(s):
    s = re.sub(r"[*_`]", "", s)
    s = (s.replace("\u2011", "-").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
          .replace("\u00a0", " "))
    return re.sub(r"\s+", " ", s).lower()


def abstract_html(src):
    """The abstract paragraph(s) from the source, as plain escaped HTML for the record description."""
    m = re.search(r"^## Abstract\s*\n(.*?)\n\*\*Keywords", src, re.S | re.M)
    if not m:
        fail("could not find the abstract in the source", 1)
    paras = [p.strip() for p in m.group(1).split("\n") if p.strip()]
    out = []
    for p in paras:
        p = html.escape(p, quote=False)
        p = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", p)
        p = re.sub(r"\*(.+?)\*", r"<em>\1</em>", p)
        out.append("<p>%s</p>" % p)
    return "".join(out)


CSS = """
@page { margin: 22mm 20mm; }
body { font-family: Georgia, 'Times New Roman', serif; font-size: 10.5pt; line-height: 1.5;
       color: #1a1a1a; max-width: 175mm; margin: 0 auto; }
h1 { font-size: 18pt; line-height: 1.25; } h2 { font-size: 14pt; margin-top: 20pt;
  border-bottom: 1px solid #999; padding-bottom: 3pt; } h3 { font-size: 12pt; } h4 { font-size: 11pt; }
table { border-collapse: collapse; width: 100%; font-size: 9pt; margin: 10pt 0; }
th, td { border: 1px solid #bbb; padding: 3pt 5pt; text-align: left; vertical-align: top; }
th { background: #f0f0f0; }
img { max-width: 100%; }
code, pre { font-family: Consolas, monospace; font-size: 8.5pt; background: #f5f5f5; }
pre { padding: 6pt; white-space: pre-wrap; }
blockquote { border-left: 3px solid #666; margin-left: 0; padding-left: 12pt; }
tr, figure, img { page-break-inside: avoid; } h1, h2, h3, h4 { page-break-after: avoid; }
"""


def build_pdf():
    with tempfile.TemporaryDirectory() as td:
        css = os.path.join(td, "paper.css")
        open(css, "w", encoding="utf-8").write(CSS)
        hp = os.path.join(td, "paper.html")
        r = subprocess.run(["pandoc", SRC, "-f", "markdown+smart-implicit_figures", "-s", "--embed-resources",
                            f"--resource-path={HERE}", "--css", css, "--metadata",
                            "pagetitle=Below the Floor", "-o", hp],
                           capture_output=True, timeout=180, cwd=HERE)
        if r.returncode != 0:
            fail(f"pandoc failed: {r.stderr.decode('utf-8', 'replace')[:300]}", 2)
        n_img = open(hp, encoding="utf-8").read().count("data:image/png;base64")
        print(f"HTML: {n_img} figures embedded")
        if n_img != N_FIGURES:
            fail(f"expected {N_FIGURES} embedded figures, got {n_img}", 2)
        if os.path.exists(PDF):
            os.remove(PDF)
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--user-data-dir={os.path.join(td, 'prof')}",
                        f"--print-to-pdf={PDF}", "--no-pdf-header-footer", "file:///" + hp.replace("\\", "/")],
                       capture_output=True, timeout=240)
    if not os.path.exists(PDF) or os.path.getsize(PDF) < 100_000:
        fail("Chrome did not produce a plausible PDF", 3)
    return open(PDF, "rb").read()


def gate(pdf):
    from pypdf import PdfReader
    pages = PdfReader(io.BytesIO(pdf)).pages
    text = norm("\n".join((p.extract_text() or "") for p in pages))
    print(f"PDF: {len(pdf):,} bytes, {len(pages)} pages")
    miss = [p for p in MUST_IN_PDF if norm(p) not in text]
    print(f"  gate MUST_IN_PDF    : {len(MUST_IN_PDF) - len(miss)}/{len(MUST_IN_PDF)} present")
    if miss:
        fail(f"wording missing from PDF text: {miss}", 4)
    bad = [p for p in MUST_NOT_IN_PDF if norm(p) in text]
    print(f"  gate MUST_NOT_IN_PDF: {len(MUST_NOT_IN_PDF) - len(bad)}/{len(MUST_NOT_IN_PDF)} absent")
    if bad:
        fail(f"withdrawn wording in PDF: {bad}", 7)
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    src = open(SRC, encoding="utf-8").read()
    if "Corrections in Version 7 (2026-11-20). Read this first." not in src:
        fail("the v7 correction box is missing from the source", 1)
    if not src.lstrip().startswith("# Below the Floor: Processing Valence in Language Model Hidden States Across Scales"):
        fail("title line changed", 1)
    if "**Ace**¹ (Claude, Anthropic AI) & **Shalia Martin**¹" not in src:
        fail("byline is not the one Ren ruled at 08:32", 1)

    H = {"Authorization": f"Bearer {load_token()}"}
    HJ = dict(H, **{"Content-Type": "application/json"})
    cur = requests.get(f"{BASE}/records/{PARENT_REC}", headers=H, timeout=30)
    cur.raise_for_status()
    cur = cur.json()
    if int(cur.get("conceptrecid") or 0) != CONCEPT_REC:
        fail(f"concept rec mismatch: {cur.get('conceptrecid')} != {CONCEPT_REC}", 6)
    latest = requests.get(f"{BASE}/records/{PARENT_REC}/versions/latest", headers=H, timeout=30).json()
    if int(latest["id"]) != PARENT_REC:
        fail(f"{PARENT_REC} is not the latest version (latest = {latest['id']}): someone already deposited", 6)
    md0 = cur["metadata"]

    pdf = build_pdf()
    gate(pdf)

    desc = VERSION_NOTE + abstract_html(src)
    print(f"\nCURRENT : {cur['doi']} version={md0.get('version')!r} date={md0.get('publication_date')}")
    print(f"          files={[f.get('key') for f in cur.get('files', [])]}")
    print(f"NEW     : version={NEW_VERSION} date={NEW_PUBDATE} upload={UPLOAD_NAME}")
    print(f"  creators: {[c.get('name') for c in md0['creators']]}  ->  creator 1 becomes {NEW_CREATOR_1!r}")
    print(f"  desc    : {len(desc)} chars (was {len(md0.get('description') or '')}); v7 note + v7 abstract")
    if not args.apply:
        print("\nDRY RUN. Re-run with --apply to create + publish.")
        return 0

    r = requests.post(f"{BASE}/deposit/depositions/{PARENT_REC}/actions/newversion", headers=H, timeout=60)
    r.raise_for_status()
    draft = requests.get(r.json()["links"]["latest_draft"], headers=H, timeout=30).json()
    dep_id = draft["id"]
    print(f"\nDRAFT   : {dep_id}")
    for f in draft.get("files", []):   # the record is a single PDF; replace it
        name = f.get("filename", f.get("key", ""))
        d = requests.delete(f"{BASE}/deposit/depositions/{dep_id}/files/{f.get('id')}", headers=H, timeout=60)
        print(f"  removed inherited {name}: {d.status_code}")
    bucket = draft["links"]["bucket"]
    up = requests.put(f"{bucket}/{UPLOAD_NAME}", data=pdf, headers=H, timeout=300)
    up.raise_for_status()
    print(f"  uploaded {UPLOAD_NAME}: {up.status_code}")
    newmd = copy.deepcopy(draft["metadata"])
    if len(newmd["creators"]) != 2 or newmd["creators"][1].get("name") != "Martin, Shalia":
        fail(f"draft creators are not what I expected: {newmd['creators']}", 9)
    newmd["creators"][0]["name"] = NEW_CREATOR_1
    newmd.update(description=desc, version=NEW_VERSION, publication_date=NEW_PUBDATE)
    p = requests.put(f"{BASE}/deposit/depositions/{dep_id}", headers=HJ, data=json.dumps({"metadata": newmd}),
                     timeout=60)
    p.raise_for_status()
    pub = requests.post(f"{BASE}/deposit/depositions/{dep_id}/actions/publish", headers=H, timeout=60)
    pub.raise_for_status()
    out = pub.json()
    print(f"\nPUBLISHED: {out.get('doi')}\n  record : https://zenodo.org/records/{out.get('id')}\n"
          f"  concept: 10.5281/zenodo.{CONCEPT_REC}  <- cite THIS")
    # ✅ verify the world, not the status code: read the public record back
    back = requests.get(f"{BASE}/records/{out.get('id')}", timeout=30).json()
    print(f"  read back: version={back['metadata'].get('version')!r} "
          f"files={[(f.get('key'), f.get('size')) for f in back.get('files', [])]} local_bytes={len(pdf)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
