# Drafts

- **Access:** `tines.stories.drafts`
- **Import:** `from tapi.stories import Drafts`
- **Part of:** [Stories](stories.md)

The drafts of a story that uses change control.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the drafts of a story. | `GET /api/v1/stories/{story_id}/drafts` |
| [`create`](#create) | Create a draft of a story. | `POST /api/v1/stories/{story_id}/drafts` |
| [`delete`](#delete) | Delete a draft of a story. | `DELETE /api/v1/stories/{story_id}/drafts/{draft_id}` |

## Methods breakdown

### `list`

`GET /api/v1/stories/{story_id}/drafts`

List the drafts of a story.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `drafts`, the drafts of the page, and `meta`, the pagination details. |
| 404 | The story does not exist or is not visible to the key. |
| 422 | The story has no change control. |

### `create`

`POST /api/v1/stories/{story_id}/drafts`

Create a draft of a story.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `name` | `str` | yes | — | The name of the draft. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the created draft. |
| 404 | The story does not exist or is not visible to the key. |
| 422 | The story already has a draft with that name. |

### `delete`

`DELETE /api/v1/stories/{story_id}/drafts/{draft_id}`

Delete a draft of a story.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `draft_id` | `int` | yes | — | The ID of the draft to delete. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The story is not visible to the key, or the draft does not belong to it. |
