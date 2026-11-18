# SEO fix backlog for DavidMortonSoldIt.com

The weekly SEO autopilot picks the top item that isn't marked done, writes exact step-by-step instructions
and ready-to-paste text for it, and sends them to David. When David says an item is done, mark it `[x]`
with the date. Add new items when the weekly health check finds problems. Priority order = list order.

## Foundation
- [x] 1. (2026-11-18: Lofty shows GSC, Bing and GBP connected, 6/6) Search Console + Bing: in Lofty (Website › SEO / Integrations) connect Google Search Console and Bing
      Webmaster Tools, then submit https://www.davidmortonsoldit.com/sitemap.xml in both. Bing also feeds ChatGPT/Copilot search.
- [x] 2. (2026-11-18: Lofty's Schema & Technical check reports all valid; custom JSON-LD optional) Business schema: paste seo/schema-realestateagent.json into Lofty's custom header code (Website › Settings ›
      Header/Tracking code), wrapped in <script type="application/ld+json"> ... </script>. Validate at
      https://validator.schema.org afterwards.
- [ ] 3. Google Business Profile: categories "Real estate agent" (primary) + "Real estate consultant"; service areas =
      Waxhaw, Weddington, Marvin, Charlotte, Matthews, Indian Trail, Fort Mill, Indian Land, Rock Hill; website link
      https://www.DavidMortonSoldIt.com; post the weekly GBP posts from seo/gbp/.

## Money pages (area pages are what should rank — blog posts feed them links)
- [x] 4. (2026-11-18 done: title/meta, new copy + FAQ, empty Map block removed. H1 is a locked template field; the Commute 'Coming Soon' tile is in a locked Lofty block) /waxhaw-NC: SEO title "Waxhaw NC Homes for Sale & Real Estate | David Morton" (52); meta description under
      155 chars; H1 "Waxhaw, NC Homes for Sale"; remove/hide the "Coming Soon" and "No Data" sections; add 300+ words
      of original local text + 3-question FAQ; remove off-topic links (Edgewater SC, Marvin communities) from this page.
- [x] 5. (2026-11-18: Weddington done; Marvin re-indexed (was noindex). Marvin page copy still to add from the Fix Kit) Same treatment for /weddington-NC and /marvin-NC.
- [x] 6. (2026-11-18 done; also removed Lofty AI 'Family-friendly'/'for families' wording) Same treatment for /charlotte-NC/ballantyne and /fort-mill-SC.
- [ ] 7. Same treatment for /matthews-NC, /indian-trail-NC, /wesley-chapel-NC, /monroe-NC, /mineral-springs-NC, /rock-hill-SC, /charlotte-NC.
- [ ] 8. Indian Land, SC has no area page (only /lancaster-SC). Add an Indian Land Feature Area in Lofty.
- [ ] 9. Add overview pages (Feature Areas) for Cortona, Rone Creek and The Bluffs at Wesley Chapel, which only have /listings pages.

## Clean-up
- [ ] 9b. Lofty area-page index switch: saving a Feature Area's SEO settings with 'Let search engines index this page' OFF publishes noindex. Always check it's ON before saving (Waxhaw, Weddington, Marvin were OFF; fixed 2026-11-18).
- [ ] 9c. Indian Trail and Wesley Chapel pages use a Charlotte skyline photo as the cover image; swap for a local photo.
- [ ] 9d. Form consent text on area pages says 'call 704-686-8897'; decide whether that should be the Lofty line 980-350-8686.
- [x] 9e. (2026-11-18) Removed Fair Housing wording from Lofty AI text on Fort Mill, Ballantyne, Indian Trail, Wesley Chapel, Rock Hill. Re-check any new Feature Area Lofty generates.
- [ ] 10. Older imported blog posts have broken titles/slugs (e.g. "/blog/h1-union-county-nc-restaurants-...",
      "/blog/-p-union-county-nc-homes-for-sale-..."). Fix the visible titles and SEO titles in Lofty. Only change a URL
      if Lofty can add a 301 redirect from the old one.
- [ ] 11. Cannibalization: at least 3 near-duplicate "Union County NC homes for sale" posts compete with each other.
      Keep the best one, expand it, and unpublish (or redirect) the others to it.
- [ ] 12. Mixed-case duplicate paths (/waxhaw-nc/canterfield-creek vs /waxhaw-NC/...): ask Lofty support to normalize
      or confirm canonical tags.

## Authority (off-site)
- [ ] 13. Claim/complete free profiles with identical name, phone (704-345-7218) and website: Zillow, Realtor.com,
      Homes.com, HomeLight, Bing Places, Apple Business Connect, Yelp, Nextdoor, Alignable, Facebook Page.
- [ ] 14. Reviews: ask 5 past clients for Google reviews that mention the town they bought/sold in
      (never script the wording or offer anything in exchange).
- [ ] 15. Local links: Waxhaw / Union County chamber membership listing, sponsor a local event page, guest post for a local site.
