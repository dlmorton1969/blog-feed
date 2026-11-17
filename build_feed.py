#!/usr/bin/env python3
"""Build feed.xml and index.html from posts/*.html.

Each post file is named YYYY-MM-DD-slug.html and starts with a header comment:

<!--
title: Waxhaw Market Update: November 2026
description: Under-155-character meta description.
date: 2026-11-17
tags: Waxhaw, Market Update, Union County
image: https://burst.shopifycdn.com/photos/example.jpg?width=1200
image_alt: Short description of the photo (no people)
image_credit: Photo by Jane Doe on Burst   (optional)
-->
<h2>...</h2><p>...</p>   (the post body as HTML)

Run: python3 build_feed.py   (standard library only)
Lofty's RSS Aggregator reads feed.xml once a day at 7:00 AM Eastern.
"""
import datetime as dt
import html
import pathlib
import re
import sys
from email.utils import format_datetime
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parent
POSTS = ROOT / "posts"
SITE_URL = "https://dlmorton1969.github.io/blog-feed"
HOME = "https://www.DavidMortonSoldIt.com"
FEED_TITLE = "David Morton Real Estate Blog"
FEED_DESC = ("Waxhaw and Greater Charlotte real estate news, neighborhood guides, "
             "and buyer and seller tips from David Morton Real Estate by Real Broker, LLC.")
AUTHOR = "David L. Morton"
MAX_ITEMS = 30
ET = ZoneInfo("America/New_York")

AUTHOR_BOX = f"""<hr>
<p><img src="{SITE_URL}/brand/logo-gold-600.png" alt="David Morton Real Estate logo" width="180"></p>
<p><img src="{SITE_URL}/brand/headshot.jpg" alt="David L. Morton, Realtor" width="140"></p>
<p><strong>About David Morton</strong><br>David L. Morton is a Realtor&reg;, real estate broker and owner of David Morton Real Estate by Real Broker, LLC. He represents buyers and sellers across Waxhaw and Greater Charlotte, with a focus on luxury homes and personalized service. Call or text <a href="tel:9803508686">980-350-8686</a> or visit <a href="{HOME}">DavidMortonSoldIt.com</a>.</p>"""

HEADER_RE = re.compile(r"\A\s*<!--(.*?)-->\s*", re.S)


def parse(path: pathlib.Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = HEADER_RE.match(text)
    if not m:
        sys.exit(f"{path.name}: missing <!-- header --> block")
    meta = {}
    for line in m.group(1).strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip().lower()] = v.strip()
    for key in ("title", "description", "date"):
        if not meta.get(key):
            sys.exit(f"{path.name}: header is missing '{key}'")
    day = dt.date.fromisoformat(meta["date"])
    meta["published"] = dt.datetime(day.year, day.month, day.day, 6, 0, tzinfo=ET)
    meta["slug"] = path.stem
    meta["body"] = text[m.end():].strip()
    meta["tags"] = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
    meta["url"] = f"{SITE_URL}/posts/{path.stem}.html"
    img = meta.get("image", "")
    photo = ""
    if img:
        alt = html.escape(meta.get("image_alt", meta["title"]))
        photo = f'<p><img src="{html.escape(img)}" alt="{alt}"></p>'
        if meta.get("image_credit"):
            photo += f'\n<p><small>{html.escape(meta["image_credit"])}</small></p>'
    card = ROOT / "docs" / "cards" / f"{path.stem}.jpg"
    if card.exists():
        # Branded card (make_card.py) is the featured image; the stock photo moves
        # below the first paragraph.
        meta["image"] = f"{SITE_URL}/cards/{path.stem}.jpg?v={int(card.stat().st_mtime)}"
        top = f'<p><img src="{html.escape(meta["image"])}" alt="{html.escape(meta["title"])}"></p>'
        body = meta["body"]
        if photo:
            cut = body.find("</p>")
            body = (body[:cut + 4] + "\n" + photo + body[cut + 4:]) if cut != -1 else photo + "\n" + body
        meta["body"] = top + "\n" + body
    elif photo:
        meta["body"] = photo + "\n" + meta["body"]
    # About-the-author box with logo and headshot, just above the brokerage line.
    firm = "<p><em>David Morton Real Estate by Real Broker, LLC</em></p>"
    body = meta["body"]
    i = body.rfind(firm)
    meta["body"] = (body[:i] + AUTHOR_BOX + "\n" + body[i:]) if i != -1 else body + "\n" + AUTHOR_BOX
    return meta


