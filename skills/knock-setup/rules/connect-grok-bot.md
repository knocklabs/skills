---
title: Connect Knock in Grok Bot
description: Route Grok Bot sessions — connect Knock MCP, then ask what marketing surface to work on
tags:
  - setup
  - mcp
  - grok-bot
category: knock-setup
last_updated: 2026-08-24
---

# Connect Knock in Grok Bot

Use this rule for Grok Bot (desktop or iOS teammate). Skip the Knock account ask and the opening encouragement. Do not use `rules/connect-cursor.md`, `rules/connect-knock-cli.md`, or grok.com connector docs.

Treat this as Grok Bot when any of the following is true:

- The session is the Grok Bot desktop or iOS app
- The user talks about Grok Bot, a named teammate, or **Agent Computer**
- The shared cloud computer is at `/workspace`

If you still cannot tell, ask in one line: are they in Grok Bot or another tool?

## Connect path

Do not ask whether they have a Knock account. Do not pitch Knock. If Knock MCP tools are already available, skip to **Surface area**.

Otherwise output only this line, nothing else:

Connect to Knock via MCP https://mcp.knock.app/mcp

Then call a Knock MCP tool once — prefer `list_environments`, or `execute_mapi_read` with `GET /v1/whoami` — and wait for success. If it fails, say the same line once more and retry. Do not loop more than twice. Do not add UI instructions.

After success, continue to **Surface area**. Do not start `discover-workflows` yet.

## Surface area

Ask what to work on. Do not invent extra options. Output:

1. One short lead-in: you can help increase engagement, set up notifications, plan the broader messaging system, or take whatever they throw at you.
2. This ordered list (keep the wording):

   1. **Increase engagement.** Re-engagement, onboarding, and in-product messaging that gets people back into the product.
   2. **Set up notifications.** First workflows, channels, and transactional sends in Knock.
   3. **Plan the messaging system.** Strategy, preferences, and fatigue before we build anything.
   4. **Something else.** Tell me the job and I will pick it up.

3. End with this as the last line, bolded:

**What should we work on first?**

### Route from their answer

- **Increase engagement** → `rules/discover-workflows.md`. There is often no app repo: ask at most 3 short product-context questions if you need them. Use `knock-lifecycle-opportunities` or `knock-product-messaging-strategy` only if they want a plan file and there is product context to scan.
- **Set up notifications** → `rules/discover-workflows.md`, then `rules/build-workflows.md`.
- **Plan the messaging system** → `knock-product-messaging-strategy`.
- **Something else** → follow their ask and use Knock MCP as the execution layer.

**Skip app wiring by default.** Do not run `rules/recommend-implementation.md`, `rules/implement-data-source.md`, or create a `knock-implementation` branch. Offer that path only if they attach a product repo or enable local-computer access.

**Wrap up.** If workflows were built, follow the MCP path in `rules/wrap-up.md`. Skip wrap-up for strategy or planning-only turns.
