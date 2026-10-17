---
title: Goals
description: How to create, pull, push, clone, and archive goals with the Knock CLI
tags:
  - knock
  - cli
  - goals
  - attribution
  - workflows
  - guides
category: knock-cli
last_updated: 2026-10-17
---

# Goals

## What goals are

A goal is an environment-scoped outcome Knock measures, such as a trial converting or a recipient entering an audience. Workflows, broadcasts, and guides can attach one goal and an attribution window. Completions are credited to the attached resource that sent the most recent message inside that window.

Read `rules/workflow-templates.md` and `rules/guides-and-message-types.md` for the resources a goal attaches to. The goal itself is a separate directory.

## How goals differ from other resources

Goals do not use the commit and promote model.

- `knock goal push` publishes the goal in the target environment. There is no `--commit` flag, and `knock commit --resource-type=goal` is not valid.
- Goals have no `--branch` flag. Do not create, edit, or attach a goal on a branch.
- Goals are not promoted. Copy a definition into another environment with `knock goal clone`.
- `knock pull` and `knock push` include goals. If goals are not enabled for the account, those commands warn, skip the `goals/` directory, and continue with the other resources.
- `knock push` writes goals before workflows and guides, so an attachment can reference a goal that the same push creates.

## File structure

With a `knock.json` file, goals live at `<knockDir>/goals/{goal-key}/goal.json`. The key is the directory name.

```json
{
  "name": "Trial conversion",
  "description": "Tracks when a trial user converts to paid",
  "condition": {
    "event": {
      "event_type": "integration_source",
      "event_key": "order.completed",
      "integration_source_key": "stripe",
      "recipient_path": "body.userId"
    }
  }
}
```

Editable fields are `name`, optional `description`, and `condition`.

- Integration source events use `event_type: "integration_source"`, plus `event_key`, `integration_source_key`, and `recipient_path`. Optional `match_conditions` refine the event.
- Audience events use `event_type: "audience"`, `event_key` of `enter` or `exit`, and `audience_key`. Audience conditions only work with dynamic audiences.
- A goal key uses only lowercase letters, numbers, dashes, or underscores.
- Pulled files add `__readonly.key` and `$schema`. Leave those in place.

`knock goal new <goal-key>` scaffolds that file. The name is the key, and the condition is an empty integration source event with `recipient_path` set to `body.userId`. The command does not prompt and errors if the directory already exists. It does not push.

## Attaching a goal

Set `goal_attachment` on the workflow or guide, then push that resource and commit it. The goal must already exist in the destination environment with the same key before you promote the workflow or guide.

```json
{
  "goal_attachment": {
    "goal_key": "trial-conversion",
    "attribution_window_days": 7
  }
}
```

`attribution_window_days` is optional and must be from 1 to 30. The default is 7. Each workflow or guide can attach one goal. Broadcasts can attach a goal in the dashboard and Management API. The CLI does not manage broadcasts.

## Commands

```bash
knock goal list
knock goal get <goal-key>
knock goal new <goal-key>
knock goal pull <goal-key> --force
knock goal pull --all --force
knock goal validate <goal-key>
knock goal push <goal-key>
knock goal open <goal-key>
```

`knock goal pull` prompts when it creates a new local directory. Pass `--force` in agent and CI runs. `knock goal push` and `knock goal validate` do not prompt. Push has no `--force` flag.

Directory overrides require `--all`:

```bash
knock goal pull --all --goals-dir=./goals --force
knock goal push --all --goals-dir=./goals
```

## Clone across environments

Cloning copies the goal definition. It does not copy which workflows, broadcasts, or guides reference the goal.

```bash
# Same environment, new key
knock goal clone trial-conversion trial-conversion-copy --force

# Another environment, same key, so attachments still resolve
knock goal clone trial-conversion trial-conversion \
  --environment=development \
  --dest-environment=production \
  --name="Trial conversion" \
  --force
```

`--name` defaults to the new key. `--dest-environment` defaults to `--environment`.

## Archive

Archiving a goal applies to every environment that has that key, stops new completions, and cannot be undone. Detach the goal from every workflow, guide, and broadcast first. Knock refuses the archive while anything is still attached.

```bash
knock goal archive <goal-key> --force
```

`--environment` selects which environment receives the request. The archive still applies to every environment.
