---
title: Building templates and workflows
description: Composing email template bodies from visual blocks, HTML-mode fallback, workflow.json shapes, subjects, and channel overrides
tags:
  - knock
  - migration
  - email
  - visual-blocks
  - workflows
  - templates
category: knock-email-template-migration
last_updated: 2026-09-08
---

# Building templates and workflows

> **Phase 3 stage 3 — Workflows and templates.** Inputs: the approved `plan/workflows.md`, `plan/variables.md`, and each template's analysis file (body copy verbatim). Outputs: `knock/workflows/<key>/` with `workflow.json` and `email_1/visual_blocks/*`, each validated, pushed, read back, and committed. Read alongside: `rules/extracting-layouts.md` for the block CSS the layout provides; the `knock-cli` skill for `workflow.json` shapes and `knock workflow` commands.

Phase 3 turns each approved plan entry into a workflow with an email step. Consult the `knock-cli` skill's rules for file/path mechanics (the `@` suffix convention, path resolution, push semantics). This file covers what to build.

## Workflow shape

One workflow per template (unless the approved plan consolidated variants — see below), keyed per the plan. Key derivation, recorded in `plan/workflows.md` as `❓default` items: a top-level file → its stem, unless the stem is generic (`regular`, `empty`, `default`, `index`, `template`, `email`, `message`, a bare number), in which case derive the key from the template's purpose or subject (`invite/regular.html` → `account-invite`) and record the stem as an alias; a directory of variant files → the directory name minus any prefix shared with its siblings (`notifications-user-joined/` → `user-joined`), with the file stems becoming step refs or discriminator values; byte-identical files in two directories → one key for the shared purpose, the other paths recorded as aliases. Keys may contain only lowercase letters, digits, `_`, and `-`: normalize anything else predictably (`+` → `-plus`, spaces and dots → `-`, uppercase → lowercase) and record the rename as `❓default` — a new key changes no existing contract — unless the user set a naming convention at intake.

```
knock/workflows/<workflow-key>/
├── workflow.json
└── email_1/
    ├── visual_blocks.json
    └── visual_blocks/
        ├── 1.content.md
        └── 3.content.html
```

```json
{
  "name": "Password reset",
  "description": "Sends the password reset email. Migrated from password_reset.html.",
  "steps": [
    {
      "ref": "email_1",
      "type": "channel",
      "channel_key": "<from `knock channel list`>",
      "channel_type": "email",
      "name": "Password reset email",
      "template": {
        "subject": "Reset your password",
        "preview_text": "Reset link inside — expires in 30 minutes",
        "settings": { "layout_key": "transactional", "pre_content": "{% assign body_align = \"center\" %}" },
        "visual_blocks@": "email_1/visual_blocks.json"
      }
    }
  ]
}
```

- Channel steps are `"type": "channel"` with a `channel_key` from `knock channel list` — never guess the key.
- `subject` is required (approved in the plan). `preview_text` only when the source had one (the layout must expose a `{{ preview_text }}` slot).
- `settings.layout_key` names the committed layout; `"layout_key": null` means "no layout" (the body must then be a complete HTML/MJML document).
- Use `settings.pre_content` for Liquid assigns the layout reads. An assign there is visible throughout the layout, including the `<head>`, so a layout can carry per-template variants like `<style>… text-align: {{ body_align | default: "left" }} …</style>`. Keep it a one-line string; omit it on templates that take the default.
- Omit `text_body` to let Knock autogenerate the plaintext version; migrate a source `.txt` companion as `text_body@` when one exists.
- Hand-written files omit `__readonly` (the CLI writes it on pull) and may omit `trigger_frequency` and `settings.attachment_key` — the defaults apply. Pulled files carry all three; when editing a pulled file, keep whatever it carries.
- **Omit `categories` during the migration.** Accounts using centralized preference categories validate workflow categories against the project's preference-category catalog **at push time** (the error names the offending category; `validate` does not catch it). Propose the category taxonomy in the plan and final report as a follow-up, to be applied once the catalog entries exist.

