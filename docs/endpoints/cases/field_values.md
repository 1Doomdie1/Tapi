# FieldValues

- **Access:** `tines.cases.field_values`
- **Import:** `from tapi.cases import FieldValues`
- **Part of:** [Cases](cases.md)

The values that a case holds for the case fields of its team.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the field values of a case. | `GET /api/v2/cases/{case_id}/fields` |
| [`get`](#get) | Get a field value of a case. | `GET /api/v2/cases/{case_id}/fields/{field_id}` |
| [`create`](#create) | Set a field value on a case. | `POST /api/v2/cases/{case_id}/fields` |
| [`update`](#update) | Change a field value. | `PATCH /api/v2/cases/{case_id}/fields/{field_id}` |
| [`delete`](#delete) | Delete a field value. | `DELETE /api/v2/cases/{case_id}/fields/{field_id}` |

## Methods breakdown

### `list`

`GET /api/v2/cases/{case_id}/fields`

List the field values of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. Tines defaults to 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `case_id`, `fields`, the field values of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The case does not exist or is not visible to the key. |

### `get`

`GET /api/v2/cases/{case_id}/fields/{field_id}`

Get a field value of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `field_id` | `int` | yes | — | The ID of the field value. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `case_id` and `field`. |
| 404 | The case or the field does not exist or is not visible to the key. |

### `create`

`POST /api/v2/cases/{case_id}/fields`

Set a field value on a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `input_id` | `int` | yes | — | The ID of the field, as defined for the team. |
| `value` | `str` | yes | — | The value, as a string. A field that allows several values takes one string separated by `\|`. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is an object with `case_id` and `field`. |
| 404 | The case does not exist or is not visible to the key. `input_id` is not a field of the team. |

### `update`

`PATCH /api/v2/cases/{case_id}/fields/{field_id}`

Change a field value.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `field_id` | `int` | yes | — | The ID of the field value. |
| `value` | `str` | yes | — | The new value, as a string. A field that allows several values takes one string separated by `\|`. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `case_id` and `field`. |
| 404 | The case or the field does not exist or is not visible to the key. |

### `delete`

`DELETE /api/v2/cases/{case_id}/fields/{field_id}`

Delete a field value.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `field_id` | `int` | yes | — | The ID of the field value. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The case or the field does not exist or is not visible to the key. |
