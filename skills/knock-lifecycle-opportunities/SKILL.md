---
name: knock-lifecycle-opportunities
description: Scan a product codebase for activation, engagement, and retention moments and recommend lifecycle messaging opportunities. Use when finding onboarding, churn, trial, or habit-forming notification candidates without creating Knock resources.
---

# Lifecycle opportunities skill

Find where users activate, stall, pay, invite, or churn in **this** product’s code and data model. Recommend messaging opportunities tied to real events and UI states.

## Hard constraint

**Do not create, update, push, or delete Knock resources** via MCP or CLI. Output an opportunity backlog and event/trigger sketches only. Hand off to `knock-setup` or `knock-product-messaging-strategy` only if the user asks to build.

## Overview

1. **Map the product lifecycle in code** (`rules/map-product-lifecycle.md`)
2. **Select high-value opportunities** (`rules/select-opportunities.md`)
3. **Write opportunity briefs** (`rules/opportunity-brief-format.md`)

## How to use this skill

1. Infer personas, accounts/workspaces, and key funnels from the repo.
2. Locate signup, onboarding, invite, billing, usage, and inactivity signals.
3. Propose a prioritized list of lifecycle messages (not a laundry list of every cron).
4. Ask which opportunities to design in depth next.
5. When the user asks to build in Knock, hand off to `knock-setup` with a structured payload — do **not** invite re-ranking:

```markdown
### Setup handoff
- **confirmed.** [names]
- **skipped.** [names]
- **deferred / blocked.** [names + reason]
```

`knock-setup` must treat `confirmed` as authoritative and skip rediscovery.

## Rule files reference

- `rules/map-product-lifecycle.md` — where to look in code
- `rules/select-opportunities.md` — prioritization
- `rules/opportunity-brief-format.md` — output template

## Docs

- https://docs.knock.app/concepts/workflows
- https://docs.knock.app/concepts/guides
- https://docs.knock.app/concepts/audiences
- https://docs.knock.app/send-notifications/triggering-workflows/audiences
- https://knock.app/manuals/product-leaders-guide-to-effective-notifications/the-product-leaders-guide-to-effective-notifications
