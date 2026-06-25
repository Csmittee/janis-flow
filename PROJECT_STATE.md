# PROJECT_STATE.md — janis-flow
> Version 1.0 — 2026-06-25
> Changes: Initial creation — bootstrap scan
> Previous: NONE

## Status: LIVE
## Domain: https://flow.janishammer.com
## Last observed state: EN+TH homepage live. 27 product pages per language (EN + TH). Airtable-driven product generation active. Skateboard/surfskate product catalogue.
## Tech stack: Vanilla HTML/CSS/JS · Airtable · Python build · GitHub Actions · Cloudflare Pages
## Injector version: UNKNOWN — loads directly from assets.janishammer.com without version pinning

## Folder structure:
  Compliant: NO
  Issues: index.html at repo root. No /public/ folder. product/ subdirectory for generated EN product pages. th/ and th/product/ for TH versions.

## SEO status (from scan):
  OG tags:   partial — og:title, og:description, og:image, og:url present. og:type MISSING. Twitter cards MISSING. OG image uses brand logo — not branded SEO_OG image.
  Canonical: missing on all pages
  Schema:    missing — no schema.org markup found
  Hreflang:  N/A — TH pages exist but not linked via hreflang

## Security status (from scan):
  No issues found. All Airtable credentials in GitHub Secrets.

## Open issues observed:
  - index.html: 980 lines — OVER 800 limit — do not edit without split plan
  - og:type missing on index.html
  - Twitter card meta tags missing on all pages
  - No canonical tags on any page
  - No schema.org markup (LocalBusiness on homepage, Product on product pages)
  - OG image is brand logo — not branded SEO_OG image

## Session log (newest first):
### 2026-06-25 — Bootstrap scan
Seed CLAUDE.md, CC_CHAT_LOG.md, PROJECT_STATE.md created. No source files touched.
