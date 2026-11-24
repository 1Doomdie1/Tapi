# Notes

- **Access:** `tines.stories.notes`
- **Import:** `from tapi.stories import Notes`
- **Part of:** [Stories](stories.md)

The notes on the storyboard of a story.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the notes, optionally of a story, a team, a group or a draft. | `GET /api/v1/notes` |
| [`get`](#get) | Get a note. | `GET /api/v1/notes/{note_id}` |
| [`create`](#create) | Create a note in a story or a group. | `POST /api/v1/notes` |
| [`update`](#update) | Update a note. | `PATCH /api/v1/notes/{note_id}` |
| [`delete`](#delete) | Delete a note. | `DELETE /api/v1/notes/{note_id}` |

## Methods breakdown

### `list`

`GET /api/v1/notes`

List the notes, optionally of a story, a team, a group or a draft.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | no | — | Only notes of this story. |
| `mode` | `StoryMode` | no | `TEST`, `LIVE` | Only notes of the story in this mode. Use it with `story_id`. |
| `team_id` | `int` | no | — | Only notes of this team. |
| `group_id` | `int` | no | — | Only notes of this group. |
| `draft_id` | `int` | no | — | Only notes of this draft. |
| `per_page` | `int` | no | Positive integer | The number of results per page. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `annotations`, the notes of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The story does not exist or is not visible to the key. |

### `get`

`GET /api/v1/notes/{note_id}`

Get a note.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `note_id` | `int` | yes | — | The ID of the note to retrieve. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the note. |
| 404 | The note does not exist or is not visible to the key. |

### `create`

`POST /api/v1/notes`

Create a note in a story or a group.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | no | — | The ID of the story. Send `story_id` or `group_id`. |
| `group_id` | `int` | no | — | The ID of the group. Send `story_id` or `group_id`. |
| `content` | `str` | yes | Up to 8000 characters | The content of the note, as Markdown. |
| `position` | [`NotePosition`](#noteposition) | no | — | The coordinates of the note on the diagram. Without it the note is at `{"x": 0, "y": 0}`. |
| `draft_id` | `int` | no | — | The ID of the draft the note is added to. Needs change control. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the created note. |
| 404 | Neither a story nor a group is given, or one of them does not exist. |
| 422 | `content` is missing, not text or too long, `position` is not two integers, or `draft_id` is used without change control. |

### `update`

`PATCH /api/v1/notes/{note_id}`

Update a note.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `note_id` | `int` | yes | — | The ID of the note to update. |
| `content` | `str` | no | Up to 8000 characters | The new content of the note, as Markdown. |
| `position` | [`NotePosition`](#noteposition) | no | — | The new coordinates of the note. Send both `x` and `y`. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated note. |
| 404 | The note does not exist or is not visible to the key. |
| 422 | `content` is not text or too long, or `position` is not two integers. |

### `delete`

`DELETE /api/v1/notes/{note_id}`

Delete a note.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `note_id` | `int` | yes | — | The ID of the note to delete. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The note does not exist or is not visible to the key. |

## Types

### `NotePosition`

The coordinates of a note on the story diagram.

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `x` | `int` | yes | — | The horizontal coordinate. |
| `y` | `int` | yes | — | The vertical coordinate. |
