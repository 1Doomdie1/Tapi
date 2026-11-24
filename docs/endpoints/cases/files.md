# Files

- **Access:** `tines.cases.files`
- **Import:** `from tapi.cases import Files`
- **Part of:** [Cases](cases.md)

The files attached to a case.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the files of a case. | `GET /api/v2/cases/{case_id}/files` |
| [`get`](#get) | Get a file of a case. | `GET /api/v2/cases/{case_id}/files/{file_id}` |
| [`create`](#create) | Attach a file to a case. | `POST /api/v2/cases/{case_id}/files` |
| [`delete`](#delete) | Delete a file of a case. | `DELETE /api/v2/cases/{case_id}/files/{file_id}` |
| [`download`](#download) | Download a file of a case. | `GET /api/v2/cases/{case_id}/files/{file_id}/download` |
| [`info`](#info) | Get the details of a file of a case: its name, type, hashes and size. | `GET /api/v2/cases/{case_id}/files/{file_id}/info` |

## Methods breakdown

### `list`

`GET /api/v2/cases/{case_id}/files`

List the files of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. Tines defaults to 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `files`, the files of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The case does not exist or is not visible to the key. |

### `get`

`GET /api/v2/cases/{case_id}/files/{file_id}`

Get a file of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `file_id` | `int` | yes | — | The ID of the file: the `id` of its activity. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the activity, with `case_id` added. |
| 404 | The case or the file does not exist or is not visible to the key. |

### `create`

`POST /api/v2/cases/{case_id}/files`

Attach a file to a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `filename` | `str` | yes | — | The name of the file. |
| `file_contents` | `str` | yes | Base64 string, such as `base64.b64encode(data).decode()` | The contents of the file, Base64 encoded. To encode bytes, use `base64.b64encode(data).decode()`. |
| `value` | `str` | no | — | A comment to add with the file, as Markdown. User mentions are written `<@user-2435>`. |
| `author_email` | `str` | no | — | The email address of the user who attaches the file. |
| `team_case_block_id` | `int` | no | — | The file block to attach the file to. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the activity that attached the file. |
| 404 | The case does not exist or is not visible to the key. |

### `delete`

`DELETE /api/v2/cases/{case_id}/files/{file_id}`

Delete a file of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `file_id` | `int` | yes | — | The ID of the file. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The case or the file does not exist or is not visible to the key. |
| 422 | The file is already deleted. |

### `download`

`GET /api/v2/cases/{case_id}/files/{file_id}/download`

Download a file of a case. `data` is the file: text as `str`, anything else as `bytes`.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `file_id` | `int` | yes | — | The ID of the file. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the file, decoded by its content type: text is a `str` and a binary file is `bytes`. |
| 404 | The case or the file does not exist or is not visible to the key. |

### `info`

`GET /api/v2/cases/{case_id}/files/{file_id}/info`

Get the details of a file of a case: its name, type, hashes and size.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `file_id` | `int` | yes | — | The ID of the file. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `filename`, `content_type`, `guid`, `md5`, `sha256` and `sizeinbytes`. |
| 404 | The case or the file does not exist or is not visible to the key. |
