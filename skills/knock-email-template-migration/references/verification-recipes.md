# Verification recipes

> Consulted from `rules/verifying-the-migration.md` (tier 2) and `rules/migration-process.md` (the preflight smoke preview and service-token handoff).

## Rendering previews

| Endpoint | Renders |
| -------- | ------- |
| `POST /v1/workflows/{key}/steps/{step_ref}/preview_template` | Generates a rendered template for a given channel step in a workflow — the migration's source of truth. Pass `data` and a `recipient` to the endpoint to render a committed email template as it would render at runtime. |
| `POST /v1/email_layouts/preview` | Renders a layout passed **inline** (`email_layout: { name, html_layout, text_layout }` plus `data`/`recipient`, and `workflow: { key }` so the namespaces are bound) without pushing it — the fastest way to check a layout's chrome or how a Liquid expression behaves before any workflow exists. Response: `{ result, layout: { html_body, text_body } }`. |
| `POST /v1/partials/preview` | Same for a partial's content and inputs. It validates `data` against the partial's `input_schema` and returns 422 `"<key>: is required"` for **any** schema key absent from `data`, regardless of `settings.required` — so pass every key, with `""` for the ones you are testing as absent (`{ "text": "", "action": "" }` for a button, `{ "url": "", "alt": "", "action": "" }` for an image), which is also what a missing scalar arrives as in isolated scope. `POST /v1/templates/preview` does it for an inline email template. Response: `{ result, template: { html_body, … } }` — note these inline previews use `html_body`, while the workflow-step preview below uses `html_content`. |

**Prefer the Knock MCP server's `execute_mapi_write` tool** (the preview endpoints are POSTs even though they only render). It is already authenticated against the account the user is working in and needs no token handling. Two consequences of how the MCP works shape the whole tier:

- **Its result is capped at roughly 6,000 tokens, and one rendered email with inlined styles is 30–70 KB.** So run the tier-2 checks *inside* the call — the JavaScript you pass can fetch the render, apply the text oracle, style fingerprint, leaked-syntax grep, empty-href count, and branch/loop/optional-field matrix, and return **findings only** (missing segments, missing declarations, leaks, counts). Never return whole renders from a batch; a 20-variant matrix costs a few hundred tokens this way and is the default shape for automated verification.
- **A render reaches disk only through the tool result.** The sandbox has no filesystem, so for the visual pass fetch one render per call and write the returned text to `previews/<key>.html` yourself. Return the HTML as a **raw string**, not inside an object — objects are pretty-printed before the cap is applied, which inflates them by a third or more — with whitespace collapsed (a 30–70 KB render becomes 10–15 KB; the cap is 6,000 tokens, applied server-side as 24,000 characters) and a one-line header carrying its length and an FNV-1a hash. After writing the file, recompute both locally and re-fetch on a mismatch: the transcription is verified, not trusted. Do this only for the one-template-per-layout representatives; rendering every email for the every-email review is the direct path's job. A collapsed render longer than the cap (a long digest, heavy inlined CSS) comes back with a `--- TRUNCATED ---` line naming its size: fetch it in slices across calls (`out.slice(start, start + 20000)`, each call re-rendering the same payload and returning the whole-document length and hash in its header), concatenate locally, and verify the whole file — the cost is one call and about 5,000 output tokens per 20,000 characters, so past three or four slices per template the direct path is cheaper.

The render call, with the shape guard every recipe opens with (`undefined` passes string checks silently, and the field name differs by endpoint):

```js
async () => {
  const res = await mapi.request({ method: "POST", path: "/v1/workflows/<key>/steps/<step_ref>/preview_template",
    query: { environment: "development" }, body: { recipient: "<test-user-id>", data: { … } } });
  const html = res.result?.template?.html_content;   // inline previews: res.result.template.html_body or res.result.layout.html_body
  if (typeof html !== "string" || html.length < 1000) return { FATAL: "html_content missing", status: res.status, got: Object.keys(res.result?.template ?? res.result ?? {}) };
  const out = html.replace(/\s+/g, " ");
  let h = 0x811c9dc5; for (let i = 0; i < out.length; i++) { h ^= out.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; }
  return `LEN=${out.length} FNV=${h.toString(16).padStart(8, "0")}\n` + out;
}
```

Write everything after the header line to the file, then check it (JavaScript string length and `charCodeAt` are UTF-16 code units, so hash the file as UTF-16):

```python
s = open("previews/<key>.html", encoding="utf-8").read().rstrip("\n")
u = s.encode("utf-16-le"); h = 0x811c9dc5
for i in range(0, len(u), 2): h ^= u[i] | (u[i + 1] << 8); h = (h * 0x01000193) & 0xffffffff
print(len(u) // 2, f"{h:08x}")   # must equal LEN and FNV from the header
```

Use direct HTTP with a service token in two cases: the MCP is unavailable, or the user chose at intake to review every email side by side, which needs every render on disk (every template, every exercised variant). The token is arranged in preflight (`rules/migration-process.md`), never mid-verification:

```bash
curl -s -X POST "https://control.knock.app/v1/workflows/<key>/steps/<step_ref>/preview_template?environment=development" \
  -H "Authorization: Bearer $KNOCK_SERVICE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "recipient": "<test-user-id>", "data": { … } }'
```

