---
title: Verifying the migration
description: Tiered verification of migrated templates, rendered previews via the management API, test sends, and the final report
tags:
  - knock
  - migration
  - email
  - testing
  - preview
  - verification
category: knock-email-template-migration
last_updated: 2026-09-08
---

# Verifying the migration

> **Phase 4 of 4 — Verify and report.** Inputs: pushed and committed resources, `plan/variables.md` contracts for realistic payloads, the source files for the text oracle and the visual comparison. Outputs: `knock-migration/previews/` (renders plus one comparison page per layout), pass/fail notes in `MIGRATION.md`, and `REPORT.md`. Read alongside: `rules/building-templates.md` and `rules/extracting-layouts.md` when a finding needs a fix.

Verification is tiered so the effort scales with the template count and the user's appetite. The tier is chosen by the verification question at the plan checkpoint (see `rules/migration-process.md`); tier 1 is never optional.

## Tier 1: validate + readback (always)

Already woven into the build loop, restated here as the minimum bar for marking a template "Pushed":

1. `knock <resource> validate` passes before every push — a **shape check only**; some server-side checks run exclusively on push.
2. `knock <resource> push` succeeds — **push is the real gate**.
3. Read back the persisted state and confirm it matches intent:

```bash
knock workflow get <key> --json
```

Check against the plan **semantically**, not byte-for-byte: subject line, `layout_key` and `pre_content`, step refs and types in order, block types in order, partial keys and the `attrs` you bound, button labels, actions, and the `style_attrs` you set. The CLI normalizes block JSON on readback and drops fields that equal their defaults, so a missing default-valued field is normalization, not loss; a missing value you set explicitly is. For layouts/partials, `knock layout get <key> --json` / `knock partial get <key> --json` equivalently. Discrepancies mean the local files and the pushed state diverged — fix locally and re-push; never hand-edit in the dashboard mid-migration.

Commit only after push and readback succeed, and mark Committed on the status board only on a successful `get` — a scoped `knock commit` reports success even when the target resource was never created, so its output is not evidence of anything.

## Tier 2: rendered previews (default when API access allows)

The management API renders a committed template without sending: `preview_template` per workflow step, plus inline layout, partial, and template previews for probing before anything is pushed. **Prefer the Knock MCP** (`execute_mapi_write` — the previews are POSTs): it is already authenticated for the account. Its result is capped at roughly 6,000 tokens and a rendered email is 30–70 KB, so run the checks *inside* the call and return findings only; fetch full renders one per call only for the per-layout representatives of the visual pass, and verify each written file against the hash the sandbox returns. Every recipe first asserts that the render field is a non-empty string — the field name differs by endpoint, and `undefined` passes string checks silently. Direct HTTP with a service token is the path the user chose at intake: a full archive of renders on disk, an unavailable MCP, or preference. Endpoints, request and response shapes, the MCP cap, the safe service-token handoff, and test-user creation are in `references/verification-recipes.md`.

