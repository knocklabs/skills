---
name: knock-product-messaging-strategy
description: Design a cross-channel product messaging system that drives activation, engagement, and retention while controlling fatigue. Use when planning lifecycle messaging, auditing notification strategy, prioritizing workflows, or turning product moments into Knock workflows, guides, preferences, and measurement.
---

# Product messaging strategy skill

Turn a product into a coordinated messaging system — not a pile of one-off notifications. This skill operationalizes [The product leader's guide to effective messaging](https://knock.app/manuals/product-leaders-guide-to-effective-notifications/the-product-leaders-guide-to-effective-notifications) into agent steps that produce Knock-ready plans and resources.

Complementary manuals:

- [In-app messaging best practices](https://knock.app/manuals/in-app-messaging/best-practices-for-in-app-messaging)
- [Transactional email](https://knock.app/manuals/transactional-email)
- [Notification infrastructure](https://knock.app/manuals/notification-infrastructure)

## Overview

Work through these rule files in order when designing or auditing a messaging system:

1. **Data foundation and triggers** — meaningful product moments and event payloads
2. **Recipients and ownership** — who should get the message and why
3. **Delivery strategy** — channels, escalation, timing, stop conditions
4. **Volume and batching** — frequency controls and digests
5. **Relevance and preferences** — personalization and preference taxonomy
6. **Measurement and review** — outcomes, fatigue signals, launch checklist
7. **Apply in Knock** — map the plan to workflows, guides, audiences, and preferences

## How to use this skill

### Designing a messaging system for a product

1. Learn the product (codebase, events, roles, lifecycle). Ask at most 3 clarifying questions if needed.
2. Follow `rules/data-foundation-and-triggers.md` to list meaningful moments and required event data.
3. For each high-value moment, complete recipient, delivery, volume, and preference decisions using the next rule files.
4. Prioritize by growth outcome: activation, retention, revenue recovery, then nice-to-have alerts.
5. Run every candidate through `rules/measurement-and-review.md` before building.
6. Use `rules/apply-in-knock.md` to create or propose Knock resources. Prefer Knock MCP / CLI when connected.

### Auditing an existing notification program

1. Inventory current workflows, guides, channels, and preference categories.
2. Score each against the review checklist in `rules/measurement-and-review.md`.
3. Flag missing stop conditions, broad recipient rules, channel spam, and preference gaps.
4. Return a prioritized 30/60/90 backlog tied to activation, engagement, churn, and fatigue risk.

### Handing off into setup or implementation

- For greenfield Knock setup after strategy is approved, continue with `knock-setup`.
- For copy and channel formatting, use `knock-notification-best-practices`.
- For in-app guides UI, use `knock-in-app-ui`.
- For local resource management, use `knock-cli`.

## Rule files reference

- `rules/data-foundation-and-triggers.md` — events, payloads, and moment types
- `rules/recipients-and-ownership.md` — recipient selection and escalation
- `rules/delivery-strategy.md` — channel progression and timing
- `rules/volume-and-batching.md` — frequency, cooldowns, digests
- `rules/relevance-and-preferences.md` — context, personalization, prefs
- `rules/measurement-and-review.md` — outcomes, fatigue, launch standard
- `rules/apply-in-knock.md` — map decisions onto Knock primitives

## Quick reference

### Four moment types

1. **User-requested outcomes** — export done, payment submitted (usually immediate)
2. **Collaborative activity** — mention, assignment, approval (immediate or batched)
3. **Product or account state changes** — integration down, usage limit, payment failed
4. **Time-based conditions** — trial ending, incomplete onboarding, overdue approval

### Non-negotiables before building

- Trigger represents a meaningful state change, not a vague inactivity heuristic alone
- Recipient is the person responsible for the next action
- Primary channel + escalation path defined
- Stop / cancel condition defined and re-checked after delays
- Preference category assigned (or explicitly marked transactional/service-critical)
- Success metric is a product outcome, not only an open rate

### Growth priority order

1. Activation / time-to-value
2. Core loop engagement (collaboration, habit)
3. Revenue protection (failed payment, trial, limits)
4. Re-engagement / win-back with precise state
5. Announcements and education (lowest interrupt)

## Output format

When proposing a messaging plan, use this structure for each recommended workflow or guide:

```markdown
### [Name]
- **Moment type.** …
- **Trigger / eligibility.** …
- **Recipient.** …
- **Intended action.** …
- **Channels.** primary → escalation (conditions)
- **Stop condition.** …
- **Frequency / batching.** …
- **Preference category.** …
- **Success metric.** …
- **Fatigue risk.** low | medium | high — why
- **Knock shape.** workflow | guide | both — brief notes
```

End strategy proposals by asking which items to build next. Put that confirmation question last, on its own line, and bolded.
