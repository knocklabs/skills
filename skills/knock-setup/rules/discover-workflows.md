---
title: Discover workflows
description: Learn the product and propose high-value notification workflows
tags:
  - setup
  - workflows
  - discovery
category: knock-setup
last_updated: 2026-07-23
---

# Discover workflows

## Prior confirmation (skip rediscovery)

If this conversation already has an approved build list from `knock-lifecycle-opportunities` or `knock-product-messaging-strategy` (user said e.g. "looks good", "build these", "skip N", or an upstream skill passed a `confirmed` / `skipped` / `deferred` payload):

1. Do **not** re-propose a new top-5.
2. Do **not** re-rank or substitute "higher volume" workflows unless the user asks.
3. Optionally restate context in 2–3 short lines (trigger / recipient notes only for the confirmed set).
4. Restate the confirmed set in one line (include explicit skips).
5. Ask only whether to proceed to build these in Knock development. The question must be the **very last thing** in your message: on its own line, and bolded.
6. On yes → go straight to `build-workflows.md`.

Example ending after prior confirmation:

Confirmed: Invite accepted, Trial ending, Payment failed, Usage limit. Skipped: Weekly digest.

**Proceed to build these in Knock development?**

Only run full discover below when there is **no** prior approved list in this conversation.

## Cold-start discover

1. Learn about the business: if you are in a codebase, examine it to understand the product, its users, and key events. Otherwise ask at most 3 short questions.
2. Propose the 5 highest-value notification workflows as a bulleted list. For each: a short name in bold, then 1-2 sentences explaining why it is valuable for THIS product — tie it to a real user moment or business outcome you found (e.g. re-engagement, retention, conversion, trust). Don't just name the trigger; sell the workflow.
3. Ask which to build. The confirmation question must be the **very last thing** in your message: on its own line, and bolded. Nothing after it.

Example ending:

**Which of these should I build?**
