---
name: in-app-ui
description: Guidance for implementing Knock in-app UI in a web app, with a focus on setting up, rendering, and debugging Knock guides in React.
---

# Knock in-app UI skill

This skill helps you build in-app UI with Knock. It covers the two in-app products — **feeds** and **guides** — at a high level, then goes deep on guides: provider setup, rendering with hooks, and debugging.

Reference: https://docs.knock.app/in-app-ui/overview

## Overview

The skill is organized into four focused rule files:

1. **Feeds vs. guides** — which product to pick for a given surface and why
2. **Setting up providers** — `KnockProvider` and `KnockGuideProvider` props, where each value comes from, and how to sequence them
3. **Rendering guides** — building a guide component with `useGuide` / `useGuides`, typed content, and engagement tracking
4. **Debugging guides** — the guides toolbar, the triage checklist, and testing workflow

## How to use this skill

### When deciding what to build

Start with `rules/feeds-vs-guides.md`:

- Confirm the surface you're building is actually a guide, not a feed
- Check the decision table before picking a direction
- If the answer is "both," wrap the app in `KnockProvider` once and render each product's provider where it's needed

### When adding guides to a React app for the first time

1. Read `rules/setup-providers.md`
2. Wire `KnockProvider` + `KnockGuideProvider` at the top of the tree
3. Source `apiKey`, `user.id`, and `channelId` from the places listed in that rule
4. Gate `readyToTarget` on any async data your targeting depends on

### When building a new guide component

1. Follow the workflow in `rules/rendering-guides.md`
2. Pick `useGuide` for single-guide surfaces, `useGuides` for lists
3. Define a TypeScript type that mirrors the Knock message type schema
4. Wire `markAsSeen`, `markAsInteracted`, and `archive` — custom components must do this themselves

### When a guide isn't rendering

1. Open `rules/debugging-guides.md` and work the triage checklist top to bottom
2. Turn on the guides toolbar (`?knock_guides_toolbar=true`) first — it answers most questions in seconds
3. Distinguish server-side (targeting/eligibility) from client-side (provider/component) failures before digging deeper

## Rule files reference

- `rules/feeds-vs-guides.md` — product selection between feeds and guides
- `rules/setup-providers.md` — configuring `KnockProvider` and `KnockGuideProvider`
- `rules/rendering-guides.md` — `useGuide`, `useGuides`, typed content, engagement tracking
- `rules/debugging-guides.md` — toolbar, triage checklist, testing workflow

## Quick reference

### Providers (minimum viable setup)

```tsx
<KnockProvider
  apiKey={process.env.NEXT_PUBLIC_KNOCK_API_KEY}
  user={{ id: currentUser.id }}
>
  <KnockGuideProvider
    channelId={process.env.NEXT_PUBLIC_KNOCK_GUIDE_CHANNEL_ID}
    readyToTarget
    listenForUpdates
  >
    {children}
  </KnockGuideProvider>
</KnockProvider>
```

### Where to source each value

- `apiKey` — Knock dashboard → **Developers → API keys** → public key (`pk_...`)
- `user.id` — your auth context; must match the id used when identifying the user from your backend
- `channelId` — Knock dashboard → **Integrations → Channels** → guide channel → channel ID

### Hooks at a glance

- `useGuide({ type })` — one guide by message type
- `useGuide({ key })` — one specific guide by key
- `useGuides({ type })` — array of guides by message type
- `useGuideContext()` — low-level client access

### Engagement methods

- `step.markAsSeen()` — impression (call from `useEffect` keyed on `step`)
- `step.markAsInteracted()` — primary action
- `step.archive()` — dismissal; removes the guide for this user going forward

### First stop when something's wrong

Append `?knock_guides_toolbar=true` to any URL. The toolbar shows all guides, which are active, which this user is eligible for, and why the rest were filtered out.

## Best practices summary

1. **Pick the right product.** Feeds for chronological lists, guides for targeted UI.
2. **Mount providers once, high in the tree.** Inside your auth boundary, above any route that renders guides.
3. **Never pass a placeholder user.** Wait for auth to resolve before mounting `KnockProvider`.
4. **Gate `readyToTarget` on async data** your targeting rules depend on.
5. **Type your content.** `useGuide<T>` should mirror the Knock message type schema.
6. **Always handle engagement.** Custom components must call `markAsSeen`, `markAsInteracted`, and `archive` themselves.
7. **Lock targeting data types.** `"true"` and `true` are different to the rule engine.
8. **Use the toolbar first.** Most "the guide isn't showing" questions are answered in seconds.
