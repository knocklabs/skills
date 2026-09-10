---
title: Migration process
description: The phased migration state machine, workspace layout, user checkpoints, build order, and commit strategy
tags:
  - knock
  - migration
  - email
  - process
  - workflow
category: knock-email-template-migration
last_updated: 2026-09-08
---

# Migration process

> **Phases 0 and 2 of 4, and the state machine for all four.** Inputs: the source directory and the intake answers (phase 0); the analysis files (phase 2). Outputs: `knock.json`, the pulled `knock/` inventory, `knock-migration/MIGRATION.md` and `source/` (phase 0); the four `plan/*.md` files and the checkpoint (phase 2). Read alongside: the phase-specific rule files named in the SKILL.md phase map; the `knock-cli` skill for command flags.

The migration is a five-phase state machine. Phases 0-2 never write to Knock. Phase 3 writes resources in a strict dependency order. Phase 4 verifies. The workspace on disk is the source of truth for progress — always read `knock-migration/MIGRATION.md` first when starting or resuming a migration.

## Phase 0: preflight and intake

### Preflight checks

Run these before anything else. Stop and help the user resolve failures (see the `knock-cli` skill for installation and authentication):

```bash
knock whoami                 # CLI installed and authenticated
knock channel list           # must include an email channel; record its `key` for channel_key and its provider
knock environment list       # confirm the target environment exists
```

Note the email channel's provider: Knock's built-in limited sender delivers only to account members' addresses, which constrains live test sends in phase 4.

Then check that the **Knock MCP server** is attached to this project: call one of its read-only tools, such as `list_environments` or `search_mapi`. If no tool from the Knock MCP server is available, stop and help the user attach it before continuing — the Knock MCP docs give the configuration for each coding agent — because rendered previews in phase 4 run through the MCP unless the user supplies a service token. Most agents configure MCP servers per project directory, so a server that works in a sibling project is not automatically available in a new workspace.

Then run one **throwaway preview** through `execute_mapi_write`: `POST /v1/workflows/<any existing workflow>/steps/<its email step ref>/preview_template` with an empty `data` object and the test recipient (create `migration-test-user` first with the MCP `upsert_user` tool — every later render needs it), and assert that `res.result.template.html_content` is a non-empty string (request shape and guard in `references/verification-recipes.md`). One call proves that the session has write access (the write tool exists only for read-write sessions), that it carries the `workflows:run` permission the preview endpoint requires, and that the response has the field the recipes read. A failure here is a setup problem to fix now, not in phase 4. On an account with no workflow yet, run the same call right after the first workflow push in phase 3.

**Service token.** Rendered previews and their checks run through the MCP without a token, so do not raise one when the MCP check passes. A token is needed in two cases only: the MCP cannot be attached (arrange it **now**, before phase 1), or the user chooses the render-archive option in the checkpoint's verification question (arrange it then, before phase 3). Check for `KNOCK_SERVICE_TOKEN` in the environment (test for its presence; never print it); if it is absent, also check for a git-ignored `.env` in the project or in `knock-migration/` that exports it and source that file in the scripts that need the token, but do not suggest the file route. If neither is present, the token has to enter the agent's environment from outside — an `export` inside a tool call does not persist between calls, and a token typed into the chat lands in the transcript — so never ask for it in the conversation. Instead: first record every checkpoint answer, including the verification choice, in the decision log so nothing is lost; then tell the user exactly how to proceed: an account owner or admin creates a dedicated token (dashboard: Settings → Service tokens → New token; shown once, starts with `knock_st_`); in the terminal they run the agent from, `export KNOCK_SERVICE_TOKEN=<token>`; then restart the agent in the same project directory and ask it to continue the migration. On that resume, `MIGRATION.md` shows the plan approved and the verification choice made: confirm the token targets the right account with `GET /v1/whoami` and the throwaway preview over curl (`references/verification-recipes.md`), then start phase 3.

Run everything below from the Knock project directory chosen at intake. Then locate the Knock directory. If the project has no `knock.json`, **do not run `knock init`** — it is interactive-only (no flags to answer its prompt) and defaults to a hidden `.knock` directory. Write the config directly, exactly as init would:

```json
{ "$schema": "https://schemas.knock.app/cli/knock.json", "knockDir": "./knock" }
```

Then create the directory and inventory existing resources so the migration never collides with or overwrites them:

```bash
mkdir -p ./knock
knock pull --force
```