def page(title: str, description: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, follow">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<style>body{{font-family:Georgia,serif;max-width:760px;margin:2rem auto;padding:0 1rem;line-height:1.6;color:#222}}
a{{color:#0b4f8a}} h1{{line-height:1.2}} img{{max-width:100%;height:auto}}</style></head>
<body>{body}
<hr><p>Official blog: <a href="{HOME}">DavidMortonSoldIt.com</a></p></body></html>
"""


def main() -> None:
    posts = sorted((parse(p) for p in POSTS.glob("*.html")),
                   key=lambda p: (p["published"], p["slug"]), reverse=True)
    out_dir = ROOT / "docs"
    (out_dir / "posts").mkdir(parents=True, exist_ok=True)

    items = []
    for p in posts[:MAX_ITEMS]:
        (out_dir / "posts" / f"{p['slug']}.html").write_text(
            page(p["title"], p["description"], f"<h1>{html.escape(p['title'])}</h1>\n{p['body']}"),
            encoding="utf-8")
        cats = "".join(f"\n      <category>{html.escape(t)}</category>" for t in p["tags"])
        body = p["body"].replace("]]>", "]]]]><![CDATA[>")
        media = ""
        if p.get("image"):
            u = html.escape(p["image"])
            media = (f'\n      <enclosure url="{u}" type="image/jpeg" length="0"/>'
                     f'\n      <media:content url="{u}" medium="image" type="image/jpeg"/>'
                     f'\n      <media:thumbnail url="{u}"/>')
        items.append(f"""    <item>
      <title>{html.escape(p['title'])}</title>
      <link>{p['url']}</link>
      <guid isPermaLink="false">{p['slug']}</guid>
      <pubDate>{format_datetime(p['published'])}</pubDate>
      <dc:creator>{AUTHOR}</dc:creator>
      <description>{html.escape(p['description'])}</description>{cats}{media}
      <content:encoded><![CDATA[{body}]]></content:encoded>
    </item>""")

    now = format_datetime(dt.datetime.now(ET))
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:atom="http://www.w3.org/2005/Atom"
     xmlns:media="http://search.yahoo.com/mrss/">
  <channel>
    <title>{FEED_TITLE}</title>
    <link>{HOME}</link>
    <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml"/>
    <description>{html.escape(FEED_DESC)}</description>
    <language>en-us</language>
    <lastBuildDate>{now}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
"""
    # simple.xml: plain RSS 2.0 (no extra namespaces) for maximum compatibility.
    simple_items = []
    for p in posts[:MAX_ITEMS]:
        enc = (f'\n      <enclosure url="{html.escape(p["image"])}" type="image/jpeg" length="0"/>'
               if p.get("image") else "")
        simple_items.append(f"""    <item>
      <title>{html.escape(p['title'])}</title>
      <link>{p['url']}</link>
      <guid isPermaLink="true">{p['url']}</guid>
      <pubDate>{format_datetime(p['published'])}</pubDate>
      <description>{html.escape(p['body'])}</description>{enc}
    </item>""")
    simple = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{FEED_TITLE}</title>
    <link>{SITE_URL}/</link>
    <description>{html.escape(FEED_DESC)}</description>
    <language>en-us</language>
    <lastBuildDate>{now}</lastBuildDate>
{chr(10).join(simple_items)}
  </channel>
</rss>
"""
    (out_dir / "simple.xml").write_text(simple, encoding="utf-8")
    # rss.xml is the address Lofty uses; feed.xml is kept as an identical copy.
    (out_dir / "feed.xml").write_text(feed, encoding="utf-8")
    (out_dir / "rss.xml").write_text(feed.replace(f"{SITE_URL}/feed.xml", f"{SITE_URL}/rss.xml"), encoding="utf-8")

    listing = "\n".join(
        f'<li><a href="posts/{p["slug"]}.html">{html.escape(p["title"])}</a> '
        f'<small>({p["published"]:%b %d, %Y})</small></li>' for p in posts[:MAX_ITEMS])
    (out_dir / "index.html").write_text(
        page(FEED_TITLE, FEED_DESC,
             f"<h1>{FEED_TITLE}</h1><p>RSS feed: <a href=\"feed.xml\">feed.xml</a></p><ul>{listing}</ul>"),
        encoding="utf-8")
    print(f"Built feed with {len(items)} item(s).")


if __name__ == "__main__":
    main()
