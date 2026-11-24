# Statuses

- **Access:** `tines.cases.statuses`
- **Import:** `from tapi.cases import Statuses`
- **Part of:** [Cases](cases.md)

The case statuses of a team. Each status is under `OPEN` or `CLOSED`.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the case statuses of a team. | `GET /api/v1/case_sub_statuses` |
| [`get`](#get) | Get a case status. | `GET /api/v1/case_sub_statuses/{status_id}` |
| [`create`](#create) | Create a case status in a team. | `POST /api/v1/case_sub_statuses` |
| [`update`](#update) | Change a case status. | `PATCH /api/v1/case_sub_statuses/{status_id}` |
| [`delete`](#delete) | Delete a case status. | `DELETE /api/v1/case_sub_statuses/{status_id}` |

## Methods breakdown

### `list`

`GET /api/v1/case_sub_statuses`

List the case statuses of a team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | yes | — | The ID of the team. |
| `parent_status` | `CaseStatus` | no | `OPEN`, `CLOSED` | Only statuses under this one. |
| `search` | `str` | no | — | Only statuses whose name contains this text, in any case. |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `case_sub_statuses`, the statuses of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The team does not exist or is not visible to the key. |

### `get`

`GET /api/v1/case_sub_statuses/{status_id}`

Get a case status.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `status_id` | `int` | yes | — | The ID of the status. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the status. |
| 404 | The status does not exist or is not visible to the key. |

### `create`

`POST /api/v1/case_sub_statuses`

Create a case status in a team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | yes | — | The ID of the team that gets the status. |
| `name` | `str` | yes | — | The name of the status. |
| `parent_status` | `CaseStatus` | no | `OPEN`, `CLOSED` | The status that this one is under. Tines defaults to `OPEN`. |
| `description` | `str` | no | — | A description of the status. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the created status. |
| 404 | The team does not exist or is not visible to the key. |
| 422 | `parent_status` is not valid, or the team already has a status with that name. |

### `update`

`PATCH /api/v1/case_sub_statuses/{status_id}`

Change a case status.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `status_id` | `int` | yes | — | The ID of the status. |
| `name` | `str` | no | — | A new name. The slug changes with it. |
| `description` | `str` | no | — | A new description. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated status. |
| 404 | The status does not exist or is not visible to the key. |

### `delete`

`DELETE /api/v1/case_sub_statuses/{status_id}`

Delete a case status. The cases that have it move to the fallback status.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `status_id` | `int` | yes | — | The ID of the status. |
| `fallback_status_id` | `int` | yes | — | The status that the cases with the deleted one move to. It must be under the same parent status. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 400 | `fallback_status_id` is missing. |
| 404 | The status or the fallback status does not exist. |
| 422 | The fallback status is not valid. |
