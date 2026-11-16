#!/usr/bin/env python3
"""Build feed.xml and index.html from posts/*.html.

Each post file is named YYYY-MM-DD-slug.html and starts with a header comment:

<!--
title: Waxhaw Market Update: November 2026
description: Under-155-character meta description.
date: 2026-11-17
tags: Waxhaw, Market Update, Union County
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
    return meta


def page(title: str, description: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, follow">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<style>body{{font-family:Georgia,serif;max-width:760px;margin:2rem auto;padding:0 1rem;line-height:1.6;color:#222}}
a{{color:#0b4f8a}} h1{{line-height:1.2}}</style></head>
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
        items.append(f"""    <item>
      <title>{html.escape(p['title'])}</title>
      <link>{p['url']}</link>
      <guid isPermaLink="false">{p['slug']}</guid>
      <pubDate>{format_datetime(p['published'])}</pubDate>
      <dc:creator>{AUTHOR}</dc:creator>
      <description>{html.escape(p['description'])}</description>{cats}
      <content:encoded><![CDATA[{body}]]></content:encoded>
    </item>""")

    now = format_datetime(dt.datetime.now(ET))
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:atom="http://www.w3.org/2005/Atom">
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
    (out_dir / "feed.xml").write_text(feed, encoding="utf-8")

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
