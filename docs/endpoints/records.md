# Records

A record is one row of a record type, with a value for each field of the type. The module is
available as `tines.records`, and the class is `tapi.records.Records`. Every method returns a
[`Response`](../responses.md). The record types and the record views are sub-areas with their own
pages, [Records: record types](records_record_types.md) and
[Records: record views](records_record_views.md). The module has two more sub-areas, `fields` and
`artifacts`, described below.

| Method                                                  | HTTP route                                                  |
| ------------------------------------------------------- | ----------------------------------------------------------- |
| `create(...)`                                           | `POST /api/v2/records`                                      |
| `get(record_id=...)`                                    | `GET /api/v2/records/{record_id}`                           |
| `update(record_id=...)`                                 | `PATCH /api/v2/records/{record_id}`                         |
| `delete(record_id=...)`                                 | `DELETE /api/v2/records/{record_id}`                        |
| `search(...)`                                           | `POST /api/v2/records/search`                               |
| `aggregate(aggregations=...)`                           | `POST /api/v2/records/aggregate`                            |
| `list_cases(record_id=...)`                             | `GET /api/v2/records/{record_id}/cases`                     |
| `link_case(record_id=..., case_id=...)`                 | `POST /api/v2/records/{record_id}/cases`                    |
| `unlink_case(record_id=..., case_id=...)`               | `DELETE /api/v2/records/{record_id}/cases/{case_id}`        |
| `list_child_record_ids(record_id=...)`                  | `GET /api/v2/records/{record_id}/child_record_ids`          |
| `list_child_records(record_id=...)`                     | `GET /api/v2/records/{record_id}/child_records`             |
| `fields.get(record_id=..., field=...)`                  | `GET /api/v2/records/{record_id}/fields/{field}`            |
| `artifacts.get(record_id=..., artifact_id=...)`         | `GET /api/v1/records/{record_id}/artifacts/{artifact_id}`   |

## The record

`data` of `create`, `get` and `update`, and the items of the lists, are records.

| Field           | Meaning                                                                                     |
| --------------- | ------------------------------------------------------------------------------------------- |
| `id`            | The ID of the record.                                                                       |
| `fields`        | An object with the value of each field, keyed by its slug, or `field_<id>` when two fields share a slug. Timestamps are ISO 8601 strings. |
| `relationships` | `record_type` with its `id`, and `parent_record` with its `id`, or `null`. With `include`, also `child_record_ids` and the flags `truncated` of `child_records` and `cases`. |
| `created_at`, `updated_at` | ISO 8601, in UTC unless a `timezone` was sent.                                   |

`JSON` and `ARTIFACT` fields are not inlined. Each is a handle, `{"expandable": true, "href":
"/api/v2/records/<id>/fields/<field_id>"}`, which `fields.get` follows, or which `expand` inlines. Next
to `data`, a reply has `field_ids`, an object that maps each slug to the immutable ID of its field.
Errors have the form `{"error": {"type": ..., "message": ...}}`, with `field` and `hint` when they
apply. A `403` means that the tenant has no access to records, or that the key may not do the
operation, and a `404` can also mean that the key cannot see the resource.

## `create()`

| Parameter          | Type                  | Meaning                                                                 |
| ------------------ | --------------------- | ----------------------------------------------------------------------- |
| `record_type_id`   | `int`                 | The record type. Send this or `record_type_name`. The ID wins.          |
| `record_type_name` | `str`                 | The name or the slug of the record type. A name that matches two types is a `400`. |
| `field_values`     | sequence of `FieldValue` | Objects with `value` and either `field_id` or `field_name`, never both. A field can appear once. A `value` of `None` clears it. |
| `parent_id`        | `int`                 | The parent record. Left out for a top-level record.                     |
| `test_mode`        | `bool`                | `True` creates a test record, which needs change control. Tines defaults to `False`. |
| `idempotency_key`  | `str`                 | At most 255 characters, sent in the `Idempotency-Key` header. See below. |

