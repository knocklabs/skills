---
title: Opportunity brief format
description: Template for each lifecycle messaging opportunity
tags:
  - lifecycle
  - output
category: knock-lifecycle-opportunities
last_updated: 2026-07-23
---

# Opportunity brief format

For each ranked opportunity:

```markdown
### [N]. [Name]
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
```

End with:

**Which opportunities should we design in more detail next?**

After the user confirms which to build (including skips), if they want Knock setup next, hand off with:

```markdown
### Setup handoff
- **confirmed.** [names]
- **skipped.** [names]
- **deferred / blocked.** [names + reason]
```

Do not ask `knock-setup` to propose a new top-5 unless the user asks to re-rank.
