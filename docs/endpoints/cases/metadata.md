# Metadata

- **Access:** `tines.cases.metadata`
- **Import:** `from tapi.cases import Metadata`
- **Part of:** [Cases](cases.md)

The key-value metadata of a case.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the metadata of a case. | `GET /api/v2/cases/{case_id}/metadata` |
| [`get`](#get) | Get one pair of the metadata of a case. | `GET /api/v2/cases/{case_id}/metadata/{key}` |
| [`create`](#create) | Add pairs to the metadata of a case. | `POST /api/v2/cases/{case_id}/metadata` |
| [`update`](#update) | Set pairs of the metadata of a case. | `PUT /api/v2/cases/{case_id}/metadata` |
| [`delete`](#delete) | Delete pairs of the metadata of a case. | `DELETE /api/v2/cases/{case_id}/metadata` |

## Methods breakdown

### `list`

`GET /api/v2/cases/{case_id}/metadata`

List the metadata of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `case_id` and `metadata`, an empty object for a case without metadata. |
| 404 | The case does not exist or is not visible to the key. |

### `get`

`GET /api/v2/cases/{case_id}/metadata/{key}`

Get one pair of the metadata of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `key` | `str` | yes | — | The key of the pair. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `case_id` and `metadata`, which holds only the pair that was asked for. |
| 404 | The case does not exist or is not visible to the key. The case has no such key. |

### `create`

`POST /api/v2/cases/{case_id}/metadata`

Add pairs to the metadata of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `metadata` | [`Mapping[str, MetadataValue]`](#metadatavalue) | yes | — | The pairs to add. A value is a string, a number, a boolean or `None`. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is an object with `case_id` and `metadata`. |
| 404 | The case does not exist or is not visible to the key. |
| 409 | A key already has a value. |

### `update`

`PUT /api/v2/cases/{case_id}/metadata`

Set pairs of the metadata of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `metadata` | [`Mapping[str, MetadataValue]`](#metadatavalue) | yes | — | The pairs to set. A value is a string, a number, a boolean or `None`. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `case_id` and `metadata`, with every pair of the case. |
| 400 | `metadata` is empty. |
| 404 | The case does not exist or is not visible to the key. |

### `delete`

`DELETE /api/v2/cases/{case_id}/metadata`

Delete pairs of the metadata of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `metadata` | `Sequence[str]` | yes | — | The keys to delete. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The case does not exist or is not visible to the key. The case has no such key. |

## Types

### `MetadataValue`

One of: `str`, `int`, `float`, `bool`, `None`.
