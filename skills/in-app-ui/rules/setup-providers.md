---
title: Setting up KnockProvider and KnockGuideProvider
description: How to configure the React providers that power Knock guides, including required props, where to source each value, and common pitfalls.
tags:
  - in-app-ui
  - guides
  - react
  - setup
category: in-app-ui
last_updated: 2026-04-22
---

# Setting up KnockProvider and KnockGuideProvider

To render guides in a React app you need two nested providers from `@knocklabs/react`: `KnockProvider` at the outer layer (authenticates the user with Knock) and `KnockGuideProvider` inside it (fetches guides for the active guide channel).

References:
- https://docs.knock.app/in-app-ui/guides/render-guides
- https://docs.knock.app/in-app-ui/react/headless/guide

## Install

```bash
npm install @knocklabs/react
```

## The minimal working setup

```tsx
import { KnockProvider, KnockGuideProvider } from "@knocklabs/react";

const MyApplication = () => {
  const currentUser = useCurrentUser();

  return (
    <KnockProvider
      apiKey={process.env.NEXT_PUBLIC_KNOCK_API_KEY}
      user={{ id: currentUser.id }}
    >
      <KnockGuideProvider
        channelId={process.env.NEXT_PUBLIC_KNOCK_GUIDE_CHANNEL_ID}
        readyToTarget
        listenForUpdates
      >
        {/* Your app components */}
      </KnockGuideProvider>
    </KnockProvider>
  );
};
```

Place these as high in the tree as possible — typically inside your auth boundary and above any route that renders a guide. Do not mount them per-route; guide fetches and websocket connections should live for the session.

## `KnockProvider` props

| Prop | Required | Purpose |
| --- | --- | --- |
| `apiKey` | Yes | Your Knock **public** API key. |
| `user` | Yes | An object identifying the signed-in user. At minimum `{ id }`. |

### Where to get `apiKey`

- Knock dashboard → **Developers → API keys**.
- Use the **public** key (prefixed `pk_`), never a secret key, in client code.
- Store it as an env var. Conventionally `NEXT_PUBLIC_KNOCK_API_KEY` (Next.js) or `VITE_KNOCK_API_KEY` (Vite). The `NEXT_PUBLIC_` / `VITE_` prefix is required so the bundler exposes it to the browser.
- Use the **development** key locally and the **production** key in your production build. Gate this with your normal env-per-stage config.

### Where to get `user`

- The `user.id` must match the `id` you use when identifying the user from your backend via Knock's identify API. If those two values drift, the user Knock targets is not the user sitting in front of your app.
- Pull it from your existing auth context (Clerk, Auth0, your own session hook, etc.). Do not hard-code it.
- Do not render `KnockProvider` until the user is loaded. If you pass an empty or placeholder id, guides will be fetched for the wrong user and you will spend an afternoon debugging it.

Production apps should also sign the user with a **user token** for authenticated Knock requests. Add it via the `userToken` prop once you enable enhanced security mode in the Knock dashboard. Generate the token on your backend; never mint it in the browser.

## `KnockGuideProvider` props

| Prop | Required | Purpose |
| --- | --- | --- |
| `channelId` | Yes | The ID of the Knock guide channel this app should read from. |
| `readyToTarget` | Recommended | Tells the provider your app is ready to evaluate targeting. Pass `false` until all data needed for targeting (e.g., current route, feature flags, plan tier) is loaded; otherwise guides may be evaluated against stale or missing context. |
| `listenForUpdates` | Recommended | Opens a websocket so the client re-evaluates guides in real time when content or targeting changes in the dashboard. |

### Where to get `channelId`

- Knock dashboard → **Integrations → Channels** → the in-app **guide** channel → copy the channel ID.
- It is not a secret, but treating it as an env var (`NEXT_PUBLIC_KNOCK_GUIDE_CHANNEL_ID`) lets you point dev and prod at different channels without code changes.
- Each environment (development, production) has its own channel ID. Using the wrong one is a very common reason "the guide isn't showing up."

### When to delay `readyToTarget`

Set `readyToTarget={false}` while you are loading data that your guide targeting depends on, then flip it to `true` once the data is ready:

```tsx
const { plan, isLoading } = useUserPlan();

<KnockGuideProvider
  channelId={process.env.NEXT_PUBLIC_KNOCK_GUIDE_CHANNEL_ID}
  readyToTarget={!isLoading}
  listenForUpdates
>
  {children}
</KnockGuideProvider>
```

If you forget this, guides that target on `plan == "pro"` may silently not match on first render.

## Passing runtime targeting data

Guides can target against arbitrary per-request data you pass at render time (for example, the current route or a computed flag). When you need this, pass it via the guide client — see the render-guides doc for the current API — rather than reaching inside the provider. Keep the *shape* of this data stable across environments; `"true"` (string) and `true` (boolean) are different values to Knock's rule engine and are the most common cause of "my targeting rule works in dev but not in prod."

## Checklist before moving on to rendering

- [ ] `KnockProvider` wraps everything that could render a guide.
- [ ] `apiKey` is the public key for the current environment.
- [ ] `user.id` matches the id you use on the server when identifying users.
- [ ] `KnockGuideProvider` is inside `KnockProvider`.
- [ ] `channelId` is the correct channel for the current environment.
- [ ] `readyToTarget` is gated on any async data your targeting rules depend on.
- [ ] `listenForUpdates` is on (unless you have a specific reason not to).
