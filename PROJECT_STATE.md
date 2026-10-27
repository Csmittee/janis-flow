# PROJECT_STATE.md — janis-flow
> Version 1.1 — 2026-10-28
> Changes: Flow SEO status (CC_SESSION_flow_seo_v1): canonical, hreflang, og/twitter, sitemap.xml, robots.txt, real card links, workflow commit step; SEO baseline; open issues updated
> Previous: Version 1.0 — 2026-06-25 (Initial creation — bootstrap scan)

## Status: LIVE
## Domain: https://flow.janishammer.com
## Last observed state: EN+TH homepage live. 27 product pages per language (EN + TH). Airtable-driven product generation active. Skateboard/surfskate product catalogue.
## Tech stack: Vanilla HTML/CSS/JS · Airtable · Python build · GitHub Actions · Cloudflare Pages
## Injector version: UNKNOWN — loads directly from assets.janishammer.com without version pinning

## Folder structure:
  Compliant: NO
  Issues: index.html at repo root. No /public/ folder. product/ subdirectory for generated EN product pages. th/ and th/product/ for TH versions.

## SEO status — 2026-10-28 (CC_SESSION_flow_seo_v1, janis-flow PR 1):
  Canonical: home / and /th/, every product page /product/[slug] and /th/product/[slug] (extensionless) — DONE (pending owner QA)
  Hreflang:  en / th / x-default (→ EN) on home pair and every product pair, byte-identical — DONE (pending owner QA)
  OG / Twitter: og:url extensionless, og:type website, twitter card/title/description/image on home + product pages — DONE (pending owner QA)
  Sitemap:   sitemap.xml written by scripts/generate_product_pages.py from the page loop (2 homes + every EN/TH product page) — DONE (pending owner QA)
  robots.txt: hand-written, points to the sitemap — DONE (pending owner QA)
  Home cards: real <a href> product links (extensionless) — DONE (pending owner QA)
  Workflow:  product_build.yml commit step — CI-skip marker removed, sitemap.xml staged, DEP-6 retry loop — DONE (pending owner QA)
  Search Console: PARTIAL — Search Console sitemap + request indexing (owner task)
  NOT VERIFIED LIVE — owner QA steps 1–10 (janis-flow PR / janishammer-central PR).

## SEO baseline (SEO-10):
  owner-reported 2026-10-28: home page indexed, product page /product/darren-menditto-natty unknown to Google, no sitemap.
  Impressions / clicks (90 days): not recorded. Last audit: not recorded.

## SEO status (from bootstrap scan 2026-06-25 — superseded above):
  OG tags:   partial — og:title, og:description, og:image, og:url present. og:type MISSING. Twitter cards MISSING. OG image uses brand logo — not branded SEO_OG image.
  Canonical: missing on all pages
  Schema:    missing — no schema.org markup found
  Hreflang:  N/A — TH pages exist but not linked via hreflang

## Security status (from scan):
  No issues found. All Airtable credentials in GitHub Secrets.

## Open issues observed:
  - index.html 991 lines / th/index.html 992 lines (measured 2026-10-28) — OVER 800 limit (HTML-1); edited 2026-10-28 under owner approval, no split; split plan proposed in CC_CHAT_LOG
  - SEO DEBT — Product schema missing on product pages (SEO-3); LocalBusiness missing on home (SEO-3)
  - SEO-4 lengths (owner copy, not padded): product titles 18–47 chars (all 54 under 50); EN descriptions 145–160 (all in range); TH descriptions 74–160 (10 under 140 — Thai text has few spaces, word-safe cut stops earlier)
  - OG image is brand logo on home — not branded SEO_OG image
  - .github/workflows/product_build.yml uses actions/checkout@v3 and actions/setup-python@v4 (old versions) — report only
  - [skip ci] removed from the generator commit (was making Cloudflare Pages skip the deploy of generated pages)
  - Fixed 2026-10-28 (pending owner QA): og:type, twitter cards, canonical — see SEO status

## Session log (newest first):
### 2026-10-28 — CC_SESSION_flow_seo_v1
Generator: extensionless canonical/og:url, hreflang x3, og:type, twitter tags, escaped head text, word-safe description cut (≤160), recommended-card links extensionless, sitemap.xml writer. Workflow commit step: no CI-skip marker, sitemap staged, retry loop. Home pair: canonical, hreflang, og:url/og:type, twitter tags, real product links. robots.txt new. 54 product pages regenerated (27 EN + 27 TH); sitemap 56 URLs. DONE (pending owner QA).

### 2026-06-25 — Bootstrap scan
Seed CLAUDE.md, CC_CHAT_LOG.md, PROJECT_STATE.md created. No source files touched.
