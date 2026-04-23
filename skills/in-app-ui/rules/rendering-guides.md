---
title: Rendering guides with useGuide and useGuides
description: How to build a Knock guide component with the React hooks, including typed content, single vs multiple guides, and engagement tracking.
tags:
  - in-app-ui
  - guides
  - react
  - hooks
category: in-app-ui
last_updated: 2026-04-22
---

# Rendering guides with useGuide and useGuides

Once providers are in place (see `setup-providers.md`), rendering a guide is just a React component that calls `useGuide` or `useGuides`, reads `content`, and reports engagement back to Knock.

References:
- https://docs.knock.app/in-app-ui/guides/render-guides
- https://docs.knock.app/in-app-ui/react/headless/guide

## Pick the right hook

| Hook | Returns | Use for |
| --- | --- | --- |
| `useGuide({ type })` | A single `step` — the next eligible guide of that message type | Banners, modals, tooltips, paywalls — any surface that shows at most one thing at a time |
| `useGuide({ key })` | A single `step` — a specific guide by its unique key | Rendering one specific guide by id |
| `useGuides({ type })` | An array of `guides` | Lists (e.g., changelog cards in a sidebar) |

Guides surfaced by `useGuide` are filtered by eligibility, throttled, and ordered server-side — if the hook returns nothing, that is usually the correct answer, not a bug. See `debugging-guides.md` for how to verify.

## Single guide: minimal example

```tsx
import { useEffect } from "react";
import { useGuide } from "@knocklabs/react";

type ChangelogCardAttrs = {
  title: string;
  body: string;
};

export const ChangelogCard = () => {
  const { step } = useGuide<ChangelogCardAttrs>({ type: "changelog-card" });

  useEffect(() => {
    if (step) step.markAsSeen();
  }, [step]);

  if (!step) return null;

  return (
    <div onClick={() => step.markAsInteracted()}>
      <h3>{step.content.title}</h3>
      <p>{step.content.body}</p>
      <button
        onClick={(e) => {
          e.stopPropagation();
          step.archive();
        }}
      >
        Dismiss
      </button>
    </div>
  );
};
```

Key points:

- Always guard on `if (!step) return null` before rendering — the user may not be eligible.
- The generic on `useGuide<T>` types `step.content`. Define the type to match the fields in the Knock **message type** so the compiler catches drift.
- `markAsSeen` in a `useEffect` keyed on `step` is the idiomatic place to record the impression. Guard with `if (step)` because `useEffect` still runs when the hook returns nothing.
- `markAsInteracted` goes on the primary action (the card click, the CTA, whatever counts as "they engaged").
- `archive` removes the guide for this user so it will not be returned again — use it for dismiss buttons.

## Multiple guides: list example

```tsx
import { useGuides } from "@knocklabs/react";

const ChangelogList = () => {
  const { guides } = useGuides({ type: "sidebar-changelog-card" });

  return (
    <div>
      {guides.map((guide) => (
        <div key={guide.key}>
          <h3>{guide.steps[0].content.title}</h3>
          <p>{guide.steps[0].content.body}</p>
        </div>
      ))}
    </div>
  );
};
```

When you render a list, you own the engagement tracking per item. A common pattern is an intersection observer that calls `guide.steps[0].markAsSeen()` the first time each card scrolls into view.

## Advanced: `useGuideContext`

```tsx
import { useGuideContext } from "@knocklabs/react";

const { client: guideClient } = useGuideContext();
```

Reach for this when you need to manually refetch, inspect state, or do something the hooks do not expose. Most components should not need it.

## Matching the component to the dashboard

A guide component is a contract between code and the dashboard:

1. **Message type** in the dashboard defines the content schema (`title`, `body`, `cta_text`, etc.).
2. The TypeScript type on `useGuide<T>` mirrors that schema.
3. The `type` string passed to the hook matches the message type's key.

If a field is renamed in the dashboard, the type and the render code both need to update. Keep the type definition near the component so reviewers see both at once.

## Shipping a new guide component: workflow

1. Decide the UX (banner / modal / card / tooltip) and where it renders.
2. In the Knock dashboard, create or reuse a **message type** whose schema matches what the UI needs (`title`, `body`, `cta_text`, `cta_url`, etc.). If the UI needs structured data the message type doesn't have, add fields first.
3. Build the React component. Call `useGuide` (or `useGuides`) with the message type key as `type`. Type the content generic to the message type schema.
4. Wire engagement: `markAsSeen` on mount, `markAsInteracted` on the primary action, `archive` on dismiss.
5. Create a guide in the dashboard using that message type. Set targeting and activation rules.
6. Test with the guides toolbar (see `debugging-guides.md`).

## Common pitfalls

- **Forgetting the `if (!step) return null` guard.** Causes a crash on any user who isn't eligible.
- **Calling `markAsSeen` unconditionally on render.** Use `useEffect` keyed on `step` so it fires once per fetched guide, not every render.
- **Mismatched `type` string.** The string passed to `useGuide` must match the message type key exactly, including case.
- **Treating `archive` like `markAsInteracted`.** `archive` removes the guide from future fetches for this user. Use it for dismissal, not for "the user clicked the card."
- **Rendering inside `Suspense` boundaries that unmount on refetch.** Causes `markAsSeen` to fire repeatedly. Mount guide components in a stable part of the tree.
