---
title: Extracting partials
description: Identifying design-system components, authoring input_schema, the isolated scope rule, and email-safe partial content
tags:
  - knock
  - migration
  - email
  - partials
  - design-system
  - input-schema
category: knock-email-template-migration
last_updated: 2026-09-08
---

# Extracting partials

> **Phase 2 (plan) and phase 3 stage 1 (build) — Partials.** Inputs: the "Partial candidates" sections of the analysis files and the pulled `knock/partials/` inventory. Outputs: `plan/partials.md` at phase 2; `knock/partials/<key>/` validated, pushed, and committed at phase 3 — before any layout or workflow that uses them. Read alongside: `rules/building-templates.md` for how a `partial` block binds inputs.

Partials are the design-system payoff of the migration: reusable HTML components with typed inputs, available as drag-and-drop blocks in the visual editor. Extract them well and the customer can build *new* emails from their own components, not just edit migrated ones.

## What makes a partial candidate

From the analysis files' structure outlines, a section is a partial candidate when any of these hold:

1. **Repeated across ≥2 templates** with the same structure (callout boxes, item/product cards, comment cards, stat rows, header/footer variants).
2. **Single-use but semantically a component** — a self-contained unit with a clear name and obvious inputs (e.g. an order-summary card). When in doubt on single-use sections, prefer an `html` block in the template and note the candidate in `plan/partials.md` for the user to decide.
3. **Multi-column section.** Visual blocks stack vertically, so side-by-side layout lives inside a single block — make it a partial to keep it editable (an `html` block keeps it frozen).
4. **A custom-styled button** that `button_set` + layout CSS can't reproduce (gradients, icons inside the label, nested tables for Outlook rounding).
5. **The repeated unit of a loop** (each item in `{{#each items}}`) — see "Repeated partials and loops" below for the two forms and how to choose.

Anti-patterns: don't create partials for one-off prose, for whole email bodies, or for trivial spacers (use `divider`/`markdown` blocks). One partial, one purpose.

A candidate can also resolve to a **built-in block**: a standard CTA is a `button_set` with `style_attrs`/`layout_attrs`, a picture is an `image` block, a bold centered heading is markdown `#` plus layout CSS. Record the disposition per candidate in `plan/partials.md` — partial, built-in block, or `html` block — so nothing is partialized that a block already does.

Record every partial in `plan/partials.md` with: key, name, description, which templates use it, drafted `input_schema`, and an example invocation.

In an additive migration, existing account partials join the candidate comparison for reuse or extension — see "Additive migrations" in `rules/migration-process.md`.

## The isolated scope rule (critical)

Partial content renders in an **isolated Liquid scope**: only the arguments explicitly passed to it plus `vars` are visible. `data`, `recipient`, `actor`, `tenant`, and batch variables are NOT available inside partial content.

- Partial content uses **bare variable names**: `{{ title }}`, `{{ items }}` — matching `input_schema` keys.
- Callers bind workflow values at the call site:
  - Visual block editor / `partial` block `attrs`: `"attrs": { "title": "{{ data.title }}" }` (attr values evaluate in the outer scope, then pass in).
  - Code editor / layouts: `{% render 'item-card', title: data.title %}` (Knock's render tag doesn't support `for`/`with` modifiers — use `{% for %}` loops and `{% assign %}` instead).
- `vars.*` is the only ambient namespace — safe to use directly inside partials for account-level values.
- Inputs are **plaintext strings by default**. Booleans and JSON become strings unless the schema field type is `boolean`, `json`, or `list`. A string `"false"` is truthy in Liquid — use typed fields, or `| from_json`, or compare `== "true"`. A scalar input bound to a value that is **missing** in the workflow arrives as `""`, not as a missing key, so guard with `!= blank` rather than a bare `{% if %}`. Workflow-scope behavior does not predict isolated-scope behavior — every partial must be rendered once with each optional input absent (see the verify rule).
- Partials nest up to 5 levels deep (partials may render other partials).

## Repeated partials and loops

A `partial` block in the visual editor renders **once** — blocks cannot be wrapped in `{% for %}`. When the source repeats a component per item (product cards, line items), choose deliberately:

- **`list`-input partial (default).** The partial takes the whole collection — a `list` schema field bound to `{{ data.items }}` — and loops internally with `{% for item in items %}`. The component stays a drag-and-drop block and remains fully editable in the visual editor.
- **`html` block wrapping the loop.** `{% for item in data.items %}{% render 'item-card', title: item.title %}{% endfor %}` inside an `html` block. Use only when per-item markup must interleave with other content, or the loop logic can't live inside the partial. The loop drops out of the block editor's editable surface (the partial itself stays editable as a resource).

The same two forms apply in HTML-mode templates, where both are plain code and the tradeoff is only about where the loop logic lives.

## Authoring input_schema

Every migrated partial gets an `input_schema` so editors see form fields instead of raw Liquid. Choose field types from the content:

| Content | Field type | Notes |
| ------- | ---------- | ----- |
| Short label, heading | `text` | `minLength`/`maxLength` in settings |
| Rich copy | `markdown` | Rendered as HTML |
| Long plain text | `textarea` | |
| Toggle a section | `boolean` | Preserves real true/false |
| Numeric (counts, prices) | `number` | Optional min/max, unit |
| Brand/accent color | `color` | Hex |
| Enum variants (info/warning) | `select` / `multi_select` | `options: [{label, value}]` |
| CTA | `button` | `text` + `action` subfields |
| Link | `url` | |
| Picture | `image` | `url` + `alt` + `action` subfields |
| Structured object (user, order) | `json` | Optional validation schema; preserves structure |
| Collection to iterate | `list` | Optional `item_schema` describing each item |

