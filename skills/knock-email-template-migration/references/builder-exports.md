# Builder exports

> Consulted from `rules/analyzing-source-templates.md` ("Format detection") and `rules/extracting-layouts.md` ("Extracting the layout from the representative file").

## Recognizing builder exports

| Builder | Markers | What the markers give you |
| --- | --- | --- |
| SendGrid design editor (v2) | `class="sg-campaigns"`, `data-editor-version="2"`, `role="module" data-type="text\|button\|divider\|image\|preheader\|code\|columns"` | every `role="module"` table is one section — module boundaries are block boundaries; the hidden `data-type="preheader"` module is the `{{ preview_text }}` slot; button modules carry the brand color on the `<a>`; the `<!--[if (gte mso 9)\|(IE)]>` conditional that closes a `columns` module emits `<tr>` where `</tr>` was meant (editor bug, harmless) |
| SendGrid legacy editor | `span.sg-image` with a `data-imagelibrary` attribute around images; `<%body%>` / `<%subject%>` slots; `:name` substitutions | strip `data-imagelibrary` (editor metadata); the slots are filled by the API call, not variables |
| BEE / Stripo | `row-content`, `block-` classes, `bee.io` assets | rows are sections; `.row-content` width is the card width; the visible rule of a divider lives on a `td.divider_inner` with `border-top` (inside `table.divider_block` in newer exports, `table.divider_content` in older ones) — anchor divider detection on that cell, not on the table's class, or the newer exports lose their rules |
| Compiled MJML | `mj-column-per-*`, `mj-outlook-group-fix` classes | the HTML is the ground truth; note it came from MJML |

## Splicing a layout out of the representative file

Splice with a script; never retype a multi-kilobyte `<head>`. The recipe for a builder export: (1) head = everything up to `</head>`, plus your block-fidelity `<style>` inserted before it; (2) header chrome = from `<body>` to the start of the first body section — if that first body module carries the column width or a max-width, move it onto the container in the layout, or `{{ content }}` will fill the card; (3) footer chrome = from the start of the last chrome section to the end; (4) `html_layout = head + header + "{{ content }}" + footer`, then swap the preheader's empty element for `{{ preview_text }}` and any per-template footer href for its Liquid form. Anchors that make this mechanical for SendGrid design-editor exports: the `td[role="modules-container"]` cell holds every module; the first `<table class="module" role="module" data-type="text"` is where the body starts; the last such text module is usually the footer link; the closing `<!--[if mso]></td></tr></table>` conditional marks the end of the container. For legacy-editor or hand-authored HTML, anchor on the wrapper `<div>` that carries the card styling. Assert each anchor exists before slicing, and diff the result against the source once to be sure nothing between the anchors was lost.
