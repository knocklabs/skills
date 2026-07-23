---
title: Messaging plan file
description: Write the full strategy plan to messaging-plan.md; keep chat minimal
tags:
  - strategy
  - output
  - plan
category: knock-product-messaging-strategy
last_updated: 2026-07-23
---

# Messaging plan file

All detailed strategy output goes in **`messaging-plan.md`** at the repo root (create or update; do not invent a different path unless the user names one). Chat is only for must-know status and confirmation questions.

## Chat contract (hard)

In chat, do **not** paste full workflow briefs, checklists, or long rationale.

Allowed chat content:

1. One short status line (what you wrote / updated and how many items)
2. Optional one-line risk or blocker (only if it blocks progress)
3. The bold confirmation question as the **last line**

Example chat after drafting:

Wrote `messaging-plan.md` with 6 recommendations (4 build-ready, 2 deferred).

**Which items should we build next?**

Example after user confirms:

Updated `messaging-plan.md` handoff: confirmed 1–4, 6; skipped 5.

**Hand off to knock-setup to build these in Knock development?**

## File structure

Write (or rewrite) `messaging-plan.md` using this skeleton:

```markdown
# Messaging plan

## Product context
- **Product.** …
- **Personas / roles.** …
- **Key objects / tenants.** …

## Preference taxonomy
- Categories and defaults (brief)

## Recommendations

### 1. [Name]
- **Status.** proposed | confirmed | skipped | deferred | blocked
- **Moment type.** …
- **Trigger / eligibility.** …
- **Recipient.** …
- **Intended action.** …
- **Channels.** primary → escalation (conditions)
- **Stop condition.** …
- **Frequency / batching.** …
- **Preference category.** … (or transactional exemption)
- **Success metric.** …
- **Fatigue risk.** low | medium | high — why
- **Knock shape.** workflow | guide | both — brief notes
- **Trigger data.** required payload / user properties
- **Notes.** …

### 2. [Name]
…

## Deferred / blocked
| Name | Reason |
| --- | --- |
| … | … |

## Audit (only when auditing)
| Existing item | Score (Keep/Fix/Merge/Kill) | Notes |
| --- | --- | --- |
| … | … | … |

## Setup handoff
- **confirmed.** …
- **skipped.** …
- **deferred / blocked.** …
```

Number recommendations so the user can answer with indexes (e.g. "build 1–4, skip 5").

## Update rules

1. After each major strategy step, update the file — do not accumulate a long chat draft then dump once.
2. When the user confirms or skips, update **Status** on each item and refresh **Setup handoff**.
3. When applying Knock shapes (`apply-in-knock.md`), enrich the matching recommendation sections in the file; keep chat to a one-line "updated Knock shapes in messaging-plan.md".
4. Downstream skills (`knock-setup`) should read `messaging-plan.md` for detail; chat handoff only needs the confirmed/skipped/deferred lists plus a pointer to the file.
