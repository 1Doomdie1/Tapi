# Records: record views

A record view is a saved view of a record type, with its filters, charts and table layout. The views are
a sub-area of [`records`](records.md), available as `tines.records.record_views`, and the class is
`tapi.records.RecordViews`. Every method returns a [`Response`](../responses.md). These routes are under
`/api/v1`, and they answer errors as a list of messages, not as the object of the other record routes.

| Method                                              | HTTP route                                         |
| --------------------------------------------------- | -------------------------------------------------- |
| `list(...)`                                         | `GET /api/v1/record_views`                         |
| `delete(record_view_id=...)`                        | `DELETE /api/v1/record_views/{record_view_id}`     |
| `export(record_view_id=...)`                        | `GET /api/v1/record_views/{record_view_id}/export` |
| `import_(team_id=..., data=...)`                    | `POST /api/v1/record_views/import`                 |

## `list()`

The endpoint is paginated, and one call returns one page; see [Pagination](../pagination.md).

| Parameter        | Type              | Meaning                                                             |
| ---------------- | ----------------- | ------------------------------------------------------------------- |
| `team_id`        | `int`             | Only the views of this team.                                        |
| `record_type_id` | `int`             | Only the views of this record type. One that does not exist is a `404` (`['RecordType not found']`). |
| `order`          | `RecordViewOrder` | `NAME`, `RECENTLY_CREATED` or `RECENTLY_UPDATED`. Tines defaults to `NAME`, also for a value that is not valid. |
| `per_page`       | `int`             | Tines defaults to 20 and caps it at 500.                            |
| `page`           | `int`             | Starting at 1. Tines defaults to 1.                                 |

`data` is an object with `record_views` and `meta`, the pagination details. A view has `id`, `name`, `team`
and `record_type` (each with `id` and `name`), `created_at`, `updated_at`, `report_view` (`record_table`,
`split_view` or `chart`), `url` and `record_report_group_id`.

## `export()` and `import_()`

`export` returns an object with `schema_version`, `export_type` (`record_view`), `exported_at` and
`record_view`. The record view has a `name`, a `report_view`, `elements` and a `layout`. Each element has an
`id`, a `name`, the name of its `record_type_name`, an `element_type` (such as `bar_chart`), `axes`, an
`aggregation`, a date range (`rolling_date_range`, `range_start` and `range_end`), `filters`, `order`,
`color_palette`, `options`, `record_fields` and `test_mode`. Each `layout` entry has an `i` that is the `id`
of the element that it places, with `h`, `w`, `x` and `y`.

| Parameter | Type                   | Meaning                                                                 |
| --------- | ---------------------- | ----------------------------------------------------------------------- |
| `team_id` | `int`                  | The team to add the view to. Required.                                  |
| `data`    | mapping                | The view as `export` returns it, with `schema_version`. Keep the `id` of each element and the `i` of each layout entry. Required. |
| `mode`    | `RecordViewImportMode` | `new`, the default, or `replace`, which replaces the view of the team that has the same name. |
| `name`    | `str`                  | The name of the view. Tines defaults to the name in `data`. With `replace` it picks the view to replace. |

The record types and the story slugs that the view refers to must exist in the team: Tines finds them by
name and does not create them. The reply has a `201` status, and `data` is an object with `id`, `name`,
`team` (`id` and `name`), `created_at` and `updated_at`. A `data` that is not a JSON object, cannot be read
or holds a team that is not valid is a `400`. Importing twice with `new` creates two views.

`delete` has a `204` status, and a view that does not exist is a `404` (`['Record view not found']`).

## What was tried

Everything was run against a tenant: `list` (with `record_type_id`, `order`, `per_page` and `page`),
`export`, `import_` of a view of a throwaway record type, which was `201`, an import of the export under
another `name`, an import with `mode="replace"`, and `delete`, which was `204` and then `404`. A new record
type already has a view, a `split_view` with the name of the type, so a list by `record_type_id` holds it
too. Views and record types that do not exist were a `404`.
