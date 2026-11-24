# Folders

- **Access:** `tines.folders`
- **Import:** `from tapi.folders import Folders`

Folders that organize stories, credentials and resources.

Every method returns a [`Response`](../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the folders, optionally of one team or one type of content. | `GET /api/v1/folders` |
| [`get`](#get) | Get a folder. | `GET /api/v1/folders/{folder_id}` |
| [`create`](#create) | Create a folder. | `POST /api/v1/folders` |
| [`update`](#update) | Rename a folder or move it. | `PATCH /api/v1/folders/{folder_id}` |
| [`delete`](#delete) | Delete a folder. | `DELETE /api/v1/folders/{folder_id}` |

## Methods breakdown

### `list`

`GET /api/v1/folders`

List the folders, optionally of one team or one type of content.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | no | — | Only folders of this team. |
| `content_type` | `FolderFilterContentType` | no | `CREDENTIAL`, `RESOURCE`, `STORY` | Only folders that hold this type of content. |
| `per_page` | `int` | no | Positive integer | The number of results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. Tines defaults to 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `folders`, the folders of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 422 | `content_type` is not a valid value. |

### `get`

`GET /api/v1/folders/{folder_id}`

Get a folder.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `folder_id` | `int` | yes | — | The ID of the folder to retrieve. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the folder. |
| 404 | The folder does not exist or the key has no access to it. |

### `create`

`POST /api/v1/folders`

Create a folder.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `name` | `str` | yes | — | The name of the folder. |
| `content_type` | `FolderContentType` | yes | `CREDENTIAL`, `RESOURCE`, `STORY` | The type of content the folder holds. |
| `team_id` | `int` | yes | — | The ID of the team the folder is created in. |
| `parent_folder_id` | `int` | no | — | The ID of the folder to create it in. Tines defaults to `null`, the root level. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the created folder. |

### `update`

`PATCH /api/v1/folders/{folder_id}`

Rename a folder or move it.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `folder_id` | `int` | yes | — | The ID of the folder to update. |
| `name` | `str` | yes | — | The name of the folder. |
| `parent_folder_id` | `int` | no | — | The ID of the folder to move it into. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated folder. |
| 404 | The folder does not exist or the key has no access to it. |

### `delete`

`DELETE /api/v1/folders/{folder_id}`

Delete a folder.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `folder_id` | `int` | yes | — | The ID of the folder to delete. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The folder does not exist or the key has no access to it. |
| 422 | The folder has contents. |
