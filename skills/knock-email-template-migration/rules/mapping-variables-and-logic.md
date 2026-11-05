---
title: Mapping variables and logic
description: Translating source template syntaxes to Liquid, namespace mapping policy, control-flow decisions, and provider artifacts
tags:
  - knock
  - migration
  - email
  - liquid
  - handlebars
  - variables
  - conditions
category: knock-email-template-migration
last_updated: 2026-10-30
---

# Mapping variables and logic

> **Phase 1 (per-template mapping) and phase 2 (the contract) — Variables and logic.** Inputs: the Variables and Control flow sections of the analysis files. Outputs: the "Proposed mapping" column during analysis; `plan/variables.md` — the customer's new trigger payload contract — at phase 2. Read alongside: `rules/building-templates.md` for where translated Liquid lands.

Every dynamic expression in a source template must be translated to Knock Liquid, and every variable must land in a Knock namespace. The output of this work is `plan/variables.md` — which doubles as the customer's new **trigger payload contract**, so treat it as an API design document, not a find-and-replace log.

## Namespace mapping policy

Knock template namespaces: `data` (trigger payload), `recipient`, `actor`, `tenant`, `vars` (environment variables), plus batch scope (`total_activities`, `total_actors`, `activities`, `actors`).

**Default: preserve the customer's contract.** Map every source variable to `data.<original_name>`, name unchanged (`{{inviterFullName}}` → `{{ data.inviterFullName }}`). This means existing backend code can trigger the workflow with the payload it already builds. Do not rename or snake_case variables unprompted.

**Propose (opt-in, at the plan checkpoint) remapping for:**

| Source variable pattern | Proposed namespace | Why |
| ----------------------- | ------------------ | --- |
| `name`, `email`, `avatar` of the *recipient* | `recipient.*` | Knock hydrates recipients server-side; payload no longer needs to carry them. A first-name variable becomes `{{ recipient.name \| split: " " \| first }}`, the convention Knock's default templates use |
| Fields describing the *person who acted* (inviter, commenter, sender) | `actor.*` | Idiomatic Knock; requires the trigger to pass an `actor` |
| Account-constant values (support email, company address, app base URL, brand colors) | `vars.*` | Set once per environment instead of per trigger. Every Knock account already has `app_name` and `app_url` variables (Settings → Variables) — map the app's base URL/origin to `vars.app_url` instead of inventing a key. Any other `vars.*` key doesn't exist until it's created: the checkpoint asks before creating it ("Creating variables" below); until it has a value, previews render it as a placeholder host (`https://example.com`) |
| Workspace/org fields in multi-tenant products | `tenant.*` | Only if the customer models tenants in Knock |

**Is it really a constant?** Arriving in every send payload is not evidence that a value varies — SendGrid, Mailgun, and Braze templates have no environment-variable concept, so constants ride along in every payload. Ask "could this value differ between two sends?". Policy, help, and legal pages, support addresses, app origins, and brand assets — especially when the same value is implied across sibling templates or referenced from chrome — are constants; anything carrying an id, slug, or query string, a name like `cta` / `campaign` / `tracking`, or per-recipient, per-org, or per-event meaning is per-send data. When ambiguous, keep it on `data.*` (preserves the contract) and flag it `❓default`. Use the base-URL + path pattern (`vars.app_url` + `data.org_id`) when many links share one origin and differ by path, never to split a single static URL. Remember the coupling: a `vars.*` value used in a layout must exist before any preview renders, and a `data.*` value used in a layout obliges every template on that layout to send it.

Every accepted remap changes what the customer's backend must send — record it explicitly in `plan/variables.md` with before/after examples. When the user declines or doesn't engage, keep everything on `data.*`.

**Composed URLs** (`{{origin}}/{{org_path}}/settings/users`) are a contract decision, not a translation detail: keep the composition in the template by default (the trigger keeps sending the parts it already sends) and offer a single finished-URL field as a `❓default` simplification.

**Defaults policy:** never invent fallback values for transactional data (an order ID with a default hides bugs). Use `| default:` only for cosmetic fallbacks (`{{ recipient.name | default: "there" }}`).

### Creating variables

The migration creates the variables its plan uses, but only after asking. At the checkpoint, after the three lists, when the approved plan uses any `vars.*` key that doesn't exist yet, ask one question that lists each key with its proposed value — the value the source hardcodes, or, when the source doesn't carry one, a value the user supplies — and says what creating them means: a variable is account-wide, so creating one sets its value in every environment, production included, as soon as it publishes, with no commit or promotion. A brand-new key isn't used by any live email, so creating it changes none. Options: create them, change some values first, or skip (the user sets them in the dashboard, and the report lists them as must-dos).

On a yes, create them at the start of phase 3, before the layouts, because previews need the values. Use `execute_mapi_write`: `PUT /v1/variables/<key>` with `{ "type": "public", "value": "<value>", "description": "Email migration: <what it holds>" }`. Set the account-wide default only, with no per-environment `environment_values` override, so the value is already in place when the migration is promoted; use `public` for every migrated constant, never `secret`. The call needs the `variables:manage` permission; if it's refused, fall back to listing the variables for the user. Record each one under **Writes to Knock**.

Never change an existing variable's value — the built-in `app_url` and `app_name` included — without its own `❓blocking` question: the new value reaches every live email that uses it as soon as it publishes.

## Syntax translation tables