Field shape: `{ "type", "key", "label", "settings": { "required", "default", "description", ... } }`. Keys must exactly match the `{{ key }}` variables in the content. Give required inputs `"required": true`; give cosmetic inputs sensible `default`s. Set `icon_name` and a `description` (≤280 chars) so the block is recognizable in the editor sidebar. `icon_name` is validated against a pinned set of Lucide icon names even though the API types it as a free string — an invalid name fails validation with an error that names the field but not the allowed values. Stick to known-good names (`BellDot`, `Flag`, `LayoutList`, `LayoutGrid`, `MessageCircle`, `Megaphone`, `Lightbulb`, `Package`, `Tag`, `Minus`, `MapPin`) and note the set uses **current** Lucide naming (`CircleAlert`, not the legacy `AlertCircle`); for any other name, `knock partial validate <key>` rejects an unknown icon before anything is pushed, so try it and validate rather than guess.

For structured inputs, callers pass Liquid references: a `list` field bound to `{{ data.items }}`, a `json` field bound to `{{ recipient }}` — then the partial iterates `{% for item in items %}` directly.

## Partial content rules

- **Email-safe HTML only**: table-based layout, no external stylesheets, no flex/grid. Copy the source markup exactly — including Outlook conditional comments (`<!--[if mso]>…<![endif]-->`) — then replace hardcoded copy/URLs with `{{ input }}` variables.
- **Component CSS travels with the partial.** Inline styles are the baseline, but a partial can also include `<style>` blocks — at compile time Knock hoists them to the top of the layout's `<head>`, deduplicated so they appear at most once per email. Use them for the component's class-based rules and, critically, its **responsive media queries** (which can never be inlined). Rules of the road:
  - Scope selectors narrowly (prefix with a partial-specific class like `.item-card`) — these styles land in the shared head.
  - Hoisted styles insert at the *top* of the head, so layout rules can override them at equal specificity; keep cascade order in mind.
  - Liquid `{% assign %}` used by a style block must live *inside* the `<style>` tag (the body's assigns are out of scope after hoisting).
  - Hoisting only happens **when the template uses a layout**. For templates with `"layout_key": null`, a partial's `<style>` blocks are dropped — those partials must rely on inline styles.
  - Multiple `<style>` tags are fine as long as they share the same parent element.
  - Keep only *this component's* rules here. Tokens shared across components, and dark-mode/theming overrides, belong in the layout (dedupe collapses only identical style blocks, never merges overlapping rules) — see `rules/extracting-layouts.md` for the split and for when a tangled source stylesheet should stay in the layout entirely.
  - Prefer static CSS in style blocks; blocks whose CSS depends on Liquid may not deduplicate across uses.
- **Partials cannot contain MJML.** For MJML sources, obtain the compiled HTML of the template (the paired `.html` export, or compile with `npx mjml`), locate the section corresponding to the component, and use that compiled HTML as the partial content. Knock auto-wraps HTML partials in `mjml-raw` when they render inside MJML templates/layouts, so the same partial works in both worlds.
- Use Liquid defaults only for cosmetic fallbacks (`{{ align | default: "center" }}`), never to invent transactional data.
- Guard optional inputs with `{% if subtitle != blank %}…{% endif %}` — `blank` matches missing keys, nulls, and empty strings alike; guard a list with `{% if items.size > 0 %}`.

## File structure

```
knock/partials/<partial-key>/
├── partial.json
└── content.html
```

```json
{
  "name": "Item card",
  "description": "Product image, title, and price row used in order emails.",
  "type": "html",
  "visual_block_enabled": true,
  "icon_name": "LayoutGrid",
  "content@": "content.html",
  "input_schema": [
    { "type": "image", "key": "image", "label": "Product image", "settings": { "required": true },
      "url":    { "type": "url",  "key": "url",    "label": "Image URL", "settings": { "required": true } },
      "alt":    { "type": "text", "key": "alt",    "label": "Alt text",  "settings": { "required": true } },
      "action": { "type": "text", "key": "action", "label": "Link",      "settings": { "required": false } } },
    { "type": "text", "key": "title", "label": "Title", "settings": { "required": true } },
    { "type": "text", "key": "price", "label": "Price", "settings": { "required": false } }
  ]
}
```

Composite fields (`image`, `button`) carry their subfields as **required top-level keys** on the field, each a full field definition: a button needs `text` and `action`, an image needs `url`, `alt`, and `action`. Write them out — the short form above does not validate for these types:

```json
{ "type": "button", "key": "cta", "label": "Button", "settings": { "required": true },
  "text":   { "type": "text", "key": "text",   "label": "Button text",   "settings": { "required": true } },
  "action": { "type": "text", "key": "action", "label": "Button link",   "settings": { "required": true } } }
```

In content, reference their parts as `{{ image.url }}`, `{{ image.alt }}`, `{{ button.text }}`, `{{ button.action }}`.

Rules:

- `type` must be `html` for anything used as a visual block (`visual_block_enabled: true` is only valid on HTML partials).
- Keys: lowercase slug, 3-255 chars, directory name = key. Check against the existing-partials inventory from preflight; collisions are ❓ items.
- Scaffold with `knock partial new -k <key> -n "Name" -t html --force`, then edit, or write the files directly.

## Validate, push, commit — before any template uses them

```bash
knock partial validate <key>
knock partial push <key>         # by key, never --all: pulled live partials sit in the same directory
knock commit -m "Migration: partials" --resource-type=partial --resource-id=<key> --force
```

Templates always render the **published** version of a partial. An uncommitted partial renders as missing in template previews and sends — this is why partials are stage 1 of the build order.
