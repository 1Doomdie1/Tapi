# Fields

- **Access:** `tines.cases.fields`
- **Import:** `from tapi.cases import Fields`
- **Part of:** [Cases](cases.md)

The case fields of a team: custom values that its cases can hold.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the case fields, optionally of one team. | `GET /api/v1/case_inputs` |
| [`get`](#get) | Get a case field. | `GET /api/v1/case_inputs/{field_id}` |
| [`create`](#create) | Create a case field in a team. | `POST /api/v1/case_inputs` |
| [`update`](#update) | Change a case field. | `PATCH /api/v2/case_inputs/{field_id}` |
| [`delete`](#delete) | Delete a case field. | `DELETE /api/v2/case_inputs/{field_id}` |
| [`list_values`](#list_values) | List the values of a field across cases. | `GET /api/v1/case_inputs/{field_id}/fields` |

## Methods breakdown

### `list`

`GET /api/v1/case_inputs`

List the case fields, optionally of one team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | no | — | Only fields of this team. |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. Tines defaults to 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `case_inputs`, the fields of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The team does not exist or is not visible to the key. |

### `get`

`GET /api/v1/case_inputs/{field_id}`

Get a case field.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `field_id` | `int` | yes | — | The ID of the field. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the field. |
| 404 | The field does not exist or is not visible to the key. |

### `create`

`POST /api/v1/case_inputs`

Create a case field in a team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `name` | `str` | yes | — | The name of the field. It is unique within the team. |
| `input_type` | `FieldType` | yes | `string`<br>`number`<br>`boolean`<br>`timestamp`<br>`email`<br>`url`<br>`ip_address` | The type of the values. |
| `team_id` | `int` | yes | — | The ID of the team that gets the field. |
| `sensitive` | `bool` | no | `True`, `False` | Whether the sensitive field permission is needed to read or write the field. |
| `validation_type` | `FieldValidation` | no | `none`, `options`, `regex` | How values are checked. `options` and `regex` are for a `string` field. |
| `validation_options` | [`FieldValidationOptions`](#fieldvalidationoptions) | no | — | What to check a value against: `{"options": [...]}` for `options`, or `{"regex": "..."}` for `regex`. |
| `group_name` | `str` | no | — | The name of the group to put the field in. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is an object with `team_case_input`, the created field. |
| 404 | The team does not exist or is not visible to the key. |

### `update`

`PATCH /api/v2/case_inputs/{field_id}`

Change a case field.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `field_id` | `int` | yes | — | The ID of the field. |
| `name` | `str` | no | — | A new name. |
| `sensitive` | `bool` | no | `True`, `False` | Whether the sensitive field permission is needed to read or write the field. |
| `validation_type` | `FieldValidation` | no | `none`, `options`, `regex` | How values are checked. |
| `validation_options` | [`FieldValidationOptions`](#fieldvalidationoptions) | no | — | What to check a value against, as for `create`. |
| `group_name` | `str` | no | — | The name of the group to put the field in. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated field, as it is. |
| 404 | The field does not exist or is not visible to the key. |

### `delete`

`DELETE /api/v2/case_inputs/{field_id}`

Delete a case field.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `field_id` | `int` | yes | — | The ID of the field. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The field does not exist or is not visible to the key. |

### `list_values`

`GET /api/v1/case_inputs/{field_id}/fields`

List the values of a field across cases.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `field_id` | `int` | yes | — | The ID of the field. |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. Tines defaults to 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `fields`, the values of the page, each with `id`, `value`, `case` (an object with an `id`) and `case_input`, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The field does not exist or is not visible to the key. |

## Types

### `FieldValidationOptions`

One of: [`FieldOptions`](#fieldoptions), [`FieldRegex`](#fieldregex).

### `FieldOptions`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `options` | `Sequence[str]` | yes | — | The allowed values. |

### `FieldRegex`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `regex` | `str` | yes | — | The pattern that a value must match. |
