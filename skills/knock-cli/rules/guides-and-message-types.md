---
title: Guides and message types
description: Working with Knock Guides for lifecycle messaging and message types as their schema
tags:
  - knock
  - cli
  - guides
  - message-types
  - in-app
  - lifecycle
  - banners
  - modals
category: knock-cli
last_updated: 2026-02-16
---

# Guides and message types

## Guides vs workflows

**Guides are NOT part of the workflow system.** This is a critical distinction:

| Concept | Purpose | Model |
|--------|---------|-------|
| **Workflows** | Notification delivery | Triggered by events (API, user actions); sends email, SMS, push, in-app feed messages |
| **Guides** | Lifecycle messaging | Rendered in-app based on targeting and activation rules; no workflow trigger |

Use workflows for **notifications** (order confirmations, password resets, comment alerts). Use guides for **lifecycle messaging** such as:

- Upgrade prompts and paywalls
- Outage or maintenance banners
- Feature announcements
- Welcome modals and onboarding
- In-place promotional UI

In-app feed messages in workflows are for notification-style content (e.g., "Someone commented on your post"). Guides power UI components that appear based on user state, audience membership, and page location.

## Message types overview

A **message type** is the schema for guide content. It defines:

- Which fields editors can author (title, body, buttons, etc.)
- One or more **variants** (e.g., default, single-action, multi-action)
- A **template preview** for the Knock dashboard editor

Every guide step references a message type and one of its variants. The guide's `values` object must match the fields defined in that variant.

### Built-in message types

Knock provides three pre-built message types:

| Key | Description |
|-----|-------------|
| `banner` | Top-of-page banner with title, body, optional buttons |
| `modal` | Centered modal with overlay, title, body, optional image and buttons |
| `card` | Inline card with headline, title, body, optional image and buttons |

Built-in message types are **immutable**. To customize their schema, clone the message type in the dashboard and then modify the clone. Do not attempt to edit built-in types via the CLI.

### Custom message types

Create custom message types when you need:

- Different field structure than banner/modal/card
- Headless components that map to your own UI
- Schemas tailored to specific use cases (e.g., changelog card, paywall)

Use `knock message-type new` to scaffold a new message type locally, or create it in the dashboard and pull it.

## Message type file structure

Message types live under `knock/message-types/{key}/`:

```
message-types/{message-type-key}/
├── message_type.json    # Schema and metadata
└── preview.html         # Optional; Liquid template for dashboard preview
```

### message_type.json

```json
{
  "name": "Banner",
  "description": "A banner at the top of our product.",
  "icon_name": "Flag",
  "variants": [
    {
      "key": "default",
      "name": "Default",
      "fields": [
        {
          "type": "text",
          "key": "title",
          "label": "Title",
          "settings": { "required": true, "default": "Banner title" }
        },
        {
          "type": "markdown",
          "key": "body",
          "label": "Body",
          "settings": { "required": true }
        },
        {
          "type": "boolean",
          "key": "dismissible",
          "label": "Dismissible?",
          "settings": { "default": true }
        }
      ]
    }
  ],
  "preview@": "preview.html",
  "$schema": "https://schemas.knock.app/cli/message-type.json"
}
```

**Key fields:**

| Field | Description |
|-------|-------------|
| `name` | Display name in the dashboard |
| `description` | Optional description |
| `icon_name` | Icon for the template editor |
| `variants` | Array of variants; each must have `key`, `name`, `fields` |
| `preview@` | File path to preview HTML (relative to message type directory) |

Every schema must define a variant with `key: "default"`.

### Field types

| Type | Description |
|------|-------------|
| `text` | Single-line text |
| `textarea` | Multi-line plain text |
| `markdown` | Markdown editor (rendered as HTML) |
| `boolean` | Checkbox (true/false) |
| `select` | Single-select from options |
| `multi_select` | Multi-select from options |
| `url` | URL field |
| `button` | Button with `text` and `action` subfields |
| `image` | Image with `url`, `alt`, `action` subfields |

### Preview HTML

The preview is a Liquid template that renders in the dashboard editor. Use field keys as variables:

```liquid
<div class="banner__title">{{ title }}</div>
<div class="banner__body">{{ body }}</div>
```

Use variant conditionals for variant-specific UI:

```liquid
{% if variant == "single-action" or variant == "multi-action" %}
  <button>{{ primary_button.text }}</button>
{% endif %}
{% if variant == "multi-action" %}
  <button>{{ secondary_button.text }}</button>
{% endif %}
```