Build the `data` payload from the workflow's trigger contract in `plan/variables.md`, with realistic example values (real-looking names, URLs, prices — not `"test"`). Then compare the rendered HTML against the source template. The bar is **same look and same text — not same markup**. The markup legitimately differs in a known, closed set of ways: source variable expressions are replaced by rendered values; partial `<style>` blocks are hoisted into the head and their rules also inlined onto the components they style — so a component that carried its styles inline in the source should read like the original; MJML sources compile to final HTML; and accounts on Knock's free developer plan get a "Powered by Knock" footer appended. (If the migration used Knock's built-in blocks — buttons, dividers, markdown prose — their base CSS is also injected into the head, with each block in its own wrapper rows.) Anything else that differs — a color, font, size, spacing, or background present in the source but not the render — is a finding, not noise:

- **Source-text oracle**: every static text segment of the source appears in the union of the rendered variants. The segmentation and normalization rules that make a miss point at one paragraph are in `references/verification-recipes.md`. The oracle is derived from the source, never written from memory — dropped and fabricated copy is the most common silent failure, and a hand-written expectation list inherits the same blind spots as the build.
- **Markup grep after every fix**: the attributes you changed never show in text. Grep the rendered HTML for `href=""` and `src=""`, hrefs on a placeholder host (previews substitute `https://example.com` for an unset `vars.*` value, so every link can pass while pointing nowhere), inline `width:100%` on images, `text-align` on markdown cells, and the block class names you overrode.
- **Style fingerprint**: every distinctive source declaration — brand colors, font families and sizes, backgrounds, button styling, widths and alignment of major sections, the dark-mode query — survives into the render. Normalization and the expected-miss list are in the reference.
- Every link href correct (including UTM params); every image src correct with alt text
- Buttons render with the right label, destination, and styling — assert that each button's `style_attrs` (`background_color`, `text_color`, `border_radius`) survive into the rendered anchor's inline style; a mismatch means a layout rule with `!important` is masking the block, which validation never catches
- Conditional branches: render once per branch of every `{% if %}` (vary the data) — both sides must be checked
- **Branch and step conditions are not exercised by `preview_template`** — it renders whichever step you name regardless of routing. A workflow with a `branch` step (or step conditions) needs a run: `knock workflow run <key> --recipients=<test-user> --data='…' --sandbox-mode` once per branch, then confirm from the message log (dashboard or the MCP `get_user_messages`) which step produced the message. Try condition operators on edge values too — `empty` with `[]` and with the key missing, numeric comparisons with strings — because the operator table and the Liquid engine do not always agree.
- Loops: render with 0, 1, and N items
- Optional fields: render at least once with **every optional field absent** and once with every optional string set to `""` — presence guards that mishandle missing keys or empty strings leak dangling labels (a `Price: $` with no value) or empty sections, and this is where any engine deviation from the truthiness rule in `rules/mapping-variables-and-logic.md` shows up. Do this per partial as well as per template: a partial's isolated scope receives its inputs differently from the template around it, so a partial that looks right from the template's `{% if %}` can still emit a blank row
- Chrome (header/footer) present via the layout; preheader appears when set
- No leaked source syntax (`{{#if`, `*|FNAME|*`, `<%…%>`) anywhere in output — grep the rendered HTML for `{{`, `{%`, `*|`, `<%` remnants

Layout-level defects — a left-aligned button the source centers, prose running the full card width where the source used a narrower column, tighter or looser paragraph rhythm — pass the text oracle and style fingerprint and only show in a rendered comparison. So the **visual pass is a required tier-2 step for at least one template per layout** (plus any template the user calls high-stakes), done by the agent whenever a browser or screenshot tool is available and by the user otherwise.

The recipe (an original rendered with the same values, the same-width comparison page, serving it to a browser tool, and what to check in which order) is in `references/verification-recipes.md`. Fix in the layout CSS or block attributes, re-push, re-render, and re-compare once.

Record a pass/fail note per template in `MIGRATION.md`, and keep the comparison page in the workspace — it is the artifact the customer signs off on.

## Tier 3: test sends (user-gated)

Live sends catch what previews can't: provider transforms, CSS inlining (when enabled on the channel), client rendering, clipping, dark mode.

```bash
# Renders and creates messages WITHOUT delivering to the provider:
knock workflow run <key> --recipients=<test-user-id> --data='{…}' --sandbox-mode

# Real delivery to the user's test inbox:
knock workflow run <key> --recipients=<test-user-id> --data='{…}'
```

- The test recipient (the inbox named with option B at the checkpoint) must exist in the development environment with the user's real inbox address for real sends.
- `--sandbox-mode` generated messages can be inspected in the dashboard, or fetched via the MCP `get_message_content` tool for automated comparison — same checklist as tier 2.
- For consolidated batch workflows, trigger multiple times inside the batch window to exercise the `total_activities > 1` copy; use `--skip-delay` where delays block the loop.
- **Scale to the set**: for >10 templates, agree on a representative sample (each layout, each partial, each control-flow pattern, plus any template the user calls high-stakes) instead of all of them. Record which were spot-checked vs fully sent.

Human review checklist for the inbox: renders in the user's primary clients, subject/preheader look right in the list view, images load, dark mode acceptable, mobile width acceptable, plaintext version sane (autogenerated text is worth one look).

Fix → re-push → re-commit → re-verify until the user signs off; mark "Verified" in the status board.

## The final report

Write `knock-migration/REPORT.md` when all templates are verified (or their tier is complete). Contents:

1. **Summary**: N templates migrated → N workflows, N layouts, N partials; environment/branch; anything skipped and why.
2. **Resource map**: source file → workflow key / step ref / layout key / partials used. One row per template.
3. **Trigger contracts**: per workflow, the trigger snippet and variable table copied from `plan/variables.md`. This is the section the customer's engineers integrate against.
4. **Design system inventory**: each partial with its inputs — the building blocks available for future emails.
5. **Open items**: unresolved ❓s, deferred work (localization, asset rehosting, unsubscribe wiring), suggested follow-ups (e.g. consolidations the user declined).
6. **Promotion instructions** (do not run them — and carry this warning into the report): `knock commit promote --to=<environment>` promotes **every unpromoted commit in the environment**, including staged changes unrelated to this migration. The default instruction is selective promotion by commit id:

```bash
# List this migration's commits per resource, then promote each by id:
knock commit list --resource-type=workflow --resource-id=<key>
knock commit promote --only=<commit-id> --force
```

Bulk promotion (`knock commit promote --to=<environment> --force`) is only safe when the environment contains nothing but this migration's commits — a `knock commit list` inspection showing no unrelated changes.

Remind the user that partials and layouts promote as their own commits — promote them before or with the workflows that depend on them.
