---
name: knock-email-template-migration
description: Migrates existing email templates (HTML, MJML, React Email, or provider exports from SendGrid, Mailchimp, Braze, etc.) into Knock workflows, extracting shared layouts and reusable components so the result is an editable email design system. Use when a user wants to move, import, or migrate email templates into Knock.
---

# Email template migration skill

This skill migrates a directory of existing email templates into Knock. The end state is not a 1:1 HTML dump: shared chrome becomes **email layouts**, repeated components become **partials** usable in the visual block editor, template bodies become **block-based templates** wherever that's faithful, and each email is delivered by a **workflow** with a documented trigger payload contract.

The migration runs as a phased process with explicit user checkpoints and a durable on-disk workspace, so it can handle large template sets, be resumed across sessions, and never writes to Knock before the user approves the plan.

## Overview

The skill has seven rule files, read one phase at a time, and six reference files the rules point at:

1. **Migration process** - the phased state machine: preflight, intake, workspace, the plan checkpoint, build order, commit strategy, additional passes, resuming
2. **Analyzing source templates** - format detection, the corpus scan into chrome families, the per-template analysis file, verbatim body copy, syntax families, subject discovery
3. **Mapping variables and logic** - namespace policy, Liquid truthiness and guards, control-flow decisions, provider artifacts, creating variables, the trigger payload contract
4. **Extracting layouts** - what belongs in a layout, deduplication, the default-layout policy, CSS strategy for blocks, MJML layouts
5. **Extracting partials** - partial candidates, the isolated scope rule, loops, input schemas, partial content and CSS
6. **Building templates and workflows** - workflow shape, block composition, HTML and MJML modes, consolidated workflows, channel overrides, validate, push, readback
7. **Verifying the migration** - readback, rendered previews and the visual pass, test sends, the final report

The references hold the tables, templates, and recipes the rules depend on. Each opens with the rule sections that point at it and is read only when a step needs it.

## Prerequisites

CLI mechanics — installation, authentication, the `knock/` directory layout, resource file formats, and push/pull/commit semantics — belong to the **knock-cli** skill. Assume it is installed and that `knock` is authenticated; consult it when a command's flags or a resource file's shape are in doubt rather than reading it in full up front. This skill covers the migration *process* and the *decision rules*.

Required before starting:

- Knock CLI installed and authenticated (`knock whoami` succeeds)
- The account's environment model known (`knock environment list`): one environment means production-only, several means environments are enabled. It decides where the migration writes and what it commits — see the environment model step in `rules/migration-process.md` preflight
- A configured email channel in the target Knock account (`knock channel list` shows one)
- The Knock MCP server attached to this project with the **Manage resources** and **Manage data** capabilities — rendered previews run through it, and the test recipient is created with it. Without the MCP, previews need a service token (see preflight)
- The user's source template files on disk

## When to apply

- A user asks to migrate, import, or move email templates into Knock.
- A user has templates in an email provider (SendGrid, Mailchimp, Mailgun, Postmark, Braze, Customer.io), in their codebase (hardcoded HTML, MJML, React Email), or in an email builder (Parcel, BEE), and wants them managed in Knock.
- A user wants to turn an existing set of emails into a reusable Knock email design system (layouts + partials).

## How to use this skill

Read this file, then read only the rule files for the phase you are entering. Every rule file opens with its inputs, its outputs, and what to read alongside it, so a phase can be executed from that file alone; the workspace on disk (`knock-migration/MIGRATION.md`) carries state between phases and sessions. Do not skip ahead: each phase's output is the next phase's input.

### For a new migration

1. **Preflight and intake** (`rules/migration-process.md`, Phase 0 and Workspace sections)
   - Read-only checks first (CLI, environment model, email channel, existing keys, MCP capabilities), then intake, then the workspace and an inventory pull into a scratch directory, then the test recipient and the throwaway preview
   - Inventory existing resources by content and usage, not just keys
   - Record the intake answers, including where to build and how the result will be reviewed, and copy the whole source directory into the workspace

2. **Analyze** (`rules/analyzing-source-templates.md`, with `rules/mapping-variables-and-logic.md` for the proposed-mapping column)
   - Corpus scan first: chrome families, variant sets, corpus-wide conventions
   - One analysis file per template from `references/analysis-file-template.md`, body copy verbatim

