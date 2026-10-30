# Knock blocks: selectors, branch workflows, channel overrides

> Consulted from `rules/extracting-layouts.md` ("CSS strategy for block-first fidelity") and `rules/building-templates.md` ("Consolidated workflows", "Per-template email settings").

## Base block selectors

**Match Knock's base block selectors.** At render time Knock injects its own block CSS at the top of the `<head>` and then inlines everything into the blocks. Its selectors are more specific than a bare `.block-row--<type>-v1` rule, so an override written at lower specificity *adds* to the base rule instead of replacing it (a divider written as `.block-row--divider-v1 .block-divider { border-top: … }` produced two lines: yours plus Knock's `border-bottom`). Write overrides at the same specificity as the base rules:

| Block | Base selector Knock injects | What it sets |
| ----- | --------------------------- | ------------ |
| markdown | `.block-row.block-row--markdown-v1 .block-markdown` (`> :first-child` / `> :last-child` margins reset to 0) | no typography — yours applies; because of the margin resets, spacing between two markdown blocks comes from each block's padding settings, never from element margins — or keep a heading and its lead paragraph in one block |
| button_set | `.block-row.block-row--button_set-v1 .block-button` (+ `--solid`, `--outline`, `--sm`) | display, sizing per `size_attrs`; colors come from the block's `style_attrs` |
| divider | `.block-row.block-row--divider-v1 .block-divider` | `border-bottom: 1px solid #DDDEE1` — override `border-bottom`, not `border-top` |
| image | `.block-row.block-row--image-v1 .block-image img` | inline `width:100%` on the `<img>` by default — for a fixed size, set the block's `style_attrs.width` to a CSS width string such as `"300px"`, which replaces the inline value |
| html | `.block-row.block-row--html-v1 .block-row__cell` | takes no padding settings (`layout_attrs` are dropped), so its spacing lives in its own markup; check the calibration render for any padding on its cell when a card or full-bleed band must sit flush |
| partial | (none) | a partial block renders with **no wrapper row at all**: no cell, no padding. Its content is responsible for its own spacing, so a partial that replaces a padded source section must carry that padding itself — inline, or in the partial's own `<style>`, which Knock hoists into the head |

Every built-in block sits in a `.block-row__cell` whose padding comes from the block's own `layout_attrs` — `padding_top`, `padding_right`, `padding_bottom`, `padding_left` — inlined on the cell (Knock's default is 8px vertical / 4px horizontal, and 0 for images). **Set spacing there, per block**: when the source's section spacing differs from the default, or the source column is narrower than the card (side padding reproduces a narrower column), set that block's `padding_*` to the source's values. Don't set cell padding from layout CSS: it only wins with `!important`, which also overrides the padding controls editors use in the dashboard, so every later change to that block's spacing would silently do nothing. Html blocks take no `layout_attrs` and partial blocks have no cell at all, so both carry their spacing in their own markup. **Render one preview before writing any block CSS** — the injected base rules are visible verbatim at the top of the rendered head, and one render tells you every selector and inline style you are working against. Run it through the Knock MCP (`execute_mapi_write`) on `POST /v1/templates/preview`: a template with a few representative blocks — a markdown paragraph, a button set, a divider, an image, and any partial block the family uses (partials are committed in stage 1, so they render) — in static text, with the layout under calibration passed inline as `layout: { html_content, text_content }`. It needs no workflow and nothing pushed, so it works on an empty account; request shape in `references/verification-recipes.md`. Iterate on the inline layout until the blocks match the source, then write the final CSS into `knock/layouts/<key>/` and push and commit it once.

## Branch workflows

File layout for a branch workflow: every email step inside a branch gets its own directory **at the workflow root**, named by its step ref, and `visual_blocks@` paths in `workflow.json` are relative to `workflow.json`:

```
knock/workflows/weekly-digest/
├── workflow.json
├── email_empty/
│   ├── visual_blocks.json
│   └── visual_blocks/1.content.md
└── email_report/
    ├── visual_blocks.json
    └── visual_blocks/…
```

```json
{
  "ref": "branch_1", "type": "branch", "name": "Anything to send?",
  "branches": [
    {
      "name": "Nothing found", "terminates": false,
      "conditions": { "all": [ { "variable": "data.items", "operator": "empty", "argument": null } ] },
      "steps": [ { "ref": "email_empty", "type": "channel", "channel_type": "email", "channel_key": "<channel_key>", "name": "Nothing found email",
                   "template": { "subject": "…", "settings": { "layout_key": "…" }, "visual_blocks@": "email_empty/visual_blocks.json" } } ]
    },
    {
      "name": "Report", "terminates": false,
      "steps": [ { "ref": "email_report", "type": "channel", "channel_type": "email", "channel_key": "<channel_key>", "name": "Report email",
                   "template": { "subject": "…", "settings": { "layout_key": "…" }, "visual_blocks@": "email_report/visual_blocks.json" } } ]
    }
  ]
}
```

This is the shape the API requires: 2–10 branches, conditions on every branch except the last, none on the last (it is the default), and at least one branch that doesn't terminate. There is no `default` field and branches take no `ref` — the API silently drops both — while step refs must be unique across all nested steps.

## Channel overrides

When analysis found per-template sender metadata, set step-level `channel_overrides` (confirm at the plan checkpoint — environment channel config is the default sender):

```json
{
  "ref": "email_1",
  "type": "channel",
  "channel_key": "…",
  "channel_overrides": { "from_address": "billing@acme.com", "reply_to_address": "support@acme.com" },
  "template": { "…": "…" }
}
```

Available overrides include `from_address`, `from_name`, `reply_to_address`, `cc_address`, `bcc_address`, `link_tracking`, `open_tracking`, and `json_overrides` (Liquid-enabled provider API payload overrides — only when the user needs provider-specific fields like SendGrid categories). Attachments: templates default to reading `data.attachments`; note `settings.attachment_key` if the customer's payload uses a different key.
