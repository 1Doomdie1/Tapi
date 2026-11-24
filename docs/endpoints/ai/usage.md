# Usage

- **Access:** `tines.ai.usage`
- **Import:** `from tapi.ai import Usage`
- **Part of:** [AI](ai.md)

The AI usage of the tenant: the totals of a time window, optionally split by model, provider, team, feature, story, user, action or day.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`get`](#get) | Get the AI usage of the tenant, totaled for a time window. | `GET /api/v1/ai_usage` |

## Methods breakdown

### `get`

`GET /api/v1/ai_usage`

Get the AI usage of the tenant, totaled for a time window.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `relative_date` | `str` | no | `today`, `yesterday`, or a count and a unit (`day`, `week`, `month`, `year`), such as `7 days` | A window relative to now. Do not combine it with `start_date` or `end_date`. Without any of the three, the last 30 days are used. |
| `start_date` | `datetime \| str` | no | ISO 8601 string, or `datetime` | The start of a custom window. Needs `end_date`. |
| `end_date` | `datetime \| str` | no | ISO 8601 string, or `datetime` | The end of the custom window: after `start_date` and at most one year later. |
| `team_id` | `int` | no | — | Only usage of this team. |
| `model_id` | `str` | no | — | Only usage of this model. |
| `provider_id` | `int` | no | — | Only usage of this AI provider. |
| `feature` | `Feature` | no | `workbench`<br>`workbench_storyboard`<br>`ai_agents`<br>`workbench_cases`<br>`workbench_apps`<br>`other` | Only usage of this feature. |
| `story_id` | `int` | no | — | Only runtime usage of AI actions and agents in this story. |
| `user_id` | `int` | no | — | Only usage started by this user. |
| `action_id` | `int` | no | — | Only runtime usage of this AI action or agent. |
| `group_by` | `GroupBy` | no | `model`<br>`provider`<br>`team`<br>`feature`<br>`story`<br>`user`<br>`action`<br>`day` | Split the usage by this key. Without it, only the totals are returned. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` has `range`, `totals` and, with `group_by`, `groups`. |
| 400 | The window is not valid (`relative_date` with a date, a single date, a date that cannot be read, a window over one year), `feature` is not valid, or AI usage is unavailable on the tenant. |
