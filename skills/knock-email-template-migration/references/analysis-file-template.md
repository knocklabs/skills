# Analysis file template

> Consulted from `rules/analyzing-source-templates.md` ("The analysis file"). Copy this structure exactly for every `analysis/<stem>.md`; later phases parse it. Give it to every parallel analysis agent.

```markdown
# <stem>

- **Source**: <path> (<format classification>)
- **Aliases**: <other paths whose file is byte-identical to this one> | <alias> (of <variant file>) when this file covers a variant set | none   # aliases get no analysis file of their own
- **Purpose**: password reset request email
- **Subject**: "Reset your password" (source: provider metadata | <title> | preheader | DRAFTED — needs approval ❓default; add "no provider metadata available" when step 1 of the ladder had nothing to search)
  e.g. `"Your weekly report is ready" (source: <title>)` · `"Order {{ data.order_id }} has shipped" (source: DRAFTED — needs approval ❓default; no provider metadata available)`
- **Preview text**: "<text>" (from hidden preheader div at <location>) | none | none (empty preheader slot present — becomes the layout's `{{ preview_text }}`)
- **Chrome family**: <family-name>  # from analysis/_chrome-families.md — reference only, don't re-describe
- **Chrome deltas**: <this template's differences from the family: e.g. footer link href variant, a normally-empty slot that carries content> | none
- **Text companion**: <path> | none

## Structure outline

1. [chrome] Header: logo linking to site (part of layout candidate)
2. [body] Heading + intro prose — simple prose
3. [body] CTA button "Reset password" → {{reset_url}} — solid, brand red
4. [body] Secondary prose with expiry note — simple prose
5. [chrome] Footer: social links row + legal text (part of layout candidate)

## Body copy (verbatim)

> Hi {{first_name}}, your order {{order_id}} shipped today and should arrive in
> 3 to 5 days.

> Need to make a change?
> Reply to this email within 24 hours and we will update the order before it
> leaves the warehouse.

## Variant deltas

- (none — not a variant set) | one `###` per variant as below

(For variant sets that share this file, and for a template whose sibling is already live from an earlier pass — in that case name the live workflow key, list the copy that differs verbatim, and state the disposition: its own workflow by default, or extend the live one. One `###` per source file with the differing copy verbatim and a proposed discriminator value, e.g. `### plan-free.html (discriminator: free)`; two variants key on a boolean unless a third is plausible, three or more on an enum — or, when the set is a grid that varies along more than one axis, one `###` per axis naming its discriminator and values. State what the consolidated template would key on — that field usually does not exist in the source and is a `❓blocking` contract change.)

## Markup defects

- (none) | unclosed `<head>` at line N | missing `<body>` | stray `</a>` in footer | `bgcolor="ffffff"` without `#` — chrome defects are repaired in the layout; defects inside body markup (a nested `<head>`/`<body>`, a stray `</b>`, `terms<a>` with no space) are repaired in the block content. Tag-adjacent whitespace that changes rendered text ("termsPrivacy") is repaired by inserting the space and listed here, so the text oracle knows why the render differs. Copy itself is never changed.

## Suspected source mistakes

- (none) | one line each — `what · where · default: reproduce what the source rendered · alternative: fix it`. Anything that looks unintended and needs the user's eye: copy the source engine never rendered (text trailing a Mako control line, a section inside a condition that can never be true — default: dropped, with the text quoted here so restoring it is one word), malformed expressions, a duplicated or truncated sentence, an empty button or heading, a missing space before a link. Structural repairs stay under Markup defects; these are consolidated at the checkpoint as their own list.

## Partial candidates

- item-card (section 3 of the body): product image + title + price grid; also appears in order-confirmed.html, order-delivered.html
- CTA button (section 3): standard solid button → disposition: **built-in `button_set` block** with `style_attrs`/`layout_attrs` (not a partial)

## Variables

| Source expression | Syntax | Where | Meaning | Example value | Proposed mapping |
| ----------------- | ------ | ----- | ------- | ------------- | ---------------- |
| {{first_name}} | Handlebars | body §2 | recipient first name | "Ada" | data.first_name (or recipient.first_name ❓default) |
| {{reset_url}} | Handlebars | body §3 | action link | https://… | data.reset_url |
| {{unsubscribe_url}} | Handlebars | chrome (footer) | preference-center link | https://… | data.unsubscribe_url — consumed by the layout |
| items (loop source: `{{#each items}}`) | Handlebars | body §4 | collection of cart items | see data shape | data.items (list) |
| {{this.name}} | Handlebars | body §4 | item name | "Widget" | loop → item.name |

Data shape (when loops or nested objects exist — reconstruct it from the template, or from an example payload if one is available):

```json
{ "items": [ { "name": "Widget", "url": "https://…" } ] }
```

Escaping: note when the source escaped a variable that carries HTML (Handlebars double-stache on `description_html`; Mako's default `h` filter) versus rendered it raw (triple-stache; Mako `| n`) — Liquid renders raw either way, so decide whether `| escape` is needed and record it here.

## Control flow

- {{#if items}}…{{else}}…{{/if}} wrapping section 4 — inline copy variation → Liquid {% if %}
- (none in this file)
- whole-body variant of <other-template> — consolidation candidate ❓blocking (record both lines when both are true: in-file logic and variant-set membership are separate facts)

## Assets and links

- Images: all absolute CDN URLs ✅ | ⚠️ local/relative/base64 images: <list> ❓
- Alt text: present | missing on <images> → proposed `""` (decorative) or "<evident purpose>" (meaningful) ❓default — never invent alt text silently
- Links carry UTM params: preserve verbatim
- Custom fonts: Google Fonts <link> in head (→ layout)

## Style notes

- The body's distinctive inline declarations, for the verification style fingerprint: brand hex colors, font families and sizes, button background/radius/padding, column widths and alignment, background colors of cards or bands — one line per section, e.g. `CTA (§3): background #1f4b99; radius 4px; 16px Helvetica; padding 12px 24px; centered`

## Provider artifacts

- Unsubscribe: <%asm_group_unsubscribe_raw_url%> in footer ❓
- Tracking pixel: <img src="…open.gif"> — strip (provider re-adds)
- From/reply-to metadata: from=support@acme.com (→ channel_overrides?)
- Provider slot: `<%body%>` filled by the sending code — slots are listed here, never in the Variables table

## Open questions

- ❓blocking … (changes the trigger contract, overwrites a resource, or chooses between topologies — the checkpoint cannot pass until answered)
- ❓default … (the agent's stated choice, applied unless the user vetoes it at the checkpoint)
- ❓fyi … (recorded for the report; no decision needed)
```
