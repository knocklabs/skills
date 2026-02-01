---
title: Workflow and template gotchas
description: Important patterns, common mistakes, and best practices when working with Knock workflows and templates via the CLI
tags:
  - knock
  - cli
  - workflows
  - templates
  - email
  - liquid
  - gotchas
  - best-practices
category: knock-cli
last_updated: 2026-02-01
---

# Workflow and template gotchas

## Critical rules

### Always read before writing

Before modifying any workflow or template file, always read the existing content first. This prevents:

- Losing existing data or configuration
- Breaking the current structure
- Overwriting uncommitted changes

```bash
# Read the current state before making changes
cat knock/workflows/my-workflow/workflow.json
```

### Always persist changes

After modifying workflow files locally, you must push the changes to Knock for them to take effect:

```bash
knock workflow push <workflow-key>
```

Local file changes are not persisted to Knock until explicitly pushed.

## Email template modes

Knock emails support two mutually exclusive modes. When modifying existing emails, always preserve the current mode.

### Visual blocks mode (preferred)

A structured array of blocks for the email body. This is the recommended approach for most emails.

**Structure:**

```
workflows/my-workflow/
└── email-step/
    ├── visual_blocks.json         # Block structure
    └── visual_blocks/
        ├── 1.content.md           # First block content (1-indexed)
        ├── 2.content.md           # Second block content
        └── ...
```

**visual_blocks.json example:**

```json
[
  {
    "type": "markdown",
    "content@": "visual_blocks/1.content.md"
  },
  {
    "type": "button_set",
    "buttons": [
      {
        "label": "View Order",
        "action": "{{data.order_url}}"
      }
    ]
  },
  {
    "type": "divider"
  },
  {
    "type": "markdown",
    "content@": "visual_blocks/2.content.md"
  }
]
```

**Block types:**

| Type | Description |
|------|-------------|
| `markdown` | Markdown content block |
| `button_set` | One or more buttons |
| `divider` | Horizontal divider |
| `image` | Image block |
| `html` | Raw HTML block |
| `row` | Multi-column row |

### HTML mode

Raw HTML template when full control is needed. Use only when explicitly requested.

**Structure:**

```
workflows/my-workflow/
└── email-step/
    └── html_body.html             # Raw HTML template
```

**In workflow.json:**

```json
{
  "ref": "email-step",
  "type": "email",
  "template": {
    "subject": "Your order is confirmed",
    "html_body@": "email-step/html_body.html"
  }
}
```

### Preserving template mode

When modifying an existing email:

1. Check which mode is currently used (visual blocks vs HTML)
2. Preserve that mode in your changes
3. Don't convert between modes unless explicitly requested

## File path reference rules

### The @ suffix convention

Knock uses `@` suffix to indicate file path references:

```json
{
  "content@": "visual_blocks/1.content.md",
  "html_body@": "body.html",
  "visual_blocks@": "email-step/visual_blocks.json"
}
```

When the field name ends with `@`, the value is a file path, and the actual content lives in the referenced file.

### Path resolution

**Critical rule:** Paths are relative to the file containing the reference.

**Example directory:**

```
workflows/order-confirmation/
├── workflow.json
└── email-step/
    ├── visual_blocks.json
    └── visual_blocks/
        └── 1.content.md
```

**In workflow.json (at workflow root):**

```json
{
  "visual_blocks@": "email-step/visual_blocks.json"
}
```

**In email-step/visual_blocks.json (inside step directory):**

```json
{
  "content@": "visual_blocks/1.content.md"
}
```

### Common mistake: Doubling the step directory

When editing `{step_ref}/visual_blocks.json`, paths are already relative to that step directory.

**Wrong:**

```json
{
  "content@": "email-step/visual_blocks/1.content.md"
}
```

**Correct:**

```json
{
  "content@": "visual_blocks/1.content.md"
}
```

## Liquid templating

Knock templates use Liquid syntax for dynamic content. Understanding the correct namespaces is critical.

### Variable namespaces

| Namespace | Description | Use for |
|-----------|-------------|---------|
| `data` | Trigger payload | Dynamic data passed when workflow is triggered |
| `vars` | Environment variables | Static values configured at environment level |
| `recipient` | Notification recipient | Recipient properties like name, email |
| `actor` | Triggering user | User who triggered the action |
| `tenant` | Tenant information | Multi-tenancy data |

### Common mistake: Using vars for trigger data

**Wrong:**

```liquid
Your order {{ vars.order_id }} has shipped.
```

**Correct:**

```liquid
Your order {{ data.order_id }} has shipped.
```

**Rule:** If the value comes from the API trigger payload, use `data.`, not `vars.`.

- `data.order_id` - Value passed when triggering the workflow
- `vars.app_name` - Static environment variable like "Acme Corp"

### Liquid syntax examples

**Variables:**