**Providing a service token safely** (see [service tokens](https://docs.knock.app/developer-tools/service-tokens)):

1. An account owner or admin creates a **dedicated** token in the dashboard: Settings → Service tokens → "+ New token", named for this migration. It is shown once, starts with `knock_st_`, and grants full management-API access to the account, so it should be revoked from the token's menu once the migration is promoted.
2. The user provides it **out of band, never in the chat**: in the terminal they run the agent from, `export KNOCK_SERVICE_TOKEN=<token>`, then start (or restart) the agent from that terminal and ask it to continue the migration. An `export` inside a tool call does not persist between calls, and a token typed into the conversation lands in the transcript. If the variable is absent, also check for a git-ignored `.env` in the project or `knock-migration/` that exports it and source it in the scripts that need it — accept that route, do not suggest it.
3. Scripts read the variable and never echo it, log request headers, or write it into any file in the workspace.
4. Before using it, confirm it targets the right account with `GET /v1/whoami` (the response carries `account_name` and `service_token_name`). Scripts must send a `User-Agent` header — a 403 whose body is `error code: 1010` is Cloudflare's bot filter rejecting a bare client, not an auth failure.

Two request-shape details: the response is `{ result: "success" | "error", content_type, template }` and the rendered output is in `template.html_content` (siblings: `text_content`, `subject_line`, `preview_text` — not `html_body`/`subject`), and `recipient` must be a **recipient reference** — an existing user ID string or `{id, collection}` object. An inline recipient object fails with an undetailed 422, so ensure the test user exists first. The Knock MCP `upsert_user` tool creates it in one call — set `name`, `email`, and any property a `recipient.*` remap reads (for example `first_name`) — and create a second user to pass as `actor` whenever templates use `actor.*`. Without the MCP, trigger any workflow once with an inline recipient (`knock workflow run <key> --recipients='[{"id":"migration-test-user","email":"…"}]' --sandbox-mode …`), which identifies the user, or create it via the dashboard.

`execute_mapi_write` is registered only for sessions with write (Manage) access, and the preview endpoint requires the `workflows:run` permission; the preflight smoke preview in `rules/migration-process.md` surfaces both before anything is built.

## Text oracle

- **Source-text oracle**: extract the source template's text nodes (strip tags, collapse whitespace, split around variable expressions **and at block-level tag boundaries** — `</p>`, `</div>`, `</td>`, `<br>` — and at inline element boundaries — `<a>`, `<b>`, `<span>` — because a variable inside a link or a bold span otherwise leaves a joined fragment such as `Welcome to Acme ,` that no render contains; drop segments under about 12 characters or made only of punctuation and whitespace) and assert every static text segment appears in the **union** of all rendered variants, so text from an optional section only has to appear in the variant that enables it. Splitting at block boundaries is what makes a miss point at one paragraph instead of failing the whole email.

The oracle's expected segments come from two places: the template's `## Body copy (verbatim)` and its family's chrome copy in `analysis/_chrome-families.md`. Segments recorded as never rendered under `## Suspected source mistakes` are excluded unless the user chose to restore them at the checkpoint.

## Style fingerprint

- **Style fingerprint**: extract the source's distinctive declarations — brand colors (hex values), font families and sizes, background colors, button styling (background, radius, text color), widths and alignment of major sections, the dark-mode media query if present — and assert each survives into the rendered output, whether as an inline style, a preserved rule, or a hoisted partial style. A declaration that went missing means layout or partial CSS extraction dropped it. Normalize before comparing — lowercase both sides and remove whitespace after colons (Knock re-serializes inline styles as `font-size:15px`) — and match hex colors only when the `#` is not preceded by `&` (a numeric character entity such as `&#127881;` is not a color). Keep one list of known dead source styles per family (a zero-width border color, an empty spacer's font size) and mark those misses expected once, so they are not re-triaged per template.

Treat shorthand and longhand forms (`padding: 12px 24px` and the four-value form), `0` and `0px`, and hex-color case as equal, and expect misses for source declarations that were dead (a `border` on an element the layout replaced, `background-color: inherit`) — record them as such once rather than re-triaging.

## Visual pass recipe

1. Produce an "original" that shows the same content as the render. For a flat template, copy the source file and string-substitute the *same* example values used for the render into its variable expressions. For a source with loops or conditionals, string substitution cannot work — render the original with its own engine using the same payload (Mako via `pip install mako`, Jinja via `jinja2`, Handlebars via `npx handlebars`). The preview endpoint's `data` accepts nested JSON — lists and objects, not just strings — so one payload file feeds both the Knock render and the source engine. When no engine can execute the source (a file that mixes Mako code, Jinja-shaped tags, and Mustache output in one template), produce the original with a source-derived substitution script — same payload, control flow resolved by hand from the analysis file — label that pane as reconstructed on the comparison page, and note it in `MIGRATION.md`.
2. Save the render to `knock-migration/previews/<key>.html` and build one comparison page for the whole migration at `knock-migration/previews/compare/index.html`: a jump list at the top, then one section per email — the representative per layout by default, every template when the user chose the every-email review — with source and render in two same-width frames (`<iframe srcdoc>`), grouped by layout. Split into one page per layout only past about twenty emails, and keep `index.html` as the index of those pages. Browser tools usually refuse `file://` URLs: serve `knock-migration/` with any static file server (for example `python3 -m http.server <port>`) — the originals reference the source copy, so the root must contain both — and open `http://127.0.0.1:<port>/previews/compare/…`; give the page a `<meta charset="utf-8">`, because a bare static server sends no charset and curly quotes will otherwise render as mojibake in both panes.
3. Compare at the email's natural width and check, in this order: horizontal alignment of every block (buttons and headings especially); column width of prose relative to the card; vertical rhythm (paragraph gaps, padding above and below buttons and dividers); button shape (padding, radius, font size); colors and fonts actually applied; anything the source shows that the render lacks or vice versa.
4. Fix in the layout CSS or block attributes, re-push, re-render, and re-compare once.
