# Knock CLI

This skill provides comprehensive guidelines for working with the Knock CLI to manage workflows, templates, and other notification resources.

## How to use this skill

When working with this skill, follow these guidelines:

1. Review the relevant rule files for your specific use case
2. Follow the guidelines and best practices outlined in each rule
3. Reference the examples and templates provided
4. Ensure compliance with any requirements mentioned

---




# CLI commands reference

## Core concepts

### Resource types

The Knock CLI manages several resource types:

| Resource | Description | Command prefix |
|----------|-------------|----------------|
| `workflow` | Notification workflows | `knock workflow` |
| `email-layout` | Email layout templates | `knock email-layout` |
| `translation` | Localization files | `knock translation` |
| `partial` | Reusable template partials | `knock partial` |
| `commit` | Version control for changes | `knock commit` |

### Global options

These options work with most commands:

| Option | Description |
|--------|-------------|
| `--environment`, `-e` | Target environment (development, staging, production) |
| `--service-token` | Service token for authentication |
| `--knock-dir` | Override the knock directory location |
| `--help` | Show help for the command |

## Pulling resources

### Pull all resources

Sync all resources from Knock to your local project:

```bash
knock pull --all
```

This pulls all resource types into the configured `knockDir`.

### Pull specific resource types

Pull only specific resource types:

```bash
# Pull only workflows
knock workflow pull --all

# Pull only email layouts
knock email-layout pull --all

# Pull only translations
knock translation pull --all
```

### Pull a specific resource

Pull a single resource by its key:

```bash
# Pull a specific workflow
knock workflow pull <workflow-key>

# Pull a specific email layout
knock email-layout pull <layout-key>
```

**Example:**

```bash
knock workflow pull order-confirmation
knock email-layout pull default
```

### Pull options

| Option | Description |
|--------|-------------|
| `--all` | Pull all resources of this type |
| `--environment`, `-e` | Target environment |
| `--hide-uncommitted-changes` | Don't include uncommitted changes |

## Pushing resources

### Push all resources

Push all local resources to Knock:

```bash
knock push --all
```

This pushes all resources from the configured `knockDir` to Knock.

### Push specific resource types

Push only specific resource types:

```bash
# Push only workflows
knock workflow push --all

# Push only email layouts
knock email-layout push --all

# Push only translations
knock translation push --all
```

### Push a specific resource

Push a single resource by its key (the directory name):

```bash
# Push a specific workflow
knock workflow push <workflow-key>

# Push a specific email layout
knock email-layout push <layout-key>
```

**Example:**

```bash
knock workflow push order-confirmation
knock email-layout push default
```

### Push options

| Option | Description |
|--------|-------------|
| `--all` | Push all resources of this type |
| `--environment`, `-e` | Target environment |
| `--commit`, `-m` | Commit changes with a message after pushing |

### Push and commit

To push changes and commit them in one operation:

```bash
knock workflow push order-confirmation --commit -m "Updated order confirmation template"
```

## Workflow commands

### List workflows

```bash
knock workflow list
```

### Pull workflow

```bash
# Pull all workflows
knock workflow pull --all

# Pull specific workflow
knock workflow pull <workflow-key>
```

### Push workflow

```bash
# Push all workflows
knock workflow push --all

# Push specific workflow
knock workflow push <workflow-key>
```

### Validate workflow

Validate workflow structure without pushing:

```bash
knock workflow validate <workflow-key>
```

### Run workflow (trigger)

Trigger a workflow for testing:

```bash
knock workflow run <workflow-key> \
  --recipients='[{"id": "user-123"}]' \
  --data='{"order_id": "12345"}'
```

## Email layout commands

### List email layouts

```bash
knock email-layout list
```

### Pull email layout

```bash
# Pull all layouts
knock email-layout pull --all

# Pull specific layout
knock email-layout pull <layout-key>
```

### Push email layout

```bash
# Push all layouts
knock email-layout push --all

# Push specific layout
knock email-layout push <layout-key>
```

## Commit commands

### List commits

View commit history:

```bash
knock commit list
```

### Create commit

Commit staged changes:

```bash
knock commit create -m "Commit message"
```

### Promote commit

Promote changes between environments:

```bash
knock commit promote --to=production
```

## Translation commands

### Pull translations

```bash
# Pull all translations
knock translation pull --all

# Pull specific locale
knock translation pull <locale>
```

### Push translations

```bash
# Push all translations
knock translation push --all

# Push specific locale
knock translation push <locale>
```

## Initialization and configuration

### Initialize project

Create a new knock.json configuration:

```bash
knock init
```

This interactive command asks for the knock directory location and creates the configuration file.

### Whoami

Check current authentication:

```bash
knock whoami
```

