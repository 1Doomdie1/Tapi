# ChangeControl

- **Access:** `tines.stories.change_control`
- **Import:** `from tapi.stories import ChangeControl`
- **Part of:** [Stories](stories.md)

The change request of a story that uses change control: create it, view it, and approve, cancel, reject or promote it.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`create`](#create) | Create a change request for a draft. | `POST /api/v1/stories/{story_id}/change_request` |
| [`view`](#view) | View the change request of a story. | `GET /api/v1/stories/{story_id}/change_request/view` |
| [`generate_description`](#generate_description) | Generate a description of a draft. | `GET /api/v1/stories/{story_id}/change_request/ai_description` |
| [`approve`](#approve) | Approve a change request. | `POST /api/v1/stories/{story_id}/change_request/approve` |
| [`cancel`](#cancel) | Cancel a change request. | `POST /api/v1/stories/{story_id}/change_request/cancel` |
| [`reject`](#reject) | Reject a change request. | `POST /api/v1/stories/{story_id}/change_request/reject` |
| [`promote`](#promote) | Promote a change request to the live story. | `POST /api/v1/stories/{story_id}/change_request/promote` |

## Methods breakdown

### `create`

`POST /api/v1/stories/{story_id}/change_request`

Create a change request for a draft.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `title` | `str` | no | — | The name of the change request. |
| `description` | `str` | no | — | A description of the change request. To mention a user, write `<@user-2435>` with the ID of the user. |
| `draft_id` | `int` | no | — | The ID of the draft. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the created change request. |
| 404 | The story does not exist or is not visible to the key. |

### `view`

`GET /api/v1/stories/{story_id}/change_request/view`

View the change request of a story. `change_request` is `null` when none was submitted.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `draft_id` | `int` | no | — | The ID of the draft. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the current change request. |
| 404 | The story does not exist or is not visible to the key. The story has no change control. |

### `generate_description`

`GET /api/v1/stories/{story_id}/change_request/ai_description`

Generate a description of a draft.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `draft_id` | `int` | yes | — | The ID of the draft. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `change_request_ai_description`, the generated text. |
| 404 | The story does not exist or is not visible to the key. The draft does not exist. |

### `approve`

`POST /api/v1/stories/{story_id}/change_request/approve`

Approve a change request.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `change_request_id` | `int` | yes | — | The ID of the change request. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the status of the change request, `APPROVED`. |
| 401 | The key may not approve it: it lacks the change control permissions, or the change request is its own. |
| 404 | The story or the change request does not exist or is not visible to the key. |

### `cancel`

`POST /api/v1/stories/{story_id}/change_request/cancel`

Cancel a change request. When the author cancels it, it goes back to `IN_PROGRESS`.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `change_request_id` | `int` | yes | — | The ID of the change request. |
| `comment` | `str` | no | Up to 1000 characters | Feedback for the author. Only when you are not the author. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` has the `change_request` with its new `status` (`IN_PROGRESS` when the author cancels it, `REJECTED` otherwise) and `comment`, an object with `id`, `message` and `created_at`, or `null`. |
| 400 | `comment` is sent by the author. |
| 401 | The key may not cancel it. |
| 404 | The story or the change request does not exist or is not visible to the key. |
| 422 | The change request is already in progress. |

### `reject`

`POST /api/v1/stories/{story_id}/change_request/reject`

Reject a change request.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `change_request_id` | `int` | yes | — | The ID of the change request. |
| `comment` | `str` | no | Up to 1000 characters | Feedback for the author. Not when you are the author. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` has the `change_request` with its new `status` (`REJECTED`, or `IN_PROGRESS` when the author cancels it) and `comment`, an object with `id`, `message` and `created_at`, or `null`. |
| 400 | `comment` is sent by the author. |
| 401 | The key may not reject it. |
| 404 | The story or the change request does not exist or is not visible to the key. |

### `promote`

`POST /api/v1/stories/{story_id}/change_request/promote`

Promote a change request to the live story.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `change_request_id` | `int` | yes | — | The ID of the change request. |
| `bypass_approval` | `bool` | no | `True`, `False` | Whether to promote a change request that is still pending, skipping its approval. |
| `bypass_approval_reason` | `str` | no | — | The reason recorded in the audit trail. |
| `delete_draft` | `bool` | no | `True`, `False` | Whether to delete the draft after promoting it. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated live story. |
| 404 | The story or the change request does not exist or is not visible to the key. |