3. **Plan and checkpoint** (`rules/migration-process.md` Phase 2, with `rules/extracting-layouts.md`, `rules/extracting-partials.md`, and `rules/mapping-variables-and-logic.md`)
   - Four plan files, then blocking questions one at a time, then the defaults, suspected-mistake, and opt-in lists
   - Hard stop until the user approves

4. **Build** (`rules/extracting-partials.md`, then `rules/extracting-layouts.md`, then `rules/building-templates.md`)
   - Partials, then layouts, then workflows; each resource validated, pushed by key, and read back before the next stage
   - Partials and layouts are always committed; workflows are committed when environments are enabled and stay drafts on a production-only account

5. **Verify and report** (`rules/verifying-the-migration.md`)
   - Tier 1 always; tier 2 rendered previews through the MCP with a visual pass per layout, or for every email when chosen — approved one at a time, or reviewed together at the end; tier 3 test sends when chosen
   - `REPORT.md` with trigger contracts and promotion instructions (environments enabled) or publishing instructions (production-only)

### For an additional pass or a resumed migration

1. **Read `knock-migration/MIGRATION.md` first** - it records the phase, the decisions, and the next unfinished template
2. **Follow the Additive migrations, Additional passes, and Resuming sections** (`rules/migration-process.md`)
   - A resumed session does not rerun phase 0: it uses the recorded target flags and never enters phase 3 without a recorded checkpoint approval
   - Existing resources are reuse candidates; new passes append dated sections; never pull into the project's knock directory

### For a question mid-migration

- Which block a section becomes: the block selector table in `rules/building-templates.md`
- How to guard an optional partial input: the isolated scope rule in `rules/extracting-partials.md`
- Which layout takes the `default` key: the default-layout policy in `rules/extracting-layouts.md`
- Why a render differs from the source: tier 2 in `rules/verifying-the-migration.md`

## Rule files reference

- `rules/migration-process.md` - Phases 0 and 2 and the state machine for all four: preflight, the environment model, intake, workspace layout, the checkpoint shape, build order, commit strategy, additional passes, parallel analysis, resuming
- `rules/analyzing-source-templates.md` - Phase 1: format detection, chrome families and variant sets, the analysis file, body-copy conventions, syntax families, control-flow classes, subject discovery
- `rules/mapping-variables-and-logic.md` - Namespace mapping policy, creating variables, truthiness and guard forms, control-flow decision rules, provider artifacts, localization, the `plan/variables.md` contract
- `rules/extracting-layouts.md` - Layout contents and contracts, splicing, deduplication and reuse, default-layout policy, file structure, CSS strategy for block fidelity, MJML layouts
- `rules/extracting-partials.md` - Partial candidates and dispositions, isolated scope, repeated partials and loops, `input_schema`, content and CSS rules, file structure
- `rules/building-templates.md` - Workflow shape and key derivation, block-first composition, HTML and MJML modes, consolidated workflows, channel overrides, validate, push, commit, readback
- `rules/verifying-the-migration.md` - The three verification tiers, the tier 2 checklist and visual pass, test sends, the final report

## Reference files

- `references/analysis-file-template.md` - The analysis file structure, copied for every template (phase 1)
- `references/syntax-and-format-tables.md` - Format detection, syntax families, and per-family translation tables (phases 1 and 2)
- `references/provider-artifacts.md` - Unsubscribe links, tracking, UTM parameters, inline images, provider metadata (phases 1 and 2)
- `references/builder-exports.md` - Builder export markers and the layout splicing recipe (phases 1 and 3)
- `references/knock-blocks.md` - Block selectors and per-block spacing, branch workflows, channel overrides (phase 3)
- `references/verification-recipes.md` - Preview endpoints, MCP recipes, service-token handoff, text oracle, style fingerprint, visual pass (phase 4)

## Quick reference

### Phase map

