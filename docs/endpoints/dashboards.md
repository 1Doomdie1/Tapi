# Dashboards

A dashboard belongs to a team and shows charts and lists of its records and cases. The module is
available as `tines.dashboards`, and the class is `tapi.dashboards.Dashboards`. Every method returns
a [`Response`](../responses.md).

Tines has no endpoint to create or change a dashboard other than `import_`. To copy a dashboard,
`export` it and `import_` the result into a team.

The Tines docs list Dashboards as their own group, and tapi follows that. The OpenAPI document tags
the same routes `Records > Dashboards`.

| Method                       | HTTP route                                       |
| ---------------------------- | ------------------------------------------------ |
| `list(...)`                  | `GET /api/v1/dashboards`                         |
| `delete(dashboard_id=...)`   | `DELETE /api/v1/dashboards/{dashboard_id}`       |
| `export(dashboard_id=...)`   | `GET /api/v1/dashboards/{dashboard_id}/export`   |
| `import_(team_id=..., data=...)` | `POST /api/v1/dashboards/import`             |

## `list()`

Lists the dashboards that the key has access to. The endpoint is paginated, and one call returns one
page; see [Pagination](../pagination.md).

All parameters are optional and keyword-only. Parameters left as `None` are not sent.

| Parameter  | Type  | Meaning                                                                               |
| ---------- | ----- | ------------------------------------------------------------------------------------- |
| `team_id`  | `int` | Only dashboards of this team.                                                         |
| `order`    | `DashboardOrder` | How to order the results. See below.                                       |
| `per_page` | `int` | The number of results per page. Tines defaults to 20 and caps it at 500.              |
| `page`     | `int` | The page to return, starting at 1. Tines defaults to 1.                               |

`DashboardOrder` is `tapi.dashboards.DashboardOrder`:

| Value                   | Order                                    |
| ----------------------- | ---------------------------------------- |
| `NAME`                  | By name. This is the default.            |
| `RECENTLY_EDITED`       | The most recently edited first.          |
| `LEAST_RECENTLY_EDITED` | The least recently edited first.         |
| `CREATED_DESC`          | The newest first.                        |
| `CREATED_ASC`           | The oldest first.                        |

These are the values of the OpenAPI document, and each was checked on dashboards created for the
purpose. The Tines docs give other values, `NAME`, `RECENTLY_CREATED` and `RECENTLY_UPDATED`. Tines
does not know `RECENTLY_CREATED` and `RECENTLY_UPDATED`. It does not refuse them either: as for any
value that is not valid, such as `BOGUS` or `name` in lower case, the reply is `200` with the
dashboards ordered by `NAME`. A mistake in `order` therefore fails silently.

`data` is an object with `dashboards`, the dashboards of the page, and `meta`, the pagination
details. A dashboard has `id`, `name`, `team` (an object with the `id` and `name` of the team),
`created_at` and `updated_at`. `meta` holds `current_page`, `previous_page` and `next_page` (links),
`next_page_number`, `per_page`, `pages` and `count`.

## `delete()`

Deletes a dashboard. The reply has a `204` status and no data. A dashboard that does not exist, or
that was deleted, is a `404` with `['Dashboard not found']`.

| Parameter      | Type  | Meaning                    |
| -------------- | ----- | -------------------------- |
| `dashboard_id` | `int` | The ID of the dashboard.   |

## `export()`

Exports a dashboard as JSON that `import_` takes, to recreate it in another team or tenant.

| Parameter      | Type  | Meaning                    |
| -------------- | ----- | -------------------------- |
| `dashboard_id` | `int` | The ID of the dashboard.   |

`data` is an object with `schema_version` (`1`), `export_type` (`dashboard`), `exported_at` and
`dashboard`. `dashboard` holds the fields below. The tenant had no charts or lists, so the table is
what the Tines docs say about the items:

| Field           | Meaning                                                                                      |
| --------------- | -------------------------------------------------------------------------------------------- |
| `name`          | The name of the dashboard.                                                                   |
| `notes`         | Notes, each with `id`, `name` and `content`.                                                 |
| `case_lists`    | Lists of cases, each with `id`, `name`, `type`, `color_palette`, `filters` and `options`.    |
| `record_charts` | Charts of records, each with `id`, `name`, `record_type_name`, `element_type`, `axes`, `aggregation`, the date range, `filters`, `order`, `color_palette`, `options`, `record_fields` and `test_mode`. |
| `layout`        | The position of each item: `i` (the `id` of the item), `x`, `y`, `w` and `h`.               |

## `import_()`

Creates a dashboard from what `export` returned, or replaces an existing one.

| Parameter  | Type                  | Meaning                                                                          |
| ---------- | --------------------- | -------------------------------------------------------------------------------- |
| `team_id`  | `int`                 | The ID of the team that gets the dashboard. Required.                            |
| `data`     | mapping               | The dashboard in exported form: the reply of `export`. Required.                 |
| `mode`     | `ImportMode`          | `new` to create a dashboard, or `replace` to replace an existing one by name. Tines defaults to `new`. |
| `new_name` | `str`                 | The name of the dashboard. Tines defaults to the name in `data`. In `replace` mode it selects which existing dashboard to replace. |

`ImportMode` is `tapi.dashboards.ImportMode`. The reply has a `201` status, and `data` is the
dashboard with `id`, `name`, `team`, `created_at` and `updated_at`.

What the server does with an import:

- The names of the dashboards of a team are unique. In `new` mode, a name that is taken is a `400`.
- `new_name` wins over the name in `data`.
- In `replace` mode, the dashboard keeps its `id` and its `created_at`, and `updated_at` moves
  when the content changed. A replace with the same content left `updated_at` as it was. A name
  with no dashboard to replace is a `400`.
- Tines gives the notes new IDs when it imports them.
- `data` needs `schema_version` `1` and a `dashboard` with a `name`. `export_type` is not checked:
  a value other than `dashboard` was accepted.

```python
exported = tines.dashboards.export(dashboard_id=7).data
copy = tines.dashboards.import_(team_id=14, data=exported, new_name="Overview (copy)")
```

## Errors

| Status | When                                                                                          |
| ------ | --------------------------------------------------------------------------------------------- |
| `400`  | `import_` with `data` that is not a JSON object (`['data must be a JSON object']`), with no `schema_version` (`['schema_version required']`) or one other than `1` (`['only schema_version value 1 supported']`), with no `dashboard.name` (`['dashboard.name required']`), with a name that the team has in `new` mode (`['dashboard with name ... already exists for team']`), and with no dashboard to replace in `replace` mode (`['dashboard with name "..." not found']`). `list` with a `per_page` or `page` that is not a positive integer (`['Invalid per_page: 0. per_page must be a positive integer.']`). |
| `404`  | `list` or `import_` with a team that does not exist (`['Team not found']`), `import_` with no `team_id` at all (also `['Team not found']`), and `export` or `delete` with a dashboard that does not exist (`['Dashboard not found']`). |
| `422`  | `import_` with a `mode` that is not valid (`['mode value invalid']`).                         |

## Not tried

Everything above was tried on 2026-11-23, with dashboards that were created for the purpose and
deleted afterwards, in a tenant that had none. The dashboards held no charts, lists or layout, so
these were not seen:

- an export of a dashboard with `case_lists`, `record_charts` or a `layout`, and an import of one.
  Their fields come from the Tines docs;
- a key that has access to only some dashboards. The docs say that `list` returns the dashboards
  that the key has access to, and the key used here saw all of them.