## Guide file structure

Guides live under `knock/guides/{key}/`:

```
guides/{guide-key}/
└── guide.json
```

### guide.json

```json
{
  "name": "Welcome Modal",
  "steps": [
    {
      "ref": "step_1",
      "schema_key": "modal",
      "schema_variant_key": "single-action",
      "values": {
        "title": "Welcome!",
        "body": "Thanks for signing up. Get started with our quick tour.",
        "dismissible": true,
        "primary_button": {
          "text": "Start tour",
          "action": "/onboarding"
        }
      }
    }
  ]
}
```

**Step fields:**

| Field | Description |
|-------|-------------|
| `ref` | Unique step reference |
| `schema_key` | Message type key (e.g., `banner`, `modal`, `card`) |
| `schema_variant_key` | Variant key from the message type (e.g., `default`, `single-action`) |
| `values` | Object matching the variant's field keys |

The `values` object must include every field defined in the selected variant. Use empty strings or defaults for optional fields if needed.

## Personalization

Guide values support Liquid. Available namespaces:

| Namespace | Description |
|-----------|-------------|
| `data` | Custom data passed from the app to the guides API |
| `vars` | Environment variables |
| `recipient` | Current user (full user object) |
| `tenant` | Tenant object if provided |

Example:

```json
{
  "title": "Hi {{ recipient.name | default: 'there' }}!",
  "body": "You're on the {{ data.plan | default: 'free' }} plan."
}
```

## CLI commands

### Guide commands

| Command | Description |
|---------|-------------|
| `knock guide list` | List all guides |
| `knock guide get <key>` | Display a single guide |
| `knock guide new` | Create a new guide (use `-k`, `-n`, `-m` for key, name, message type) |
| `knock guide pull [key]` | Pull guide(s); use `--all` for all |
| `knock guide push [key]` | Push guide(s); use `--all` for all |
| `knock guide validate [key]` | Validate guide(s) locally |
| `knock guide activate <key>` | Activate or deactivate a guide |
| `knock guide open <key>` | Open guide in dashboard |
| `knock guide generate-types` | Generate TypeScript/Python/Go/Ruby types for guides |

### Message type commands

| Command | Description |
|---------|-------------|
| `knock message-type list` | List all message types |
| `knock message-type get <key>` | Display a single message type |
| `knock message-type new` | Create a new message type (use `-k`, `-n`) |
| `knock message-type pull [key]` | Pull message type(s); use `--all` for all |
| `knock message-type push [key]` | Push message type(s); use `--all` for all |
| `knock message-type validate [key]` | Validate message type(s) locally |
| `knock message-type open <key>` | Open message type in dashboard |

**Note:** Message type push and validate operate only in the development environment.

## Key gotchas

### Guides are not workflows

Do not treat guides like workflows. They have no steps that send notifications, no triggers, and no channel steps. They are rendered by your application via the guides API.

### Message types must exist first

Before creating a guide, ensure the message type it references exists. Run `knock message-type list` to discover available message type keys. Use `-m <message-type-key>` when running `knock guide new`.

### Built-in types are immutable

The `banner`, `modal`, and `card` message types cannot be edited. To customize, clone in the dashboard and use the clone's key.

### Guide values must match the schema

Each guide step's `values` object must match the fields of the selected `schema_key` + `schema_variant_key`. Missing or extra keys can cause validation errors.

### Always push after modifying

Local changes to guides and message types are not synced to Knock until you push:

```bash
knock guide push <guide-key>
knock message-type push <message-type-key>
```

### Discover before creating

Before creating guides or message types:

```bash
knock message-type list   # See available message type keys
knock guide list          # See existing guides
```

Use the exact keys from this output—don't assume keys from examples or other projects.

## Best practices summary

1. **Understand the model** — Guides are for lifecycle messaging; workflows are for notifications
2. **Message type first** — Create or pull the message type before creating guides that use it
3. **Match the schema** — Guide step `values` must align with the variant's fields
4. **Use built-ins when possible** — Banner, modal, and card cover many use cases
5. **Discover keys** — Run `knock message-type list` and `knock guide list` before creating
6. **Push after changes** — Local edits are not persisted until pushed
7. **Validate before push** — Use `knock guide validate` and `knock message-type validate` to catch errors early
