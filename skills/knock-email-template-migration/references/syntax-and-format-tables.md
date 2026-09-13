# Syntax and format tables

> Consulted from `rules/analyzing-source-templates.md` ("Format detection", "Variables and source syntax") and `rules/mapping-variables-and-logic.md` ("Syntax translation tables").

## Format detection

| Signal | Classification | Ground truth for migration |
| ------ | -------------- | -------------------------- |
| `.html` with `mj-column-per-*` / `mj-outlook-group-fix` classes | Compiled MJML export | The HTML itself; note it came from MJML |
| `.html` with BEE/builder classes (`row-content`, `block-`, `bee.io` assets) | Builder export (BEE, Stripo, etc.) | The HTML |
| `.html` with `class="sg-campaigns"`, `data-editor-version`, `role="module" data-type="text|button|divider|preheader|code"` | SendGrid design-editor export | The HTML; each `role="module"` table is one section — module boundaries are your block boundaries |
| `.html` with `span.sg-image` / `data-imagelibrary` attributes | SendGrid legacy-editor export | The HTML; strip the `data-imagelibrary` metadata |
| Fragment with no `<html>`/`<head>`/`<body>` | Headless fragment | The HTML; the sending code supplied the chrome — which layout it adopts is a `❓default` |
| `.html` whose content is plain text (literal `\n` sequences, no tags) | Plain-text source | Migrate as `text_body` plus a minimal HTML body under a layout `❓default` |
| Structural defects: no `<body>`, unclosed `<head>`, stray closing tags | Handcrafted HTML with defects | The HTML; repair the defects in the layout and list each in the analysis file's `## Markup defects` |
| `.html`, hand-authored table markup | Handcrafted HTML | The HTML |
| `.mjml` using only standard `mj-*` components | Standard MJML | The MJML (keep as MJML in Knock) |
| `.mjml` with non-standard tags (e.g. `eds-header`, `block-preview-text`) | MJML with custom components | The paired/compiled HTML — the MJML **cannot** run in Knock but is the best map of component boundaries |
| `.tsx` / `.jsx` (React Email), `.vue`, etc. | Component source | Must be rendered to HTML first (`npx react-email export` or the user's build); ask the user to run it if the toolchain isn't available |
| Same stem with both `.mjml` and `.html` | Pair | Per the MJML rules below |
| `.txt` with a matching stem | Plaintext body companion | Migrate as the template's `text_body` |
| `.json` provider export (SendGrid/Mailchimp) | Metadata | Mine for subject lines, from addresses, versions |

## Syntax families

| Syntax family | Variable | Conditional | Loop |
| ------------- | -------- | ----------- | ---- |
| Handlebars/Mustache (SendGrid dynamic, Mailgun, Braze-ish) | `{{var}}`, `{{{raw}}}` | `{{#if x}}…{{else}}…{{/if}}`, `{{#unless}}` | `{{#each items}}…{{this}}…{{/each}}` |
| Mailchimp merge tags | `*|FNAME|*` | `*|IF:X|*…*|END:IF|*` | — |
| SendGrid legacy substitutions | `-name-`, `%name%`, `:name` (colon form; keys may contain spaces, e.g. `:first name`) | — | — |
| SendGrid legacy slots | `<%body%>`, `<%subject%>` — filled by the API call, **not variables** | — | — |
| Mako (Python) | `${var}` | line-based: `% if x == 'y':` … `% elif x >= 1:` … `% else:` … `% endif` | `% for x in xs:` … `% endfor` |
| Ruby / i18n interpolation | `%{var}` | — | — |
| Python format strings | `{}` (positional, unnamed), `{var}`, `%(var)s` | — | — |
| Liquid (Shopify, Customer.io, Braze Liquid) | `{{ var }}` | `{% if %}` | `{% for %}` | 
| Jinja/Django | `{{ var }}` | `{% if %}` | `{% for %}` |
| Code interpolation (extracted from app code) | `${var}`, `#{var}`, `<%= var %>` | in host language ❓ | in host language ❓ |

## Translation tables

### Handlebars/Mustache (SendGrid dynamic templates, Mailgun, many app codebases)

| Source | Knock Liquid |
| ------ | ------------ |
| `{{first_name}}` | `{{ data.first_name }}` |
| `{{{raw_html}}}` | `{{ data.raw_html }}` (Liquid does not HTML-escape output by default) |
| `{{#if x}}…{{else}}…{{/if}}` | `{% if data.x %}…{% else %}…{% endif %}` |
| `{{#unless x}}…{{/unless}}` | `{% unless data.x %}…{% endunless %}` |
| `{{#each items}}…{{this.name}}…{{/each}}` | `{% for item in data.items %}…{{ item.name }}…{% endfor %}` |
| `{{@index}}` | `{{ forloop.index0 }}` |
| `{{#if (eq a b)}}` and other helpers | `{% if data.a == data.b %}` — translate helper semantics case by case; unmappable helpers are ❓ items |

See the truthiness rule in `rules/mapping-variables-and-logic.md` before translating `{{#if}}` — Handlebars treats empty strings as falsy and Liquid does not, so an optional string needs `!= blank`.

### Mailchimp merge tags

| Source | Knock Liquid |
| ------ | ------------ |
| `*|FNAME|*` | `{{ data.first_name }}` (or `{{ recipient.first_name }}` if remap approved) |
| `*|EMAIL|*` | `{{ recipient.email }}` |
| `*|IF:X|*…*|ELSE:|*…*|END:IF|*` | `{% if %}…{% else %}…{% endif %}` |
| `*|UNSUB|*`, `*|UPDATE_PROFILE|*` | See provider artifacts below |
| `*|CURRENT_YEAR|*` | `{{ timestamp | date: "%Y" }}` |

### SendGrid legacy substitutions

`-name-` / `%name%` / `:name` → `{{ data.name }}`. The colon form's keys may contain spaces (`:first name`), which cannot be a Liquid identifier — rename (`data.first_name`) and flag `❓blocking`. `<%body%>` and `<%subject%>` are slots the API call filled, not variables: drop the slot (the surrounding copy is usually the whole email) or expose it as `data.body` rendered raw — `❓blocking`. These templates have no conditionals; any logic lived in the sending code — ask the user what the code did and re-express it (see control flow).

### Mako (Python)

| Source | Knock Liquid |
| ------ | ------------ |
| `${var}` (often mangled to `{{var}` by a find/replace) | `{{ data.var }}` |
| `${var}` output was HTML-escaped by default (Mako's `h` filter); `${var | n}` was raw | add `\| escape` unless the variable's name says it carries HTML (`description_html`) |
| `% if x == 'y':` … `% elif x >= 1:` … `% else:` … `% endif` | `{% if data.x == "y" %}` … `{% elsif data.x >= 1 %}` … `{% else %}` … `{% endif %}` — Mako control lines are whole-line: markup written on the same line as `% endif` never rendered in the source, so decide whether to keep it `❓default` |
| `% for item in items:` … `% endfor` | `{% for item in data.items %}` … `{% endfor %}` |
| `${len(xs)}`, `${x or y}` | `{{ data.xs | size }}`, `{{ data.x | default: data.y }}` |
| `'k' in d`, `d.get('k')` | `{% if data.d.k %}` |
| `d['k']`, `d[key]` | `data.d.k`, `data.d[key]` (bracket indexing with a variable works in Knock's Liquid) |
| `xs[-1]` | `{{ data.xs | last }}` |
| `xs[:-1]` | `{% assign n = data.xs | size | minus: 1 %}{% for x in data.xs limit: n %}…{% endfor %}` |
| `range(len(xs))` over parallel arrays `xs[i]`, `ys[i]` | `{% for x in data.xs %}{{ data.ys[forloop.index0] }}{% endfor %}` — loop one array and index the others |
| other Python expressions | `❓default` with the translation stated when it is obvious; `❓blocking` only when the semantics are unclear |

### Ruby and Python interpolation

`%{var}`, `{var}`, `%(var)s` → `{{ data.var }}`. A positional `{}` has no name: invent one from context (`data.reset_url`), flag `❓blocking`, and put it in the trigger contract.

### Liquid-family sources (Shopify notifications, Customer.io, Braze Liquid, Jinja)

Syntax mostly carries over; the work is namespace prefixes and filter compatibility. Verify every filter against the Knock docs "Liquid helpers reference" — Knock adds helpers like `timezone`, `format_date_in_locale`, `json`/`from_json`, and its `date` filter takes a `timezone` option but does not support full strftime (`%e`, `%l` are unreliable). Provider-specific tags (Braze `{% connected_content %}`, Customer.io `{% snippet %}`) are ❓ items — connected content generally maps to an `http_fetch` workflow step; snippets map to partials.

### Code interpolation (`${var}`, `<%= var %>`, `#{var}`)

Mechanical variable mapping is the same (`→ {{ data.var }}`). The surrounding code's conditionals/loops must be re-expressed in the template or workflow — ask the user to describe what the code varied.
