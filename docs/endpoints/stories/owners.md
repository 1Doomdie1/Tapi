# Owners

- **Access:** `tines.stories.owners`
- **Import:** `from tapi.stories import Owners`
- **Part of:** [Stories](stories.md)

The owners of a story.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`add`](#add) | Add an owner to a story. | `POST /api/v1/stories/{story_id}/owners` |
| [`remove`](#remove) | Remove an owner from a story. | `DELETE /api/v1/stories/{story_id}/owners` |

## Methods breakdown

### `add`

`POST /api/v1/stories/{story_id}/owners`

Add an owner to a story.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `user_id` | `int` | yes | — | The ID of the user to add. The user must be a member of the team of the story. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the story, with the new owner in `owners`. |
| 404 | The story does not exist or is not visible to the key. The user does not exist. |

### `remove`

`DELETE /api/v1/stories/{story_id}/owners`

Remove an owner from a story.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `user_id` | `int` | yes | — | The ID of the user to remove. The user must be an owner of the story. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The story does not exist or is not visible to the key. The user does not exist. |