The reply has a `201` status, and `data` is an object with `data` (the record) and `field_ids`. Scalar
fields take a string, a number or a boolean, a timestamp takes an ISO 8601 string, a `JSON` field takes
an object or an array, and an `ARTIFACT` field takes a text. A timestamp with an offset is converted to
UTC, and one without an offset is stored as written, so send `Z`.

With an `idempotency_key`, a create is safe to retry. The same key and the same body replay the first
reply. The same key with another body is a `422` (`idempotency_key_reuse`), a retry while the first
request is still running is a `409` (`idempotency_in_progress`), and a replay after the record was
deleted is a `410`. A key expires after 24 hours.

## `get()`

| Parameter        | Type                         | Meaning                                                             |
| ---------------- | ---------------------------- | ------------------------------------------------------------------- |
| `record_id`      | `int`                        | The record. Required.                                               |
| `record_type_id` | `int`                        | Only a record of this type. A record of another type is a `404`.    |
| `include`        | sequence of `RecordInclude`  | `record_type`, `parent_record`, `child_records`, `child_record_ids` and `cases`, sent as one comma-separated value. |
| `expand`         | sequence of `str`            | The `JSON` and `ARTIFACT` fields to inline, such as `fields.payload` or `fields.*`, sent as one comma-separated value. |
| `fields`         | sequence of `str`            | The slugs of the fields to return, sent as one comma-separated `fields[record]`. |
| `timezone`       | `str`                        | An IANA timezone name. Tines defaults to `UTC`.                     |

`data` is an object with `data`, `field_ids` and, with `include`, `included`: `record_type` is a list with
the `id`, `name` and `slug` of the type, and `child_records` and `cases` hold at most 20 items each. A
case has `id` (its number), `name`, `status`, `priority`, `linked_at`, `created_at` and `updated_at`. An
unknown field, `include`, `expand` or `timezone` is a `400`.

## `update()` and `delete()`

`update` takes `record_id`, `field_values` and `parent_id`, which are all that the request may set, and
`test_mode`. What is left out stays. A request that sets no field value and no `parent_id` is a `400`,
and an empty `field_values` is accepted only with `parent_id`. Tines detaches a record from its parent
for a `parent_id` of `null`, which tapi cannot send. `data` is an object with `data` and `field_ids`.
The reply is a `422` when the record type is not editable, a value is not valid, the new parent would
make a cycle or `test_mode` does not match.

`delete` takes `record_id` and `test_mode`, and has a `204` status. `test_mode` is a guard for both: `True`
requires a test record and `False` a live record, and a record of the other mode is a `422`. A write
that takes too long is a `408`, and can be retried.

## `search()`

The request reads records, although it is a `POST`. An unknown key in the body is a `400`.

| Parameter          | Type                           | Meaning                                                           |
| ------------------ | ------------------------------ | ----------------------------------------------------------------- |
| `record_type_id`, `record_type_name` | `int`, `str` | The record type. One of them is required.                         |
| `filter`           | `RecordFilterNode`             | A condition or a group. See below.                                |
| `sort`             | sequence of `RecordSort`       | Keys in priority order, each with `field_id` or `field_name`, and a `direction`, `ASC` by default. `created_at` is a `field_name` for the creation time. Without it, the newest records come first. |
| `fields`           | sequence of `str`              | The slugs of the fields to return.                                |
| `include`          | sequence of `RecordSearchInclude` | `record_type`. `parent_record` changes nothing.                |
| `ids`              | sequence of `int`              | At most 500 record IDs. Not with `after`. Without `limit`, all of them come back in one page. |
| `time_range`       | sequence of `RecordTimeRange`  | At most two windows, one for each of `created_at` and `updated_at`. |
| `timezone`         | `str`                          | An IANA timezone name for the presets and the timestamps.         |
| `limit`            | `int`                          | From 1 to 500. Tines defaults to 20, or to the number of `ids`.   |
| `after`            | `str`                          | The `page.next_page_token` of the previous page. The sort of the first request is kept. |
| `include_total`    | `bool`                         | `True` adds `page.total`.                                         |
| `test_mode`        | `bool`                         | `True` searches test records, which needs change control.         |

