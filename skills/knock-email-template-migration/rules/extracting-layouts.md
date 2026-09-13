---
title: Extracting layouts
description: Splitting shared chrome into Knock email layouts, deduplication, CSS strategy, MJML layouts, and default-layout policy
tags:
  - knock
  - migration
  - email
  - layouts
  - css
  - mjml
category: knock-email-template-migration
last_updated: 2026-09-08
---

# Extracting layouts

> **Phase 2 (plan) and phase 3 stage 2 (build) — Layouts.** Inputs: `analysis/_chrome-families.md`, the `[chrome]` sections of the analysis files, and the pulled `knock/layouts/` inventory. Outputs: `plan/layouts.md` at phase 2; `knock/layouts/<key>/` validated, pushed, and committed at phase 3. Read alongside: `rules/building-templates.md` for the block types the layout CSS must style; the `knock-cli` skill for `knock layout` commands.

The layout is the shared "frame": doctype, `<head>` CSS, background wrappers, header, and footer. At send time Knock injects the template body into the layout's `{{ content }}`. Getting the layout right is the fidelity keystone for block-first migrations, because markdown and button blocks emit nearly bare HTML and inherit their typography from layout CSS.

## What belongs in the layout

From each template's chrome sections (marked `[chrome]` in analysis files):

- The full HTML document skeleton: doctype, `<html>`, `<head>` (all CSS, meta tags, font `<link>` tags — note `@import` is not supported), `<body>`, and the outer wrapper tables
- Header (logo, nav) and footer (legal text, social links, address)
- Dark mode media queries and Outlook conditionals from the source — preserve verbatim
- A `{{ content }}` placeholder where the body sections were (required — a layout without it is invalid)
- A `{{ preview_text }}` slot replacing the source's hidden preheader div, if it had one
- Any `[chrome-data]` element from the analysis: the layout may read `data.*` (it renders in workflow scope), but every such field is part of the layout's own contract — list them in `plan/layouts.md`, guard each (`{% if data.update_count %}…{% endif %}`) so templates that do not send the field render cleanly, and prefer `vars.*` when the value is account-constant. The reverse also holds: a template that **adopts** an existing layout (a no-chrome fragment given the `default` layout, a new member of a live family) inherits that layout's contract — every `data.*` field the layout reads becomes a field this template's trigger must send. List those fields in the template's contract and raise the adoption as `❓blocking`, because it changes the trigger payload
- Optionally `{{ footer_links }}` if the user wants dashboard-configurable footer links

Header/footer can be inlined in the layout or extracted as partials rendered from the layout (`{% render 'email-footer' %}`) — prefer partials when the same header/footer also appears in emails that use a *different* layout, or when the user wants them editable as components. Layouts render in the full workflow scope, so they can pass `data.*`/`recipient.*` into those partials as args.

## Extracting the layout from the representative file

Splice with a script; never retype a multi-kilobyte `<head>`. `html_layout = head (+ your block-fidelity <style>) + header chrome + "{{ content }}" + footer chrome`, then swap the preheader's empty element for `{{ preview_text }}` and any per-template footer href for its Liquid form. Assert each anchor exists before slicing and diff the result against the source once. Per-builder anchors and quirks (SendGrid design editor, SendGrid legacy editor, BEE, compiled MJML) are in `references/builder-exports.md`.

## Deduplication

Group templates by chrome family (from `analysis/_chrome-families.md`). Then:

- **Identical chrome** → one layout.
- **Near-identical chrome** (same structure, small content differences like a headline color or a different footer sentence) → one layout, with the difference expressed as:
  - a template-set variable via `settings.pre_content` (Liquid assigns available above `{{ content }}` — e.g. `{% assign accent = "#1f4b99" %}`), or
  - an environment variable (`vars.*`) when it's account-global (support email; the app URL is the built-in `vars.app_url` every account has), or
  - Liquid conditionals in the layout only when driven by workflow scope (e.g. `tenant`).
