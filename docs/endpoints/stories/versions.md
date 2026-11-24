# Versions

- **Access:** `tines.stories.versions`
- **Import:** `from tapi.stories import Versions`
- **Part of:** [Stories](stories.md)

The versions of a story: snapshots that can be named, read and deleted.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the versions of a story. | `GET /api/v1/stories/{story_id}/versions` |
| [`create`](#create) | Create a version of a story. | `POST /api/v1/stories/{story_id}/versions` |
| [`get`](#get) | Get a version of a story, with its export. | `GET /api/v1/stories/{story_id}/versions/{version_id}` |
| [`update`](#update) | Rename a version. | `POST /api/v1/stories/{story_id}/versions/{version_id}` |
| [`delete`](#delete) | Delete a version. | `DELETE /api/v1/stories/{story_id}/versions/{version_id}` |

## Methods breakdown

### `list`

`GET /api/v1/stories/{story_id}/versions`

List the versions of a story.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `draft_id` | `int` | no | — | Only versions of this draft. |
| `per_page` | `int` | no | Positive integer | The number of results per page. Tines defaults to 20 and caps it at 500. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. Tines defaults to 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `story_versions`, the versions of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The story does not exist or is not visible to the key. |

### `create`

`POST /api/v1/stories/{story_id}/versions`

Create a version of a story.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `name` | `str` | no | — | The name of the version. |
| `draft_id` | `int` | no | — | The ID of the draft to create the version for. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `story_version`, the created version. |
| 404 | The story does not exist or is not visible to the key. |

### `get`

`GET /api/v1/stories/{story_id}/versions/{version_id}`

Get a version of a story, with its export.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `version_id` | `int` | yes | — | The ID of the version to retrieve. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `story_version`, the version with its `export_file`. |
| 404 | The story or the version does not exist or is not visible to the key. |

### `update`

`POST /api/v1/stories/{story_id}/versions/{version_id}`

Rename a version.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `version_id` | `int` | yes | — | The ID of the version to rename. |
| `name` | `str` | yes | — | The new name of the version. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `story_version`, the updated version. |
| 404 | The story or the version does not exist or is not visible to the key. |

### `delete`

`DELETE /api/v1/stories/{story_id}/versions/{version_id}`

Delete a version.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `version_id` | `int` | yes | — | The ID of the version to delete. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `destroyed_id`, the ID of the deleted version. |
| 404 | The story or the version does not exist or is not visible to the key. |