A condition is `{"field_name": "Status", "operator": "EQUAL", "value": "open"}`, with a `field_id` in
place of a `field_name` if you like. A group is `{"op": "AND", "nodes": [...]}`, and it can nest, up to
4 levels and 50 nodes in all. `value` is a list for `IS_ANY_OF`, `IS_NONE_OF`, `IS_IN_ANY_CIDR` and
`IS_NOT_IN_ANY_CIDR`, it is left out for `IS_EMPTY`, `IS_NOT_EMPTY`, `IS_TRUE` and `IS_FALSE`, and it is
one value for the others. Which operators a field takes depends on its type:

| Operators                                                                   | Field types                                                    |
| --------------------------------------------------------------------------- | -------------------------------------------------------------- |
| `EQUAL`, `NOT_EQUAL`                                                        | text, enum, regex, email, URL, IP address, number, timestamp   |
| `GREATER_THAN`, `GREATER_THAN_OR_EQUAL_TO`, `LESS_THAN`, `LESS_THAN_OR_EQUAL_TO` | number, timestamp                                         |
| `IS_ANY_OF`, `IS_NONE_OF`                                                   | text, enum, regex, email, URL, IP address, number              |
| `CONTAINS`, `STARTS_WITH`, `ENDS_WITH`                                      | text, enum, regex, email, URL, IP address                      |
| `IS_EMPTY`, `IS_NOT_EMPTY`                                                  | all but `JSON` and `ARTIFACT`                                  |
| `IS_TRUE`, `IS_FALSE`                                                       | boolean                                                        |
| `IS_IN_ANY_CIDR`, `IS_NOT_IN_ANY_CIDR`                                      | IP address                                                     |

`JSON` and `ARTIFACT` fields cannot be filtered, and IP address, `JSON` and `ARTIFACT` fields cannot be
sorted. A field name matches in any case and with any separator, but stops matching when the field is
renamed, so a `field_id` is safer.

A time range window has a `field` (`created_at` by default, or `updated_at`), and either a
`rolling_date_range` (`TODAY`, `YESTERDAY`, `LAST_7_DAYS`, `LAST_31_DAYS`, `LAST_365_DAYS` or `ALL_TIME`)
or `range_start` and `range_end`, which are inclusive and take a `datetime` or an ISO 8601 string. A
naive `datetime` is treated as UTC.

`data` is an object with `data` (the records of the page), `field_ids`, `included` with `include`,
`page` (`next_page_token` when there is another page, and `total`) and `applied`, which holds the
`filter` and the `sort` as the server read them, with field IDs. A `503` means that search is not
available: retry, or start again from the first page.

## `aggregate()`

The request reads records, although it is a `POST`, and it does not page.

| Parameter          | Type                            | Meaning                                                           |
| ------------------ | ------------------------------- | ----------------------------------------------------------------- |
| `aggregations`     | sequence of `RecordAggregation` | One to five values to compute. Required.                          |
| `record_type_id`, `record_type_name` | `int`, `str`  | The record type. One of them is required.                         |
| `group_by`         | sequence of `RecordGroupBy`     | Up to two fields. Without it there is one row.                    |
| `filter`           | `RecordFilterNode`              | A condition or a group, as for `search`.                          |
| `time_range`       | sequence of `RecordTimeRange`   | At most two windows, as for `search`.                             |
| `order_by`         | sequence of `RecordOrderBy`     | At most one key.                                                  |
| `parent_ids`       | sequence of `int`               | At most 100 record IDs: only their direct children are counted.   |
| `timezone`         | `str`                           | An IANA timezone name for the buckets and the time ranges.        |
| `limit`            | `int`                           | From 1 to 500. Without it Tines returns up to 1000 rows.          |