```liquid
{{ recipient.name }}
{{ data.order_id }}
{{ vars.support_email }}
```

**Filters:**

```liquid
{{ recipient.name | default: "there" }}
{{ data.amount | currency }}
{{ data.date | date: "%B %d, %Y" }}
```

**Conditionals:**

```liquid
{% if data.items.size > 0 %}
  You have {{ data.items.size }} items in your order.
{% else %}
  Your cart is empty.
{% endif %}
```

**Loops:**

```liquid
{% for item in data.items %}
  - {{ item.name }}: {{ item.price | currency }}
{% endfor %}
```

### Default values

Always provide defaults for optional values:

```liquid
Hi {{ recipient.name | default: "there" }},
```

## Step types

### Channel steps (have template content)

These step types send notifications and can have extracted template content:

| Type | Description |
|------|-------------|
| `email` | Email notifications |
| `sms` | SMS text messages |
| `push` | Push notifications |
| `chat` | Chat app messages (Slack, Teams) |
| `in_app_feed` | In-app notification feed |
| `webhook` | Webhook calls |

### Function steps (no template directories)

These step types control workflow logic and never have step directories:

| Type | Description |
|------|-------------|
| `delay` | Wait for a specified time |
| `batch` | Batch multiple triggers |
| `throttle` | Limit notification frequency |
| `branch` | Conditional branching |
| `fetch` | Fetch external data |
| `trigger_workflow` | Trigger another workflow |

## Workflow.json structure

### Minimal workflow

```json
{
  "name": "My Workflow",
  "steps": []
}
```

### Complete workflow example

```json
{
  "name": "Order Confirmation",
  "description": "Sends order confirmation across multiple channels",
  "categories": ["transactional", "orders"],
  "steps": [
    {
      "ref": "email-confirmation",
      "type": "email",
      "template": {
        "subject": "Order #{{data.order_id}} confirmed",
        "visual_blocks@": "email-confirmation/visual_blocks.json"
      }
    },
    {
      "ref": "delay-step",
      "type": "delay",
      "settings": {
        "duration": "1 hour"
      }
    },
    {
      "ref": "push-notification",
      "type": "push",
      "template": {
        "title": "Order Shipped!",
        "body": "Your order #{{data.order_id}} is on its way."
      }
    }
  ]
}
```

## Channel-specific templates

### SMS template

```json
{
  "ref": "sms-step",
  "type": "sms",
  "template": {
    "body": "Your code is {{data.code}}. Valid for 10 minutes."
  }
}
```

### Push notification template

```json
{
  "ref": "push-step",
  "type": "push",
  "template": {
    "title": "{{data.title}}",
    "body": "{{data.message}}"
  }
}
```

### In-app feed template

```json
{
  "ref": "in-app-step",
  "type": "in_app_feed",
  "template": {
    "markdown": "**{{actor.name}}** commented on your post",
    "action_url": "{{data.post_url}}"
  }
}
```

### Webhook template

```json
{
  "ref": "webhook-step",
  "type": "webhook",
  "template": {
    "json_body": {
      "event": "order.confirmed",
      "order_id": "{{data.order_id}}",
      "customer_email": "{{recipient.email}}"
    }
  }
}
```

## Validation and debugging

### Check the schema

When encountering validation errors, reference the JSON schema:

```
knock/workflows/workflow.schema.json
```

### Validate before pushing

```bash
knock workflow validate <workflow-key>
```

### Common validation errors

**"Invalid step type"**
- Check that `type` matches a valid step type
- Verify spelling (e.g., `in_app_feed`, not `in-app-feed`)

**"Missing required field"**
- Channel steps require a `template` object
- Templates require specific fields based on channel type

**"Invalid file reference"**
- Check that referenced files exist
- Verify path is relative to the containing file
- Ensure no doubled directory paths

## Testing workflows

### Use the CLI to trigger test runs

```bash
knock workflow run <workflow-key> \
  --recipients='[{"id": "user-123", "email": "test@example.com", "name": "Test User"}]' \
  --data='{"order_id": "12345", "amount": 99.99}'
```

### Test checklist

- [ ] Variables render correctly with real data
- [ ] Default values appear when data is missing
- [ ] Conditional logic works as expected
- [ ] Links and buttons point to correct URLs
- [ ] Email displays properly across clients
- [ ] All channels receive appropriate content

## Best practices summary

1. **Read before writing** - Always check existing structure first
2. **Preserve template modes** - Don't switch between visual blocks and HTML
3. **Use correct namespaces** - `data` for trigger payload, `vars` for environment variables
4. **Paths are relative** - To the file containing the reference
5. **Don't double directories** - Inside step directories, paths are relative to that directory
6. **Always push changes** - Local changes aren't persisted until pushed
7. **Validate first** - Use validate command before pushing to catch errors
8. **Provide defaults** - Use Liquid defaults for optional values
