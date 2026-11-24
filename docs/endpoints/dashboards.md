# Dashboards

- **Access:** `tines.dashboards`
- **Import:** `from tapi.dashboards import Dashboards`

Dashboards of the tenant: list them, delete them, and export and import them.

Every method returns a [`Response`](../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the dashboards, optionally of one team. | `GET /api/v1/dashboards` |
| [`delete`](#delete) | Delete a dashboard. | `DELETE /api/v1/dashboards/{dashboard_id}` |
| [`export`](#export) | Export a dashboard in a form that `import_` takes. | `GET /api/v1/dashboards/{dashboard_id}/export` |
| [`import_`](#import_) | Import a dashboard into a team, as a new one or in place of one with the same name. | `POST /api/v1/dashboards/import` |

## Methods breakdown

### `list`

`GET /api/v1/dashboards`

List the dashboards, optionally of one team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | no | — | Only dashboards of this team. |
| `order` | `DashboardOrder` | no | `NAME`<br>`RECENTLY_EDITED`<br>`LEAST_RECENTLY_EDITED`<br>`CREATED_DESC`<br>`CREATED_ASC` | How to order the results: `NAME` (the default), `RECENTLY_EDITED` (the latest edit first), `LEAST_RECENTLY_EDITED`, `CREATED_DESC` (the newest first) or `CREATED_ASC`. |
| `per_page` | `int` | no | Positive integer | The number of results per page. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `dashboards`, the dashboards of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | `team_id` does not exist. |

### `delete`

`DELETE /api/v1/dashboards/{dashboard_id}`

Delete a dashboard.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `dashboard_id` | `int` | yes | — | The ID of the dashboard. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The dashboard does not exist. |

### `export`

`GET /api/v1/dashboards/{dashboard_id}/export`

Export a dashboard in a form that `import_` takes.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `dashboard_id` | `int` | yes | — | The ID of the dashboard. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `schema_version` (1), `export_type` (`dashboard`), `exported_at` and `dashboard`. |
| 404 | The dashboard does not exist. |

### `import_`

`POST /api/v1/dashboards/import`

Import a dashboard into a team, as a new one or in place of one with the same name.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | yes | — | The ID of the team that gets the dashboard. |
| `data` | `Mapping[str, Any]` | yes | — | The dashboard in exported form: what `export` returned. Tines needs a `schema_version` of 1 and a `dashboard` object with a `name`. |
| `mode` | `ImportMode` | no | `new`, `replace` | `new` to create a dashboard or `replace` to replace an existing one by name. A replaced dashboard keeps its ID and its creation time. |
| `new_name` | `str` | no | — | The name of the dashboard. In `replace` mode, it selects which existing dashboard to replace. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the dashboard. |
| 400 | `data` is not a valid export (not an object, no `schema_version` or one other than `1`, no `dashboard.name`), the name exists in `new` mode, or there is nothing to replace in `replace` mode. |
| 404 | `team_id` is missing or does not exist. |
| 422 | `mode` is not valid. |