- **Structurally different chrome** (e.g. transactional vs marketing) → separate layouts.

Target a small set — most migrations land on 1-3 layouts. Record the mapping in `plan/layouts.md`: layout key, member templates, and how variants are handled.

In an additive migration, the account's existing layouts join this comparison as reuse candidates — see "Additive migrations" in `rules/migration-process.md`. Tiebreak for a partial match (same logo, card, and footer spec but different markup): reuse a live layout only when every live template on it renders identically afterwards — re-render one live template per candidate layout to prove it — otherwise create the new layout and record the shared pieces (logo row, card frame, footer) as follow-up partial candidates in `plan/partials.md`. A new layout that keeps live emails byte-identical is not the "near-duplicate" failure the additive rule warns about; a silently changed live email is. If a reused live layout already sets button colors with `!important` (an older migration, or a hand-built layout), a new template's `style_attrs` will be masked: prefer removing those properties from the layout when a re-render of one live template per layout shows no change (its buttons carried the same colors on the block, or the layout value was the only source and you move it onto each live block); otherwise carry the new template's CTA as a small `html` block and record the loss of editor-level button editing as a `❓default`.

### Default layout policy

Every account starts with a stock layout keyed `default`, and out of the box it is the layout a template gets unless it names another — including templates the customer creates in the dashboard after the migration. So the migrated layout that should carry that key is the one used most often: the chrome family with the most member templates. Decide from the preflight inventory, and record the decision in `plan/layouts.md`:

- `default` is **stock and unused** (no non-stock colors, fonts, or `{% render %}` tags in its `html_layout`, and no existing workflow on it — every fresh account): replace it with the dominant family's layout as a `❓default`, applied unless vetoed at the checkpoint, with the reason on the plan line ("dashboard-created templates will use it"). Other families get keyed layouts (e.g. `marketing`).
- `default` is **customized, or in use by a live workflow**: `❓blocking` — list the workflows it would change and offer a keyed layout for the dominant family as the alternative.

Either way it is never overwritten silently (guardrail 7): the checkpoint's accepted default list is the confirmation.

## File structure

```
knock/layouts/<layout-key>/
├── layout.json
├── html_layout.html      # or html_layout.mjml when is_mjml
└── text_layout.txt
```

Note the naming asymmetry: the directory is `layouts/`, the CLI topic is `knock layout`, but the commit resource type is `email_layout`. Writing layouts under an `email-layouts/` directory means the CLI never finds them.

```json
{
  "name": "Transactional",
  "html_layout@": "html_layout.html",
  "text_layout@": "text_layout.txt",
  "footer_links": [{ "label": "Unsubscribe", "url": "{{ vars.commercial_unsubscribe_url }}" }]
}
```

Rules:

- An HTML layout must be a complete document (`<html>` and `<body>` tags present) containing `{{ content }}`.
- **Liquid executes inside HTML comments.** A `<!-- … {% assign x = "y" %} … -->` note runs on every render. Put explanations in `{% comment %}…{% endcomment %}` or in `plan/layouts.md`, never as literal tags in an HTML comment.
- **`text_layout` is required.** Write a minimal plaintext frame — `{{ content }}` plus a text footer mirroring the HTML footer's essentials. Migrate a source `.txt` layout if one exists.
- `footer_links` is optional; only include it if the layout renders `{{ footer_links }}`.

## CSS strategy for block-first fidelity

Three CSS layers must end up in the layout `<head>`:

1. **The source template's own CSS**, copied verbatim (media queries, client hacks, fonts).
2. **Typography for markdown blocks.** Markdown blocks render as `<p>/<h1>/<a>/<ul>` inside `.block-markdown` cells with no styling of their own. Map the source's body-copy styles onto them:

```css
.block-row--markdown-v1 .block-markdown p {
  font-family: Helvetica, Arial, sans-serif; font-size: 16px; line-height: 1.5; color: #333333;
}
.block-row--markdown-v1 .block-markdown a { color: #1f4b99; text-decoration: underline; }
```

