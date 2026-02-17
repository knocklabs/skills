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

### Interactive prompts and the `--force` flag

Many Knock CLI commands display interactive confirmation prompts that require user input. This is critical for AI agents and automated scripts, because commands will hang or default to "no" if input is not provided.

**Commands that prompt for confirmation (and support `--force`):**

| Command | Prompt | When |
|---------|--------|------|
| `knock workflow pull <key>` | `Create a new workflow directory? (y/N)` | When the local directory doesn't exist yet |
| `knock email-layout pull <key>` | `Create a new email layout directory? (y/N)` | When the local directory doesn't exist yet |
| `knock guide pull <key>` | `Create a new guide directory? (y/N)` | When the local directory doesn't exist yet |
| `knock message-type pull <key>` | `Create a new message type directory? (y/N)` | When the local directory doesn't exist yet |
| `knock partial pull <key>` | `Create a new partial directory? (y/N)` | When the local directory doesn't exist yet |
| `knock pull --all` | Multiple directory creation prompts | When pulling resources that don't exist locally yet |
| `knock commit promote` | Confirmation prompt | When promoting changes between environments |
| `knock commit` | Confirmation prompt | When committing changes |
| `knock workflow activate` | Confirmation prompt | When activating/deactivating a workflow |
| `knock guide activate` | Confirmation prompt | When activating/deactivating a guide |

**Handling prompts:** Pass `--force` to skip all confirmation prompts. Always use `--force` when running commands from agents or automated scripts:

```bash
# Pull without confirmation prompts
knock workflow pull <workflow-key> --force
knock pull --all --force

# Commit and promote without prompts
knock commit -m "message" --force
knock commit promote --to=production --force
```

**Commands that are interactive and cannot use `--force`:**

| Command | Behavior |
|---------|----------|
| `knock init` | Multi-step interactive wizard for project setup. Use `--knock-dir` to skip the directory prompt. If a `knock.json` already exists, there is no need to run `knock init`. |
| `knock auth login` | Opens a browser window for authentication. Must be run manually by the user. |
| `knock workflow new` | Interactive step selection. Use `--key` and `--steps` flags to skip prompts. |
| `knock guide new` | Interactive message type selection. Use `--key` and `--message-type` flags to skip prompts. |
| `knock message-type new` | Interactive setup. Use `--key` and `--name` flags to skip prompts. |
| `knock partial new` | Interactive setup. Use `--key` and `--type` flags to skip prompts. |

**Commands that never prompt (safe for direct execution):**

- All `list` commands (`knock workflow list`, `knock channel list`, etc.)
- All `push` commands (`knock workflow push <key>`, `knock push --all`, etc.)
- All `validate` commands (`knock workflow validate <key>`, etc.)
- `knock whoami` / `knock auth whoami`
- `knock workflow run` (trigger)
- Pull commands when the local directory already exists (updates in place without prompting)

### Push required after changes

Local edits to Knock resources (workflows, layouts, partials, etc.) are not synced to Knock until you push. Always run the appropriate push command after modifying files—otherwise Knock continues using the previous version.

### Resource types

The Knock CLI manages several resource types:

| Resource | Description | Command prefix |
|----------|-------------|----------------|
| `workflow` | Notification workflows | `knock workflow` |
| `email-layout` | Email layout templates | `knock email-layout` |
| `guide` | In-app guides (lifecycle messaging) | `knock guide` |
| `message-type` | Message type schemas for guides | `knock message-type` |
| `channel` | Notification channels | `knock channel` |
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