## Common workflows

### Initial setup

```bash
# 1. Authenticate
export KNOCK_SERVICE_TOKEN=<your-token>

# 2. Initialize project
knock init

# 3. Pull existing resources
knock pull --all
```

### Make changes and deploy

```bash
# 1. Make local changes to workflow files

# 2. Push changes
knock workflow push <workflow-key>

# 3. Commit changes
knock commit create -m "Updated workflow"

# 4. Promote to production
knock commit promote --to=production
```

### Sync before editing

```bash
# Always pull latest before making changes
knock pull --all

# Make edits...

# Push and commit
knock push --all --commit -m "Updated templates"
```

## Error handling

### Common errors

**"Resource not found"**
- The specified key doesn't match any resource
- Verify the key matches the directory name exactly

**"Validation failed"**
- The resource has structural errors
- Check the error message for specific field issues
- Reference the JSON schema for correct structure

**"Uncommitted changes exist"**
- There are pending changes that haven't been committed
- Either commit first or use `--force` if available

**"Environment not found"**
- The specified environment doesn't exist
- Check available environments in the Knock dashboard

### Debugging

Use verbose output for troubleshooting:

```bash
knock workflow push <key> --verbose
```

---



# CLI installation and authentication

## Installation

### Prerequisites

The Knock CLI requires Node.js 18+ or can be installed via Homebrew on macOS.

### Installation methods

**Using npm (recommended):**

```bash
npm install -g @knocklabs/cli
```

**Using Homebrew (macOS):**

```bash
brew install knocklabs/tap/knock
```

**Verify installation:**

```bash
knock --version
```

### Expectation for agents

When working with a project that uses Knock, the CLI should already be installed. If the `knock` command is not available:

1. First attempt to install it using `npm install -g @knocklabs/cli`
2. If npm is not available, try Homebrew on macOS
3. If installation fails, inform the user that the Knock CLI needs to be installed

## Authentication

The Knock CLI supports two authentication methods: service tokens (recommended for CI/CD and automation) and interactive dashboard login (for local development).

### Method 1: Service token authentication (recommended)

Service tokens are the preferred method for automated workflows and CI/CD pipelines.

**Setting up a service token:**

1. Generate a service token from the Knock dashboard under Developer settings
2. Set the environment variable:

```bash
export KNOCK_SERVICE_TOKEN=<your-service-token>
```

**Using in commands:**

```bash
# The CLI automatically uses KNOCK_SERVICE_TOKEN if set
knock pull --all

# Or pass explicitly
knock pull --all --service-token=<your-service-token>
```

**Best practices for service tokens:**

- Store tokens securely in environment variables or secrets management
- Use different tokens for different environments (development, staging, production)
- Rotate tokens periodically
- Never commit tokens to version control

### Method 2: Dashboard account authentication

For local development, you can authenticate using your Knock dashboard account.

**Interactive login:**

```bash
knock auth login
```

This opens a browser window for authentication. Once authenticated, credentials are stored locally.

**Check authentication status:**

```bash
knock auth whoami
```

**Logout:**

```bash
knock auth logout
```

## Environment configuration

### Working with multiple environments

Knock supports multiple environments (development, staging, production). Specify the environment when running commands:

```bash
# Pull from development environment
knock pull --all --environment=development

# Push to production
knock push --all --environment=production
```

### Environment variables

| Variable | Description |
|----------|-------------|
| `KNOCK_SERVICE_TOKEN` | Service token for authentication |
| `KNOCK_API_ORIGIN` | Custom API origin (rarely needed) |

## Project initialization

After authentication, initialize your project:

```bash
knock init
```

This creates a `knock.json` configuration file in your project root. See the directory structure documentation for details on this file.

## Troubleshooting

### Common issues

**"Command not found: knock"**
- The CLI is not installed or not in PATH
- Try reinstalling: `npm install -g @knocklabs/cli`

**"Authentication required"**
- Set the `KNOCK_SERVICE_TOKEN` environment variable
- Or run `knock auth login` for interactive authentication

**"Invalid service token"**
- Verify the token is correct and hasn't been revoked
- Check if the token has access to the target environment

**"Permission denied"**
- The authenticated user/token may lack permissions for the operation
- Verify role assignments in the Knock dashboard

### Verifying setup

Run this command to verify your setup is working:

```bash
knock whoami
```

This displays the authenticated account and available environments.

---



# Knock directory structure

## Project configuration

### The knock.json file

Running `knock init` creates a `knock.json` file in your project root. This file configures where Knock resources are stored.

**Basic structure:**

```json
{
  "knockDir": "./knock"
}
```

**Configuration options:**

| Property | Description | Default |
|----------|-------------|---------|
| `knockDir` | Path to the directory containing Knock resources | `./knock` |