**Truthiness.** Every source family has its own idea of what `if x` means for a missing key, an empty string, or the string `"false"`. Knock's Liquid is standard Liquid: only `nil` and `false` are falsy; `""`, `"false"`, `0`, and `[]` are all truthy. Translate guards accordingly — an optional string is `{% if data.x != blank %}` (`blank` covers missing, `nil`, and `""`), a list is `{% if data.xs.size > 0 %}`, a boolean-like string is `{% if data.flag == "true" %}` — and note that a Handlebars `{{#if x}}` over a string that may be empty maps to the first form, because Handlebars treats `""` as falsy and Liquid does not. Verification renders every optional field both absent and as `""` (`rules/verifying-the-migration.md`), which is where any engine deviation from these semantics shows up, on the customer's own templates.

Per-family translation tables — Handlebars/Mustache, Mailchimp merge tags, SendGrid legacy substitutions and slots, Mako, Ruby and Python interpolation, Liquid-family sources, code interpolation — are in `references/syntax-and-format-tables.md`. Three rules travel with every table: forced renames (a key that cannot be a Liquid identifier, an unnamed positional placeholder) are `❓blocking` and go in the contract; provider *slots* such as `<%body%>` are not variables; other-language expressions get a stated translation as `❓default` when obvious and `❓blocking` only when the semantics are unclear.

## Control flow decision rules

Classify each item from the analysis files and translate accordingly:

1. **Inline copy variation** (words/sentences change) → Liquid `{% if %}` inside the block/partial content. Stays in one template.
2. **Section toggle** (a whole section appears conditionally) → `{% if %}` around the section content, or a `boolean` partial input, when the section is copy inside a block. Blocks themselves can't be conditional, so when the toggle shows or hides a button, image, or partial, prefer a `branch` step with an email step per outcome over an html block: every version stays editable as blocks in the dashboard, at the cost of duplicating the copy they share (put sizable shared sections in partials). Branches nest, so several flags still fit; keep an html block only when the outcomes multiply past what an editor could follow. Ask it once at the checkpoint as a corpus-wide `❓default`, not per template.
3. **Loop over a collection** → `{% for %}`; when the repeated unit is a component, render a partial per item (`{% for item in data.items %}{% render 'item-card', title: item.title %}{% endfor %}`) or pass the whole collection to a `list`-input partial.
4. **Batched vs single variants** (same email, aggregate copy for N events) → one workflow: `batch` step + copy switching on `{% if total_activities > 1 %}`, per-item content from `activities`. Propose at the checkpoint; needs the customer to accept that triggers-per-event replace pre-aggregated sends.
5. **Divergent whole-email variants** (subject AND body differ substantially, driven by one flag — plan tiers, user roles) → one workflow with a `branch` step and an email step per branch. Propose at the checkpoint; alternative is separate workflows (the safe default when the user is unsure).
6. **Multi-file copy variants** (the same email exported as several files that differ by a sentence or a label) → one template with `{% case data.<discriminator> %}` around the differing copy. The discriminator almost never exists in the source, so consolidating is itself a trigger-contract change: `❓blocking`, with one-workflow-per-file as the no-change fallback. Boundaries: a subject-only delta does not make a set "divergent" — the subject takes the same `{% case %}`; when the discriminator already exists in the source payload, consolidation is `❓default`; a two-file set may key on a boolean instead of an enum; and a rename or remap recorded in `analysis/_conventions.md` from an earlier pass is inherited, not re-asked.

Rule of thumb: conditionals that change *copy* stay in Liquid; conditionals that toggle whole blocks, change *which email*, or decide *whether/when it sends* belong in workflow structure (branch, batch, step conditions, delays).

Condition syntax for branches/step conditions uses structured JSON (`{"variable": "data.plan", "operator": "equal_to", "argument": "free"}`), not Liquid — see the knock-cli skill's workflow-templates rules.

## Provider artifacts

Source templates carry provider-specific machinery that must not be copied verbatim. The artifact-by-artifact table (unsubscribe tags, tracking pixels, click-tracking wrappers, UTM parameters, preference links, view-in-browser links, inline images by content-id, provider metadata) is in `references/provider-artifacts.md`. The principles:

- Unsubscribe and preference links are the customer's contract decision: never drop one from a commercial email, never add one silently, and keep the customer's own preference-center URL on `data.*`. Knock's hosted preference center and commercial-unsubscribe variables need those features configured first, so propose them as `❓fyi` follow-ups.
- Strip open-tracking pixels and restore click-wrapped hrefs to their destinations; the Knock channel re-adds tracking at send.
- Preserve UTM and attribution parameters verbatim; flag stale values and malformed encodings as `❓default` with the corrected form proposed.
- Inline images by content-id are `❓blocking` either way: supported on SendGrid, Postmark, and Resend via an attachment object, hosted-URL otherwise.

## Localization

If sources exist per locale (or switch on locale), how to handle the variants is the customer's decision: ask it as a `❓blocking` checkpoint question instead of choosing. Common options are migrating the default locale now and leaving the others for a translations follow-up, keeping a workflow per locale as today, or adopting Knock [translations](https://docs.knock.app/template-editor/translations) now. Translations are a larger project with their own setup, so if the customer chooses them, follow the docs and the customer's direction. Record the affected templates and the decision in `MIGRATION.md`.

## Deliverable: plan/variables.md

One table for the whole migration plus per-workflow trigger contracts:

```markdown
## password-reset — trigger contract

Trigger: POST /v1/workflows/password-reset/trigger

​```json
{
  "recipients": ["user_123"],
  "data": { "reset_url": "https://…", "expires_in_minutes": 30 }
}
​```

| Template variable | Source expression | Type | Required | Notes |
| ----------------- | ----------------- | ---- | -------- | ----- |
| data.reset_url | {{reset_url}} | string (URL) | yes | |
| recipient.name | {{name}} | string | via recipient | remap approved 2026-08-11 |
```

This section is copied into the final report — it's what the customer's engineers integrate against.