3. **Button typography and padding for button_set blocks.** Colors, radius, and border belong on the block's `style_attrs` and alignment on `layout_attrs` (see `rules/building-templates.md`); layout CSS covers only what those attributes cannot express — font family, size, line height, letter spacing, and padding — and needs `!important` to win over Knock's runtime-injected sizes. **Never set `background-color`, `color`, `border-color`, `border-radius`, or `border-width` in layout CSS**: an `!important` there silently masks every template's own button color, validation does not catch it, and only a render does.

```css
.block-row.block-row--button_set-v1 .block-button--solid {
  font-family: Helvetica, Arial, sans-serif !important; font-size: 16px !important;
  line-height: 16px !important; letter-spacing: 0 !important; padding: 12px 24px !important;
}
```

**Match Knock's base block selectors.** At render time Knock injects its own block CSS at the top of the `<head>`, then inlines everything into the blocks. Its selectors are more specific than a bare `.block-row--<type>-v1` override, so a lower-specificity rule *adds* to the base rule instead of replacing it. Write overrides as `.block-row.block-row--<type>-v1 …`, and **render one preview before writing any block CSS** — the injected base rules are visible at the top of the rendered head. The per-block selector table, the cell padding every block carries (overriding it needs `!important` — Knock appends its own padding to the inlined style after yours), and the quirks of the image, html, and partial blocks are in `references/knock-blocks.md`.

**Where CSS lives: partial by default, layout for what's shared.** CSS that only matters when one component is present (an item card's grid, a callout's colors, their mobile media queries) defaults to that partial's own `<style>` blocks — Knock hoists partial styles into the layout `<head>` at compile time, deduplicated, only for emails that actually use the partial (see `rules/extracting-partials.md`). The layout keeps everything shared: the document skeleton, typography, fonts, the block base-style overrides above, **cross-component design tokens** (dedupe collapses only identical style blocks — overlapping rules spread across different partials all ship, so shared tokens need one home), and **dark mode / theming overrides** (hoisted partial styles insert at the *top* of the head, so later layout rules — dark-mode `!important` overrides, `vars.branding.*` theming — win at equal specificity).

This split is a default, not a mandate. When the source is one tangled stylesheet whose selectors don't factor cleanly per component, keep it intact in the layout — fidelity beats architecture during a migration. Move CSS into a partial only when the extraction is clean and verifiable, and record the fuller component-CSS refactor as a follow-up in the final report.

If the source design maps cleanly onto Knock branding, propose (as an opt-in) moving brand colors/logo to account branding and referencing `vars.branding.primary_color`, `vars.branding.logo_url`, etc. in the layout. Default is to hardcode the source's values — it changes nothing about how the emails look.

## MJML layouts

For standard-MJML sources, keep the layout in MJML:

- Set `"is_mjml": true` in `layout.json`; the layout file becomes `html_layout.mjml`.
- The layout must be a **complete MJML document** with a root `<mjml>` tag.
- `{{ content }}` goes where body sections were (template fragments and visual blocks render as MJML components inside it).
- Plain HTML inside an MJML layout (e.g. a `{{ footer_links }}` slot) must be wrapped in `mjml-raw`.
- Source `<mj-attributes>`, `<mj-style>`, and font setup stay in `<mj-head>` — that's the MJML equivalent of the CSS strategy above.

MJML layouts pair with MJML or visual-block templates. HTML partials still work inside them (Knock auto-wraps partial output in `mjml-raw`).

## Validation and push

```bash
knock layout validate <key>      # command topic is `layout`; files live in knock/layouts/
knock layout push <key>          # by key, never --all: the pulled `default` layout sits in the same directory
knock commit -m "Migration: email layouts" --resource-type=email_layout --resource-id=<key> --force
```

Layouts must be committed before workflow templates that reference them will render with them. A template's `settings.layout_key` must name a layout that exists in the environment, or the workflow push fails validation.