**Note:** Pull commands prompt for confirmation when creating new local directories. Use `--force` to skip these prompts (see [Interactive prompts and the `--force` flag](#interactive-prompts-and-the---force-flag)).

### Pull all resources

Sync all resources from Knock to your local project:

```bash
knock pull --all --force
```

This pulls all resource types into the configured `knockDir`.

### Pull specific resource types

Pull only specific resource types:

```bash
# Pull only workflows
knock workflow pull --all --force

# Pull only email layouts
knock email-layout pull --all --force

# Pull only translations
knock translation pull --all --force

# Pull only guides
knock guide pull --all --force

# Pull only message types
knock message-type pull --all --force
```

### Pull a specific resource

Pull a single resource by its key:

```bash
# Pull a specific workflow
knock workflow pull <workflow-key> --force

# Pull a specific email layout
knock email-layout pull <layout-key> --force
```

**Example:**

```bash
knock workflow pull order-confirmation --force
knock email-layout pull default --force
```

**Note:** If the local directory already exists, pull commands update in place without prompting. The `--force` flag is only needed for the first pull of a given resource, but is safe to always include.

### Pull options

| Option | Description |
|--------|-------------|
| `--all` | Pull all resources of this type |
| `--environment`, `-e` | Target environment |
| `--hide-uncommitted-changes` | Don't include uncommitted changes |
| `--force` | Skip confirmation prompts (always use in automated/agent contexts) |

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

# Push only guides
knock guide push --all

# Push only message types
knock message-type push --all
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
knock workflow pull --all --force

# Pull specific workflow
knock workflow pull <workflow-key> --force
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
knock email-layout pull --all --force

# Pull specific layout
knock email-layout pull <layout-key> --force
```

### Push email layout

```bash
# Push all layouts
knock email-layout push --all

# Push specific layout
knock email-layout push <layout-key>
```

## Guide commands

### List guides

```bash
knock guide list
```

### Create a new guide

```bash
knock guide new -k <guide-key> -n "Guide name" -m <message-type-key>
```

### Pull guide

```bash
# Pull all guides
knock guide pull --all --force

# Pull specific guide
knock guide pull <guide-key> --force
```

### Push guide

```bash
# Push all guides
knock guide push --all

# Push specific guide
knock guide push <guide-key>
```

### Validate guide

```bash
knock guide validate <guide-key>
```

### Activate or deactivate guide

```bash
knock guide activate <guide-key> --environment <env> --status true
knock guide activate <guide-key> --environment <env> --status false
```

### Other guide commands

```bash
knock guide get <guide-key>      # Display a single guide
knock guide open <guide-key>     # Open in dashboard
knock guide generate-types --output-file types.ts  # Generate TypeScript types
```

## Message type commands

### List message types

```bash
knock message-type list
```

Lists all message types with their keys. Use these keys when creating guides. Message type keys are project-specific—discover them before creating guides.

### Create a new message type

```bash
knock message-type new -k <message-type-key> -n "Message type name"
```

### Pull message type

```bash
# Pull all message types
knock message-type pull --all --force

# Pull specific message type
knock message-type pull <message-type-key> --force
```

### Push message type

```bash
# Push all message types
knock message-type push --all

# Push specific message type
knock message-type push <message-type-key>
```

Message type push operates only in the development environment.

### Validate message type

```bash
knock message-type validate <message-type-key>
```

### Other message type commands

```bash
knock message-type get <message-type-key>   # Display a single message type
knock message-type open <message-type-key>  # Open in dashboard
```

## Channel commands

### List channels

```bash
knock channel list
```

Lists all channels configured in the project with their keys. Channel keys are project-specific—they vary per project and must be discovered, not assumed. Use the keys from this output for `channel_key` in workflow steps.

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
# Prompts for confirmation; use --force to skip
knock commit promote --to=production --force
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

# 2. Initialize project (interactive wizard — use --knock-dir to skip prompts, or run manually)
knock init --knock-dir=./knock

# 3. Pull existing resources (--force skips confirmation prompts)
knock pull --all --force
```

### Discover before creating

Before creating workflows that use channels or layouts, discover the project's configuration:

```bash
# List available channel keys (use these for channel_key in workflow steps)
knock channel list

# List available email layout keys (use these for layout_key in template settings)
knock email-layout list
```

Before creating guides, discover available message types:

```bash
# List available message type keys (use these when creating guides)
knock message-type list

# List existing guides
knock guide list
```

Use the exact keys from this output—don't assume keys from schema examples or other projects.

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
# Always pull latest before making changes (--force skips any new directory prompts)
knock pull --all --force

# Make edits...

# Push and commit (push does not prompt)
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
- If the error mentions `channel_key` does not exist (e.g., `'knock-in-app' does not exist`), run `knock channel list` to find valid channel keys for this project

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

### Important: Interactive prompts and the `--force` flag

Many Knock CLI commands use interactive prompts (y/N confirmations, multi-step wizards, browser-based auth). These prompts will cause commands to hang or default to "no" if not handled.

**For agents and scripts:** Most commands that prompt support a `--force` flag that skips all confirmation prompts. Always use `--force` when running commands non-interactively:

```bash
knock workflow pull <workflow-key> --force
knock pull --all --force
knock commit promote --to=production --force
```

Some commands like `knock init`, `knock auth login`, and `knock workflow new` are fully interactive and don't support `--force`. Use their explicit flags (e.g., `--knock-dir`, `--key`, `--steps`) to avoid prompts, or have the user run them manually.

See the CLI commands reference (`rules/cli-commands-reference.md`) for a full table of which commands prompt, which support `--force`, and which are safe to run directly.

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

**Interactive login (requires browser — cannot be automated by agents):**

```bash
knock auth login
```

This opens a browser window for authentication. Once authenticated, credentials are stored locally. Because this requires browser interaction, it must be run manually by the user—agents cannot complete this flow.

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
  "channel_key": "knock-guide",
  "steps": [
    {
      "ref": "step_1",
      "schema_key": "modal",
      "schema_semver": "0.0.1",
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

**Guide-level fields:**

| Field | Description | Required |
|-------|-------------|----------|
| `name` | Display name for the guide | Yes |
| `channel_key` | The key of the `in_app_guide` channel. Discover with `knock channel list` and use the key where `Type` is `in_app_guide`. | Yes |

**Step fields:**

| Field | Description | Required |
|-------|-------------|----------|
| `ref` | Unique step reference | Yes |
| `schema_key` | Message type key (e.g., `banner`, `modal`, `card`, or a custom key) | Yes |
| `schema_semver` | Semver of the message type (e.g., `"0.0.1"`). Find this in the message type's `__readonly.semver` field after pulling it, or default to `"0.0.1"` for newly created types. | Yes |
| `schema_variant_key` | Variant key from the message type (e.g., `default`, `single-action`) | Yes |
| `values` | Object matching the variant's field keys | Yes |

The `values` object must include every field defined in the selected variant. For `button` fields, both `text` and `action` must be non-empty strings.

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

### `knock guide new` scaffold is incomplete

The `knock guide new` command generates a `guide.json` that is **missing two required fields**: `channel_key` (on the guide) and `schema_semver` (on each step). Pushing or validating the scaffold as-is will fail. Always add both fields before pushing. See the [guide.json](#guidejson) section for the correct structure.

### `channel_key` is required on every guide

Every guide must include a `channel_key` pointing to an `in_app_guide` channel. Without it, the API returns `"channel_key" can't be blank`. Run `knock channel list` and use the key where the `Type` column shows `in_app_guide` (commonly `knock-guide`).

### `schema_semver` is required on every guide step

Every guide step must include `schema_semver` matching the message type's version. Without it, the API returns a **misleading** error: `"steps[0].schema_key" template schema not found` — even though the message type key is correct and exists. This error does **not** mean the key is wrong; it means the semver is missing.

To find the correct semver:
1. Pull the message type: `knock message-type pull <key> --force`
2. Look at `__readonly.semver` in `message_type.json` (e.g., `"0.0.1"`)

For newly created message types, the semver is always `"0.0.1"`.

### Custom message types must be committed before guides can reference them

A pushed-but-uncommitted custom message type cannot be used by guides. The API will return `"schema_key" template schema not found`. You must commit the message type first (via the dashboard or `knock commit`), then push the guide.

### Message types must exist first

Before creating a guide, ensure the message type it references exists. Run `knock message-type list` to discover available message type keys. Use `-m <message-type-key>` when running `knock guide new`.

### Built-in types are immutable

The `banner`, `modal`, and `card` message types cannot be edited. To customize, clone the message type in the dashboard and use the clone's key.

### Guide values must match the schema

Each guide step's `values` object must match the fields of the selected `schema_key` + `schema_variant_key`. Missing or extra keys can cause validation errors.

### Button field values must be non-empty

When a message type variant includes a `button` field (e.g., `primary_button`), the guide's `values` must provide both `text` and `action` as **non-empty strings**. An empty `action` (e.g., `"action": ""`) will cause a validation error: `"fields[N].action.value" can't be blank`. Use a meaningful action URL or a placeholder like `"submit"` or `"dismiss"`.

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
knock channel list        # Find the in_app_guide channel key
```

Use the exact keys from this output—don't assume keys from examples or other projects.

## Creating a guide end-to-end

The recommended workflow for creating a guide from the CLI:

```bash
# 1. Discover available message types and channels
knock message-type list
knock channel list

# 2. Create (or pull) the message type
knock message-type new -k my-type -n "My type" --force
# Edit the message_type.json with your fields and variants
knock message-type push my-type

# 3. Commit the message type (required before guides can reference it)
knock commit -m "Add my-type message type" --force

# 4. Find the schema_semver after pushing
knock message-type pull my-type --force
# Check __readonly.semver in message_type.json (e.g., "0.0.1")

# 5. Scaffold the guide
knock guide new -k my-guide -n "My guide" -m my-type --force

# 6. Fix the scaffolded guide.json (add missing required fields)
#    - Add "channel_key": "<your-in_app_guide-channel-key>" at the guide level
#    - Add "schema_semver": "<semver>" to each step

# 7. Push the guide
knock guide push my-guide
```

## Best practices summary

1. **Understand the model** — Guides are for lifecycle messaging; workflows are for notifications
2. **Message type first** — Create or pull the message type before creating guides that use it
3. **Commit before referencing** — Custom message types must be committed before guides can use them
4. **Always add `channel_key` and `schema_semver`** — The CLI scaffold omits these required fields; add them manually before pushing
5. **Match the schema** — Guide step `values` must align with the variant's fields; button `action` values must be non-empty
6. **Use built-ins when possible** — Banner, modal, and card cover many use cases
7. **Discover keys** — Run `knock message-type list`, `knock guide list`, and `knock channel list` before creating
8. **Push after changes** — Local edits are not persisted until pushed
9. **Validate before push** — Use `knock guide validate` and `knock message-type validate` to catch errors early

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
├── guides/                       # In-app guides (lifecycle messaging)
│   └── {guide-key}/
│       └── guide.json            # Guide definition and content
│
├── message-types/                # Message type schemas for guides
│   └── {message-type-key}/
│       ├── message_type.json     # Schema and metadata
│       └── preview.html          # Optional; Liquid template for dashboard preview
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

## Guides

Guides are in-app UI components for lifecycle messaging (banners, modals, announcements). Each guide lives in its own directory:

```
guides/{guide-key}/
└── guide.json                    # Guide definition with steps and content
```

### guide.json

A guide contains a `name` and a `steps` array. Each step references a message type via `schema_key` and `schema_variant_key`, with content in `values`. See the guides and message types rule file for full details.

## Message types

Message types define the schema for guide content. They live under `message-types/`:

```
message-types/{message-type-key}/
├── message_type.json             # Schema with variants and fields
└── preview.html                  # Optional; Liquid template for dashboard preview
```

### message_type.json

The message type schema defines `name`, `description`, `icon_name`, and `variants`. Each variant has `key`, `name`, and `fields`. The `preview@` field references the preview HTML file. See the guides and message types rule file for schema details.

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
| Guide | Directory name under `guides/` | `guides/welcome-modal/` → key: `welcome-modal` |
| Message Type | Directory name under `message-types/` | `message-types/banner/` → key: `banner` |
| Partial | Directory name under `partials/` | `partials/footer/` → key: `footer` |

This key is used in CLI commands:

```bash
knock workflow push order-confirmation
knock email-layout push default
knock guide push welcome-modal
knock message-type push banner
```

---



# Partials

## What partials are

**Partials** are reusable template snippets that can be inserted into email templates via the visual block editor. They serve as building blocks for an email design system—callout cards, quote blocks, comment cards, footers, headers, and other repeatable components.

Partials are:

- Stored in `knock/partials/{key}/`
- Rendered with Liquid; they receive variables from the block editor or from the workflow context
- Available in the email visual block editor when `visual_block_enabled` is true
- Defined by a `partial.json` schema and a content file (HTML, markdown, text, or JSON)

## File structure

Partials live under `knock/partials/{key}/`:

```
partials/{partial-key}/
├── partial.json      # Schema, metadata, and input_schema
└── content.html      # Or content.md, content.txt, content.json
```

The partial key is the directory name and is used in CLI commands: `knock partial push callout-card`.

## partial.json schema

```json
{
  "name": "Callout card",
  "description": "A highlighted callout box for tips and important information.",
  "type": "html",
  "visual_block_enabled": true,
  "content@": "content.html",
  "icon_name": "BellDot",
  "input_schema": [
    {
      "type": "text",
      "key": "title",
      "label": "Title",
      "settings": { "required": false }
    },
    {
      "type": "markdown",
      "key": "body",
      "label": "Body",
      "settings": { "required": true }
    }
  ]
}
```

**Key fields:**

| Field | Description |
|-------|-------------|
| `name` | Display name in the dashboard and block editor |
| `description` | Optional description (max 280 characters) |
| `type` | Content type: `html`, `json`, `markdown`, or `text` |
| `visual_block_enabled` | When true, the partial appears in the email visual block editor |
| `content@` | File path to the content template (relative to the partial directory) |
| `icon_name` | Icon shown in the block editor (e.g., BellDot, Flag) |
| `input_schema` | Array of field definitions for the block editor; same format as a message type variant's `fields` |

## input_schema

The `input_schema` defines the fields that editors see when adding or editing a partial block in the email visual block editor. It uses the **exact same field format** as a message type variant's `fields` array.

Each field has:

- `type` — One of the supported field types
- `key` — Variable name passed to the Liquid template (must match `{{ key }}` in content)
- `label` — Display label in the editor
- `settings` — Object with `required`, `default`, `description`, and type-specific options

### Supported field types

| Type | Description | Settings |
|------|-------------|----------|
| `text` | Single-line text | `required`, `default`, `description`, `min_length`, `max_length` |
| `textarea` | Multi-line plain text | `required`, `default`, `description`, `min_length`, `max_length` |
| `markdown` | Markdown editor (rendered as HTML) | `required`, `default`, `description` |
| `boolean` | Checkbox (true/false) | `required`, `default`, `description` |
| `select` | Single-select from options | `required`, `default`, `description`, `options` (array of `{ label, value }`) |
| `multi_select` | Multi-select from options | `required`, `default`, `description`, `options` |
| `url` | URL field | `required`, `default`, `description` |
| `button` | Button with `text` and `action` subfields | `required`, `text`, `action` (each with `key`, `label`, `settings`) |
| `image` | Image with `url`, `alt`, `action` subfields | `required`, `url`, `alt`, `action` |

### input_schema example

```json
{
  "input_schema": [
    {
      "type": "text",
      "key": "title",
      "label": "Title",
      "settings": {
        "required": false,
        "description": "Optional heading"
      }
    },
    {
      "type": "markdown",
      "key": "body",
      "label": "Body",
      "settings": {
        "required": true,
        "description": "The main content"
      }
    },
    {
      "type": "select",
      "key": "type",
      "label": "Type",
      "settings": {
        "required": false,
        "default": "info",
        "options": [
          { "label": "Info", "value": "info" },
          { "label": "Warning", "value": "warning" }
        ]
      }
    }
  ]
}
```

The field `key` values become Liquid variables in the content template: `{{ title }}`, `{{ body }}`, `{{ type }}`.

## Partial types

| Type | Content file | Use case |
|------|--------------|----------|
| `html` | `content.html` | Email design system components (callouts, cards, blocks) |
| `markdown` | `content.md` | Markdown snippets |
| `text` | `content.txt` | Plain text snippets |
| `json` | `content.json` | Structured data blocks |

For email design systems, `html` is the most common type. Use inline styles for email client compatibility.

## CLI commands

### List partials

```bash
knock partial list
```

### Create a new partial

```bash
# Interactive; use flags to skip prompts
knock partial new -k <partial-key> -n "Partial name" -t html --force
```

| Flag | Description |
|------|-------------|
| `-k`, `--key` | The partial key (directory name) |
| `-n`, `--name` | Display name |
| `-t`, `--type` | `html`, `json`, `markdown`, or `text` |
| `--force` | Skip confirmation prompts |
| `-p`, `--push` | Push to Knock after creation |

### Pull partials

```bash
# Pull all partials
knock partial pull --all --force

# Pull a specific partial
knock partial pull <partial-key> --force
```

Use `--force` to skip "Create a new partial directory?" prompts when the directory does not exist locally.

### Push partials

```bash
# Push all partials
knock partial push --all

# Push a specific partial
knock partial push <partial-key>
```

### Validate partials

```bash
knock partial validate <partial-key>
knock partial validate --all
```

### Other commands

```bash
knock partial get <partial-key>    # Display a single partial
knock partial open <partial-key>   # Open in Knock dashboard
```

## Creating a partial end-to-end

1. **Create the partial locally**

   ```bash
   knock partial new -k callout-card -n "Callout card" -t html --force
   ```

2. **Edit partial.json** — Add `description`, `visual_block_enabled`, and `input_schema` with fields matching the variables your content template expects.

3. **Edit the content file** — Write the Liquid template (e.g., `content.html`) using `{{ key }}` for each input_schema field.

4. **Validate**

   ```bash
   knock partial validate callout-card
   ```

5. **Push**

   ```bash
   knock partial push callout-card
   ```

6. **Commit** (optional) — Use `knock commit -m "Add callout-card partial" --force` to commit the change in Knock.

## Using partials in templates

When a partial is added as a visual block in an email template, Knock renders it with the values editors provide in the block editor. Those values come from the `input_schema` fields and are passed as Liquid variables.

In your partial content, reference them by key:

```liquid
<table>
  <tr>
    <td>{{ body }}</td>
  </tr>
</table>
```

Partials can also use workflow context: `data`, `vars`, `recipient`, `actor`, `tenant`. Use `data.` for trigger payload values, not `vars.`.

## Key gotchas

### Push after every change

Local edits to partials are not synced to Knock until you push. Run `knock partial push <key>` after modifying any partial file.

### Use --force on pulls

When pulling a partial that does not exist locally, the CLI prompts for confirmation. Pass `--force` to skip the prompt in automated contexts.

### visual_block_enabled required for email editor

Only partials with `visual_block_enabled: true` appear in the email visual block editor. HTML partials without this flag are not available as blocks.

### input_schema keys must match content variables

Each `input_schema` field's `key` must correspond to a variable used in the content template. A field with `key: "author_name"` should be referenced as `{{ author_name }}` in the content.

### Path resolution for content@

The `content@` path is relative to the partial directory. Use `"content@": "content.html"` for a file in the same directory.

## Best practices

1. **Design system thinking** — Build partials as reusable components (callouts, quotes, cards, dividers) that enforce consistent styling across emails.

2. **Keep partials focused** — One partial, one purpose. Avoid monolithic partials that try to handle many use cases.

3. **Use input_schema** — Always define `input_schema` for partials used in the visual block editor so editors get proper form fields instead of raw Liquid.

4. **Email-safe HTML** — Use inline styles and table-based layouts for HTML partials. Avoid external CSS, flexbox, or grid for broad email client support.

5. **Provide defaults** — Use Liquid defaults for optional values: `{{ title | default: "Untitled" }}`.

6. **Discover before creating** — Run `knock partial list` to see existing partials and avoid key collisions.

---



# Workflow templates

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

### Always push after modifying

**Local file changes are not synced to Knock until you push.** Editing files in the knock directory does nothing in Knock until you run the appropriate push command.

```bash
# After modifying a workflow
knock workflow push <workflow-key>

# After modifying other resources
knock email-layout push <layout-key>
knock partial push <partial-key>
knock push --all   # Push everything
```

If you don't push, your changes exist only on disk—Knock will continue using the previous version.

### Channel keys are project-specific

Channel keys (e.g., `knock-email`, `in-app`) are configured per-project. Don't assume keys from schema examples or other projects—they may not exist in your project.

Before creating workflows that use channels:

1. Run `knock channel list` to see available channel keys
2. Use the exact `key` values from the output for `channel_key` in workflow steps

### Workflows do not support guide steps

**Never add guide or message-type steps to a workflow.** Guides and workflows are completely separate systems in Knock:

- **Workflows** send notifications (email, SMS, push, in-app feed, webhook) and use function steps (delay, batch, branch, fetch).
- **Guides** power lifecycle UI (banners, modals, cards) and are configured separately via `knock guide` commands.

There is no `guide` or `message-type` step type in `workflow.json`. If a user asks for in-app lifecycle messaging (announcements, upgrade prompts, onboarding), use guides (`rules/guides-and-message-types.md`), not workflows. If they want in-app notifications (e.g., "Someone commented on your post"), use a workflow with an `in_app_feed` step.

## Email template modes

Knock emails support two mutually exclusive modes: visual blocks and HTML.

**Always use visual blocks for new emails.** When creating a new email step, default to visual blocks mode. Only use HTML mode if the user explicitly requests it.

When modifying an existing email, preserve the current mode unless asked to change it.

### Visual blocks mode (default for new emails)

A structured array of blocks for the email body. Use this for all new emails.

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
        "action": "{{ data.order_url }}",
        "variant": "solid"
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
| `button_set` | One or more buttons (requires `variant` per button) |
| `divider` | Horizontal divider |
| `image` | Image block |
| `html` | Raw HTML block |
| `row` | Multi-column row |

### Button_set: variant requirement

Each button in a `button_set` block must include a `variant` field. Valid values are `solid` and `outline`.

### HTML mode

Raw HTML template when full control is needed. **Do not use HTML mode unless the user explicitly requests it.** Visual blocks should be the default for all new emails.

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

Channel steps use `"type": "channel"` with a `channel_key` and `channel_type`. They send notifications and can have extracted template content in step directories. The `channel_type` values are:

| `channel_type` | Description |
|------|-------------|
| `email` | Email notifications |
| `sms` | SMS text messages |
| `push` | Push notifications |
| `chat` | Chat app messages (Slack, Teams) |
| `in_app_feed` | In-app notification feed |
| `webhook` | Webhook calls |

### Function steps (no template directories)

These step types control workflow logic and never have step directories. Function steps use `settings` (not `template`) for their configuration.

| Type | Description |
|------|-------------|
| `delay` | Wait for a specified time |
| `batch` | Batch multiple triggers |
| `throttle` | Limit notification frequency |
| `branch` | Conditional branching |
| `http_fetch` | Fetch external data via HTTP |
| `trigger_workflow` | Trigger another workflow |
| `update_user` | Update recipient user properties |
| `update_object` | Update an object |
| `update_tenant` | Update tenant properties |
| `update_data` | Update workflow run data |
| `random_cohort` | Randomly assign recipients to cohorts |
| `ai_agent` | AI agent step |

**Important:** The HTTP fetch step type is `http_fetch`, not `fetch`. The API will reject `fetch` as an invalid type.

## Batch steps

Batch steps collect multiple triggers over a time window before continuing. Use them for commenting, likes, or any high-volume activity where you want to send one notification instead of many.

### Batch step configuration

```json
{
  "ref": "batch_comments",
  "type": "batch",
  "name": "Batch comments",
  "settings": {
    "batch_key": "data.content_id",
    "batch_window": {
      "unit": "minutes",
      "value": 5
    },
    "batch_order": "asc"
  }
}
```

| Setting | Description |
|---------|-------------|
| `batch_key` | Data path to group batches (e.g. `data.content_id`). Batches are per-recipient; the key further segments by value. Omit to batch all triggers for a recipient together. |
| `batch_window` | Duration object with `unit` (seconds, minutes, hours, days) and `value` (number) |
| `batch_order` | `"asc"` (first 10 items) or `"desc"` (last 10 items) for which activities appear in templates. Default: `"asc"` |

### Batch variables in templates

After a batch step, these variables are available in subsequent channel step templates:

| Variable | Description |
|----------|-------------|
| `total_activities` | Number of items in the batch |
| `total_actors` | Number of unique actors who triggered the batch |
| `activities` | Array of batched activities (up to 10 by default). Each has `data` and `actor`. |
| `actors` | Array of unique actors (up to 10 by default) |

These are in the workflow run scope—use them directly in Liquid, not under `data.` or `run.`.

### Single vs plural copy

Use `total_activities` and `total_actors` to vary copy for one vs many:

```liquid
{% if total_activities > 1 %}
  **{{ total_actors }} people** left {{ total_activities }} comments on {{ data.content_title | default: 'your content' }}
{% else %}
  **{{ actors[0].name | default: 'Someone' }}** left a comment on {{ data.content_title | default: 'your content' }}
{% endif %}
```

### Accessing per-activity data

Each item in `activities` has its own `data` and `actor`. Use this for per-trigger content:

```liquid
{% for activity in activities %}
  {{ activity.actor.name }}: {{ activity.data.comment_text }}
{% endfor %}
```

### Data after batching

When a batch step runs, `data` is merged from all triggers (last value wins for shared keys). For per-trigger data, reference `activities` instead of `data`. The merged `data` is useful for shared context (e.g. `data.content_url`) that is the same across the batch.

### Using actors for single-activity batches

When `total_activities` is 1, use `actors[0]` with a default:

```liquid
{{ actors[0].name | default: "Someone" }}
```

### Batch variables in conditions

Use `run.total_activities` in branch step conditions to branch on batch size:

```json
{
  "variable": "run.total_activities",
  "operator": "greater_than",
  "argument": 1
}
```

## Branch steps

The `branch` step type enables if/else logic within workflows. It evaluates conditions against the workflow run scope and executes the first branch whose conditions are true. A default branch runs when no other branch matches.

### Branch step JSON structure

**Critical rules:**
- The `branches` array must contain **at least 2 entries** (including the default branch)
- Exactly one branch must have `"default": true` — this is the fallback when no conditions match
- Every non-default branch must have at least one condition
- Maximum 10 branches per branch step (including default)
- Maximum nesting depth of 5 levels for nested branch steps

```json
{
  "name": "Branch by plan type",
  "ref": "plan_branch",
  "type": "branch",
  "branches": [
    {
      "name": "Free plan",
      "ref": "free_plan",
      "conditions": {
        "all": [
          {
            "variable": "recipient.plan_type",
            "operator": "equal_to",
            "argument": "free"
          }
        ]
      },
      "steps": [
        {
          "channel_key": "knock-email",
          "channel_type": "email",
          "name": "Free welcome email",
          "ref": "free_email",
          "template": {
            "settings": { "layout_key": "default" },
            "subject": "Get started with free features",
            "visual_blocks@": "free_email/visual_blocks.json"
          },
          "type": "channel"
        }
      ]
    },
    {
      "name": "Default",
      "ref": "default_branch",
      "default": true,
      "steps": [
        {
          "channel_key": "knock-email",
          "channel_type": "email",
          "name": "Paid welcome email",
          "ref": "paid_email",
          "template": {
            "settings": { "layout_key": "default" },
            "subject": "Getting started with your plan",
            "visual_blocks@": "paid_email/visual_blocks.json"
          },
          "type": "channel"
        }
      ]
    }
  ]
}
```

### Common mistake: Using a separate default_branch key

The default branch must be inside the `branches` array with `"default": true`. Do not use a separate `default_branch` top-level key — the API will reject the payload with "must have at least 2 branches" if only one branch is in the array.

**Wrong:**

```json
{
  "type": "branch",
  "branches": [
    { "name": "Free plan", "ref": "free", "conditions": {...}, "steps": [...] }
  ],
  "default_branch": { "name": "Default", "ref": "default", "steps": [...] }
}
```

**Correct:**

```json
{
  "type": "branch",
  "branches": [
    { "name": "Free plan", "ref": "free", "conditions": {...}, "steps": [...] },
    { "name": "Default", "ref": "default", "default": true, "steps": [...] }
  ]
}
```

### Terminating branches

Each branch can optionally terminate the workflow so no subsequent steps run after the branch. Set `"terminates": true` on the branch:

```json
{
  "name": "Inactive user",
  "ref": "inactive",
  "terminates": true,
  "conditions": { "all": [{ "variable": "recipient.is_active", "operator": "equal_to", "argument": "false" }] },
  "steps": []
}
```

### Steps inside branches

Branches can contain any step type: channel steps, delays, batches, throttles, fetches, and even nested branch steps. Step `ref` values must be unique across the entire workflow, not just within a branch.

## Conditions

Conditions are used in branch steps and step-level conditions to control workflow logic. Each condition compares a `variable` against an `argument` using an `operator`.

### Condition structure

```json
{
  "variable": "recipient.plan_type",
  "operator": "equal_to",
  "argument": "free"
}
```

### Combining conditions

Use `"all"` for AND logic (all must be true) or `"any"` for OR logic (at least one must be true):

```json
{
  "conditions": {
    "all": [
      { "variable": "recipient.plan_type", "operator": "equal_to", "argument": "enterprise" },
      { "variable": "data.priority", "operator": "equal_to", "argument": "high" }
    ]
  }
}
```

```json
{
  "conditions": {
    "any": [
      { "variable": "recipient.plan_type", "operator": "equal_to", "argument": "pro" },
      { "variable": "recipient.plan_type", "operator": "equal_to", "argument": "enterprise" }
    ]
  }
}
```

### Condition variable prefixes

These are the same namespaces used in Liquid templates, but formatted as condition variables:

| Prefix | Description | Example |
|--------|-------------|---------|
| `data.` | Trigger payload property | `data.priority` |
| `recipient.` | Recipient property | `recipient.plan_type` |
| `actor.` | Actor property | `actor.role` |
| `vars.` | Environment variable | `vars.feature_flag` |
| `tenant.` | Tenant property | `tenant.plan` |
| `run.` | Workflow run state | `run.total_activities` |
| `workflow.` | Workflow property | `workflow.categories` |
| `refs.<step_ref>.delivery_status` | Message delivery status | `refs.email_1.delivery_status` |
| `refs.<step_ref>.engagement_status` | Message engagement status | `refs.email_1.engagement_status` |

### Condition operators

| Operator | Description |
|----------|-------------|
| `equal_to` | `==` |
| `not_equal_to` | `!=` |
| `greater_than` | `>` |
| `greater_than_or_equal_to` | `>=` |
| `less_than` | `<` |
| `less_than_or_equal_to` | `<=` |
| `contains` | Argument is in variable (strings and lists) |
| `not_contains` | Argument is not in variable |
| `empty` | Variable is empty/null (no argument needed) |
| `not_empty` | Variable is not empty/null (no argument needed) |

## HTTP fetch steps

The `http_fetch` step executes an HTTP request during a workflow run. The JSON response is shallow-merged into the trigger `data`, making it available to all subsequent steps via `{{ data.<field> }}`.

### Fetch step JSON structure

```json
{
  "name": "Fetch user data",
  "ref": "fetch_user",
  "type": "http_fetch",
  "settings": {
    "method": "get",
    "url": "https://api.example.com/v1/users/{{ recipient.id }}",
    "headers": [
      {
        "key": "Authorization",
        "value": "Bearer {{ vars.api_key }}"
      },
      {
        "key": "Content-Type",
        "value": "application/json"
      }
    ]
  }
}
```

### Settings fields

| Field | Description | Required |
|-------|-------------|----------|
| `method` | HTTP method: `get`, `post`, `put`, `delete`, `patch` | Yes |
| `url` | HTTP URL (supports Liquid) | Yes |
| `headers` | Array of `{ "key": "...", "value": "..." }` maps | No |
| `query_params` | Array of `{ "key": "...", "value": "..." }` maps | No |
| `json_body` | JSON request body for POST/PUT (supports Liquid) | No |

### Common mistakes with fetch steps

**Wrong type name:**

The step type is `http_fetch`, not `fetch`. The API will reject `fetch`.

```json
{ "type": "fetch" }
```

Use:

```json
{ "type": "http_fetch" }
```

**Using `template` instead of `settings`:**

Fetch steps are function steps and use `settings`, not `template`. Only channel steps use `template`.

**Headers as a flat object:**

Headers must be an array of key-value maps, not a flat object.

Wrong:

```json
{ "headers": { "Authorization": "Bearer token" } }
```

Correct:

```json
{ "headers": [{ "key": "Authorization", "value": "Bearer token" }] }
```

### Response data merging

Knock uses a shallow-merge strategy:
- Top-level attributes from the response merge into trigger `data`
- Nested attributes are completely overwritten (not deep-merged)
- Response data overwrites original trigger data for matching keys

You can set a response path in the step settings to place the response at a specific location (e.g., `user_data` would make the response available at `data.user_data`).

### Authentication

Use Knock secret variables (`vars`) for API keys and tokens in headers to keep them obfuscated in the dashboard:

```json
{
  "key": "Authorization",
  "value": "Bearer {{ vars.internal_api_key }}"
}
```

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

**"buttons[0].variant can't be blank" or "variant is invalid"**
- The `button_set` block requires a `variant` field on each button
- Use `solid` or `outline` for the variant value

**"must have at least 2 branches"**
- The `branches` array in a branch step must contain at least 2 entries
- The default branch must be inside the `branches` array with `"default": true`, not as a separate `default_branch` key

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
9. **Discover channel keys** - Run `knock channel list` before creating workflows that use channels; use the returned keys for `channel_key`

---
