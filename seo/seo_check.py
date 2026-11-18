#!/usr/bin/env python3
"""SEO engine for the daily blog. Standard library only.

  python3 seo/seo_check.py next              -> the keyword to target today (and why)
  python3 seo/seo_check.py check posts/X.html -> pass/fail SEO lint for one post (exit 1 on failure)
  python3 seo/seo_check.py mark posts/X.html  -> records the post's `keyword:` as used in keyword-map.csv

Each post header must include `keyword: <exact keyword from seo/keyword-map.csv>`.
"""
import csv
import datetime as dt
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAP = ROOT / "seo" / "keyword-map.csv"
POSTS = ROOT / "posts"
HEADER_RE = re.compile(r"\A\s*<!--(.*?)-->\s*", re.S)
SITE = "davidmortonsoldit.com"


def load_map():
    with MAP.open(newline="") as f:
        return list(csv.DictReader(f))


def save_map(rows):
    with MAP.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def header(path):
    text = path.read_text(encoding="utf-8")
    m = HEADER_RE.match(text)
    meta = {}
    if m:
        for line in m.group(1).strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip().lower()] = v.strip()
    return meta, (text[m.end():] if m else text)


def recent_towns(n=4):
    towns = []
    for p in sorted(POSTS.glob("*.html"), reverse=True)[:n]:
        tags = header(p)[0].get("tags", "")
        if tags:
            towns.append(tags.split(",")[0].strip().lower())
    return towns


def cmd_next():
    rows = load_map()
    recent = recent_towns()
    recent_cats = []
    for p in sorted(POSTS.glob("*.html"), reverse=True)[:3]:
        t = header(p)[0].get("tags", "").split(",")
        if len(t) > 1:
            recent_cats.append(t[1].strip().lower())
    free = [r for r in rows if not r["used_on"]]
    if not free:
        sys.exit("Every keyword in the map is used. Add new rows to seo/keyword-map.csv.")

    def score(r):
        return (int(r["priority"]),
                r["town"].lower() in recent,           # avoid towns used in the last 4 posts
                r["category"].lower() in recent_cats,  # avoid the last 3 categories
                rows.index(r))
    best = sorted(free, key=score)[0]
    print(f"keyword: {best['keyword']}")
    print(f"town: {best['town']}  category: {best['category']}  priority: {best['priority']}")
    print(f"MUST link (in the first 3 paragraphs): {best['target_url']}")
    print(f"Also link: {best['support_url']}")
    print(f"Recent towns to avoid: {', '.join(recent) or 'none'}")


def cmd_check(path):
    path = pathlib.Path(path)
    meta, body = header(path)
    rows = {r["keyword"].lower(): r for r in load_map()}
    errs, warns = [], []
    kw = meta.get("keyword", "")
    title, desc = meta.get("title", ""), meta.get("description", "")
    slug = path.stem[11:] if re.match(r"\d{4}-\d{2}-\d{2}-", path.stem) else path.stem

    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        errs.append(f"slug '{slug}' must be lowercase words joined by single hyphens")
    if len(slug) > 60:
        warns.append(f"slug is {len(slug)} chars; keep it under 60")
    if not kw:
        errs.append("header is missing 'keyword:' (pick one with `seo_check.py next`)")
    row = rows.get(kw.lower())
    if kw and not row:
        errs.append(f"keyword '{kw}' is not in seo/keyword-map.csv")
    if row and row["used_on"] and row["used_on"] != meta.get("date"):
        errs.append(f"keyword '{kw}' was already used on {row['used_on']} (cannibalization)")
    if not 25 <= len(title) <= 60:
        errs.append(f"title is {len(title)} chars; needs 25-60")
    if not 110 <= len(desc) <= 155:
        errs.append(f"description is {len(desc)} chars; needs 110-155")
    if re.search(r"<[^>]+>|[*#]{1,}|&lt;", title + desc):
        errs.append("title/description contains HTML or markdown characters")

    plain = re.sub(r"<[^>]+>", " ", body)
    words = len(plain.split())
    if words < 700:
        errs.append(f"body is {words} words; needs 700+")
    if row:
        town = row["town"].lower()
        if town.split()[0] not in title.lower():
            errs.append(f"title must name the town '{row['town']}'")
        first = " ".join(re.findall(r"<p>(.*?)</p>", body, re.S)[:2]).lower()
        core = [w for w in re.findall(r"[a-z]+", kw.lower()) if w not in ("nc", "sc", "a", "in", "what", "is", "my")]
        if not all(w in first for w in core):
            warns.append(f"first two paragraphs should use the keyword phrase: '{kw}'")
        h2s = " ".join(re.findall(r"<h2>(.*?)</h2>", body, re.S)).lower()
        if town.split()[0] not in h2s:
            warns.append("no <h2> mentions the town")
        tgt = row["target_url"].lower()
        links = [h.lower() for h in re.findall(r'href="([^"]+)"', body)]
        if not any(l.rstrip("/") == tgt.rstrip("/") for l in links):
            errs.append(f"missing internal link to the area page {row['target_url']}")
        else:
            paras = re.findall(r"<p>(.*?)</p>", body, re.S)[:3]
            if not any(tgt in p.lower() for p in paras):
                warns.append("area-page link should appear in the first 3 paragraphs")
        internal = [l for l in links if SITE in l]
        if len(set(internal)) < 3:
            errs.append(f"only {len(set(internal))} distinct links to DavidMortonSoldIt.com; need 3+")
    if "<h1" in body.lower():
        errs.append("body must not contain <h1>")
    if len(re.findall(r"<h3>", body)) < 2:
        errs.append("FAQ needs at least 2 <h3> questions")
    phones = set(re.findall(r"\d{3}[-.)\s]*\d{3}[-.\s]*\d{4}", plain))
    if any(re.sub(r"\D", "", p) != "9803508686" for p in phones):
        errs.append(f"wrong phone number in post: {phones}")
    if "David Morton Real Estate by Real Broker, LLC" not in body:
        errs.append("brokerage line missing")
    bad = re.findall(r"\b(safe neighborhood|family[- ]friendly|kid[- ]friendly|perfect for families|"
                     r"exclusive neighborhood|family neighborhood|best schools|walking distance to church)\b",
                     plain, re.I)
    if bad:
        errs.append(f"Fair Housing words: {sorted(set(b.lower() for b in bad))}")

    for e in errs:
        print("FAIL:", e)
    for w in warns:
        print("warn:", w)
    print("SEO CHECK PASSED" if not errs else f"SEO CHECK FAILED ({len(errs)} issue(s))")
    sys.exit(1 if errs else 0)


def cmd_mark(path):
    path = pathlib.Path(path)
    meta, _ = header(path)
    rows = load_map()
    for r in rows:
        if r["keyword"].lower() == meta.get("keyword", "").lower():
            r["used_on"] = meta.get("date", dt.date.today().isoformat())
            save_map(rows)
            print(f"marked '{r['keyword']}' used on {r['used_on']}")
            return
    sys.exit("keyword not found in map")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("next", "check", "mark"):
        sys.exit(__doc__)
    if sys.argv[1] == "next":
        cmd_next()
    elif len(sys.argv) < 3:
        sys.exit("give a post path")
    elif sys.argv[1] == "check":
        cmd_check(sys.argv[2])
    else:
        cmd_mark(sys.argv[2])
