---
title: Opportunity brief format
description: Write lifecycle opportunity briefs to lifecycle-opportunities.md; keep chat minimal
tags:
  - lifecycle
  - output
  - plan
category: knock-lifecycle-opportunities
last_updated: 2026-07-23
---

# Opportunity brief format

All briefs go in **`lifecycle-opportunities.md`** at the repo root. Chat stays status + confirmation only — never paste the full briefs.

## File structure

```markdown
# Lifecycle opportunities

## Product context
- **Product.** …
- **Personas / roles.** …
- **Key objects / tenants.** …

## Signals found
| Stage | Signal | Evidence (path) | Recipient | Existing message? |
| --- | --- | --- | --- | --- |
| … | … | … | … | … |

## Opportunities

### 1. [Name]
- **Status.** proposed | confirmed | skipped | deferred | blocked
- **Lifecycle stage.** activation | engagement | expansion | revenue | win-back
- **Evidence in code.** paths / models / events
- **Trigger (precise).** …
- **Recipient.** …
- **Intended action.** …
- **Stop condition.** …
- **Suggested channels.** …
- **Knock shape (future).** workflow | guide | both
- **Why it matters.** 1–2 sentences on growth outcome
- **Dependencies.** data you do not yet emit, etc.

### 2. [Name]
…

## Deferred / filtered out
| Idea | Reason |
| --- | --- |
| … | … |

## Setup handoff
- **plan.** lifecycle-opportunities.md
- **confirmed.** …
- **skipped.** …
- **deferred / blocked.** …
```

Number opportunities so the user can answer with indexes.

## Chat after drafting

Wrote `lifecycle-opportunities.md` with N ranked opportunities.

**Which opportunities should we take next?**

## After user confirms

1. Update **Status** and **Setup handoff** in the file.
2. Chat: one line with confirmed/skipped + path.
3. If they want Knock build next, hand off to `knock-setup` with the payload (no re-rank).
4. If they want deeper messaging design next, hand off to `knock-product-messaging-strategy` with the confirmed list (that skill writes `messaging-plan.md`).

Do not ask `knock-setup` to propose a new top-5 unless the user asks to re-rank.
