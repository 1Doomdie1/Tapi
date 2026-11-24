# Records

- **Access:** `tines.cases.records`
- **Import:** `from tapi.cases import Records`
- **Part of:** [Cases](cases.md)

The records attached to a case.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the records attached to a case. | `GET /api/v2/cases/{case_id}/records` |
| [`get`](#get) | Get a record of a case. | `GET /api/v2/cases/{case_id}/records/{record_id}` |
| [`create`](#create) | Attach a record to a case. | `POST /api/v2/cases/{case_id}/records` |
| [`delete`](#delete) | Remove a record from a case. | `DELETE /api/v2/cases/{case_id}/records/{record_id}` |

## Methods breakdown

### `list`

`GET /api/v2/cases/{case_id}/records`

List the records attached to a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. Tines defaults to 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `case_id`, `records`, the records of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The case does not exist or is not visible to the key. |

### `get`

`GET /api/v2/cases/{case_id}/records/{record_id}`

Get a record of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `record_id` | `int` | yes | — | The ID of the record. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `case_id` and `record`. |
| 404 | The case or the record does not exist or is not visible to the key. |

### `create`

`POST /api/v2/cases/{case_id}/records`

Attach a record to a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `record_id` | `int` | yes | — | The ID of the record to attach. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is an object with `case_id` and `record`. |
| 404 | The case or the record does not exist or is not visible to the key. |

### `delete`

`DELETE /api/v2/cases/{case_id}/records/{record_id}`

Remove a record from a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `record_id` | `int` | yes | — | The ID of the record to remove. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The case or the record does not exist or is not visible to the key. |
