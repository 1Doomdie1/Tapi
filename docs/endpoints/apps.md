# Apps

- **Access:** `tines.apps`
- **Import:** `from tapi.apps import Apps`

Apps built inside Tines. Create an app, replace its draft files, publish it, export it and delete it.

Every method returns a [`Response`](../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the apps visible to you. | `GET /api/v1/apps` |
| [`get`](#get) | Get an app. | `GET /api/v1/apps/{app_id}` |
| [`create`](#create) | Create an app. | `POST /api/v1/apps` |
| [`delete`](#delete) | Delete an app and all of its versions. | `DELETE /api/v1/apps/{app_id}` |
| [`export`](#export) | Export an app as its name, description and files. | `GET /api/v1/apps/{app_id}/export` |
| [`replace_files`](#replace_files) | Replace all the draft files of an app. | `PUT /api/v1/apps/{app_id}/files` |
| [`publish`](#publish) | Publish the draft of an app. | `POST /api/v1/apps/{app_id}/publish` |

## Methods breakdown

### `list`

`GET /api/v1/apps`

List the apps visible to you.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. Tines defaults to 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `apps`, the apps of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |

### `get`

`GET /api/v1/apps/{app_id}`

Get an app.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `app_id` | `int` | yes | — | The ID of the app to retrieve. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the app. |
| 404 | The app does not exist or is not visible to the key. |

### `create`

`POST /api/v1/apps`

Create an app. It cannot be in a personal team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | yes | — | The ID of the team the app belongs to. It must not be a personal team. |
| `name` | `str` | no | — | The name of the app. |
| `description` | `str` | no | — | A description of the app. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the created app. |
| 422 | `team_id` is a personal team. |

### `delete`

`DELETE /api/v1/apps/{app_id}`

Delete an app and all of its versions.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `app_id` | `int` | yes | — | The ID of the app to delete. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The app does not exist or is not visible to the key. |

### `export`

`GET /api/v1/apps/{app_id}/export`

Export an app as its name, description and files.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `app_id` | `int` | yes | — | The ID of the app to export. |
| `version_id` | `int` | no | — | The ID of the app version to export. Tines defaults to the current draft. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with the `name` of the app, its `description` (`null` if there is none) and its `files`: a list of objects with a `path` and `contents`, in the format that `replace_files` takes. |
| 404 | The app does not exist or is not visible to the key. |
| 413 | The files of the app are too large to export. |

### `replace_files`

`PUT /api/v1/apps/{app_id}/files`

Replace all the draft files of an app. Files that are left out are deleted.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `app_id` | `int` | yes | — | The ID of the app whose draft files are replaced. |
| `files` | [`Sequence[AppFile]`](#appfile) | yes | — | The complete set of draft files. Files that are left out are deleted. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `files`, the complete set of draft files of the app, each with a `path` and `contents`. |
| 404 | The app does not exist or is not visible to the key. |
| 422 | No file has the path `App.tsx`. |

### `publish`

`POST /api/v1/apps/{app_id}/publish`

Publish the draft of an app.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `app_id` | `int` | yes | — | The ID of the app to publish. |
| `name` | `str` | no | — | A name for the published version. |
| `description` | `str` | no | — | A description of the published version. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the published app, with `published_version` set. |
| 404 | The app does not exist or is not visible to the key. |
| 422 | The build failed. |
| 500 | The build failed on a syntax error in `App.tsx`. |

## Types

### `AppFile`

A file of an app: its `path` and, optionally, its `contents`.

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `path` | `str` | yes | — | The path of the file. One file must have the path `App.tsx`. |
| `contents` | `str` | no | — | The contents of the file. An empty string by default. |
