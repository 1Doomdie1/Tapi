# Records: record types

A record type defines the fields of its records and how long Tines keeps them. The record types are a
sub-area of [`records`](records.md), available as `tines.records.record_types`, and the class is
`tapi.records.RecordTypes`. Every method returns a [`Response`](../responses.md).

**Be careful with `delete`.** It deletes the record type with all its records, their artifacts and the
record views built on it, and it cannot be undone.

| Method                                    | HTTP route                                       |
| ----------------------------------------- | ------------------------------------------------ |
| `list(...)`                               | `GET /api/v2/record_types`                       |
| `get(record_type_id=...)`                 | `GET /api/v2/record_types/{record_type_id}`      |
| `create(name=..., team_id=..., fields=...)` | `POST /api/v2/record_types`                    |
| `update(record_type_id=...)`              | `PATCH /api/v2/record_types/{record_type_id}`    |
| `delete(record_type_id=...)`              | `DELETE /api/v2/record_types/{record_type_id}`   |

## The record type

`data` of `get`, `create` and `update`, and the items of `list`, are record types.

| Field                    | Meaning                                                                          |
| ------------------------ | -------------------------------------------------------------------------------- |
| `id`, `name`, `slug`     | The ID, the name and the URL-safe slug.                                          |
| `description`            | A description, or `null`.                                                        |
| `editable`               | Whether the records of the type can be edited.                                   |
| `ttl_days`               | How long Tines keeps a record, in days, or `null` for ever.                      |
| `retention_column_name`  | The timestamp that `ttl_days` counts from: `CREATED_AT` or `UPDATED_AT`.         |
| `on_limit_reached`       | `REJECT` or `EVICT_OLDEST`.                                                      |
| `custom_records_limit`   | The limit that was set, or `null`.                                               |
| `effective_max_records`, `has_custom_limit` | The limit that applies, and whether it is a custom one. Tines computes them. |
| `relationships`          | `team` with its `id`.                                                            |
| `created_at`, `updated_at` | ISO 8601, in UTC.                                                              |
| `fields`                 | The fields, ordered by ID. See below.                                            |

A field has `id` (which stays the same when it is renamed), `name`, `slug`, `result_type`,
`fixed_values` (the values of a `TEXT_ENUM`), `description` (or `null`) and `config` (`regex` of a
`TEXT_REGEX`, `disable_hyperlink` of a `URL`, and an empty object otherwise). `result_type` is one of
`TEXT`, `TEXT_ENUM`, `TEXT_REGEX`, `EMAIL`, `URL`, `IP_ADDRESS`, `NUMBER`, `BOOLEAN`, `TIMESTAMP`, `JSON`
and `ARTIFACT`. A `URL` takes HTTP, HTTPS and FTP links with a host, and an `IP_ADDRESS` takes one IPv4 or
IPv6 address, not a range.

## `list()`

| Parameter   | Type              | Meaning                                                                  |
| ----------- | ----------------- | ------------------------------------------------------------------------ |
| `team_id`   | `int`             | Only the record types that this team can read. A team that does not exist is a `404`. |
| `order`     | `RecordTypeOrder` | `NAME`, `CREATED_AT` or `UPDATED_AT`, in any case. Tines defaults to `NAME`. |
| `direction` | `SortDirection`   | `ASC` or `DESC`, in any case. Tines defaults to `ASC`.                   |
| `limit`     | `int`             | From 1 to 500. Tines defaults to 20.                                     |
| `after`     | `str`             | The `page.next_page_token` of the previous page.                         |

`data` is an object with `data`, the record types, and `page`, which has `next_page_token` only when there
is another page.

## `create()`

| Parameter               | Type                         | Meaning                                                   |
| ----------------------- | ---------------------------- | --------------------------------------------------------- |
| `name`                  | `str`                        | The name. Required.                                       |
| `team_id`               | `int`                        | The team that owns it. Required.                          |
| `fields`                | sequence of `RecordTypeField` | The custom fields, at most 50. Required.                 |
| `description`           | `str`                        | A description.                                            |
| `editable`              | `bool`                       | Tines defaults to `False`.                                |
| `ttl_days`              | `float`                      | One of 0.25, 0.5, 1, 2, 3, 7, 14, 30, 60, 90, 180, 365, 548, 730, 1095, 1460, 1825, 2190, 2555, 2920, 3285 and 3650. Without it records are kept for ever. |
| `retention_column_name` | `RetentionColumn`            | `CREATED_AT`, the default, or `UPDATED_AT`.               |
| `on_limit_reached`      | `OnLimitReached`             | `REJECT`, the default, or `EVICT_OLDEST`.                 |
| `custom_records_limit`  | `int`                        | A positive integer, at most the limit of the tenant.      |

A field definition has a `name` and a `result_type`, and optionally a `description`, `fixed_values` and a
`config`. A `TEXT_ENUM` needs `fixed_values`, at most 100, and no other type takes them. A `TEXT_REGEX`
needs `config` with a `regex`, which cannot be changed afterwards. A `URL` takes `disable_hyperlink` in
`config` to show its values as plain text. The reply has a `201` status.

## `update()`

`update` takes `record_type_id` and any of `name`, `description`, `editable`, `ttl_days`,
`retention_column_name`, `on_limit_reached` and `custom_records_limit`, as `create` does, and two more:

| Parameter             | Type                                | Meaning                                                  |
| --------------------- | ----------------------------------- | -------------------------------------------------------- |
| `fields`              | sequence of `RecordTypeFieldChange` | The fields to add and to change. A field with an `id` is changed, and one without is added, with a `name` and a `result_type`. The fields that are not listed stay. A `config` replaces the old one. |
| `field_ids_to_delete` | sequence of `int`                   | The IDs of the fields to delete. The built-in fields cannot be deleted. |

What is left out stays as it is, and the request must change something: an empty body, an empty `fields`
or `field_ids_to_delete`, and a field entry that has only an `id` are a `400`. A field ID can appear once,
and not in both lists. Tines clears the description, turns retention off and drops the custom limit for a
`null`, which tapi cannot send.

## `delete()`

`delete` has a `204` status. A record type that does not exist, or that the key cannot see, is a `404`.

## Errors

| Status | When                                                                                          |
| ------ | --------------------------------------------------------------------------------------------- |
| `400`  | A request that changes nothing, an unknown parameter, or an `order`, `direction`, `limit` or `after` that is not valid (`{"error": {"type": "bad_request", "message": "direction must be one of: ASC, DESC", "field": "direction"}}`). |
| `403`  | The tenant has no access to records, or the key may not do it in the team.                    |
| `404`  | A record type or a team that does not exist, or that the key cannot see.                      |
| `408`  | A write timed out. Retry it.                                                                  |
| `422`  | `create` or `update` that Tines cannot carry out, such as a `result_type` that is not valid.  |

## What was tried

Everything was run against a tenant, with a throwaway record type: `create` with every parameter,
`get`, `list` (with `team_id`, `order`, `direction` and `limit`), `update`, which changed the description,
the retention, the limits, a field, added a field and deleted one, and `delete`, which was `204`. An
`update` that changes nothing was a `400`, and a `result_type` that does not exist was a `422`. Record
types and teams that do not exist were a `404`. A new record type gets a view of its own, a `split_view`
with the name of the type, which `delete` removes with the type.
