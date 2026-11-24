# Groups

- **Access:** `tines.stories.groups`
- **Import:** `from tapi.stories import Groups`
- **Part of:** [Stories](stories.md)

The runs of a group: list them and list the events of one.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list_runs`](#list_runs) | List the runs of a group. | `GET /api/v1/groups/{group_id}/runs` |
| [`list_run_events`](#list_run_events) | List the events of a group run. | `GET /api/v1/groups/{group_id}/runs/{group_run_guid}` |

## Methods breakdown

### `list_runs`

`GET /api/v1/groups/{group_id}/runs`

List the runs of a group.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `group_id` | `int` | yes | — | The ID of the group. |
| `per_page` | `int` | no | Positive integer | The number of results per page. Tines defaults to 20 and caps it at 500. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. Tines defaults to 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `group_runs`, the runs of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The group does not exist or is not visible to the key. |

### `list_run_events`

`GET /api/v1/groups/{group_id}/runs/{group_run_guid}`

List the events of a group run.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `group_id` | `int` | yes | — | The ID of the group. |
| `group_run_guid` | `str` | yes | — | The guid of the group run. |
| `per_page` | `int` | no | Positive integer | The number of results per page. Tines defaults to 20 and caps it at 500. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. Tines defaults to 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `group_run_events`, a list of objects with `id`, `action_id` (the action that emitted the event), `created_at` and `is_reemitted`, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The group does not exist or is not visible to the key. |
