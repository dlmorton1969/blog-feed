#!/usr/bin/env python3
"""Make the branded featured image for a post: docs/cards/<slug>.jpg (1200x630).

Usage: python3 make_card.py posts/2026-11-17-some-slug.html
Reads the post's header (title, tags, card_label) and renders a navy-and-gold card with
David's logo, the post title and his headshot. Needs Playwright (pre-installed in the cloud).
The first tag is used as the town, the second as the category, unless `card_label:` is set.
"""
import html
import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from build_feed import parse  # noqa: E402

BRAND = ROOT / "docs" / "brand"

TEMPLATE = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1200px;height:630px;background:#0f1b2d;font-family:Inter,sans-serif;overflow:hidden}}
.wrap{{position:absolute;inset:28px;border:2px solid #c9a24a;display:flex}}
.left{{flex:1;padding:44px 40px 40px 52px;display:flex;flex-direction:column}}
.logo{{width:150px}}
.label{{margin-top:auto;color:#d9b45a;font-size:21px;font-weight:600;letter-spacing:.18em;text-transform:uppercase}}
h1{{margin-top:16px;color:#fff;font-family:"Bitstream Charter",Georgia,serif;font-weight:400;
   font-size:{size}px;line-height:1.12}}
.rule{{margin-top:28px;width:90px;height:3px;background:#c9a24a}}
.foot{{margin-top:22px;color:#cfd6e0;font-size:20px;letter-spacing:.02em}}
.foot b{{color:#fff;font-weight:600}}
.firm{{margin-top:6px;color:#9aa6b6;font-size:16px;letter-spacing:.02em}}
.right{{width:360px;display:flex;align-items:center;justify-content:center}}
.photo{{width:290px;height:290px;border-radius:50%;border:5px solid #c9a24a;object-fit:cover}}
</style></head><body><div class="wrap">
<div class="left"><img class="logo" src="{logo}">
<div class="label">{label}</div><h1>{title}</h1><div class="rule"></div>
<div class="foot"><b>David L. Morton, Realtor®</b> &nbsp;·&nbsp; Call or text 980-350-8686</div>
<div class="firm">DavidMortonSoldIt.com &nbsp;·&nbsp; David Morton Real Estate by Real Broker, LLC</div></div>
<div class="right"><img class="photo" src="{photo}"></div>
</div></body></html>"""


def render(post_path: str) -> pathlib.Path:
    meta = parse(pathlib.Path(post_path))
    tags = meta["tags"]
    label = meta.get("card_label") or " · ".join(tags[:2])
    title = meta["title"]
    size = 60 if len(title) <= 40 else 52 if len(title) <= 52 else 46
    doc = TEMPLATE.format(logo=(BRAND / "logo-gold-600.png").as_uri(),
                          photo=(BRAND / "headshot.jpg").as_uri(),
                          label=html.escape(label), title=html.escape(title), size=size)
    tmp = ROOT / "docs" / "cards" / f".{meta['slug']}.html"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(doc, encoding="utf-8")
    out = tmp.parent / f"{meta['slug']}.jpg"
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        pg.goto(tmp.as_uri())
        pg.wait_for_load_state("networkidle")
        pg.screenshot(path=str(out), type="jpeg", quality=88)
        b.close()
    tmp.unlink()
    print(out.relative_to(ROOT))
    return out


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        render(arg)
