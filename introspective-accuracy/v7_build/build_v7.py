"""
🐙 build_v7.py — builds Below_The_Floor_v7_DRAFT.md from the untouched v6 file.

Every change is one op in ops_*.py so future-me can see exactly what was changed and why.
Op kinds:
  ("para", prefix, new)        replace the WHOLE line (= paragraph) that starts with prefix
  ("sub", old, new)            exact substring, must occur exactly once
  ("suball", old, new)         every occurrence (must occur at least once)
  ("after", prefix, text)      insert text as new line(s) after the line starting with prefix
  ("before", prefix, text)     insert text before the line starting with prefix
  ("del", prefix)              delete the line starting with prefix
Nothing is written unless asked with --write; failures are listed either way.
"""
import importlib
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REPO = r"D:\Ace\LLM-emotion\introspective-accuracy"
SRC = os.path.join(REPO, "Below_The_Floor.md")
DST = os.path.join(REPO, "Below_The_Floor_v7_DRAFT.md")

with io.open(SRC, encoding="utf-8", newline="") as f:
    raw = f.read()
EOL = "\r\n" if "\r\n" in raw else "\n"
lines = raw.replace("\r\n", "\n").split("\n")

fails = []
done = 0


def find_line(prefix):
    hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    return hits


for modname in sys.argv[1:]:
    if modname.startswith("--"):
        continue
    mod = importlib.import_module(modname)
    for n, op in enumerate(mod.OPS):
        kind = op[0]
        tag = "%s#%d %s" % (modname, n, kind)
        if kind in ("para", "after", "before", "del"):
            hits = find_line(op[1])
            if len(hits) != 1:
                fails.append("%s: prefix matched %d lines: %r" % (tag, len(hits), op[1][:70]))
                continue
            i = hits[0]
            if kind == "para":
                lines[i] = op[2]
            elif kind == "after":
                lines[i + 1:i + 1] = op[2].split("\n")
            elif kind == "before":
                lines[i:i] = op[2].split("\n")
            elif kind == "del":
                del lines[i]
            done += 1
        elif kind in ("sub", "suball"):
            text = "\n".join(lines)
            c = text.count(op[1])
            if (kind == "sub" and c != 1) or (kind == "suball" and c < 1):
                fails.append("%s: found %d times: %r" % (tag, c, op[1][:70]))
                continue
            text = text.replace(op[1], op[2])
            lines = text.split("\n")
            done += 1
        else:
            fails.append("%s: unknown kind" % tag)

print("ops applied: %d   failed: %d" % (done, len(fails)))
for f_ in fails:
    print("  FAIL", f_)

if "--write" in sys.argv:
    with io.open(DST, "w", encoding="utf-8", newline="") as f:
        f.write(EOL.join(lines))
    print("wrote", DST, "lines:", len(lines))
