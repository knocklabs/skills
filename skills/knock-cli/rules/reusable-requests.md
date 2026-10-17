---
title: Reusable requests
description: How to create, pull, push, validate, and archive reusable fetch requests with the Knock CLI
tags:
  - knock
  - cli
  - reusable-requests
  - fetch
  - workflows
category: knock-cli
last_updated: 2026-10-17
---

# Reusable requests

## What reusable requests are

A reusable request is a saved HTTP fetch configuration that workflow fetch steps can apply. Updating the reusable request updates every step that uses it. Unlike a goal, a reusable request is a versioned resource: push it, commit it, and promote it the same way you do a workflow.

`knock pull` and `knock push` include reusable requests. Bulk push writes them before workflows, because a workflow fetch step can reference one.

## File structure

With a `knock.json` file, reusable requests live at `<knockDir>/reusable-requests/{key}/reusable_request.json`. The key is the directory name. Pulled files store it under `__readonly.key`.

```json
{
  "name": "Fetch user",
  "description": "Loads a user from the API.",
  "type": "http_fetch",
  "settings": {
    "method": "get",
    "url": "https://example.com/users"
  }
}
```

- `type` is `http_fetch`. That is the only supported type.
- `settings.method` is `get`, `post`, `put`, `delete`, or `patch`.
- `settings` can also include `url`, `body`, `headers`, `query_params`, `response_path`, and `signing_key`.
- `settings.data_input_schema` is an optional JSON Schema for per-workflow inputs. `settings.data_input_values_str` holds preview values as a JSON string.
- `conditions` is optional and decides whether the request runs.
- A key is 3 to 255 characters and uses only lowercase letters, numbers, dashes, or underscores.

## Commands

```bash
knock reusable-request list
knock reusable-request get <key>
knock reusable-request new -k <key> -n "Name" --method=get --url=https://example.com --force
knock reusable-request pull <key> --force
knock reusable-request pull --all --force
knock reusable-request validate <key>
knock reusable-request push <key>
knock reusable-request push <key> --commit -m "Updated fetch user request"
```

`knock reusable-request new` prompts for a name and key unless you pass `-n` and `-k`. It also prompts before writing the directory unless you pass `--force`. `--type` defaults to `http_fetch`, `--method` defaults to `get`, and `--url` defaults to `https://example.com`. Pass `-p` to push after scaffolding.

`knock reusable-request pull` prompts when it creates a new local directory. Pass `--force`. Push and validate do not prompt. Push accepts `--force` to overwrite the remote resource, and `--allow-empty` together with `--commit` for an empty commit of an already published request.

Commit the resource with type `reusable_request`:

```bash
knock commit -m "Updated fetch user request" \
  --resource-type=reusable_request \
  --resource-id=<key> \
  --force
```

Directory overrides require `--all`:

```bash
knock reusable-request pull --all --reusable-requests-dir=./reusable-requests --force
knock reusable-request push --all --reusable-requests-dir=./reusable-requests
```

There is no `knock reusable-request open` command.

## Archive

Archiving a reusable request applies to every environment and cannot be undone. `--environment` is required. When `knock.json` is present and a local directory exists at `<knockDir>/reusable-requests/<key>`, the command deletes that directory so the next `knock push` does not create the request again.

```bash
knock reusable-request archive <key> --environment=development --force
```

`--json` requires `--force`.
