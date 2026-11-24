# Webhooks

- **Access:** `tines.cases.webhooks`
- **Import:** `from tapi.cases import Webhooks`
- **Part of:** [Cases](cases.md)

The webhooks of a team that Tines calls when its cases change.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the case webhooks, optionally of one team. | `GET /api/v1/case_webhooks` |
| [`get`](#get) | Get a case webhook. | `GET /api/v1/case_webhooks/{webhook_id}` |
| [`create`](#create) | Create a case webhook in a team. | `POST /api/v1/case_webhooks` |
| [`update`](#update) | Change a case webhook. | `PATCH /api/v1/case_webhooks/{webhook_id}` |
| [`delete`](#delete) | Delete a case webhook. | `DELETE /api/v1/case_webhooks/{webhook_id}` |

## Methods breakdown

### `list`

`GET /api/v1/case_webhooks`

List the case webhooks, optionally of one team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | no | — | Only webhooks of this team. |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. Tines defaults to 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `webhooks`, the webhooks of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The team does not exist or is not visible to the key. |

### `get`

`GET /api/v1/case_webhooks/{webhook_id}`

Get a case webhook.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `webhook_id` | `int` | yes | — | The ID of the webhook. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `webhook`. |
| 404 | The webhook does not exist or is not visible to the key. |

### `create`

`POST /api/v1/case_webhooks`

Create a case webhook in a team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | yes | — | The ID of the team that gets the webhook. |
| `url` | `str` | yes | — | The address that Tines sends the requests to. |
| `name` | `str` | no | — | A name to show for the webhook. |
| `notifications` | `Sequence[WebhookNotification]` | no | `ALL`, `CREATED`, `ASSIGNED`, `UNASSIGNED`, `COMMENTED`, `DELETED_COMMENT`, `COMMENT_UPDATED`, `STATUS_UPDATED`, `SUB_STATUS_UPDATED`, `SEVERITY_UPDATED`, `TAGS_ADDED`, `TAGS_REMOVED`, `FILE_ATTACHED`, `FILE_ATTACHED_AND_COMMENTED`, `FILE_DELETED`, `FILE_PASTED`, `CHECKLIST_ITEM_COMPLETED`, `CHECKLIST_ITEM_INCOMPLETE`, `LINKED_CASE_ADDED`, `LINKED_CASE_REMOVED`, `METADATA_UPDATED`, `SLA_WARNING`, `SLA_EXCEEDED`, `TEAM_UPDATED`, `FIELD_UPDATED`, `DESCRIPTION_UPDATED`, `NOTE_ADDED`, `NOTE_UPDATED`, `NOTE_DELETED`, `TITLE_UPDATED`, `TASK_CREATED`, `TASK_DELETED`, `TASK_COMPLETED`, `TASK_INCOMPLETE`, `TASK_UPDATED`, `TASK_ASSIGNED`, `TASK_UNASSIGNED` | The events that trigger the webhook. Tines defaults to `ALL`. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is an object with `webhook`. |
| 404 | The team does not exist or is not visible to the key. |
| 422 | `url` or a notification is not valid. |

### `update`

`PATCH /api/v1/case_webhooks/{webhook_id}`

Change a case webhook.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `webhook_id` | `int` | yes | — | The ID of the webhook. |
| `url` | `str` | no | — | A new address. |
| `name` | `str` | no | — | A new name. |
| `notifications` | `Sequence[WebhookNotification]` | no | `ALL`, `CREATED`, `ASSIGNED`, `UNASSIGNED`, `COMMENTED`, `DELETED_COMMENT`, `COMMENT_UPDATED`, `STATUS_UPDATED`, `SUB_STATUS_UPDATED`, `SEVERITY_UPDATED`, `TAGS_ADDED`, `TAGS_REMOVED`, `FILE_ATTACHED`, `FILE_ATTACHED_AND_COMMENTED`, `FILE_DELETED`, `FILE_PASTED`, `CHECKLIST_ITEM_COMPLETED`, `CHECKLIST_ITEM_INCOMPLETE`, `LINKED_CASE_ADDED`, `LINKED_CASE_REMOVED`, `METADATA_UPDATED`, `SLA_WARNING`, `SLA_EXCEEDED`, `TEAM_UPDATED`, `FIELD_UPDATED`, `DESCRIPTION_UPDATED`, `NOTE_ADDED`, `NOTE_UPDATED`, `NOTE_DELETED`, `TITLE_UPDATED`, `TASK_CREATED`, `TASK_DELETED`, `TASK_COMPLETED`, `TASK_INCOMPLETE`, `TASK_UPDATED`, `TASK_ASSIGNED`, `TASK_UNASSIGNED` | The events that trigger the webhook. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `webhook`. |
| 404 | The webhook does not exist or is not visible to the key. |
| 422 | `url` or a notification is not valid. |

### `delete`

`DELETE /api/v1/case_webhooks/{webhook_id}`

Delete a case webhook.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `webhook_id` | `int` | yes | — | The ID of the webhook. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The webhook does not exist or is not visible to the key. |
