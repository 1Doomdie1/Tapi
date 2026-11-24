# ChangeRequests

- **Access:** `tines.change_requests`
- **Import:** `from tapi.change_requests import ChangeRequests`

Change requests across stories: list them and read one. The operations on the change request of one story are in `stories.change_control`.

Every method returns a [`Response`](../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the change requests, optionally of some teams or statuses. | `GET /api/v1/change_requests` |
| [`get`](#get) | Get a change request, with the exports of the live story and the draft. | `GET /api/v1/change_requests/{change_request_id}` |

## Methods breakdown

### `list`

`GET /api/v1/change_requests`

List the change requests, optionally of some teams or statuses.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_ids` | `Sequence[int]` | no | — | Only change requests of stories in these teams. |
| `statuses` | `Sequence[ChangeRequestStatus]` | no | `PENDING`<br>`APPROVED`<br>`REJECTED`<br>`PUSHED`<br>`IN_PROGRESS` | Only change requests with one of these statuses. Without it, every status except `PUSHED` is returned. |
| `per_page` | `int` | no | Positive integer | The number of results per page. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `change_requests`, the change requests of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | A team does not exist or the key cannot access it. |
| 422 | A status is not valid. It is case-sensitive. |

### `get`

`GET /api/v1/change_requests/{change_request_id}`

Get a change request, with the exports of the live story and the draft.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `change_request_id` | `int` | yes | — | The ID of the change request. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the change request, with the fields that `list` returns and also `live_story_export` and `draft_export`, each a string that holds the JSON export of a story. |
| 404 | The change request does not exist or is not visible to the key. |
