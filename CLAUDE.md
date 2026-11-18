# blog-feed — daily automatic blog for DavidMortonSoldIt.com

This repo hosts the RSS feed that David Morton's Lofty website imports every day.
Lofty's RSS Aggregator reads `https://dlmorton1969.github.io/blog-feed/rss.xml` (feed.xml is an identical copy) once a day at
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

1. Topic = keyword (SEO engine). Run `python3 seo/seo_check.py next`. It picks today's target keyword
   from `seo/keyword-map.csv` (priority towns first, rotating town and category, never a keyword already
   used, so posts don't compete with each other in Google). Write the post AROUND that exact keyword:
   - Add `keyword: <the keyword, exactly>` to the header, and put the town first and the category second in `tags:`.
   - Title (under 60 chars) contains the town and the keyword's main idea; use the phrase naturally in the
     first two paragraphs and work the town into at least one <h2>.
   - Link the area page `target_url` within the first 3 paragraphs with descriptive anchor text
     (e.g. "homes for sale in Marvin"), and link `support_url` too. At least 3 distinct DavidMortonSoldIt.com links in total.
   - Where it fits, link 1 earlier post from this repo's feed by its live title on DavidMortonSoldIt.com/blog only if you know the URL; never guess URLs.
   - Slug: lowercase words with single hyphens, under 60 chars, keyword-led (e.g. `marvin-nc-homes-for-sale-guide`).
   If David asks for a specific topic, use the closest unused keyword, or add a new row to the map first.
2. Research with web search. Every number (prices, days on market, inventory, rates) must come from a
   source retrieved in this run (Canopy MLS / Canopy Realtor Association, Redfin, Realtor.com, NAR,
   Freddie Mac, official town/county sites). Name the source and month in the text and link it.
   Never invent or estimate a statistic. If current numbers can't be found, write a post that doesn't need them.
3. Length 700–1,000 words. Title under 60 characters including the town/area. Meta description under
   155 characters. Body uses <h2> subheads, <p>, <ul>/<li>, <a> only (no <h1>, no inline styles, no scripts,
   no <img> tags — the photo goes in the header instead). Include a short FAQ (2–3 questions as <h3> + <p>). Close with a call to action:
   call or text 980-350-8686, visit <a href="https://www.DavidMortonSoldIt.com">DavidMortonSoldIt.com</a>,
   or get a free home value at <a href="https://www.DavidMortonSoldIt.com/evaluation">DavidMortonSoldIt.com/evaluation</a>.
   Last line: <p><em>David Morton Real Estate by Real Broker, LLC</em></p>
   Tone: professional, warm, local, conversion-focused.
4. Fair Housing: describe properties, amenities and places — never people. No words about race, color,
   religion, national origin, sex, familial status ("perfect for families", "kid-friendly"), disability,
   and no "safe", "exclusive", "family neighborhood" or similar. No steering. Schools: names and district
   only, link the district site, no ranking or "best schools" claims.
5. Photo (required on every post): add `image:`, `image_alt:` and `image_credit:` header lines. The builder places
   the photo at the top of the post and in the feed; Lofty uses it as the featured/social image.
   - Use a free-for-commercial-use stock photo: Burst (shopify.com/stock-photos — direct URL form
     `https://burst.shopifycdn.com/photos/<slug>.jpg?width=1200&format=pjpg&exif=0&iptc=0`, take it from the
     photo page's og:image) or Unsplash (direct images.unsplash.com URL from the photo page). Confirm the
     page states a free commercial license, and credit the photographer ("Photo by NAME on Burst/Unsplash").
   - Match the topic and look like the Carolinas (brick or siding homes, porches, wooded lots, green lawns,
     a downtown streetscape, a home interior). Avoid snow scenes, palm trees, mountains or foreign cities.
   - Never use photos of identifiable people, real listings, other agents' or brokerages' photos, logos or
     watermarked images, Google/Zillow/MLS images, or AI images that pretend to be a real Waxhaw place.
   - Never reuse the same photo as one of the last 10 posts. alt text describes the photo plainly (no people).
5b. Branding (automatic): after saving the post, run `python3 make_card.py posts/<file>.html`. It renders
   `docs/cards/<slug>.jpg`, a navy-and-gold 1200x630 card with David's logo, the post title, his headshot,
   980-350-8686 and the brokerage name. The builder uses that card as the featured image (top of post, RSS
   enclosure, Lofty thumbnail), moves the stock photo below the first paragraph, and adds an "About David Morton"
   box with logo and headshot above the brokerage line. The card label is "<first tag> · <second tag>", so put
   the town first and the category second in `tags:` (or set `card_label:`). Look at the rendered card before
   committing. Brand assets live in `docs/brand/` (logo-gold.png, logo-gold-600.png, headshot.jpg) — never alter them.
   Only if you could actually view the stock photo may it be used; if image hosts are blocked, say so in the report.
6. Self-check before committing: every number matches its source; only 980-350-8686 appears; Fair Housing
   rules pass; title/description lengths; brokerage line present. If anything fails, fix it. If you can't
   produce a post that passes, commit nothing and tell David.
   Then run `python3 seo/seo_check.py check posts/<file>.html`. Every FAIL must be fixed before committing;
   fix warnings too unless doing so would make the writing awkward.
7. Save as `posts/<today's date ET>-<slug>.html`, run `python3 make_card.py` on it, then `python3 build_feed.py`,
   then `python3 seo/seo_check.py mark posts/<file>.html`, commit ("Post: <title>", including seo/keyword-map.csv)
   and push to `main`.

## SEO engine files (seo/)
- `keyword-map.csv` — every target keyword with its town, category, priority (1 = core market), the area page it
  must link to, and the date it was used. Add rows freely; never clear a `used_on` date.
- `seo_check.py` — `next` / `check` / `mark` (see its docstring).
- `rank-log.csv` — written by the weekly SEO autopilot: date, keyword, whether DavidMortonSoldIt.com showed in the
  web results checked, and the best position seen. It's a rough spot check, not a rank tracker.
