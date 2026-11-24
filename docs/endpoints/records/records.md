# Records

- **Access:** `tines.records`
- **Import:** `from tapi.records import Records`

Records store structured data in record types. Create, read, update, delete, search and aggregate records, link them to cases, and read their child records.

Every method returns a [`Response`](../../responses.md).

## Sub-endpoints

| Class | Access | Description |
| --- | --- | --- |
| [`Artifacts`](artifacts.md) | `tines.records.artifacts` | The artifacts of a record. |
| [`Fields`](fields.md) | `tines.records.fields` | The large fields of a record. |
| [`RecordTypes`](record_types.md) | `tines.records.record_types` | The record types: the schema of a kind of record. |
| [`RecordViews`](record_views.md) | `tines.records.record_views` | The record views: saved tables and charts of a record type. |

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`create`](#create) | Create a record in a record type. | `POST /api/v2/records` |
| [`get`](#get) | Get a record, optionally with its record type, parent, children or cases. | `GET /api/v2/records/{record_id}` |
| [`update`](#update) | Change the field values or the parent of a record. | `PATCH /api/v2/records/{record_id}` |
| [`delete`](#delete) | Delete a record. | `DELETE /api/v2/records/{record_id}` |
| [`search`](#search) | Search the records of a record type with a filter, a sort and cursor pagination. | `POST /api/v2/records/search` |
| [`aggregate`](#aggregate) | Compute counts, sums, averages and other aggregations of the records of a record type, optionally grouped. | `POST /api/v2/records/aggregate` |
| [`list_cases`](#list_cases) | List the cases that are linked to a record. | `GET /api/v2/records/{record_id}/cases` |
| [`link_case`](#link_case) | Link a case to a record. | `POST /api/v2/records/{record_id}/cases` |
| [`unlink_case`](#unlink_case) | Unlink a case from a record. | `DELETE /api/v2/records/{record_id}/cases/{case_id}` |
| [`list_child_record_ids`](#list_child_record_ids) | List the IDs of the child records of a record. | `GET /api/v2/records/{record_id}/child_record_ids` |
| [`list_child_records`](#list_child_records) | List the child records of a record. | `GET /api/v2/records/{record_id}/child_records` |

## Methods breakdown

### `create`

`POST /api/v2/records`

Create a record in a record type.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `record_type_id` | `int` | no | — | The ID of the record type. Send this or `record_type_name`. |
| `record_type_name` | `str` | no | — | The name or the slug of the record type. |
| `field_values` | [`Sequence[FieldValue]`](#fieldvalue) | no | — | The values of the fields. A field can appear once, and a `value` of `None` clears it. |
| `parent_id` | `int` | no | — | The ID of the parent record. Leave it out for a top-level record. |
| `test_mode` | `bool` | no | `True`, `False` | `True` creates a test record, which needs change control. |
| `idempotency_key` | `str` | no | Up to 255 characters | A key that makes the create safe to retry. The same key with the same body replays the first reply. Sent in the `Idempotency-Key` header. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is an object with `data`, the record, and `field_ids`. |
| 400 | The request is not valid, or neither record type argument is sent. |
| 403 | The tenant has no access to records, the key may not create records, or `test_mode` is used without change control. |
| 404 | The record type or the parent does not exist. |
| 408 | The write timed out. Retry it. |
| 409 | A retry with the same `idempotency_key` while the first request is still running. |
| 422 | The same `idempotency_key` was used with another body. |

### `get`

`GET /api/v2/records/{record_id}`

Get a record, optionally with its record type, parent, children or cases.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `record_id` | `int` | yes | — | The ID of the record. |
| `record_type_id` | `int` | no | — | Only a record of this type. |
| `include` | `Sequence[RecordInclude]` | no | `record_type`, `parent_record`, `child_records`, `child_record_ids`, `cases` | What to embed in the reply. |
| `expand` | `Sequence[str]` | no | — | The JSON and artifact fields to inline, such as `fields.payload`, or `fields.*` for all of them. |
| `fields` | `Sequence[str]` | no | — | The slugs of the fields to return, instead of all of them. |
| `timezone` | `str` | no | IANA timezone name | The timezone of the timestamps. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `data`, the record, `field_ids` and, with `include`, `included`. |
| 400 | `include`, `expand`, `fields` or `timezone` is not valid. |
| 403 | The tenant has no access to records, or the key may not read them. |
| 404 | The record does not exist or the key cannot see it. |

### `update`

`PATCH /api/v2/records/{record_id}`

Change the field values or the parent of a record.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `record_id` | `int` | yes | — | The ID of the record. |
| `field_values` | [`Sequence[FieldValue]`](#fieldvalue) | no | — | The values to set. A `value` of `None` clears the field. |
| `parent_id` | `int` | no | — | The ID of the new parent record. |
| `test_mode` | `bool` | no | `True`, `False` | A guard: `True` requires a test record and `False` a live record. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `data`, the updated record, and `field_ids`. |
| 400 | The request is not valid, or it changes nothing. |
| 403 | The tenant has no access to records, or the key may not change them. |
| 404 | The record does not exist or the key cannot see it. |
| 408 | The write timed out. Retry it. |
| 422 | `test_mode` does not match the record. |

### `delete`

`DELETE /api/v2/records/{record_id}`

Delete a record.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `record_id` | `int` | yes | — | The ID of the record. |
| `test_mode` | `bool` | no | `True`, `False` | A guard: `True` requires a test record and `False` a live record. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 403 | The tenant has no access to records, or the key may not delete them. |
| 404 | The record does not exist or the key cannot see it. |
| 408 | The write timed out. Retry it. |
| 422 | `test_mode` does not match the record. |

### `search`

`POST /api/v2/records/search`

Search the records of a record type with a filter, a sort and cursor pagination.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `record_type_id` | `int` | no | — | The ID of the record type. Send this or `record_type_name`. |
| `record_type_name` | `str` | no | — | The name or the slug of the record type. |
| `filter` | [`RecordFilterNode`](#recordfilternode) | no | — | A condition or a group of conditions, up to 4 levels and 50 nodes. |
| `sort` | [`Sequence[RecordSort]`](#recordsort) | no | — | The sort keys, in priority order. Without it the newest records come first. |
| `fields` | `Sequence[str]` | no | — | The slugs of the fields to return. |
| `include` | `Sequence[RecordSearchInclude]` | no | `record_type`, `parent_record` | What to add under `included`. |
| `ids` | `Sequence[int]` | no | Up to 500 record IDs | Only these records. Not with `after`. |
| `time_range` | [`Sequence[RecordTimeRange]`](#recordtimerange) | no | — | At most two windows, one for each time field. |
| `timezone` | `str` | no | IANA timezone name | The timezone of the timestamps. |
| `limit` | `int` | no | 1 to 500 | The number of records in a page. |
| `after` | `str` | no | — | The `page.next_page_token` of the previous page. |
| `include_total` | `bool` | no | `True`, `False` | `True` adds `page.total`. |
| `test_mode` | `bool` | no | `True`, `False` | `True` searches test records, which needs change control. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` has `data` (the records), `field_ids`, `page` and `applied`, and `included` with `include`. |
| 400 | The request is not valid: an unknown field or timezone, a filter that is too large, or neither record type argument. |
| 403 | The tenant has no access to records, or the key may not read them. |
| 404 | The record type does not exist. |

### `aggregate`

`POST /api/v2/records/aggregate`

Compute counts, sums, averages and other aggregations of the records of a record type, optionally grouped.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `aggregations` | [`Sequence[RecordAggregation]`](#recordaggregation) | yes | — | The values to compute, one to five. |
| `record_type_id` | `int` | no | — | The ID of the record type. Send this or `record_type_name`. |
| `record_type_name` | `str` | no | — | The name or the slug of the record type. |
| `group_by` | [`Sequence[RecordGroupBy]`](#recordgroupby) | no | — | The fields to group by, up to two. |
| `filter` | [`RecordFilterNode`](#recordfilternode) | no | — | A condition or a group of conditions, as for `search`. |
| `time_range` | [`Sequence[RecordTimeRange]`](#recordtimerange) | no | — | At most two windows, as for `search`. |
| `order_by` | [`Sequence[RecordOrderBy]`](#recordorderby) | no | — | How to order the rows, at most one key. |
| `parent_ids` | `Sequence[int]` | no | Up to 100 record IDs | Only the direct children of these records are counted. |
| `timezone` | `str` | no | IANA timezone name | The timezone of the timestamps. |
| `limit` | `int` | no | 1 to 500 | The number of rows. Without it Tines returns up to 1000. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` has `rows` and `meta` (`row_count`, `truncated` and `columns`). |
| 400 | The request is not valid. |
| 403 | The tenant has no access to records, or the key may not read them. |
| 404 | The record type does not exist. |

### `list_cases`

`GET /api/v2/records/{record_id}/cases`

List the cases that are linked to a record.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `record_id` | `int` | yes | — | The ID of the record. |
| `timezone` | `str` | no | IANA timezone name | The timezone of the timestamps. |
| `limit` | `int` | no | 1 to 500 | The number of cases in a page. |
| `after` | `str` | no | — | The `page.next_page_token` of the previous page. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `data`, the cases, each with `id` (the case number), `name`, `status`, `priority`, `linked_at`, `created_at` and `updated_at`, and `page`. |
| 403 | The tenant has no access to records, or the key may not read them. |
| 404 | The record does not exist or the key cannot see it. |

### `link_case`

`POST /api/v2/records/{record_id}/cases`

Link a case to a record.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `record_id` | `int` | yes | — | The ID of the record. |
| `case_id` | `int` | yes | — | The number of the case. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The record or the case does not exist. |
| 408 | The write timed out. Retry it. |
| 422 | The case cannot be linked, for example without permission to manage records. |

### `unlink_case`

`DELETE /api/v2/records/{record_id}/cases/{case_id}`

Unlink a case from a record.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `record_id` | `int` | yes | — | The ID of the record. |
| `case_id` | `int` | yes | — | The number of the case. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The record or the case does not exist. |
| 408 | The write timed out. Retry it. |

### `list_child_record_ids`

`GET /api/v2/records/{record_id}/child_record_ids`

List the IDs of the child records of a record.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `record_id` | `int` | yes | — | The ID of the parent record. |
| `limit` | `int` | no | 1 to 500 | The number of IDs in a page. Tines defaults to 20. |
| `after` | `str` | no | — | The `page.next_page_token` of the previous page. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `data`, a list of integers, and `page`. |
| 404 | The record does not exist or the key cannot see it. |

### `list_child_records`

`GET /api/v2/records/{record_id}/child_records`

List the child records of a record.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `record_id` | `int` | yes | — | The ID of the parent record. |
| `timezone` | `str` | no | IANA timezone name | The timezone of the timestamps. Tines defaults to `UTC`. |
| `limit` | `int` | no | 1 to 500 | The number of records in a page. Tines defaults to 20. |
| `after` | `str` | no | — | The `page.next_page_token` of the previous page. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `data`, the child records, and `page`. |
| 404 | The record does not exist or the key cannot see it. |

## Types

### `FieldValue`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `value` | `Any` | yes | — | The value. `None` clears the field. A scalar field takes a string, a number, a boolean or an ISO 8601 string, and a JSON field takes any JSON. |
| `field_id` | `int` | no | — | The ID of the field. Send `field_id` or `field_name`, not both. |
| `field_name` | `str` | no | — | The name of the field. Send `field_id` or `field_name`, not both. |

### `RecordFilterNode`

One of: [`RecordFilterCondition`](#recordfiltercondition), [`RecordFilterGroup`](#recordfiltergroup).

### `RecordFilterCondition`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `operator` | `FilterOperator` | yes | `EQUAL`, `NOT_EQUAL`, `GREATER_THAN`, `GREATER_THAN_OR_EQUAL_TO`, `LESS_THAN`, `LESS_THAN_OR_EQUAL_TO`, `IS_ANY_OF`, `IS_NONE_OF`, `CONTAINS`, `STARTS_WITH`, `ENDS_WITH`, `IS_EMPTY`, `IS_NOT_EMPTY`, `IS_TRUE`, `IS_FALSE`, `IS_IN_ANY_CIDR`, `IS_NOT_IN_ANY_CIDR` | The comparison. |
| `field_id` | `int` | no | — | The ID of the field. Send `field_id` or `field_name`. |
| `field_name` | `str` | no | — | The name of the field. Send `field_id` or `field_name`. |
| `value` | `Any` | no | — | The value to compare with. Not for `IS_EMPTY`, `IS_NOT_EMPTY`, `IS_TRUE` or `IS_FALSE`. |

### `RecordFilterGroup`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `op` | `str` | yes | `AND` | How the nodes combine. |
| `nodes` | [`Sequence[RecordFilterNode]`](#recordfilternode) | yes | — | The conditions and groups of the group. |

### `RecordSort`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `field_id` | `int` | no | — | The ID of the field. Send `field_id` or `field_name`. |
| `field_name` | `str` | no | — | The name of the field. Send `field_id` or `field_name`. |
| `direction` | `SortDirection` | no | `ASC`, `DESC` | The direction of the sort. |

### `RecordTimeRange`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `field` | `TimeRangeField` | no | `created_at`, `updated_at` | The timestamp that the window applies to. One window for each. |
| `rolling_date_range` | `RollingDateRange` | no | `TODAY`<br>`YESTERDAY`<br>`LAST_7_DAYS`<br>`LAST_31_DAYS`<br>`LAST_365_DAYS`<br>`ALL_TIME` | A window relative to now. Or send `range_start` and `range_end`. |
| `range_start` | `datetime \| str` | no | — | The start of a custom window: an ISO 8601 string or a `datetime`. |
| `range_end` | `datetime \| str` | no | — | The end of a custom window: an ISO 8601 string or a `datetime`. |

### `RecordAggregation`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `fn` | `AggregationFunction` | yes | `COUNT`<br>`SUM`<br>`AVG`<br>`MIN`<br>`MAX`<br>`MEDIAN`<br>`P90`<br>`P95`<br>`P99` | The function to compute. |
| `field_id` | `int` | no | — | The ID of the field. Not for `COUNT`. |
| `field_name` | `str` | no | — | The name of the field. Not for `COUNT`. |
| `alias` | `str` | no | — | The name of the value in the rows. |

### `RecordGroupBy`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `field_id` | `int` | no | — | The ID of the field. Send `field_id` or `field_name`. |
| `field_name` | `str` | no | — | The name of the field. Send `field_id` or `field_name`. |
| `date_trunc` | `DateTrunc` | no | `hour`<br>`day`<br>`week`<br>`month`<br>`year` | For a timestamp field: the size of the bucket. |

### `RecordOrderBy`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `field_id` | `int` | no | — | A group-by field. Send one of `field_id`, `field_name` and `alias`. |
| `field_name` | `str` | no | — | A group-by field. Send one of `field_id`, `field_name` and `alias`. |
| `alias` | `str` | no | — | The alias of an aggregation. |
| `direction` | `SortDirection` | no | `ASC`, `DESC` | The direction of the order. |
