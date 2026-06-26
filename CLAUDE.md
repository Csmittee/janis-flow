# CLAUDE.md — janis-flow
> Version 1.0 — 2026-06-25
> Changes: Initial creation — governance seed
> Previous: NONE

Project: Janis Flow — Skateboard, surfskate, and lifestyle gear mini-site (BUS04)
Domain: flow.janishammer.com
BUS ID: BUS04

Governance: ALL rules at janishammer-central/RULES.md + .claude/rules/
Read janishammer-central CLAUDE.md before reading anything in this repo.

Injector:
  injector-config.js — YES — sync from assets.janishammer.com
  injector-core.js   — YES — sync from assets.janishammer.com

Local key files:
  index.html                       — EN homepage (980L ⚠️ OVER 800 LINES)
  product/*.html (27)              — EN product pages (generated)
  th/product/*.html (27)           — TH product pages (generated)
  scripts/generate_product_pages.py — Airtable → bilingual product HTML

Critical constraint: index.html is 980 lines — over the 800-line limit.
Do not edit without reading RULES-html.md (HTML-1) and proposing a split plan
to the owner first. See RETROFIT_QUEUE item #9.

Tech: Vanilla HTML/CSS/JS · Airtable · Python build · GitHub Actions · Cloudflare Pages
