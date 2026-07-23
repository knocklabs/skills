---
title: Migration plan
description: Produce a phased Knock migration plan without mutating Knock resources
tags:
  - migrate
  - plan
  - phases
category: knock-migrate-to-knock
last_updated: 2026-07-23
---

# Migration plan

After inventory and mapping, deliver a phased plan. Do not execute Knock resource creation unless the user explicitly asks.

## Plan structure

### 1. Summary

- Source platform(s) detected
- Approximate number of message types
- Suggested first slice (usually auth + billing transactional)
- Link the primary tutorial (Braze / Courier / generic)

### 2. Phases

Use this default order (align with [Braze](https://docs.knock.app/tutorials/migrate-from-braze) and [Courier](https://docs.knock.app/tutorials/migrate-from-courier) tutorials):

| Phase | Work | Done when |
| --- | --- | --- |
| 0. Foundations | Knock account, environments, channel providers | Channels send a test in development |
| 1. Critical transactional | Password reset, verify email, invites, receipts | Parity with old sends; dual-run or feature flag |
| 2. Product / collaboration | Mentions, assignments, digests | Batching and prefs defined |
| 3. Lifecycle | Onboarding, trial, win-back | Exit criteria documented |
| 4. Preferences and users | Identify users, preference center, categories | Old opt-outs respected |
| 5. Tenants / subscriptions | If B2B or list-based sends | Scoped correctly |
| 6. In-app | Feed and/or guides | UI wired in app |
| 7. Cutover | Remove old provider calls | No dual sends |
| 8. Cleanup | Delete unused campaigns/providers | Docs updated |

### 3. Application code changes (local only)

List concrete files/modules to change for triggers and identify calls. Propose diffs only if the user asks. Do not push workflows.

### 4. Risks and open questions

- Dashboard-only templates with no export path
- Missing stable user ids
- Marketing vs transactional deliverability (separate email channels)
- Compliance (SMS consent, unsubscribe)

### 5. What not to do yet

Explicitly state that Knock MCP/CLI resource writes and the [email MCP migration tutorial](https://docs.knock.app/tutorials/migrate-email-with-mcp-server) wait until the user opts in.

## Closing question

End with a single bold confirmation question, for example:

**Which migration phase should we plan in more detail next?**