Record the existing workflow, layout, and partial keys in `MIGRATION.md`. Any key collision found later must be surfaced to the user, never silently overwritten.

**Inventory content, not just keys.** Read the pulled `default` layout (and any resource whose key the plan will reuse). Concretely: grep its `html_layout` for `{% render` (partials it depends on — check they exist with `knock partial list`), for hex colors and font `<link>`s that are not Knock's stock ones, and for a company or product name. Anything non-stock means the layout was customized: flag it `❓blocking` — reuse, replace, or leave untouched is the user's call — never treat it as stock because the key is expected. Record the verdict (stock and unused, or customized / in use): it decides whether the most-used migrated layout takes the `default` key (default-layout policy in `rules/extracting-layouts.md`). Note that `knock pull` prints "Successfully created the … directory" for every resource type, including ones with zero resources where no directory is created; trust `ls knock/` and the `knock <resource> list` commands, not the pull log.

Offer to run the whole migration in one (`knock branch create email-migration`) so it stays isolated from other work in the development environment.

### Intake

Six answers are needed before phase 1. Take any the user's prompt already gave; for the rest, present **one confirmation card** and wait for an explicit reply — never fill them in silently, whether from the skill's defaults or from what the files suggest. A "just do it", "test run", or "use your judgment" framing does not skip the card; it only means the user will probably reply "go".

1. **Source directory**: where the template files are, and anything in it to skip.
2. **Knock project location**: where `knock.json`, `knock/`, and `knock-migration/` live. Default: a new directory next to the source files; the customer's app repo only if they name it. Every `knock` command in this skill runs from that directory — the CLI resolves `knock.json` from the current directory.
3. **Target shape**: a new workflow per email (default), or email steps added to existing workflows — which ones?
4. **Composition mode**: block-first (default: visual blocks + partials, editable by non-technical users) or pixel-perfect HTML mode (raw HTML bodies + `{% render %}` partials). State the tradeoff in one sentence each.
5. **Environment**: development (default), or a branch.
6. **Naming**: any key prefix or naming conventions to follow.

The card lists only the answers the prompt did not give, one line each: the proposed value and its basis — `(default)`, or `(from the files: …)` when the corpus suggested it, e.g. "skip `drafts/` and `.DS_Store` (from the files: 3 files in `drafts/` are unfinished copies)". End with "reply go, or change any". Record every answer in `MIGRATION.md` with its basis (given, default, or confirmed inference). Verification depth is not an intake answer: it is asked explicitly as the last plan-checkpoint question, where the corpus size is known (see Phase 2).

Do not ask about things the files settle outright (format detection, chrome families); those are findings, not decisions, and belong in the analysis. In an additional pass over the same workspace, reuse the recorded intake answers unless the user's prompt changes one, and write "inherited from pass N" in the new pass's intake section.

## Additive migrations (adding to an existing Knock setup)

When the account already has migrated or hand-built resources (intake answers, or preflight finds substantive layouts/partials), the process runs unchanged — additive mode changes the *inputs to the plan*, not the phases:

