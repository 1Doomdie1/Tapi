# RecordViews

- **Access:** `tines.records.record_views`
- **Import:** `from tapi.records import RecordViews`
- **Part of:** [Records](records.md)

The record views: saved tables and charts of a record type.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the record views, optionally of one team or one record type. | `GET /api/v1/record_views` |
| [`delete`](#delete) | Delete a record view. | `DELETE /api/v1/record_views/{record_view_id}` |
| [`export`](#export) | Export a record view in a form that `import_` takes. | `GET /api/v1/record_views/{record_view_id}/export` |
| [`import_`](#import_) | Import a record view into a team. | `POST /api/v1/record_views/import` |

## Methods breakdown

### `list`

`GET /api/v1/record_views`

List the record views, optionally of one team or one record type.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | no | — | Only the views of this team. |
| `record_type_id` | `int` | no | — | Only the views of this record type. |
| `order` | `RecordViewOrder` | no | `NAME`, `RECENTLY_CREATED`, `RECENTLY_UPDATED` | How to order the views. Tines defaults to `NAME`. |
| `per_page` | `int` | no | Positive integer | The number of results per page. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `record_views`, the views of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | `record_type_id` does not exist. |

### `delete`

`DELETE /api/v1/record_views/{record_view_id}`

Delete a record view.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `record_view_id` | `int` | yes | — | The ID of the record view. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The record view does not exist. |

### `export`

`GET /api/v1/record_views/{record_view_id}/export`

Export a record view in a form that `import_` takes.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `record_view_id` | `int` | yes | — | The ID of the record view. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `schema_version`, `export_type` (`record_view`), `exported_at` and `record_view`, which has `name`, `report_view`, `elements` (each with an `id` and the settings of a chart or a table) and `layout` (each entry has an `i` that is the `id` of its element). |
| 404 | The record view does not exist. |

### `import_`

`POST /api/v1/record_views/import`

Import a record view into a team. The record types that it uses must exist in the team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | yes | — | The team to add the view to. |
| `data` | `Mapping[str, Any]` | yes | — | The view in the form that `export` returns, with `schema_version`. Keep the `id` of each element and the `i` of each layout entry. |
| `mode` | `RecordViewImportMode` | no | `new`, `replace` | Whether to create a view or replace one of the team that has the same name. Tines defaults to `new`. |
| `name` | `str` | no | — | The name of the view. With `replace` it picks the view to replace. Tines defaults to the name in `data`. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is an object with `id`, `name`, `team` (with `id` and `name`), `created_at` and `updated_at`. |
| 400 | `data` is not a JSON object, cannot be read, or holds a team that is not valid. |
| 404 | The team or a record type of the view does not exist. |
