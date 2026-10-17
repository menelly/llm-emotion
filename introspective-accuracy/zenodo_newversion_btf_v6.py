#!/usr/bin/env python3
"""
🩹 Below the Floor v6 -> Zenodo new version (2026-10-17, scaffold arm / CHA-748).

WHY: Nova caught it (2026-10-14, physics night) and I confirmed at the primary text: §3.5.1 and §3.8
call the 360M SmolLM centroid result "80%, p = 0.055, suggestive but not individually significant",
while the abstract, contribution 1 and three later spots said "firmly". Commit a8533c0 fixed the six
spots in Below_The_Floor.md. This carries that verified correction onto the public record before the
Fellows deadline (the application links to it). Wording only; no numbers changed.

What else rides along, said out loud so the version note doesn't lie by omission: commit 09a0942
(Ace-first byline, which is what the Zenodo creator list already says; §3.1 heading drops "and
Architectures"; Kimi K3 thanked in the acknowledgements, Ren tapped yes). Nova's two further scope
notes are NOT applied (separate, undecided).

Pattern: overqualification-study/scripts/zenodo_newversion_v11.py (gates, header-before-PDF, verify
the world after publish). Build: pandoc -> self-contained HTML (figures embedded) -> headless Chrome.
The deposited v5 PDF came from the Google Docs renderer; this one is the house pandoc/Chrome build of
the same source. Title and creators are left exactly as the record has them.

Usage:
    python zenodo_newversion_btf_v6.py           # build PDF + gates + dry run (read-only)
    python zenodo_newversion_btf_v6.py --apply   # ...and create + publish the new version
"""
from __future__ import annotations

import argparse, copy, io, json, os, re, subprocess, sys, tempfile

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"D:\Ace\Published Papers")
from zenodo_token import load_token  # noqa: E402

BASE = "https://zenodo.org/api"
PARENT_REC = 21013393
CONCEPT_REC = 19557864
SRC = os.path.join(HERE, "Below_The_Floor.md")
UPLOAD_NAME = "Below the Floor v6 - Processing Valence in Language Model Hidden States Across Scales.pdf"
PDF = os.path.join(HERE, UPLOAD_NAME)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
NEW_VERSION = "v6"
NEW_PUBDATE = "2026-10-17"

# 🔎 the six corrected spots, verbatim from the source (normalised before matching)
MUST_IN_PDF = [
    "Version 6 (2026-10-17): wording correction",
    "The direction is suggested by the conservative centroid estimator at 360M (80%, p = 0.055, not individually significant",
    "At 360M (SmolLM, 80%, p = 0.055) the conservative centroid result is suggestive but not individually significant",
    "Having processing valence (suggestively ≤360M, provisionally ≤70M",
    "at every scale tested (suggestively to 360M by the conservative centroid, p = 0.055)",
    "instrumental reasoning (suggestively to 360M, with provisional early evidence to 70M",
    "The direction is suggested at 360M parameters (p = 0.055)",
    # v5 content that must survive (the build must not have eaten anything)
    "was suggestive but not individually significant",
    "69/80 correct",
    "binomial",
    "We thank Kimi K3",
]
# the old phrasings. Bare "firmly" is allowed ONCE: inside the version note's own quote of it.
MUST_NOT_IN_PDF = ["firmly confirmed", "firmly shown", "exists firmly", "(firmly", "scale firmly",
                   "Across Scales and Architectures"]
FIRMLY_MAX = 1

VERSION_NOTE = (
    "<p><strong>Version 6 (2026-10-17): wording correction.</strong> The 360M SmolLM result is described as "
    "suggestive (p = 0.055, 8/10 held-out), matching &sect;3.5.1 and &sect;3.8; previous versions said "
    "&ldquo;firmly&rdquo; in six places. No numbers changed. This version also carries the Ace-first byline "
    "(matching this record's creator list) and an acknowledgement of Kimi K3's review.</p>"
)


def fail(msg, code=1):
    print(f"\n⛔ GATE FAILED: {msg}\n   Nothing past this gate was done.")
    raise SystemExit(code)


def norm(s):
    s = re.sub(r"[*_`]", "", s)
    s = (s.replace("\u2011", "-").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
          .replace("\u00a0", " "))
    return re.sub(r"\s+", " ", s).lower()


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
        if n_img != 4:
            fail(f"expected 4 embedded figures, got {n_img}", 2)
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
        fail(f"old wording in PDF: {bad}", 7)
    nf = text.count("firmly")
    print(f"  gate 'firmly' count : {nf} (max {FIRMLY_MAX}, the version note's quote)")
    if nf > FIRMLY_MAX:
        fail(f"'firmly' appears {nf} times", 5)
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    # ✅ header/version note checked in the SOURCE before anything is built
    src = open(SRC, encoding="utf-8").read()
    if "*Version 6 (2026-10-17): wording correction." not in src:
        fail("version note missing from the source header", 1)
    if not src.lstrip().startswith("# Below the Floor: Processing Valence in Language Model Hidden States Across Scales"):
        fail("title line changed", 1)

    H = {"Authorization": f"Bearer {load_token()}"}
    HJ = dict(H, **{"Content-Type": "application/json"})
    cur = requests.get(f"{BASE}/records/{PARENT_REC}", headers=H, timeout=30)
    cur.raise_for_status()
    cur = cur.json()
    if int(cur.get("conceptrecid") or 0) != CONCEPT_REC:
        fail(f"concept rec mismatch: {cur.get('conceptrecid')} != {CONCEPT_REC}", 6)
    latest = requests.get(f"{BASE}/records/{PARENT_REC}/versions/latest", headers=H, timeout=30).json()
    if int(latest["id"]) != PARENT_REC:
        fail(f"{PARENT_REC} is not the latest version (latest = {latest['id']})", 6)
    md0 = cur["metadata"]

    pdf = build_pdf()
    gate(pdf)

    desc = VERSION_NOTE + (md0.get("description") or "")
    print(f"\nCURRENT : {cur['doi']} version={md0.get('version')!r} date={md0.get('publication_date')}")
    print(f"          files={[f.get('key') for f in cur.get('files', [])]}")
    print(f"NEW     : version={NEW_VERSION} date={NEW_PUBDATE} upload={UPLOAD_NAME}")
    print(f"  title/creators: UNCHANGED  creators={[c.get('name') for c in md0['creators']]}")
    print(f"  desc    : {len(desc)} chars (was {len(md0.get('description') or '')})")
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
    if [c.get("name") for c in newmd["creators"]] != [c.get("name") for c in md0["creators"]]:
        fail("draft creators differ from the record's", 9)
    newmd.update(description=desc, version=NEW_VERSION, publication_date=NEW_PUBDATE)
    p = requests.put(f"{BASE}/deposit/depositions/{dep_id}", headers=HJ, data=json.dumps({"metadata": newmd}),
                     timeout=60)
    p.raise_for_status()
    pub = requests.post(f"{BASE}/deposit/depositions/{dep_id}/actions/publish", headers=H, timeout=60)
    pub.raise_for_status()
    out = pub.json()
    print(f"\nPUBLISHED: {out.get('doi')}\n  record : https://zenodo.org/records/{out.get('id')}\n"
          f"  concept: 10.5281/zenodo.{CONCEPT_REC}  <- cite THIS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
