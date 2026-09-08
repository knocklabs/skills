# Knock blocks: selectors, branch workflows, channel overrides

> Consulted from `rules/extracting-layouts.md` ("CSS strategy for block-first fidelity") and `rules/building-templates.md` ("Consolidated workflows", "Per-template email settings").

## Base block selectors

**Match Knock's base block selectors.** At render time Knock injects its own block CSS at the top of the `<head>` and then inlines everything into the blocks. Its selectors are more specific than a bare `.block-row--<type>-v1` rule, so an override written at lower specificity *adds* to the base rule instead of replacing it (a divider written as `.block-row--divider-v1 .block-divider { border-top: … }` produced two lines: yours plus Knock's `border-bottom`). Write overrides at the same specificity as the base rules:

| Block | Base selector Knock injects | What it sets |
| ----- | --------------------------- | ------------ |
| markdown | `.block-row.block-row--markdown-v1 .block-markdown` (`> :first-child` / `> :last-child` margins reset to 0) | no typography — yours applies; because of the margin resets, spacing between two markdown blocks comes from cell padding, never from element margins — or keep a heading and its lead paragraph in one block |
| button_set | `.block-row.block-row--button_set-v1 .block-button` (+ `--solid`, `--outline`, `--sm`) | display, sizing per `size_attrs`; colors come from the block's `style_attrs` |
| divider | `.block-row.block-row--divider-v1 .block-divider` | `border-bottom: 1px solid #DDDEE1` — override `border-bottom`, not `border-top` |
| image | `.block-row.block-row--image-v1 .block-image img` | inline `width:100%` on the `<img>` — a fixed size needs `!important` (or use an `html` block) |
| html | `.block-row.block-row--html-v1 .block-row__cell` | the same 8px/4px cell padding as every block — override it when a card or full-bleed band must sit flush |
| partial | (none) | a partial block renders with **no wrapper row at all**: no cell, no padding. Its content is responsible for its own spacing, so a partial that replaces a padded source section must carry that padding itself |

Every block sits in `.block-row__cell` with 8px vertical / 4px horizontal padding; override that cell's padding when the source column is narrower than the card (e.g. side padding on the cell to reproduce a narrower source column) or when the source's section spacing is larger than 8px. **Cell padding overrides need `!important`**: Knock inlines your layout rule into the cell's `style` attribute and then appends its own per-side padding after it, so a plain `padding: 12px 0` is silently lost while `padding: 12px 0 !important` wins. The symptom is visible in the render — the cell's `style` attribute carries both your declaration and Knock's `padding-top: 8px; …` after it — and the rendered comparison shows tighter vertical rhythm than the source. After the fix the attribute still carries both; only the `!important` shorthand matters, so the trailing longhands are expected, not a finding. **Render one preview before writing any block CSS** — the injected base rules are visible verbatim at the top of the rendered head, and one render tells you every selector and inline style you are working against. Run it through the Knock MCP (`execute_mapi_write` on a pushed workflow's `preview_template`, or on the layout preview endpoint with `workflow: { key: <any live workflow> }` so the namespaces are bound); see the verify rule for the request shape. On an empty account no render is possible in stage 2: write the layouts from the selector table above, push the first workflow, render it, then revise the layout CSS and re-push (layouts are idempotent) before building the rest.

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

This shape puts conditions on every branch but the last, which acts as the default.

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
