# Workbench

- **Access:** `tines.workbench`
- **Import:** `from tapi.workbench import Workbench`

Workbench and other AI conversations. The module is read only.

Every method returns a [`Response`](../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the conversations, optionally filtered by title, type, creator, favorite or creation time. | `GET /api/v1/workbench` |
| [`get`](#get) | Get a conversation with its usage and its steps. | `GET /api/v1/workbench/{conversation_id}` |

## Methods breakdown

### `list`

`GET /api/v1/workbench`

List the conversations, optionally filtered by title, type, creator, favorite or creation time.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `search` | `str` | no | — | Only conversations whose title matches this text. |
| `favorited` | `bool` | no | `True`, `False` | Only conversations that are favorited (`True`) or that are not (`False`). Every conversation is returned when this is left out. |
| `creator_id` | `int` | no | — | Only conversations created by the user with this ID. |
| `conversation_type` | `ConversationType` | no | `workbench`, `task_agent`, `chat_agent`, `workbench_storyboard` | Only conversations of this type: `workbench`, `task_agent`, `chat_agent` or `workbench_storyboard`. |
| `created_after` | `datetime \| str` | no | ISO 8601 string, or `datetime` | Only conversations created at or after this time. It needs a time, such as `2026-11-01T00:00:00Z`. |
| `created_before` | `datetime \| str` | no | ISO 8601 string, or `datetime` | Only conversations created at or before this time. It needs a time. |
| `per_page` | `int` | no | Positive integer | The number of results per page. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `conversations`, the conversations of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. `conversation_type` or a timestamp is not valid, or `created_after` is not before `created_before`. |

### `get`

`GET /api/v1/workbench/{conversation_id}`

Get a conversation with its usage and its steps.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `conversation_id` | `str` | yes | — | The `guid` of the conversation, as `list` returns it. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the conversation, with the fields of `list` and also `status`, `usage` (token counts and `model_ids`) and `steps`, the messages, each with a `role` of `user`, `assistant` or `tool`. |
| 404 | The conversation does not exist, or the ID is not a GUID. |
