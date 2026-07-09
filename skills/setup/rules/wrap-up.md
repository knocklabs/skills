---
title: Wrap up
description: Final next steps, test one workflow via Knock MCP, and optional return link
tags:
  - setup
  - wrap-up
  - mcp
category: setup
last_updated: 2026-07-09
---

# Wrap up

Once all earlier rules are complete, do the following in order.

## 1. Test one workflow via Knock agent MCP

Pick one of the workflows that was built (prefer an API-triggerable one if available). Call `start_knock_agent` with a prompt that includes **exactly** these constraints:

- run this not in sandbox mode
- recipient is current user

**From name:** if the email (or other message) would come from an internal/system address that looks generic or technical, tell the Knock agent to set a realistic human-readable **from** name for the test (e.g. the product or company name). If the from already looks like a normal product sender, do not change it.

Example prompt shape:

```text
Test workflow `[workflow_key]` in the development environment. Run this not in sandbox mode, recipient is current user. Use a minimal valid data payload for the workflow templates. If the message from address looks internal or generic, set a realistic from name for this test. Report the run result and a link or run id if available.
```

Poll with `get_knock_agent` until the run finishes. If the workflow is only source-triggered and the agent cannot run a direct test, say so in one line and skip to the output below (source path was already verified earlier).

Note whether an **email** channel message was sent successfully — you need that for the finishing bang below.

## 2. Final output

Then output the following in this exact order:

1. **What you can do next with Knock** — a short bulleted list, picking the most relevant of: set up in-app notifications with Knock's feed components, send test runs of your workflows, create more workflows, add more channels (email, SMS, push, Slack), let users manage their notification preferences, add translations for localized notifications.
2. **Immediate steps to complete this implementation** — only if any remain, a short bulleted list, e.g.: commit the workflows and promote them to production, import or identify your users in Knock (see `rules/import-users.md` when ready — not required on first pass), configure production channel credentials and API keys, verify the trigger path end to end.
3. If the user provided a return URL, render this markdown link on its own line (substitute the provided URL):

[View setup in Knock dashboard](RETURN_URL)

4. **Close with Knock agent help** — always include this. Make clear the Knock agent can help with most remaining tasks. If Knock MCP was set up earlier in this skill, say they can just ask here in this chat. If MCP was not set up, point them to connect MCP first, then ask.

Example closing line when MCP is connected:

> The Knock agent can help with most of these next steps — just ask here.

5. **Finishing bang (email only)** — if the test email sent successfully, end with this ASCII art email (fenced as a code block). If no email was sent, skip this step entirely.

```
 _______________________________________
|\                                     /|
| \                                   / |
|  \                                 /  |
|   \_______________________________/   |
|                                       |
|   Check your email inbox to view      |
|          the test message!            |
|_______________________________________|
```