## Block-first composition (default mode)

Decompose the body sections (from the analysis outline) into blocks. The email block types are `markdown`, `html`, `button_set`, `image`, `divider`, and `partial` — use only these. Blocks stack vertically; side-by-side layout (columns, grids) always lives inside a single `partial` or `html` block.

| Source section | Block | Rule |
| -------------- | ----- | ---- |
| Simple prose (headings, paragraphs, basic lists/links) | `markdown` | Only when markdown can express it losslessly; typography comes from layout CSS. Prose that sits in a column narrower than the card (an inline-block narrower than the layout frame) is reproduced only by padding the block cell in the layout (`.block-row.block-row--markdown-v1 .block-row__cell { padding-left/right }`) — note it in the plan |
| Standard CTA button | `button_set` | Set color, radius, border, and alignment **on the block** (`style_attrs`, `layout_attrs` — see below); layout CSS only for font family, size, and padding; a button partial only for shapes the block cannot express (gradients, icons in the label, nested Outlook tables) |
| Standalone image | `image` | `url`, `alt`, `action` |
| Horizontal rule/separator | `divider` | Styled via layout CSS |
| Component from the plan | `partial` | Bind inputs via `attrs`; renders once — for per-item repetition see "Repeated partials and loops" in `rules/extracting-partials.md` |
| Anything else (multi-column grids, nested tables, Outlook conditionals, bespoke markup) | `html` | Copy source markup verbatim |

**Never rewrite bespoke email markup as markdown.** When a section doesn't cleanly map, `html` block beats a lossy conversion — fidelity first, editability where it's free.

### visual_blocks.json

```json
[
  { "type": "markdown", "content@": "visual_blocks/1.content.md" },
  {
    "type": "partial",
    "key": "item-card",
    "name": "Item card",
    "attrs": {
      "image": { "url": "{{ data.image_url }}", "alt": "Product" },
      "title": "{{ data.item_title }}",
      "price": "{{ data.price }}"
    }
  },
  {
    "type": "button_set",
    "layout_attrs": { "horizontal_align": "center" },
    "buttons": [{
      "label": "Track order", "action": "{{ data.tracking_url }}", "variant": "solid",
      "style_attrs": { "background_color": "#1F4B99", "text_color": "#FFFFFF", "border_color": "#1F4B99", "border_radius": 4, "border_width": 0 },
      "size_attrs": { "size": "sm" }
    }]
  },
  { "type": "divider" },
  { "type": "html", "content@": "visual_blocks/5.content.html" }
]
```

- Number extracted content files by block position (1-indexed): `visual_blocks/1.content.md`, `visual_blocks/5.content.html`. Paths are relative to the file containing the reference.
- `button_set` blocks default to **left** alignment (`layout_attrs.horizontal_align: "left"`); almost every migrated email centers its CTA, so set `"center"` explicitly. Per-button `style_attrs` (`background_color`, `text_color`, `border_color`, `border_radius`, `border_width`) and `size_attrs` (`size`: always `sm`) are what the editor shows and edits — put the brand color there, not in layout CSS, which covers only what the attributes cannot (font, size, line height, letter spacing, padding — see `rules/extracting-layouts.md`). Labels and actions are Liquid-enabled — output *and* tags: `"label": "{{ data.button_text }}"` and `"label": "{% if data.is_admin %}Manage team{% else %}View team{% endif %}"` both render.
- Partial block `attrs` keys must match the partial's `input_schema` keys; values may be literals or Liquid evaluated in workflow scope (`{{ data.x }}`, `{{ recipient.name }}`).
- Block content is Liquid-enabled: inline conditionals and loops from the variable/logic mapping live inside markdown/html content files.
- Preserve `<!--[if mso]>…<![endif]-->` conditionals byte-for-byte inside html block content.

