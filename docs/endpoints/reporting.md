# Reporting

- **Access:** `tines.reporting`
- **Import:** `from tapi.reporting import Reporting`

Reports about the tenant: the flow usage of each team and the time saved.

Every method returns a [`Response`](../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`flow_usage`](#flow_usage) | Get the flow usage of the tenant, by team. | `GET /api/v1/reporting/flow_usage` |
| [`time_saved`](#time_saved) | List the time saved, grouped by hour, day, week or month. | `GET /api/v1/reporting/time_saved` |

## Methods breakdown

### `flow_usage`

`GET /api/v1/reporting/flow_usage`

Get the flow usage of the tenant, by team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `per_page` | `int` | no | 1 to 500 | The number of teams per page, at most 500. |
| `page` | `int` | no | Positive integer | The page to return, from 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` has `flows` (`used`, `limit`, `allocated` and `unallocated`), `teams` (each with `id`, `name`, `flows_used`, `flows_allocated` and `flows_available`) and `meta`. |
| 400 | `per_page` or `page` is not a positive integer. The tenant is not on the flows pricing model. |

### `time_saved`

`GET /api/v1/reporting/time_saved`

List the time saved, grouped by hour, day, week or month.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `start_date` | `datetime \| str` | no | ISO 8601 string, or `datetime` | Only records after this time. Pass it to get any records. |
| `end_date` | `datetime \| str` | no | ISO 8601 string, or `datetime` | Only records before this time. |
| `date_unit` | `DateUnit` | no | `hour`, `day`, `week`, `month` | How to group the records: `hour`, `day`, `week` or `month`, in lower case. A value in upper case is not refused, and the reply holds no records. |
| `fill_gaps` | `bool` | no | `True`, `False` | Whether to fill the groups that have no data with a value of 0. `False` is sent, and then only the groups that have data are returned. |
| `team_id` | `int` | no | — | Only records of this team. |
| `story_id` | `int` | no | — | Only records of this story. |
| `action_id` | `int` | no | — | Only records of this action. |
| `per_page` | `int` | no | Positive integer | The number of results per page. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `time_saved`, the records of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. `date_unit` is not valid, or `end_date` is not later than `start_date`. |
| 404 | `team_id`, `story_id` or `action_id` does not exist or is not visible to the key. |
| 422 | A date cannot be read. |