The `knockDir` is relative to the location of `knock.json`. All CLI operations use this directory as the root for reading and writing resources.

## Directory layout

The knock directory contains subdirectories for each resource type:

```
knock/
├── workflows/                    # Workflow definitions
│   ├── workflow.schema.json      # JSON Schema for validation
│   └── {workflow-key}/           # One directory per workflow
│       ├── workflow.json         # Main workflow definition
│       └── {step-ref}/           # Channel step content (optional)
│           └── ...               # Template files
│
├── email-layouts/                # Email layout templates
│   └── {layout-key}/
│       ├── layout.json           # Layout configuration
│       └── ...                   # Layout template files
│
├── translations/                 # Translation files
│   └── {locale}/
│       └── ...                   # Translation JSON files
│
├── partials/                     # Reusable template partials
│   └── {partial-key}/
│       └── ...                   # Partial template files
│
└── commits/                      # Commit history (managed by CLI)
```

## Workflow structure

Each workflow lives in its own directory under `workflows/`:

```
workflows/{workflow-key}/
├── workflow.json                 # Main workflow definition
└── {step-ref}/                   # Directory per channel step (optional)
    └── ...                       # Template content files
```

### workflow.json

The main workflow definition file contains:

```json
{
  "name": "Order Confirmation",
  "description": "Sends order confirmation notifications",
  "categories": ["transactional", "orders"],
  "steps": [
    {
      "ref": "email-step",
      "type": "email",
      "template": {
        "subject": "Order #{{data.order_id}} confirmed",
        "visual_blocks@": "email-step/visual_blocks.json"
      }
    }
  ]
}
```

**Key fields:**

| Field | Description |
|-------|-------------|
| `name` | Display name for the workflow |
| `description` | Optional description |
| `categories` | Optional array of category tags |
| `steps` | Array of workflow steps |

### Step directories

Channel steps (email, SMS, push, etc.) can have their template content extracted into separate files within a step directory:

```
workflows/order-confirmation/
├── workflow.json
└── email-step/
    ├── visual_blocks.json        # Email visual blocks structure
    └── visual_blocks/
        ├── 1.content.md          # First block content
        ├── 2.content.md          # Second block content
        └── ...
```

**When step directories exist:**
- Channel steps with extracted template content
- Complex templates that benefit from separate files

**When step directories don't exist:**
- Function steps (delay, batch, branch, fetch, etc.) never have directories
- Simple templates with inline content

## Email layouts

Email layouts define reusable structure for email templates:

```
email-layouts/{layout-key}/
├── layout.json                   # Layout configuration
├── html_layout.html              # HTML layout template (optional)
└── ...                           # Additional layout files
```

### layout.json

```json
{
  "name": "Default Layout",
  "html_layout@": "html_layout.html",
  "text_layout": "{{ content }}",
  "footer_links": [
    {
      "label": "Unsubscribe",
      "url": "{{ unsubscribe_url }}"
    }
  ]
}
```

## File path references

Knock uses the `@` suffix convention to indicate file path references:

```json
{
  "content@": "visual_blocks/1.content.md",
  "html_body@": "body.html",
  "visual_blocks@": "email-step/visual_blocks.json"
}
```

**Path resolution rules:**

1. Paths are **relative to the file containing the reference**
2. In `workflow.json` (at workflow root): paths start from the workflow directory
3. In `visual_blocks.json` (inside step directory): paths are relative to that step directory

**Example:**

```
workflows/my-workflow/
├── workflow.json                 # Uses: "visual_blocks@": "email-step/visual_blocks.json"
└── email-step/
    ├── visual_blocks.json        # Uses: "content@": "visual_blocks/1.content.md"
    └── visual_blocks/
        └── 1.content.md
```

**Common mistake:** Doubling the step directory path. If you're in `email-step/visual_blocks.json`, use `visual_blocks/1.content.md`, NOT `email-step/visual_blocks/1.content.md`.

## JSON Schema

The `workflows/workflow.schema.json` file provides validation for workflow definitions. Reference this schema when:

- Creating or modifying templates
- Working with specific channel types
- Encountering validation errors
- Adding function steps

## Resource identification

Resources are identified by their directory name (the key):

| Resource Type | Key Location | Example |
|---------------|--------------|---------|
| Workflow | Directory name under `workflows/` | `workflows/order-confirmation/` → key: `order-confirmation` |
| Email Layout | Directory name under `email-layouts/` | `email-layouts/default/` → key: `default` |
| Partial | Directory name under `partials/` | `partials/footer/` → key: `footer` |

This key is used in CLI commands:

```bash
knock workflow push order-confirmation
knock email-layout push default
```

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

---
