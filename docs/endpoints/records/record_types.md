# RecordTypes

- **Access:** `tines.records.record_types`
- **Import:** `from tapi.records import RecordTypes`
- **Part of:** [Records](records.md)

The record types: the schema of a kind of record, with its fields, its retention and its limits.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the record types, optionally of one team. | `GET /api/v2/record_types` |
| [`get`](#get) | Get a record type with its fields. | `GET /api/v2/record_types/{record_type_id}` |
| [`create`](#create) | Create a record type. | `POST /api/v2/record_types` |
| [`update`](#update) | Change a record type: its settings, and the fields to add, change or delete. | `PATCH /api/v2/record_types/{record_type_id}` |
| [`delete`](#delete) | Delete a record type, with its records and views. | `DELETE /api/v2/record_types/{record_type_id}` |

## Methods breakdown

### `list`

`GET /api/v2/record_types`

List the record types, optionally of one team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | no | — | Only the record types that this team can read. |
| `order` | `RecordTypeOrder` | no | `NAME`, `CREATED_AT`, `UPDATED_AT` | How to order the record types. Tines defaults to `NAME`. |
| `direction` | `SortDirection` | no | `ASC`, `DESC` | The direction of the order. Tines defaults to `ASC`. |
| `limit` | `int` | no | 1 to 500 | The number of record types in a page. Tines defaults to 20. |
| `after` | `str` | no | — | The `page.next_page_token` of the previous page. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `data`, the record types of the page, and `page`, which has `next_page_token` only when there is another page. |
| 400 | `order`, `direction`, `limit` or `after` is not valid. |
| 403 | The tenant has no access to records. |
| 404 | `team_id` does not exist or the key cannot see it. |

### `get`

`GET /api/v2/record_types/{record_type_id}`

Get a record type with its fields.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `record_type_id` | `int` | yes | — | The ID of the record type. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `data`, the record type. |
| 403 | The tenant has no access to records. |
| 404 | The record type does not exist or the key cannot see it. |

### `create`

`POST /api/v2/record_types`

Create a record type. A new type also gets a view of its own.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `name` | `str` | yes | — | The name of the record type. |
| `team_id` | `int` | yes | — | The ID of the team that owns it. |
| `fields` | [`Sequence[RecordTypeField]`](#recordtypefield) | yes | — | The custom fields of the type, at most 50. |
| `description` | `str` | no | — | A description. |
| `editable` | `bool` | no | `True`, `False` | Whether the records of the type can be edited. |
| `ttl_days` | `float` | no | 0.25, 0.5, 1, 2, 3, 7, 14, 30, 60, 90, 180, 365, 548, 730, 1095, 1460, 1825, 2190, 2555, 2920, 3285, 3650 | How long Tines keeps a record, in days. Without it records are kept for ever. |
| `retention_column_name` | `RetentionColumn` | no | `CREATED_AT`, `UPDATED_AT` | The timestamp that `ttl_days` counts from. Tines defaults to `CREATED_AT`. |
| `on_limit_reached` | `OnLimitReached` | no | `REJECT`, `EVICT_OLDEST` | What Tines does when the limit of records is reached. Tines defaults to `REJECT`. |
| `custom_records_limit` | `int` | no | Positive integer, up to the limit of the tenant | The most records the type can hold. Without it the limit of the tenant applies. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is an object with `data`, the record type. |
| 400 | The request is not valid. |
| 403 | The tenant has no access to records, or the key may not create record types in the team. |
| 404 | `team_id` does not exist. |
| 408 | The write timed out. Retry it. |
| 422 | Tines cannot carry it out, for example a `result_type` that is not valid. |

### `update`

`PATCH /api/v2/record_types/{record_type_id}`

Change a record type: its settings, and the fields to add, change or delete.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `record_type_id` | `int` | yes | — | The ID of the record type. |
| `name` | `str` | no | — | The new name. |
| `description` | `str` | no | — | The new description. |
| `editable` | `bool` | no | `True`, `False` | Whether the records of the type can be edited. |
| `ttl_days` | `float` | no | 0.25, 0.5, 1, 2, 3, 7, 14, 30, 60, 90, 180, 365, 548, 730, 1095, 1460, 1825, 2190, 2555, 2920, 3285, 3650 | How long Tines keeps a record, in days. |
| `retention_column_name` | `RetentionColumn` | no | `CREATED_AT`, `UPDATED_AT` | The timestamp that `ttl_days` counts from. |
| `on_limit_reached` | `OnLimitReached` | no | `REJECT`, `EVICT_OLDEST` | What Tines does when the limit of records is reached. |
| `custom_records_limit` | `int` | no | Positive integer, up to the limit of the tenant | The most records the type can hold. |
| `fields` | [`Sequence[RecordTypeFieldChange]`](#recordtypefieldchange) | no | — | The fields to add and to change. A field with an `id` is changed and one without is added. The fields that are not listed stay. |
| `field_ids_to_delete` | `Sequence[int]` | no | — | The IDs of the fields to delete. The built-in fields cannot be deleted. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `data`, the record type. |
| 400 | The request changes nothing or is not valid. |
| 403 | The tenant has no access to records, or the key may not change the type. |
| 404 | The record type does not exist or the key cannot see it. |
| 408 | The write timed out. Retry it. |
| 422 | Tines cannot carry it out, for example a `result_type` that is not valid. |

### `delete`

`DELETE /api/v2/record_types/{record_type_id}`

Delete a record type, with its records and views.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `record_type_id` | `int` | yes | — | The ID of the record type. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 403 | The tenant has no access to records, or the key may not delete the type. |
| 404 | The record type does not exist or the key cannot see it. |
| 408 | The write timed out. Retry it. |

## Types

### `RecordTypeField`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `name` | `str` | yes | — | The name of the field. |
| `result_type` | `FieldResultType` | yes | `TEXT`<br>`TEXT_ENUM`<br>`TEXT_REGEX`<br>`EMAIL`<br>`URL`<br>`IP_ADDRESS`<br>`NUMBER`<br>`BOOLEAN`<br>`TIMESTAMP`<br>`JSON`<br>`ARTIFACT` | The type of the field. |
| `fixed_values` | `Sequence[str]` | no | — | The allowed values of a `TEXT_ENUM` field, at most 100. No other type takes them. |
| `description` | `str` | no | — | A description of the field. |
| `config` | `Mapping[str, Any]` | no | — | Settings of the field. A `TEXT_REGEX` field needs its regular expression here. |

### `RecordTypeFieldChange`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `id` | `int` | no | — | The ID of the field to change. Without it a field is added. |
| `name` | `str` | no | — | The name of the field. |
| `result_type` | `FieldResultType` | no | `TEXT`<br>`TEXT_ENUM`<br>`TEXT_REGEX`<br>`EMAIL`<br>`URL`<br>`IP_ADDRESS`<br>`NUMBER`<br>`BOOLEAN`<br>`TIMESTAMP`<br>`JSON`<br>`ARTIFACT` | The type of the field. |
| `fixed_values` | `Sequence[str]` | no | — | The allowed values of a `TEXT_ENUM` field, at most 100. |
| `description` | `str` | no | — | A description of the field. |
| `config` | `Mapping[str, Any]` | no | — | Settings of the field. They replace the old ones. |
