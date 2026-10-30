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
last_updated: 2026-10-29
---

# Migration process

> **Phases 0 and 2 of 4, and the state machine for all four.** Inputs: the source directory and the intake answers (phase 0); the analysis files (phase 2). Outputs: `knock.json`, the pulled `knock/` inventory, `knock-migration/MIGRATION.md` and `source/` (phase 0); the four `plan/*.md` files and the checkpoint (phase 2). Read alongside: the phase-specific rule files named in the SKILL.md phase map; the `knock-cli` skill for command flags.

The migration is a five-phase state machine. Phases 0-2 never write to Knock. Phase 3 writes resources in a strict dependency order. Phase 4 verifies. The workspace on disk is the source of truth for progress — always read `knock-migration/MIGRATION.md` first when starting or resuming a migration.

## Phase 0: preflight and intake

Phase 0 has four steps, in this order: read-only checks, intake, workspace and inventory, then the test recipient and smoke preview. Nothing is written to Knock or to disk until intake is answered, because the answers decide where everything goes.

### Step 1: read-only checks

Run these first. Stop and help the user resolve any failure (the `knock-cli` skill covers installation and authentication):

```bash
knock whoami                 # CLI installed and authenticated
knock channel list           # must include an email channel; record its `key` for channel_key and its provider
knock environment list       # one environment = production-only; several = environments enabled
```

If there's more than one email channel, ask which one the workflows use, recommending the customer's own provider over Knock's test channel. Note the email channel's provider: Knock's built-in limited sender delivers only to account members' addresses, which constrains live test sends in phase 4.

**Environment model.** `knock environment list` decides where the migration writes and what it may commit. It governs intake question 5, the target flags, the phase 3 commit policy, the preview recipes, and the final report:

- **One environment: production-only.** Environments are not enabled, so there are no branches and no promotion. `knock push` creates drafts in production and `knock commit` publishes live. The migration commits only partials and layouts, which templates cannot render without, and leaves every workflow as a draft (commit strategy in phase 3). Every write this skill makes — the test recipient in step 4 included — lands in production.
- **Several environments: environments enabled.** The migration targets development (the account's default) or a branch of it, commits there, and never writes to or promotes into production. Development starts fresh when environments are enabled, with only a copy of the `default` layout, while earlier content stays in production — so production is inventoried too, and a planned key that already exists there is a `❓blocking` collision: promoting the development resource later overwrites the live one (guardrail 7).

**Key inventory.** List the existing workflows, layouts, and partials (`knock workflow list`, `knock layout list`, `knock partial list`) in the environment the migration will build in — production on a production-only account, development otherwise, since a branch starts from development's content — and, with environments enabled, again with `--environment=production`. These reads tell intake whether there are workflows to extend (question 3) and tell the plan which keys are taken.

**Knock MCP server.** Call a read-only tool such as `list_environments` or `search_mapi` to confirm the server is attached to this project, then confirm the session has the two capabilities the migration uses: **Manage resources**, which provides `execute_mapi_write` (the preview endpoints are POSTs), and **Manage data**, which provides `upsert_user` for the test recipient and is off by default on the OAuth consent screen. If the server or either tool is missing, stop and help the user reconnect with both enabled before intake, so they reconnect only once — the Knock MCP docs give the configuration for each coding agent. Most agents configure MCP servers per project directory, so a server that works in a sibling project is not automatically available here. If the user cannot enable Manage data, they create the test recipient in the dashboard instead (step 4); if the MCP cannot be attached at all, previews need a service token (step 4).

### Step 2: intake

Eight answers are needed before phase 1. Take any the user's prompt already gave; ask for the rest **one question at a time**, each as a plain-language question with selectable options, and wait for the answer — never fill them in silently, whether from the skill's defaults or from what the files suggest. A "just do it", "test run", or "use your judgment" framing does not skip the questions; it only means the user will probably pick the recommended option each time.

1. **Source directory**: where the template files are, and anything in it to skip.
2. **Knock project location**: where `knock.json`, `knock/`, and `knock-migration/` live. Default: the directory the agent was launched in, where its MCP configuration and permissions apply; another directory only if the user names one. If the directory already has a `knock.json`, the migration uses that file's `knockDir`. Every `knock` command in this skill runs from that directory — the CLI resolves `knock.json` from the current directory. Ask it without naming any of those files — for example, "Where should I keep the migration's working files? (A) Here, in `<launch directory>` (recommended) — your email files in Knock's format, plus my notes, plans, and previews in a `knock-migration` folder you can delete afterwards. (B) Somewhere else — tell me the folder." When the folder already holds a Knock project, say so in option A ("this folder already manages your Knock resources; I'll add the migrated emails alongside them").
3. **Target shape**: a new workflow per email (default), or email steps added to existing workflows — which ones? Skip this question when the key inventory found no workflows, and record the answer as "new workflow per email (no existing workflows)".
4. **Composition mode**: block-first (default: visual blocks + partials, editable by non-technical users) or pixel-perfect HTML mode (raw HTML bodies + `{% render %}` partials). State the tradeoff in one sentence each.
5. **Environment**: depends on the environment model found in preflight — development or a branch when environments are enabled; on a production-only account, build there as drafts or turn on environments first (see the environment question below).
6. **Naming**: any key prefix or naming conventions to follow.
7. **Review scope**: a side-by-side comparison for one representative email per layout (default); every email, approved one at a time as each is verified; or every email on one comparison page at the end. Both every-email options need a service token, arranged before phase 1.
8. **Test sends**: none (default), or test emails to a named inbox.

Write every question for someone who has never read this skill: none of the labels above ("target shape", "composition mode"), no internal mechanics, just the question in their terms and what each option means for them. Use the agent's structured question tool where it has one, one question per call: two to four options, the recommended one first and marked as such, and when the files suggest an answer, make it an option whose description says what was found ("Skip `migration-plan.html` and `knock.json` — they look like an earlier attempt's plan and config, not templates"). Answers that are free text (a path, a naming convention) go through the tool's custom-answer option. Without such a tool, ask the same question in text with lettered options and wait for the letter. For example, composition mode becomes: "How should the email bodies be built?" with options "From editable blocks (recommended) — your team can edit them in the dashboard" and "As the exact HTML — byte-faithful, but only engineers can change it". Record every answer in `MIGRATION.md` with its basis (given, default, or confirmed inference).

**Verification is always asked explicitly** — questions 7 and 8 of intake, even when the user called the run a test or gave no preference; never inferred or folded into a default list. That reasoning, and the mechanics after the cards, are for you: the user sees only the questions, phrased as what they will get to look at and what they need to provide, with no counts of layouts, partials, or patterns and no mention of tiers, the MCP, or token mechanics. Every email is checked automatically whichever they choose; the questions decide what they review by eye and whether anything is sent.

```
Q7. How much would you like to review side by side before we finish?

Options:
  A. A few representative emails (recommended). Every email is rendered
     and compared to the original automatically; you review a comparison
     page for one representative email per distinct design. Nothing else
     needed from you.
  B. Every email, one at a time. Same automatic checks; as each email is
     verified, I show you its side-by-side comparison and wait for you to
     approve it or ask for changes before moving on to the next.
  C. Every email at the end. Same automatic checks, plus one comparison
     page covering every migrated email once they're all done.

B and C save each rendered email in the project folder, which needs a
service token and one restart of this session; I'll explain how.

Reply with a letter.
```

```
Q8. Would you also like test emails sent to an inbox?

Options:
  A. No (recommended unless you want to check them in a real mail client).
  B. Yes — tell me the inbox, and I'll send a test of each email for
     you to confirm (on a large set, I'll ask whether you'd rather check a
     representative sample).

Reply with a letter; for B, name the inbox.
```

Behind the options: all three options of the first question are tier 1 plus tier 2 through the MCP. A adds the visual pass on one template per layout (for sets over ten templates the sample also covers each partial and control-flow pattern — the card says only how many emails the comparison covers, never what the sample is built from). B and C render every template through the direct path and build a comparison for each, which needs the service-token handoff **now**, before phase 1 (see the service-token step in preflight); B pauses after each template for the user's approval (the one-at-a-time loop in `rules/verifying-the-migration.md`), and C presents them all at the end. Check for `KNOCK_SERVICE_TOKEN` before writing the card; if it is already set, replace the note under the options with "Your service token is already set up, so B and C need nothing else from you." When the user chose B, word the second card's option B as "Yes — tell me the inbox, and each email's test arrives as part of approving it." On a production-only account, add to the second card's option B that the test emails go out through the live email provider. A "yes" to the second question adds tier 3 (a sandbox run first, then delivery). Record both answers in `MIGRATION.md`; they set the tier and scope `rules/verifying-the-migration.md` runs.

**The environment question follows the environment model.** With environments enabled, ask whether to build in development (recommended — the account's default) or in a branch of development (`knock branch create email-migration`, then `--branch=email-migration` on every environment-scoped command), which keeps the migration isolated from other work in progress there. Never offer production. On a production-only account, offer both paths below **without marking either as recommended** — the one exception to the recommended-first rule, because the right model depends on who will own these emails, not on anything the files show:

```
Q5. Where should the migrated emails be built?

Your Knock account has a single environment today: production.

Options:
  A. Keep your current setup. The emails are built as unpublished drafts
     in production, so nothing sends until you publish each one. New
     shared layouts and components are published, because emails can't
     render without them; that doesn't change any email that's already
     live. Any change to something already live is asked about first.
  B. Turn on environments first. This adds a development environment,
     separate from your production users and data, where the emails are
     built and tested before you promote them to production. An account
     owner or admin turns it on in the dashboard, and it can't be turned
     off. Teams usually choose this when engineers own these emails and
     ship them alongside app code.

Reply with a letter.
```

On B: ask the user to enable environments (dashboard: Settings → Environments → Enable environments) and to reply when it is done, and wait. Then re-run step 1's `knock environment list` and key inventory, which now covers development and production, and ask the development-or-branch question. Steps 3 and 4 then run against the new target, so nothing has to be redone.

Do not ask about things the files settle outright (format detection, chrome families); those are findings, not decisions, and belong in the analysis. In an additional pass over the same workspace, reuse the recorded intake answers unless the user's prompt changes one, and write "inherited from pass N" in the new pass's intake section.

### Step 3: workspace and inventory

Everything from here runs from the Knock project directory chosen at intake — by default, the directory the agent was launched in.

If that directory already has a `knock.json`, keep it and use its `knockDir`. If not, **do not run `knock init`** — it is interactive-only (no flags to answer its prompt) and defaults to a hidden `.knock` directory. Write the config directly, exactly as init would, and create the directory it names:

```json
{ "$schema": "https://schemas.knock.app/cli/knock.json", "knockDir": "./knock" }
```

Create the workspace (structure under "The workspace" below), copy the source directory into it, and write `MIGRATION.md` with the intake answers and the environment model.

**Target flags.** Record the target in `MIGRATION.md` as one flags string — `Target flags: --environment=<env-slug>`, plus ` --branch=<branch-slug>` on a branch — and append it to every environment-scoped `knock` command. The examples in this skill write it as `<target-flags>`; API calls pass the same values as the `environment` and `branch` query parameters. Channel commands are account-scoped and take neither. Never rely on the account default: a resumed session, or a rule file read on its own, would otherwise write to the wrong place. On a branch, create it now (`knock branch create <branch-slug>`) and record it under **Writes to Knock** in `MIGRATION.md`.

**Inventory pull.** Pull the existing resources into a scratch inventory inside the workspace, never into the project's knock directory:

```bash
knock pull --knock-dir=knock-migration/inventory/<env-slug> <target-flags> --force
knock pull --knock-dir=knock-migration/inventory/production --environment=production --force   # environments enabled only
```

Nothing is authored in `inventory/`, so a forced pull there is always safe, and re-running it is how a later session refreshes the inventory. The project's knock directory holds only what the migration writes, plus any resource files an app repo already had. Never run `knock pull --force` into it: that deletes local resource files that don't exist in Knock and overwrites local edits that haven't been pushed. `knock pull` prints "Successfully created the … directory" for every resource type, including ones with zero resources where no directory is created, so trust `ls` and the `knock <resource> list` commands, not the pull log.

Record the existing workflow, layout, and partial keys in `MIGRATION.md`. Any key collision found later must be surfaced to the user, never silently overwritten.

**Inventory content, not just keys.** Read the pulled `default` layout (and any resource whose key the plan will reuse). Concretely: grep its `html_layout` for `{% render` (partials it depends on — check they exist with `knock partial list`), for hex colors and font `<link>`s that are not Knock's stock ones, and for a company or product name. Anything non-stock means the layout was customized: flag it `❓blocking` — reuse, replace, or leave untouched is the user's call — never treat it as stock because the key is expected. Then check whether it is **in use**: a layout or partial is in use when any workflow references it (its `layout_key`, a `{% render '<key>' %}`, or a partial block) in the target environment or, with environments enabled, in production, where promotion carries every change. Grep the inventory workflow directories for all three. Record the verdict (stock and unused, customized, or in use and where): it decides whether the most-used migrated layout takes the `default` key (default-layout policy in `rules/extracting-layouts.md`).

### Step 4: test recipient and smoke preview

Create the test recipient in the target environment: `migration-test-user`, with the MCP `upsert_user` tool (set `name` and `email`). Every later render needs it. Without Manage data, ask the user to create a user with that id in the dashboard. Record it under **Writes to Knock**; on a production-only account it is a real production user, deleted after the migration (report open items).

Then run one **throwaway preview** through `execute_mapi_write`, against the target environment and never another: `POST /v1/templates/preview` with a minimal inline email template (a `subject` and a one-line `html_body`), `channel_type: "email"`, and the test recipient, and assert that `res.result.template.html_body` is a non-empty string (request shape in `references/verification-recipes.md`). It needs no existing workflow, so it always runs here, and one call proves that the session has write access (the write tool exists only for read-write sessions), and that it carries the `workflows:run` permission the template, layout, and step previews require. It does not prove the recipient exists — an unknown id renders too — so confirm the test user with the MCP `get_user` tool. A failure here is a setup problem to fix now, not in phase 4. The step preview's own response field (`template.html_content`) is checked by the guard the first time phase 4 renders a workflow.

**Service token.** Rendered previews and their checks run through the MCP without a token, so do not raise one when the MCP check passes. A token is needed in two cases only, and in both it is arranged before phase 1: the MCP cannot be attached, or the user chose at intake to review every email (one at a time or at the end). Never ask for the token in the conversation — a token typed into the chat lands in the transcript. First record every intake answer in `MIGRATION.md`, since the handoff restarts the session; then walk the user through the handoff in `references/verification-recipes.md` ("Providing a service token safely"). On the resumed session, `MIGRATION.md` holds the intake answers: confirm the token with `GET /v1/whoami` and the throwaway preview over curl, then start phase 1.

**Report preflight in the user's terms.** Write for someone who doesn't know Knock's internals and doesn't need the skill's: only what they must do, what limits a later choice, and what was written to their Knock account, in at most five short lines plus any steps they have to take. No file or folder names (`knock.json`, `knock/`, `MIGRATION.md`), no tool, CLI, or API names, no account or environment slugs, and nothing that went as expected (an empty account, nothing to reuse). For example:

```
Setup's done. Two things before I start on your templates:
- I'll build everything in your development environment; nothing touches your live emails.
- Test emails can only go to people on your Knock account, so I'll send them to you.

To review every email side by side, I need a key from your Knock account:
1. In the dashboard, go to Settings → Service tokens → New token. (Revoke it when we're done.)
2. In your terminal, run: export KNOCK_SERVICE_TOKEN=<the token>  — don't paste it here.
3. Restart me from the same folder and say "continue the email migration".
```

Anything else — the test user, the files created, which copy of the skill to resume with — goes in `MIGRATION.md`, not the message.

## Additive migrations (adding to an existing Knock setup)

When the account already has migrated or hand-built resources (intake answers, or preflight finds substantive layouts/partials), the process runs unchanged — additive mode changes the *inputs to the plan*, not the phases:

- The phase 0 inventory becomes **reuse discovery**, not just collision safety: pulled layouts and partials enter the dedup pools as first-class candidates.
- The corpus scan fingerprints new templates against **existing Knock layouts** as well as each other (compare chrome against each layout's `html_layout`), and partial candidates against **existing partial content**. A new template whose chrome fits a live layout should land on that layout.
- The plan checkpoint decides **reuse / extend / create** for every layout and partial candidate. *Extend* changes already-live emails: before proposing it, find the affected workflows (grep the inventory workflow directories — the target environment's, and production's when environments are enabled — for the `layout_key`, `{% render '<key>' %}`, and partial blocks using that key) and list them in the checkpoint item — extending a shared resource without that list is an overwrite in disguise (guardrail 7). Level: changing a layout or partial that any workflow uses — in the target environment or, with environments enabled, in production — is always `❓blocking`, on both environment models. The question names the affected workflows and where they live, says when the change reaches them (the moment it's committed on a production-only account; on promotion with environments enabled), offers a new key as the alternative, and **offers** to show before-and-after renders. Produce the renders only if the user asks, through inline previews that write nothing: `POST /v1/partials/preview` with an affected call site's inputs, or `POST /v1/templates/preview` with the layout passed inline and a live template's body.
- When environments were enabled after content was built in production, the reusable layouts and partials live in production, not development. Reusing one means bringing it into development under the **same key** first (pull it with `--environment=production`, push it to development, commit), so a later promotion updates the live resource instead of colliding with it; list each such resource in the plan.
- Follow the account's existing naming conventions for new keys, not this skill's defaults.
- Building a parallel set of near-duplicate layouts and partials next to the live ones is a failure outcome. When reuse is close but imperfect, surface the tradeoff at the checkpoint instead of quietly creating `footer-2`.

## The workspace

Create `knock-migration/` in the Knock project directory in step 3 of phase 0 (suggest adding it to `.gitignore` if the user doesn't want it committed — recommend keeping it until the migration is approved and promoted or published). Copy the **whole** source directory into `knock-migration/source/` at intake (template exports are small; skip dotfiles and empty directories, which have no key-derivation rule, and dependency or build output such as `node_modules/`, `dist/`, or `build/`; when the source directory contains the project directory, skip that too, so the copy never includes itself) and record which files are in scope as a list in `MIGRATION.md`; point every analysis file at the copy. A partial copy leaves the corpus scan's evidence (out-of-scope siblings, mislabeled duplicates) unreachable, agents may be unable to read outside the project directory, and a full copy lets the migration resume and re-verify even if the originals move:

```
knock-migration/
├── MIGRATION.md
├── inventory/                  # scratch pulls of existing resources, one directory per environment (phase 0 step 3); never authored in
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

Phase: 3 (build) · Next: workflow `order-shipped`
Checkpoint approved: 2026-08-12

## Intake
- Source: ./emails/ (48 templates; skip: drafts/)
- Target: new workflow per template | Mode: block-first
- Env model: environments enabled | Env: development (branch: email-migration)
- Target flags: --environment=development --branch=email-migration
- Existing resources: 3 workflows (…), 1 layout (default — stock, unused), 0 partials
- Review: one email per layout | Test sends: test@example.com

## Writes to Knock
- 2026-08-11: branch `email-migration`
- 2026-08-11: test recipient `migration-test-user` (development)

## Setup checks
- Smoke preview: passed 2026-08-11
- Layout CSS calibrated against a real render: pending

## Resources
| Resource | Type | Pushed | Committed |
| -------- | ---- | ------ | --------- |
| card-header | partial | ✅ | ✅ 3f9a2c1 |
| transactional | email_layout | ✅ | — |

## Status
| Template | Analyzed | Planned | Built | Pushed | Committed | Verified |
| -------- | -------- | ------- | ----- | ------ | --------- | -------- |
| password-reset | ✅ | ✅ | ✅ | ✅ | ✅ 8c41d07 | ✅ |
| account-signup | ✅ | ✅ | — | — | — | — |

## Decisions
- 2026-08-11: "User comments" consolidated into one workflow with a batch step (user approved).

## Open questions
- ❓ `Deleted Item.html` has no discoverable subject line; drafted "Your item was removed" — needs approval.
```

The header line says where the migration stands and what comes next; `Checkpoint approved` is written only when the user approves the plan, and no session enters phase 3 without it. **Writes to Knock** lists every write outside the migration's resources — the test recipient, a branch, variables — and drives the cleanup items in the final report whatever the environment model ends up being. **Resources** tracks the partials and layouts; **Status** tracks each template through its workflow. The columns mean: Analyzed — analysis file written; Planned — in the approved plan; Built — local files written; Pushed — push and readback both succeeded; Committed — the commit confirmed with `knock commit list` and its id recorded (`draft` for workflows on a production-only account, which the migration never commits); Verified — passed verification at the depth chosen at intake.

On a production-only account, the intake lines read `Env model: production-only | Env: production (workflows stay drafts)` and `Target flags: --environment=production`.

Update the status table and decision log as you go. Every unresolved item becomes a ❓ entry tagged `blocking`, `default`, or `fyi` (levels defined in the Open questions section of `references/analysis-file-template.md`). The plan checkpoint cannot pass while **blocking** items are unanswered; `default` items are presented as one "applied unless vetoed" list; `fyi` items go straight to the final report.

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



Present blocking questions **in the chat, not by pointing at plan files**: the plan is the record, the chat is the interface. Ask them **one at a time**, each waiting for its answer before the next, so every question is read before it is answered and later questions can build on earlier answers; never batch them, and where the agent has a structured question tool use it with one question per call. Each is written for a reader who has **not** opened the workspace and has not read this skill — no internal terms (question levels, chrome families, tiers, preflight mechanics); say what each option means for their email and their trigger payload — and follows one shape:

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

That is: a one-line question; **Source** (which template(s) and what the source does today, in a sentence); **Options**, lettered, each with its consequence for the trigger payload and for the email; **Recommendation** with the reason; and how to answer. Workspace ids (`B1`, `L2`) belong in the plan files, never in the prompt. After the last question, present three lists **one at a time**, each in its own message ending with its own reply instruction, and wait for that reply before showing the next; proceed on nothing less than an explicit reply to each. In order: **Defaults** — one line each (`template → what I'll do → why`), ending "reply go, or name the ones to change"; then **Suspected source mistakes** — consolidated from the analysis files, one line each (`what · where · default: reproduce what the source rendered · alternative: fix it`), ending "reply go, or name the ones to fix" (skip this message when there are none, and say so in one line); then **Offered, not applied** — the opt-in remaps and simplifications the mapping rule produced (`actor.*`, `vars.*` for a constant, a finished-URL field), one line each (`what → what changes if you take it`), ending "name any to apply, or reply none". Nothing in these lists is applied or skipped on silence. Then, when the approved plan uses `vars.*` keys that don't exist yet, ask the variables question ("Creating variables" in `rules/mapping-variables-and-logic.md`). Required approvals before phase 3:

- The overall plan (layouts, partials, workflow topology, keys)
- Every drafted subject line for templates that had none
- Any proposed consolidation of variant templates into one workflow
- Any remapping of variables off the default `data.*` contract
- Any overwrite of an existing resource, especially the `default` layout
- On a production-only account, the commit policy itself: the new partials and layouts are published live (unused until a workflow references them), and every workflow stays a draft
- Creating any new variables the plan uses, with their values
- Handling for unresolved assets, unsubscribe links, or unmappable variables

Record approvals in the decision log. If the user changes the plan, update the plan docs first, then proceed.

## Phase 3: build

Build order is mandatory on either environment model, because templates render only the *published* (committed) version of partials and layouts, while a workflow renders its latest pushed version, draft or not. Every command takes the target flags recorded in `MIGRATION.md`. First, when the user approved creating variables, create them ("Creating variables" in `rules/mapping-variables-and-logic.md`), since previews need their values. Then:

1. **Partials**: write `knock/partials/<key>/`, then per partial `knock partial validate <key> <target-flags>`, `knock partial push <key> <target-flags>`, read back with `knock partial get <key> <target-flags> --json`, and commit.
2. **Layouts**: write `knock/layouts/<key>/`, then per layout `knock layout validate <key> <target-flags>`, `knock layout push <key> <target-flags>`, read back with `knock layout get <key> <target-flags> --json`, and commit.
3. **Workflows**: write `knock/workflows/<key>/`, then per workflow `knock workflow validate <key> <target-flags>`, `knock workflow push <key> <target-flags>`, read back with `knock workflow get <key> <target-flags> --json`, and — only when environments are enabled — commit (commit strategy below).

Push **by key**, never `--all`: an app repo's knock directory can hold resources the migration doesn't own, and `--all` would push those too, reverting any dashboard edit made since they were last pulled (guardrail 7).

Calibrate each layout's block CSS before committing it: render a representative template's visual blocks through `POST /v1/templates/preview` with the layout passed inline, revise the CSS until the blocks match the source, then push and commit the layout once (recipe in `references/knock-blocks.md`). The inline preview ignores a template's `settings.pre_content`, so any layout variant driven by `pre_content` is checked with the step preview once the first workflow using it is pushed. Nothing is pushed or committed while iterating, so on a production-only account nothing is published until the CSS is right. Record the calibration under **Setup checks**.

Update `MIGRATION.md` after each resource. If validation fails, fix and re-validate; never push a resource that fails validation, and treat push, not validate, as the gate (`rules/building-templates.md` lists what only push checks). Commit only after push and readback both succeed, then confirm the commit with `knock commit list --resource-type=<type> --resource-id=<key> <target-flags> --json`: the newest entry must be this migration's commit. Record its id in the Resources table or the template's Committed cell. A scoped `knock commit` reports success even when nothing was committed (a mistyped key, the wrong resource type, a missing branch flag), and `knock <resource> get` returns uncommitted changes by default, so neither one proves the commit.

### Commit strategy

What the migration commits depends on the environment model recorded at preflight:

| Resource | Environments enabled (development or a branch) | Production-only |
| -------- | ---------------------------------------------- | --------------- |
| New partial or layout | Push, then a scoped commit | Push, then a scoped commit. This publishes it live, which changes no email: nothing live references a new key |
| Existing partial or layout (extended or replaced, including `default`) | Push and commit once the checkpoint approves the change. If production emails use it, the checkpoint item names them, because promotion will change them | Push and commit once the checkpoint approves the change. If live emails use it, the checkpoint item names them, because the commit changes them immediately |
| Workflow | Push, then a scoped commit | Push only. It stays a **draft**, which previews and test sends still exercise; its Committed cell reads `draft` |

How the checkpoint asks about changing an existing resource is set by the additive-migration rules above and the default-layout policy in `rules/extracting-layouts.md`. An approval covers later re-commits of the same resource during this migration, such as a CSS calibration or a verification fix.

Scope every commit to one resource, on a branch too, so unrelated pending changes are never swept up — other work in a shared development environment, or someone's unpublished drafts in production:

```bash
knock commit -m "Migration: add <key> partial" --resource-type=partial --resource-id=<key> <target-flags> --force
knock commit -m "Migration: add <key> layout" --resource-type=email_layout --resource-id=<key> <target-flags> --force
knock commit -m "Migration: add <key> workflow" --resource-type=workflow --resource-id=<key> <target-flags> --force   # environments enabled only
```

Never run `knock commit promote`, and never commit a workflow on a production-only account: promoting and publishing are the user's decisions, documented in the final report.

## Phase 4: verify and report

Verify each workflow at the depth chosen at intake, per `rules/verifying-the-migration.md`, then write the final report (created resources, template → workflow map, per-workflow trigger payload contract, remaining TODOs, and promotion instructions when environments are enabled or publishing instructions on a production-only account).

## Additional passes in the same workspace

A second or later pass (more templates from the same corpus, or a follow-up batch months later) shares the workspace and **appends**; it never starts a parallel workspace or rewrites earlier records:

- `MIGRATION.md`: add dated `## Intake (pass N)`, `## Resources (pass N)`, `## Status (pass N)`, `## Decisions (pass N)`, `## Verification log (pass N)`, and `## Open questions (pass N)` sections, and append new entries to **Writes to Knock**. Earlier sections stay as the approved record.
- Re-run step 1 of phase 0 before the new intake: the environment model can change between passes (an account may have enabled environments since), and the target flags must follow it.
- `plan/*.md`: append a `## Pass N` section to each of the four files with the same headings as the original; earlier plan sections are the approved decisions the new pass inherits.
- `analysis/_chrome-families.md`: add a dated addendum for new families, new members of existing families, and corrections to earlier `(probable)` claims. Earlier per-template analysis files are untouched; new templates get new files.
- `previews/passN/` for renders and `previews/compare/passN.html` for the visual comparison; `REPORT.md` gains a `## Pass N` section.
- Existing resources in Knock are reuse candidates first (see "Additive migrations" above); a pass that rebuilds a live layout or partial must list the workflows it changes.
- Refresh the inventory by pulling into `knock-migration/inventory/<env-slug>/` again (phase 0 step 3), and diff it against the project's knock directory when dashboard-side edits are suspected. Never pull into the project's knock directory itself.

## Parallelizing analysis

Phase 1 can be fanned out to several agents (one per chrome family works well) once the corpus scan is done. Finish and **freeze** `analysis/_chrome-families.md` and `analysis/_conventions.md` first; every agent gets both, treats them as read-only, and writes only its own `analysis/<stem>.md` files. The orchestrator owns `MIGRATION.md` and the status board, applies any corrections the agents report (a family a template does not fit, a syntax the scan missed) after every agent has finished, and merges their ❓ items into `MIGRATION.md` before planning. Hand each agent this brief, with every path made absolute (the skill's directory for `rules/` and `references/`, the workspace for the rest) — a subagent can't resolve relative paths from its own starting directory:

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

- On any new session, read `MIGRATION.md` first; its header line gives the phase and the next step.
- Do not rerun phase 0. Re-check only what can change between sessions, read-only — `knock whoami` and the MCP tools — and use the recorded target flags for every command.
- Never enter phase 3 unless `Checkpoint approved` is recorded; without it, the plan is still waiting on the user.
- Never pull into the project's knock directory: it can hold built files that were never pushed. Refresh the inventory directory instead.
- After a restart to supply a service token, `MIGRATION.md` already holds the intake answers: run preflight's service-token confirmation and continue with phase 1 — do not re-ask intake.
- Re-running a phase for a template is safe: analysis files are overwritten in place; builds re-push the same keys (idempotent upsert).
- For large sets, process in batches of 5-10 templates per phase-1/phase-3 sitting, updating `MIGRATION.md` between batches. The plan checkpoint (phase 2) still happens once, over the full set — partial and layout extraction only work well with the whole corpus analyzed.
