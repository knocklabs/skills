# Batched comments workflow

This workflow batches comments together, waits 5 minutes, then sends an email digest.

## Current flow

1. **Batch** – Collects comments for 5 minutes, grouped by `content_id`
2. **Delay** – Waits 5 minutes
3. **Email** – Sends a digest email with batched comment summary

## Adding in-app notifications

To send an in-app notification when the batch closes (before the 5-minute delay), add an in-app channel step between the batch and delay steps.

1. Configure an in-app feed channel in your Knock dashboard (Developers → Channels)
2. Add this step to `workflow.json` after the `batch_comments` step and before the `delay_5min` step:

```json
{
  "ref": "in_app_1",
  "type": "channel",
  "name": "In-app notification",
  "channel_key": "knock-in-app",
  "channel_type": "in_app_feed",
  "template": {
    "markdown_body": "{% if total_activities > 1 %}**{{ total_actors }} people** left {{ total_activities }} comments on {{ data.content_title | default: 'your content' }}{% else %}**{{ actors[0].name | default: 'Someone' }}** left a comment on {{ data.content_title | default: 'your content' }}{% endif %}",
    "action_url": "{{ data.content_url | default: '' }}"
  }
}
```

Update `channel_key` to match your in-app channel key (e.g. `knock-in-app` or your channel group key).

## Trigger data

When triggering this workflow, pass:

| Field         | Required | Description                                      |
|---------------|----------|--------------------------------------------------|
| `content_id`  | Yes      | ID of the content (used for batch grouping)      |
| `content_title` | No     | Title for display in notifications              |
| `content_url` | No       | URL to view the content                          |

Example trigger:

```javascript
await knock.workflows.trigger("batched-comments", {
  recipients: ["user-123"],
  data: {
    content_id: "post-456",
    content_title: "My awesome post",
    content_url: "https://app.example.com/posts/456"
  },
  actor: "commenter-789"
});
```

## Batch variables

After the batch step, templates have access to:

- `total_activities` – Number of comments in the batch
- `total_actors` – Number of unique commenters
- `activities` – Array of batched activities (up to 10)
- `actors` – Array of unique actors (up to 10)
