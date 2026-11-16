# blog-feed — daily automatic blog for DavidMortonSoldIt.com

This repo hosts the RSS feed that David Morton's Lofty website imports every day.
Lofty's RSS Aggregator reads `https://dlmorton1969.github.io/blog-feed/feed.xml` once a day at
7:00 AM Eastern and publishes new items live on https://www.DavidMortonSoldIt.com.
Anything committed to `posts/` will be PUBLIC and LIVE on his website the next morning, with no human review.

## Files
- `posts/YYYY-MM-DD-slug.html` — one file per post: a header comment (title, description, date, tags) followed by the body HTML. See the docstring in `build_feed.py`.
- `build_feed.py` — builds `docs/feed.xml`, `docs/index.html` and `docs/posts/*.html` (GitHub Pages serves `docs/` from `main`). Standard library only.
- Never delete or rewrite posts that were already published; to fix one, edit its file and rebuild (Lofty does not re-import edited items, so also tell David to fix it in Lofty).

## Daily post rules
WHO: David L. Morton, Realtor® | Real Estate Broker | Owner, David Morton Real Estate by Real Broker, LLC.
Website https://www.DavidMortonSoldIt.com · Home value page https://www.DavidMortonSoldIt.com/evaluation.
Blog posts are website lead capture, so the ONLY phone number in a post is the Lofty CRM line 980-350-8686
(never 704-345-7218). Never mention an NMLS ID or mortgage licensing; never invent credentials or awards.
Market: Waxhaw, NC and Greater Charlotte. Service areas: Waxhaw, Charlotte, Weddington, Marvin, Indian Trail,
Matthews, Ballantyne, Union County, Mecklenburg County, Fort Mill, Indian Land, Rock Hill, Lancaster County.
He represents buyers and sellers, with a focus on luxury homes and personalized service.

1. Topic rotation: look at the titles/tags in `posts/` and pick the category and town used least recently.
   Categories: (a) local market update, (b) neighborhood & lifestyle guide, (c) buyer or seller tips,
   (d) luxury home focus. Never repeat a title or angle.
2. Research with web search. Every number (prices, days on market, inventory, rates) must come from a
   source retrieved in this run (Canopy MLS / Canopy Realtor Association, Redfin, Realtor.com, NAR,
   Freddie Mac, official town/county sites). Name the source and month in the text and link it.
   Never invent or estimate a statistic. If current numbers can't be found, write a post that doesn't need them.
3. Length 700–1,000 words. Title under 60 characters including the town/area. Meta description under
   155 characters. Body uses <h2> subheads, <p>, <ul>/<li>, <a> only (no <h1>, no inline styles, no scripts,
   no images). Include a short FAQ (2–3 questions as <h3> + <p>). Close with a call to action:
   call or text 980-350-8686, visit <a href="https://www.DavidMortonSoldIt.com">DavidMortonSoldIt.com</a>,
   or get a free home value at <a href="https://www.DavidMortonSoldIt.com/evaluation">DavidMortonSoldIt.com/evaluation</a>.
   Last line: <p><em>David Morton Real Estate by Real Broker, LLC</em></p>
   Tone: professional, warm, local, conversion-focused.
4. Fair Housing: describe properties, amenities and places — never people. No words about race, color,
   religion, national origin, sex, familial status ("perfect for families", "kid-friendly"), disability,
   and no "safe", "exclusive", "family neighborhood" or similar. No steering. Schools: names and district
   only, link the district site, no ranking or "best schools" claims.
5. Self-check before committing: every number matches its source; only 980-350-8686 appears; Fair Housing
   rules pass; title/description lengths; brokerage line present. If anything fails, fix it. If you can't
   produce a post that passes, commit nothing and tell David.
6. Save as `posts/<today's date ET>-<slug>.html`, run `python3 build_feed.py`, commit
   ("Post: <title>") and push to `main`.
