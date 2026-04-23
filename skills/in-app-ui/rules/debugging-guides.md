---
title: Testing and debugging Knock guides
description: A triage checklist and toolbar workflow for diagnosing why a Knock guide isn't rendering, plus best practices for testing targeting and engagement.
tags:
  - in-app-ui
  - guides
  - debugging
  - testing
category: in-app-ui
last_updated: 2026-04-22
---

# Testing and debugging Knock guides

"The guide isn't showing up" has a handful of recurring root causes. Work the triage list top-down — the earlier steps rule out the broadest categories.

Reference: https://docs.knock.app/in-app-ui/guides/debugging-guides

## The guides toolbar

The guides toolbar is the single most useful debugging tool. It overlays your running app with live info on which guides were fetched, which are eligible, and why others were filtered out.

Requirements: `@knocklabs/react` v0.11.13 or newer.

Two ways to enable it:

1. **From the dashboard.** Open your guide channel, click **Preview**, and enter the URL of the page you want to test.
2. **By URL flag.** Append `?knock_guides_toolbar=true` to any URL in an app wrapped in `KnockGuideProvider`.

The toolbar has three viewing modes:

- **All guides** — every guide in the channel.
- **Active guides** — guides currently live in this environment.
- **Eligible guides** — guides that *this user* qualifies for on *this page*.

Each row shows status badges (`Inactive`, `Archived`, `Not targeted`, `Not queried`, etc.) and eligibility indicators (active, unarchived, targeted). The **Focus** button forces a guide to render for inspection. The settings panel lets you toggle sandbox engagement mode (so tests don't pollute production analytics), bypass throttling, and inspect the target parameters the client sent.

If the toolbar shows the guide as eligible but it still doesn't render, the problem is in your React code, not in Knock targeting.

## Triage checklist

Work through these in order. Most "guide not showing" bugs are resolved in the first three.

### 1. Is the guide live in this environment?

- Is the guide's status **Active** (not Draft or Archived) in the dashboard?
- Are you looking at the right environment (development vs. production)? Guides and channel IDs are environment-scoped.
- Does the `channelId` your app is passing to `KnockGuideProvider` match the channel the guide belongs to?

### 2. Is the user eligible?

- Does the user match **targeting rules**? Check audience membership, user properties, tenant properties.
- Does the page match the guide's **activation rules**? Path patterns are exact unless you use wildcards.
- Has the user already archived this guide? Un-archive them in the dashboard to re-test.
- If targeting uses runtime data passed from the client, is the value being sent, and is its **type** correct? `"true"` (string) and `true` (boolean) are different values. This is the most common targeting bug.

Call the Guides API directly with that user's id if you want ground truth: if the API returns the guide, the server says it's eligible, and the bug is client-side.

### 3. Is the provider configured correctly?

- Is `readyToTarget` true by the time you expect the fetch? If it's gated on async data that never resolves, the guide will never be evaluated.
- Does `user.id` on `KnockProvider` match the id you identified the user with from your backend? A mismatch means Knock is evaluating against a user who has none of the properties you expect.
- Is `listenForUpdates` on? Without it, dashboard changes won't propagate until the next page load.

### 4. Is the component code correct?

- Does the `type` string passed to `useGuide` / `useGuides` exactly match the message type key?
- Are you guarding `if (!step) return null`? A thrown error inside the component looks identical to "not showing" in some boundaries.
- Are you reading `step.content.<field>` with the correct field names from the message type schema?
- Is the component actually mounted on this route?

### 5. Is engagement tracking wired up?

Custom guide components *must* call `markAsSeen`, `markAsInteracted`, and `archive` themselves. Pre-built components do this for you; headless ones do not. If the dashboard shows zero engagement on a guide that is obviously rendering, this is almost always the reason.

## Testing new guides

Before shipping a new guide:

- [ ] **Page targeting.** Visit a page that should match and one that shouldn't. Confirm with the toolbar.
- [ ] **User targeting.** Sign in as a user who qualifies and one who doesn't. Confirm both outcomes.
- [ ] **Runtime data.** If targeting uses client-provided data, test each branch of the rule.
- [ ] **Engagement.** Trigger `seen`, `interacted`, and `archived` and confirm each shows up in the dashboard for that guide.
- [ ] **All interactive elements.** Click every CTA; confirm navigation and that the archive-on-dismiss behavior is correct.
- [ ] **Repeat cycle.** Unarchive the guide from the dashboard and re-run to confirm the guide reappears after reset.
- [ ] **Real-time update.** With the app open, edit the guide content in the dashboard. Confirm the app reflects the change without a reload (`listenForUpdates` must be on).

## Common gotchas

- **Type coercion on targeting data.** Passing numeric IDs as strings (or vice versa) silently breaks comparisons. Lock the type at the data source.
- **Targeting a user who isn't identified yet.** If your providers mount before auth resolves, the fetch runs for an anonymous / placeholder user.
- **Wrong environment's channel ID.** Dev channel in prod or vice versa — the channel ID is not a secret, but it is environment-scoped.
- **Archive stickiness during testing.** Once a user archives a guide, it's gone for that user until you unarchive them. Have a designated test user whose archive state you reset between runs.
- **Throttling.** Guides can be throttled so a user doesn't see the same thing repeatedly. Bypass throttling in the toolbar settings during testing.
- **Websocket blocked.** Corporate networks and some ad blockers drop the websocket. `listenForUpdates` silently no-ops; the initial fetch still works, but dashboard edits won't show up live.