## HTML-mode fallback

Use raw HTML mode for a template when the user chose pixel-perfect mode at intake, or when the body is monolithic bespoke markup that would become one giant `html` block anyway:

```json
"template": {
  "subject": "…",
  "settings": { "layout_key": "transactional" },
  "html_body@": "email_1/html_body.html"
}
```

- `html_body` and `visual_blocks` are mutually exclusive.
- With a layout: strip the source's `<html>/<head>/<body>` wrapper — the body content only. Head CSS belongs in the layout.
- With `"layout_key": null`: keep the complete source document as-is (fastest lift-and-shift; no shared chrome benefits). Caveat: partial `<style>` blocks are only hoisted into a *layout's* head — with no layout, any partial used by the template must carry its styles inline (or the document head must include them).
- Reference partials with `{% render 'partial-key', title: data.title %}` — partials remain reusable for future emails even in HTML mode.

## MJML templates

For standard-MJML sources being kept as MJML:

- Set `"is_mjml": true` inside the `template` object; the extracted body file becomes `html_body.mjml`.
- Under an MJML layout (`is_mjml: true`), the body is an **MJML fragment** (`<mj-section>`s, no `<mjml>` root).
- With `"layout_key": null`, the body must be a **complete MJML document**.
- An MJML template requires an MJML layout (or no layout) — never pair MJML bodies with an HTML layout.
- Visual-block mode also works under MJML layouts (blocks render as MJML components), so block-first composition applies to MJML migrations too; plain-HTML `html` blocks and partials are auto-wrapped in `mjml-raw`.

## Consolidated workflows (approved variants only)

When the plan consolidated a variant set:

- **Batched vs single** (e.g. "new comment batched/single"): one workflow with a `batch` step before the email step; one template whose copy switches on batch scope:

```liquid
{% if total_activities > 1 %}
Hi {{ data.first_name }}, {{ total_activities }} people commented on your post.
{% else %}
Hi {{ data.first_name }}, someone commented on your post.
{% endif %}
```

- **Divergent variants** (different subject AND substantially different body): one workflow with a `branch` step containing an email step per variant. Branch conditions come from the variable map (e.g. `data.plan`, `run.total_activities`).

Every email step inside a branch gets its own directory **at the workflow root**, named by its step ref, with `visual_blocks@` paths relative to `workflow.json`; put conditions on every branch but the last, which acts as the default; step refs must be unique across the workflow. The directory tree and a minimal branch-step JSON are in `references/knock-blocks.md`; `batch` step JSON and the condition operator table are in the knock-cli skill.

## Per-template email settings

When analysis found per-template sender metadata, set step-level `channel_overrides` (`from_address`, `from_name`, `reply_to_address`, cc/bcc, link and open tracking, `json_overrides` for provider-specific fields) — confirm at the plan checkpoint, since the environment's channel config is the default sender. Templates read attachments from `data.attachments` unless `settings.attachment_key` says otherwise. The JSON shape is in `references/knock-blocks.md`.

## Validate, push, commit, readback

Per workflow:

```bash
knock workflow validate <key>
knock workflow push <key>
knock workflow get <key> --json     # readback: confirm subject, layout_key, step/block structure
knock commit -m "Migration: <key> workflow" --resource-type=workflow --resource-id=<key> --force
```

**`validate` is a local shape check — `push` is the real gate.** Some server-side checks (the preference-category catalog among them) run only on push, so a green validate is not a go signal. After every push, run the readback (`get`); commit only after push and readback both succeed — a scoped commit for a resource that never pushed still reports success and records nothing.

Fix validation errors before pushing. Common ones: invalid `channel_key` (re-run `knock channel list`), `layout_key` not found (layout not pushed/committed), missing button `variant`, doubled step-directory paths in `content@` references. Common push-time rejections validate misses: workflow `categories` not in the preference-category catalog (omit categories — see above), invalid partial `icon_name`.