- Preflight inventory becomes **reuse discovery**, not just collision safety: pulled layouts and partials enter the dedup pools as first-class candidates.
- The corpus scan fingerprints new templates against **existing Knock layouts** as well as each other (compare chrome against each layout's `html_layout`), and partial candidates against **existing partial content**. A new template whose chrome fits a live layout should land on that layout.
- The plan checkpoint decides **reuse / extend / create** for every layout and partial candidate. *Extend* changes already-live emails: before proposing it, find the affected workflows (grep the pulled workflow directories for `{% render '<key>' %}` and for partial blocks using that key) and list them in the checkpoint item — extending a shared resource without that list is an overwrite in disguise (guardrail 7). Level: an extension is `❓default` when re-rendering one live template per affected layout or partial shows no change (attach the affected-workflow list and the render evidence); it is `❓blocking` if any live render changes.
- Follow the account's existing naming conventions for new keys, not this skill's defaults.
- Building a parallel set of near-duplicate layouts and partials next to the live ones is a failure outcome. When reuse is close but imperfect, surface the tradeoff at the checkpoint instead of quietly creating `footer-2`.

## The workspace

Create `knock-migration/` in the Knock project directory (suggest adding it to `.gitignore` if the user doesn't want it committed — recommend keeping it until the migration is approved and promoted). Copy the **whole** source directory into `knock-migration/source/` at intake (template exports are small; skip dotfiles and empty directories, which have no key-derivation rule) and record which files are in scope as a list in `MIGRATION.md`; point every analysis file at the copy. A partial copy leaves the corpus scan's evidence (out-of-scope siblings, mislabeled duplicates) unreachable, agents may be unable to read outside the project directory, and a full copy lets the migration resume and re-verify even if the originals move:

```
knock-migration/
├── MIGRATION.md
├── source/                     # copy of the whole source directory, taken at intake (scope is a list in MIGRATION.md)
├── analysis/
│   ├── _chrome-families.md     # corpus scan: chrome families and variant sets
│   ├── _conventions.md         # corpus scan: syntaxes, malformed-expression convention, forced renames, approved remaps
│   └── <template-stem>.md      # one per source template, written during phase 1
└── plan/
    ├── layouts.md              # phase 2 output
    ├── partials.md
    ├── variables.md
    └── workflows.md
```

### MIGRATION.md structure

```markdown
# Email template migration

## Intake
- Source: ../emails/ (48 templates; skip: drafts/)
- Target: new workflow per template | Mode: block-first | Env: development
- Existing resources: 3 workflows (…), 1 layout (default — stock, unused), 0 partials

## Status

| Template | Analyzed | Planned | Built | Pushed | Committed | Verified |
| -------- | -------- | ------- | ----- | ------ | --------- | -------- |
| password-reset | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| account-signup | ✅ | ✅ | — | — | — | — |

## Decisions
- 2026-08-11: "User comments" consolidated into one workflow with a batch step (user approved).
- 2026-08-11: Verification: MCP previews + visual pass per layout; test sends to test@example.com added by the user at the checkpoint.

## Open questions
- ❓ `Deleted Item.html` has no discoverable subject line; drafted "Your item was removed" — needs approval.
```

Update the status table and decision log as you go. Every unresolved item becomes a ❓ entry tagged `blocking`, `default`, or `fyi` (levels defined in `rules/analyzing-source-templates.md`). The plan checkpoint cannot pass while **blocking** items are unanswered; `default` items are presented as one "applied unless vetoed" list; `fyi` items go straight to the final report.

## Phase 1: analyze

Start with the **corpus scan** (`rules/analyzing-source-templates.md`): fingerprint chrome across every file, group templates into chrome families, pair variant sets, and write `analysis/_chrome-families.md`. Then analyze templates **one at a time** and write `analysis/<stem>.md` immediately after each — variant sets share a single analysis file with per-variant sections. Never hold more than one source template in working memory — the analysis files are how large sets stay tractable and how the migration resumes after interruption.

Read-only phase: no resource writes to Knock (render-only previews are allowed), no file writes outside `knock-migration/`.

## Phase 2: plan and checkpoint

Consolidate the analysis files into the four plan documents:

- `plan/layouts.md` — deduplicated layout set, which templates use each, default-layout proposal (`rules/extracting-layouts.md`)
- `plan/partials.md` — partial inventory with usage matrix and drafted `input_schema` per partial (`rules/extracting-partials.md`)
- `plan/variables.md` — every source variable → Knock namespace mapping, with types and example values (`rules/mapping-variables-and-logic.md`)
- `plan/workflows.md` — template → workflow/step topology, proposed keys, subjects, and any consolidation proposals (variant sets → one workflow with batch/branch; `rules/mapping-variables-and-logic.md`)

Minimal skeleton per plan file (headings in this order, so the checkpoint and the final report can be assembled from them):

- `layouts.md`: **Layout set** (table: key · family · templates · format) · **Per-layout design** (skeleton source, header, `{{ content }}` placement, footer, CSS additions, `text_layout`) · **Default-layout policy** · **Open questions**
- `partials.md`: **Candidate dispositions** (table: candidate · seen in · family-wide reuse · disposition: partial / built-in block / html block) · **Partial specs** (name, icon, `input_schema`, content, example invocation) · **Usage matrix** · **Key collisions**
- `variables.md`: **Corpus-wide map** (table) · **Remap proposals** · **Per-workflow trigger contracts** (trigger snippet + variable table each)
- `workflows.md`: **Topology** (table: key · layout · subject in Liquid · blocks in order · consolidation) · **Consolidation proposals** · **Body composition notes** · **Step shape**

Then present the plan to the user as a short summary, the **blocking** ❓ questions asked one at a time, then the default, suspected-mistake, and opt-in lists, and **stop**. Two recurring cases are `default`, not blocking, so they do not multiply the question count: a sibling of a workflow that is already live becomes its own workflow (extending the live one is offered, not asked); byte-identical source files become one workflow keyed on the first file, with the others recorded as aliases in the plan and the report.

**Verification is always an explicit question** — the last one in the checkpoint, in the same card shape, even when the user called the run a test or gave no preference; it is never inferred or folded into the default list, because it decides what "done" means and whether a service token or an inbox is needed:

```
Q<n>. How should the migration be verified?

Options:
  A. Readback, rendered previews through the Knock MCP, and a side-by-side
     visual pass for one template per layout. No token, no sends.
  B. A, plus live test sends to <inbox> (sandbox run first, then delivery).
  C. A, plus a full archive of every render on disk. Needs a service token
     (arranged before phase 3); through the MCP alone each archived render
     costs about twice its size in output tokens.

Recommendation: A. For sets over ten templates the visual pass samples one
template per layout, partial, and control-flow pattern.
Reply with a letter; for B, name the inbox.
```

Record the answer in the decision log; it sets the tier `rules/verifying-the-migration.md` runs.

Present blocking questions **in the chat, not by pointing at plan files**: the plan is the record, the chat is the interface. Ask them **one at a time**, each waiting for its answer before the next, so every question is read before it is answered and later questions can build on earlier answers; never batch them, and where the agent has a structured question tool use it with one question per call. The verification question is always the last. Each is written for a reader who has **not** opened the workspace and follows one shape:

```
Q1. Consolidate the three "plan changed" emails into one workflow?

Source: three exported files (upgraded, downgraded, cancelled) that differ by
one sentence describing the change.

Options:
  A. One workflow keyed on a NEW trigger field data.plan_change
     (upgrade | downgrade | cancel). The backend must start sending it.
  B. Three workflows, one per file. No payload change; three near-identical
     templates to maintain.

Recommendation: A — the sending code already knows which file it picked.
Reply with a letter, or "A but call the field change_type".
```

That is: a one-line question; **Source** (which template(s) and what the source does today, in a sentence); **Options**, lettered, each with its consequence for the trigger payload and for the email; **Recommendation** with the reason; and how to answer. Workspace ids (`B1`, `L2`) belong in the plan files, never in the prompt. After the last question, present three lists in one message, each ending with its own reply instruction, and proceed on nothing less than an explicit reply: **Defaults** — one line each (`template → what I'll do → why`), ending "reply go, or name the ones to change"; **Suspected source mistakes** — consolidated from the analysis files, one line each (`what · where · default: reproduce what the source rendered · alternative: fix it`), ending "reply go, or name the ones to fix"; **Offered, not applied** — the opt-in remaps and simplifications the mapping rule produced (`actor.*`, `vars.*` for a constant, a finished-URL field), one line each (`what → what changes if you take it`), ending "name any to apply". Nothing in these lists is applied or skipped on silence. Required approvals before phase 3:

- The overall plan (layouts, partials, workflow topology, keys)
- Every drafted subject line for templates that had none
- Any proposed consolidation of variant templates into one workflow
- Any remapping of variables off the default `data.*` contract
- Any overwrite of an existing resource, especially the `default` layout
- Handling for unresolved assets, unsubscribe links, or unmappable variables

Record approvals in the decision log. If the user changes the plan, update the plan docs first, then proceed.

## Phase 3: build

Build order is mandatory, because templates render only the *published* (committed) version of partials and layouts:

1. **Partials**: write `knock/partials/<key>/`, then per partial `knock partial validate <key>`, `knock partial push <key>`, and commit `knock commit --resource-type=partial --resource-id=<key>`.
2. **Layouts**: write `knock/layouts/<key>/`, then per layout `knock layout validate <key>`, `knock layout push <key>`, and commit `knock commit --resource-type=email_layout --resource-id=<key>`.

Push **by key**, never `--all`: the preflight pull placed the account's existing resources (the stock `default` layout, any live partial) in the same directories, and `--all` would push those copies back — reverting any dashboard edit made since the pull (guardrail 7).
3. **Workflows**: write `knock/workflows/<key>/`, then per workflow: `knock workflow validate <key>`, `knock workflow push <key>`, and commit `knock commit --resource-type=workflow --resource-id=<key>`.

On an account with no workflow yet, push the first workflow alone, then run the deferred preflight preview and one render; revise the layout CSS against that render, re-push the layouts, and only then build the remaining workflows.

Update the status board after each template. If validation fails, fix and re-validate before pushing; never push a resource that fails validation. But treat `validate` as a shape check, not the gate — some server-side checks run only on push, so **push success is the real gate**. Commit only after a successful push, and mark a resource Committed only after `knock <resource> get <key>` returns it: a scoped commit for a resource that never pushed still reports success and would record a phantom ✅ on the status board.

### Commit strategy

On a shared development environment, scope commits to the resources this migration created so unrelated pending changes are never swept up:

```bash
knock commit -m "Migration: add <key> partial" --resource-type=partial --resource-id=<key> --force
knock commit -m "Migration: add <key> layout" --resource-type=email_layout --resource-id=<key> --force
knock commit -m "Migration: add <key> workflow" --resource-type=workflow --resource-id=<key> --force
```

In an isolated branch, bulk commits (`knock commit -m "Migration: partials" --force`) are acceptable. Never run `knock commit promote` — promotion to higher environments is the user's decision, documented in the final report.

## Phase 4: verify and report

Verify each workflow at the depth chosen in the checkpoint's verification question, per `rules/verifying-the-migration.md`, then write the final report (created resources, template → workflow map, per-workflow trigger payload contract, remaining TODOs, promotion instructions).

## Additional passes in the same workspace

A second or later pass (more templates from the same corpus, or a follow-up batch months later) shares the workspace and **appends**; it never starts a parallel workspace or rewrites earlier records:

- `MIGRATION.md`: add dated `## Intake (pass N)`, `## Status (pass N)`, `## Built resources (pass N)`, `## Decisions (pass N)`, `## Verification log (pass N)`, and `## Open questions (pass N)` sections. Earlier sections stay as the approved record.
- `plan/*.md`: append a `## Pass N` section to each of the four files with the same headings as the original; earlier plan sections are the approved decisions the new pass inherits.
- `analysis/_chrome-families.md`: add a dated addendum for new families, new members of existing families, and corrections to earlier `(probable)` claims. Earlier per-template analysis files are untouched; new templates get new files.
- `previews/passN/` for renders and `previews/compare/passN.html` for the visual comparison; `REPORT.md` gains a `## Pass N` section.
- Existing resources in Knock are reuse candidates first (see "Additive migrations" above); a pass that rebuilds a live layout or partial must list the workflows it changes.
- **Do not `knock pull --force` over a workspace that already holds local files** — it overwrites uncommitted drafts. Inventory keys with `knock workflow list`, `knock layout list`, and `knock partial list` (or the MCP), and if dashboard-side edits are suspected, pull into a scratch project directory with its own `knock.json` and diff it against the workspace.

## Parallelizing analysis

Phase 1 can be fanned out to several agents (one per chrome family works well) once the corpus scan is done. Finish and **freeze** `analysis/_chrome-families.md` and `analysis/_conventions.md` first; every agent gets both, treats them as read-only, and writes only its own `analysis/<stem>.md` files. The orchestrator owns `MIGRATION.md` and the status board, applies any corrections the agents report (a family a template does not fit, a syntax the scan missed) after every agent has finished, and merges their ❓ items into `MIGRATION.md` before planning. Hand each agent this brief verbatim:

```
You are analyzing <N> templates for a Knock email migration. Rules: rules/analyzing-source-templates.md
and rules/mapping-variables-and-logic.md; file structure: references/analysis-file-template.md.
Inputs (read-only): knock-migration/source/, analysis/_chrome-families.md, analysis/_conventions.md
(including the malformed-expression convention).
Outputs: analysis/<stem>.md for your templates only — nothing else. Do not edit MIGRATION.md,
_chrome-families.md, _conventions.md, or any other agent's file.
Report back: your ❓blocking / ❓default / ❓fyi items, and any correction to the frozen files
(a family a template does not fit, a syntax the scan missed) as a note — do not apply it.
```

## Resuming and batching

- On any new session, read `MIGRATION.md` first; it tells you the phase and the next unfinished template.
- After a restart to supply a service token, the decision log already holds the approved plan and the verification choice: run preflight's service-token confirmation and go straight to phase 3 — do not re-ask the checkpoint.
- Re-running a phase for a template is safe: analysis files are overwritten in place; builds re-push the same keys (idempotent upsert).
- For large sets, process in batches of 5-10 templates per phase-1/phase-3 sitting, updating the status board between batches. The plan checkpoint (phase 2) still happens once, over the full set — partial and layout extraction only work well with the whole corpus analyzed.