| Phase | Read when entering | Produces |
| ----- | ------------------ | -------- |
| **0 · Preflight and intake** | `rules/migration-process.md` (Phase 0 and Workspace sections; on an additional pass also the Additive migrations and Additional passes sections; a resumed session reads the Resuming section instead) | `knock.json`, `knock-migration/MIGRATION.md` with intake answers, target flags, and inventory, `knock-migration/source/`, `knock-migration/inventory/` |
| **1 · Analyze** | `rules/analyzing-source-templates.md`, plus `rules/mapping-variables-and-logic.md` for the "Proposed mapping" column | `analysis/_chrome-families.md` and `analysis/_conventions.md` from the corpus scan, then one `analysis/<stem>.md` per template (or variant set) |
| **2 · Plan and checkpoint** | `rules/migration-process.md` (Phase 2), `rules/extracting-layouts.md`, `rules/extracting-partials.md`, `rules/mapping-variables-and-logic.md` | `plan/layouts.md`, `plan/partials.md`, `plan/variables.md`, `plan/workflows.md` — then a **hard stop** until the user approves |
| **3 · Build** | `rules/extracting-partials.md`, then `rules/extracting-layouts.md`, then `rules/building-templates.md` | `knock/partials/`, `knock/layouts/`, `knock/workflows/` — each stage validated, pushed, read back, and committed per the account's environment model before the next |
| **4 · Verify and report** | `rules/verifying-the-migration.md` | `knock-migration/previews/` (renders and the side-by-side comparison page, offered in the browser), `REPORT.md` with trigger contracts |

### Critical guardrails

These invariants prevent broken or destructive migrations — never break them, in any mode, for any corpus. Everything else in this skill (the phases, workspace shapes, file formats, batch sizes) is the **proven default plan**: follow it by default; when the setup genuinely doesn't fit, adapt the plan, keep every invariant, and record what changed and why in the `MIGRATION.md` decision log. A large corpus (a hundred templates or more) is the common case: group templates by pattern, script the repetitive steps, and keep long lists in workspace files rather than chat. Agents that build or verify read that phase's rule files themselves; a brief adds the corpus decisions, never replaces them.

1. **Never write to Knock before the user approves the migration plan.** Phases 0-2 write no resources to Knock: pulls, lists, render-only previews, the test recipient, and a branch when the user chose one — each recorded under **Writes to Knock** in `MIGRATION.md`.
2. **Build order is partials → layouts → workflows, and partials and layouts are committed before any workflow uses them** — on either environment model. Templates render the *published* version of partials and layouts, so an uncommitted partial renders as missing in previews and sends.
3. **Partials render in an isolated Liquid scope.** Only explicitly passed arguments plus `vars` are available inside partial content. `data`, `recipient`, `actor`, and `tenant` are NOT ambient — bind them at the call site.
4. **Compose bodies only from the six email block types** — `markdown`, `html`, `button_set`, `image`, `divider`, `partial` — and remember that blocks stack vertically: any side-by-side layout lives *inside* a single block. Build multi-column sections as partials (editable) or html blocks (frozen).
5. **Never rewrite bespoke email markup as markdown.** Markdown blocks are for simple prose only. Preserve table layouts and Outlook conditional comments (`<!--[if mso]>`) verbatim inside html blocks or partials.
6. **Body copy is verbatim content.** Capture it exactly in the analysis file and carry it into templates unchanged — never paraphrase, summarize, or reconstruct prose from structure notes or memory. Verification asserts the source's text against the rendered output.
7. **Never overwrite existing Knock resources without explicit confirmation.** This includes the account's `default` email layout and any workflow/partial/layout key that already exists.
8. **Never change the customer's trigger data contract without approval.** The default mapping is `data.*` with original variable names; any remap (e.g., to `recipient.*`) is opt-in at the plan checkpoint.
9. **Never promote, and never publish a workflow.** When environments are enabled, the migration pushes and commits in development (or a branch) and never touches production. On a production-only account, a commit publishes live, so the migration commits only partials and layouts (templates can't render without them, and changing an existing one needs explicit approval at the checkpoint) and leaves every workflow as an unpublished draft. The final report tells the user how to promote (environments enabled) or publish (production-only).
10. **A template is not migrated until verified.** Every resource passes push + readback before it's marked Pushed, and every template's rendered output is checked against source-derived assertions at the depth chosen at intake.
