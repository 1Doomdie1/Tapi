# Recipients

- **Access:** `tines.stories.recipients`
- **Import:** `from tapi.stories import Recipients`
- **Part of:** [Stories](stories.md)

The monitoring recipients of a story: the addresses that receive its monitoring messages.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`add`](#add) | Add a recipient to a story. | `POST /api/v1/stories/{story_id}/recipients` |
| [`remove`](#remove) | Remove a recipient from a story. | `DELETE /api/v1/stories/{story_id}/recipients` |

## Methods breakdown

### `add`

`POST /api/v1/stories/{story_id}/recipients`

Add a recipient to a story.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `address` | `str` | yes | — | The email address or webhook URL that receives the messages. |
| `draft_id` | `int` | no | — | The ID of the draft to update. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the story, with the new recipient in `recipients`. |
| 404 | The story does not exist or is not visible to the key. |

### `remove`

`DELETE /api/v1/stories/{story_id}/recipients`

Remove a recipient from a story.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `address` | `str` | yes | — | The email address or webhook URL to remove. |
| `draft_id` | `int` | no | — | The ID of the draft to update. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | No data. |
| 404 | The story does not exist or is not visible to the key. The address is not a recipient of the story. |
