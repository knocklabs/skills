---
title: Analyzing source templates
description: Format detection, source-format preservation rules, and the per-template analysis file
tags:
  - knock
  - migration
  - email
  - mjml
  - handlebars
  - analysis
category: knock-email-template-migration
last_updated: 2026-09-08
---

# Analyzing source templates

> **Phase 1 of 4 — Analyze.** Inputs: the source files (from `knock-migration/source/`) and the intake section of `MIGRATION.md`. Outputs: `analysis/_chrome-families.md` from the corpus scan, then one `analysis/<stem>.md` per template or variant set. Read alongside: `rules/mapping-variables-and-logic.md` for the "Proposed mapping" column and the control-flow classes.

Phase 1 turns each source file into a structured analysis document, written to `knock-migration/analysis/<stem>.md` before the next template is opened.

## Format detection

Classify every file in the source directory first, and record the inventory in `MIGRATION.md`. The signal → classification table is in `references/syntax-and-format-tables.md`; read it once per corpus. In short: compiled MJML and builder exports migrate as their HTML (the builder's own module markup marks the section boundaries — see `references/builder-exports.md`); standard MJML stays MJML; component sources (React Email, Vue) must be rendered to HTML first; headless fragments and plain-text files need a layout decision (`❓default`); structural defects (no `<body>`, unclosed `<head>`, stray closing tags) are repaired in the layout and listed under `## Markup defects`; `.txt` companions become `text_body`; provider `.json` exports are mined for subjects and senders.

## Choosing the target format: preserve what Knock can execute

Knock supports MJML natively (MJML layouts, MJML template bodies, visual blocks that render as MJML components). The rule is to **preserve the customer's authoring format whenever Knock can execute it**:

- **Standard MJML sources** → migrate as MJML: MJML layout + MJML/visual-block template bodies. Do not flatten to HTML. Exception: partial *content* must be HTML (partials cannot contain MJML) — see `rules/extracting-partials.md` for extracting partial HTML from compiled output.
- **MJML with custom components** → the MJML cannot run in Knock. Use (or ask the user for) the compiled HTML as ground truth; use the MJML to identify component boundaries and semantic names (a custom `<eds-footer>` tag is a partial candidate with a name already chosen for you).
- **HTML sources** → migrate as HTML.
- **Mixed directories** → decide per template set, not per file; templates sharing chrome should land on the same layout and therefore the same format. Flag mixed-format chrome as a ❓ for the plan checkpoint.

Verify "standard MJML" by compiling: `npx mjml <file> -o /dev/null`. Unknown-tag errors mean custom components. For HTML builder exports, open the representative file of each family in a browser once (serve the source copy with a static file server — browser tools refuse `file://` URLs; see the visual-pass recipe in `references/verification-recipes.md`) to confirm it renders standalone — a file that depends on the provider injecting `<head>` content or images will look wrong here and needs a layout decision before analysis proceeds. Record the verdict as a `renders standalone: yes | no` line in the family's entry in `analysis/_chrome-families.md`.

## Corpus scan: chrome families and variant sets (do this first)

Before per-template analysis, make one cheap pass over the whole corpus — it drives the layout plan and prevents redundant analysis:

1. For each file, slice the chrome regions: everything before the first body section (doctype/head/CSS/wrapper/header) and everything after the last (footer). Builder exports mark the boundaries with their module markup (`references/builder-exports.md`); for hand-authored or legacy files anchor on the card wrapper that carries the background color, not on `<body>` — a `<body>`-based trailer hashes to the same value for every family, so for those files the markers in step 2 are the primary grouping key. Before hashing, normalize: collapse whitespace runs, blank out `<title>…</title>`, and replace every variable expression with a placeholder — otherwise a per-file title or a footer variable gives every file its own hash.
2. Group templates whose chrome hashes match (or near-match after ignoring obviously variable content). Confirm the grouping with a second, marker-based signal that survives hand edits: builder class names (`sg-campaigns`, `sg-image`, `row-content`), the wrapper's background color, the logo URL, the primary button color. Each group is a **chrome family** — name it (e.g. `acme-transactional`) and pick a representative file. Headless fragments and plain-text files form their own group, `none`, with no chrome. Mark members you grouped by hash or marker but did not open as `(probable)`.
3. During the same pass, pair **variant sets**: templates whose *bodies* are near-duplicates (e.g. `order-batched` / `order-single`, per-plan copies of one email). These become consolidation candidates and share one analysis file.
4. Hash each **whole file** and each **body** (chrome stripped) too. Byte-identical files under different names are one template — key it on the first and record the others as aliases. An identical *body* under an unrelated name (a file named for product A that contains product B's email) is a possible mislabeled export: flag it `❓blocking` and do not migrate it until the user confirms which name is right. Any `(probable)` family or variant claim that a plan decision will rest on must be confirmed by opening the file — hashing groups, it does not verify. In the analysis files, cite reuse evidence that rests on an unopened member as such (`also appears in x.html (probable)`) so phase 2 knows which siblings to open.

Write the results to `analysis/_chrome-families.md`: per family — name, member templates, representative file, any notable per-member chrome differences, and the family's **chrome copy verbatim** (header line, footer sentences, legal text) — the text oracle reads it alongside each template's body copy. Chrome is described **once** here; per-template analysis files reference the family by name and never re-describe it.

The scan's second output is `analysis/_conventions.md` — the corpus-wide notes every later step (and every parallel analysis agent) needs: the templating syntaxes found and which files use which, the malformed-expression convention in force (e.g. "`{{x}` is Mako `${x}`"), forced renames, remaps approved in earlier passes, and key-derivation rules for directory-based or duplicate files. Phase 2 updates it with the approved decisions so a later pass inherits them.

## The analysis file

Write one file per template — except variant sets, which share one file with a common base plus a short per-variant section for the deltas (copy, subject, extra sections). Sharing a file is an analysis convenience for near-identical siblings; it does not decide whether they become one workflow or several — the plan decides that. This template wins over any analysis files already in the workspace — earlier passes may predate a slot; do not copy their omissions.

The template lives in `references/analysis-file-template.md`; use its structure exactly (later phases parse it), copy it when writing the first analysis file, and hand it to every parallel analysis agent. Its sections, in order: header fields, structure outline (sections marked `[chrome]` / `[chrome-in-body]` / `[chrome-data]` / `[body]`), body copy (verbatim), variant deltas, markup defects, partial candidates, variables, control flow, assets and links, style notes, provider artifacts, open questions tagged `❓blocking` / `❓default` / `❓fyi`.

Tag every ❓ with one of the three levels. A 15-template corpus produces around a hundred open questions; without levels the checkpoint is unanswerable. Blocking is rare — a handful per migration.

## What to look for

### Chrome vs body

Chrome is the shared **frame**: doctype/`<head>`/CSS, background wrapper tables, header (logo), footer (links, legal, social). Body is the content between them. Shared *content* components (a repeated heading style, a CTA, an admin note that appears in ten emails) are not chrome — they are partial candidates. Chrome that sits *between* body sections (a divider module after the prose but before the button, an empty "code" slot that one template fills) cannot go in the layout; mark it `[chrome-in-body]` so the build carries it in the body as a block. Frame elements that read template variables (a header line like "Showing {{count}} updates", footer links built from `account_id`) are `[chrome-data]`: they stay in the layout, which renders in workflow scope, but the fields they read become part of that layout's contract (listed in `plan/layouts.md`) and must be guarded so a template that does not send them still renders cleanly. Mark each top-level section `[chrome]`, `[chrome-in-body]`, `[chrome-data]`, or `[body]` and reference the chrome family assigned in the corpus scan — the family definitions in `analysis/_chrome-families.md` are the input to layout deduplication (`rules/extracting-layouts.md`).

### Body copy is captured verbatim

The analysis file is the build phase's source for prose, so the `## Body copy (verbatim)` section must contain the **exact text of every body section** — complete, in order, with source variable expressions in place. No ellipses, no summaries, no paraphrase: a summarized analysis forces the build to reconstruct copy, which drops sentences and fabricates new ones. Verification later asserts this text against rendered output (`rules/verifying-the-migration.md`).

Conventions for the quoted text: keep inline tags that carry meaning (`<b>`, `<a href="…">`, `<br>`) and any control-flow lines in place; drop block wrappers (`<div>`, `<td>`, `<table>`) and describe their styling in the outline instead; write entities decoded (`&nbsp;` → space, `&#39;` → `'`); quote headings, button labels, and image alt text as their own lines labelled with their section number. Verification strips tags and control-flow lines before matching, so the quote stays comparable to rendered output. Edge cases: quote `<ol>`/`<ul>` items as `1.` / `-` lines; quote a loop body once, with its control lines around it, not once per item; when a block element sits inside an inline one (`<a><div>…</div></a>`), keep the inline tag and drop the inner block wrappers; a section whose whole content is one variable is quoted as the bare expression on its own line (the oracle skips variable-only segments); record an empty button label or heading, and a spacer-only element (an `&nbsp;` paragraph, an empty row), as its own section with `(empty)` copy — a button with no label and no href is listed the same way and dropped at the plan as a `❓default`; copy the source engine never rendered (text trailing a Mako control line) goes under `## Suspected source mistakes`, not in the quote; emphasis carried by a class or an inline style (`<span style="font-weight:900">`, a styled `<p>` wrapper) goes in `## Style notes`, not in the quote.

### Variables and source syntax

Identify the templating syntax before extracting variables — it determines which translation table applies. The syntax families and their variable, conditional, and loop forms (Handlebars/Mustache, Mailchimp, SendGrid legacy substitutions and slots, Mako, Ruby and Python interpolation, Liquid, Jinja, code interpolation) are tabulated in `references/syntax-and-format-tables.md`.

Three rules the tables cannot express:

- **Malformed expressions** (`{{x}` with a single closing brace, `{x}}`, leftovers of a bad find/replace) are common in exports. Record the expression verbatim, map it as the nearest family (`{{x}` → `{{ data.x }}`), and flag the file once (`❓default`: "confirm these were `${x}` Mako expressions") — not once per occurrence.
- **Mixed syntaxes in one file** happen (a Jinja loop inside a SendGrid template with Mako substitutions). Record the family per expression in the Variables table and flag the mix as `❓fyi`; do not force one translation table on the whole file.
- **Look-alikes**: Jinja/Nunjucks `.length` → Liquid `| size`; `elif` → `elsif`; Handlebars `{{{raw}}}` and Liquid `{{ raw }}` both render unescaped (see the escaping note in the Variables section).

Record every variable with its source expression verbatim. For Liquid-family sources, still record filters used — Knock's Liquid supports a specific helper set (see the Knock docs "Liquid helpers reference"); non-standard filters are ❓ items.

If templates were extracted from application code, ask the user whether conditionals/loops lived in the surrounding code — that logic must be re-expressed in the template or workflow (see control-flow rules).

### Control flow classification

Classify every conditional and loop now as one of the classes the decision rules in `rules/mapping-variables-and-logic.md` consume: **inline copy variation** (words change within a section), **section toggle** (a whole section shows or hides), **whole-body variant** (the same email as several files or one big conditional, e.g. `order-batched.html` vs `order-single.html` — a consolidation candidate, flag ❓), or **loop over a collection** (a repeated component is also a partial candidate with a `list` input).

### Subject line discovery ladder

Knock requires a subject on every email template. Search in order; record the source; anything below step 3 is a ❓ requiring approval:

1. Provider metadata — subject and sender fields in an export JSON, adjacent config, or the code that sent the template. An example *payload* file is not metadata: it feeds the data shape, and the ladder moves on
2. A meaningful `<title>` tag — specific to this email and not shared by *different* emails (files that are byte-identical or variants of one email count as one), and not just a product name (builder exports usually leave it empty — check)
3. The preheader/preview text (often mirrors the subject)
4. **Draft one** from the email's main heading and purpose, marked `DRAFTED — needs approval ❓default`. Write drafted subjects in Knock Liquid on the `data.*` contract as the source implies it (`Order {{ data.order_id }} has shipped`), variables allowed; the plan rewrites them to the approved namespaces at the checkpoint (`{{ actor.name }}` once an actor remap is approved) so `workflow.json` always matches the final contract. Mirror a conditional heading only if the user asks for it.

Step 1 assumes access to the sending code or a provider export; when neither is available, say so in the analysis file and move on to step 2.

### Preview text

A hidden preheader (`display:none` div at the top of the body) becomes the template's `preview_text` field, and the div's *slot* moves into the layout as `{{ preview_text }}`. Record both the text and its location.

## Batching

Process 5-10 templates per sitting, updating the `MIGRATION.md` status board after each file. The analysis file must be complete enough that phases 2-3 never re-open the source template except to copy exact markup and body copy during builds.