An aggregation has an `fn`, one of `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `MEDIAN`, `P90`, `P95` and `P99`,
a `field_id` or `field_name` for every function but `COUNT`, and an `alias`. All the functions but `COUNT`
need a number field. A group-by entry has a `field_id` or `field_name`, and a `date_trunc` (`hour`, `day`,
`week`, `month` or `year`) for a timestamp. An order key is a group-by field or an `alias`, with a
`direction`.

`data` is an object with `rows`, flat objects with a key for each group-by field and each aggregation
(`COUNT` is an integer, and the other values are strings), and `meta` with `row_count`, `truncated`
(true when more than 1000 rows matched and `limit` was left out) and `columns`. A query that takes more
than 30 seconds is a `504`.

## Cases and child records

- `list_cases(record_id=..., timezone=..., limit=..., after=...)` returns `data`, the cases, oldest
  first, and `page`.
- `link_case(record_id=..., case_id=...)` and `unlink_case(record_id=..., case_id=...)` have a `204`
  status. Neither is an error when the case is linked or unlinked already, and neither deletes the record
  or the case. `case_id` is the number of the case. A case that cannot be linked is a `422`, for example
  for a key that may add records to cases but not manage records.
- `list_child_record_ids(record_id=..., limit=..., after=...)` returns `data`, the IDs of every direct
  child, newest first, also of children that the key cannot read, and `page`.
- `list_child_records(record_id=..., timezone=..., limit=..., after=...)` returns `data`, the child
  records, newest first, and `page`. Children in a record type that the key cannot access are left out.

## `fields` and `artifacts`

- `fields.get(record_id=..., field=..., format=...)` reads a `JSON` or `ARTIFACT` field. `field` is its ID,
  its name or its slug. The reply has no envelope: `data` is the parsed JSON for `json`, and a `str` for
  `text`, `txt` and `plain`. Tines defaults to `json` for a `JSON` field and `text` for a text artifact. A
  field that is not stored as an artifact is a `400`, and one without a value is a `404`.
- `artifacts.get(record_id=..., artifact_id=...)` returns an object with `id`, `value`, `record_field`
  (its `id` and `name`), `created_at` and `updated_at`. Its errors are a list of messages.

## Errors

| Status | When                                                                                          |
| ------ | --------------------------------------------------------------------------------------------- |
| `400`  | A body or a query that is not valid, an unknown parameter, field or timezone, an unknown `include`, or neither record type. |
| `403`  | The tenant has no access to records, the key may not do the operation, or `test_mode` without change control. |
| `404`  | A record, a record type, a team or an artifact that does not exist, or that the key cannot see (`{"error": {"type": "not_found", "message": "Record not found"}}`). |
| `408`  | A write timed out. Retry it.                                                                  |
| `409`, `410`, `422` | See `create`, `update` and `delete`.                                              |
| `503`, `504` | Search is not available, or an aggregation took more than 30 seconds.                   |

## What was tried

Everything was run against a tenant, with a throwaway record type and a throwaway case, except a
successful `artifacts.get`: it was seen only with an ID that does not exist (`404`, `['Record artifact
not found']`), because the ID of an artifact is not in any reply that was seen.

- `create` with the `Idempotency-Key`: the same key and body replayed the first record, and the same key
  with another body was a `422`. A child record was created with `parent_id` and `test_mode=False`. A
  create without a record type is a `400`, one with a type that does not exist is a `404`, and a text in
  a number field is a `422`.
- `get` with `include`, `expand`, `fields` and `timezone`, and with a `record_type_id` that does not match
  (`404`). `fields.get` returned the text of an artifact by ID and by slug, and a field that is not an
  artifact (`status`) was a `400`.
- `update` set values, cleared a field with a `value` of `None`, and was a `400` for an empty
  `field_values` without a `parent_id`. A `test_mode=True` for a live record was a `422`.
- `search` with a group of conditions, sorting, `fields`, `include`, a `time_range` from a `datetime`,
  `include_total`, paging with `after` and `ids`. A cursor that is not valid is a `400`. `aggregate` with
  `COUNT` and `SUM`, grouping and ordering, and an empty `aggregations` (`400`).
- `link_case` and `unlink_case` were `204` twice in a row, and `list_cases` followed them. The lists of
  the child record IDs and the child records held the child.
- `delete` was `204`, and a second one was a `404`.
