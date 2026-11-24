# Folders

Folders organize stories, credentials and resources. The module is available as `tines.folders`,
and the class is `tapi.folders.Folders`. Every method returns a [`Response`](../responses.md).

| Method                                            | HTTP route                           |
| ------------------------------------------------- | ------------------------------------ |
| `list(...)`                                       | `GET /api/v1/folders`                |
| `get(folder_id=...)`                              | `GET /api/v1/folders/{folder_id}`    |
| `create(name=..., content_type=..., team_id=...)` | `POST /api/v1/folders`               |
| `update(folder_id=..., name=..., ...)`            | `PATCH /api/v1/folders/{folder_id}`  |
| `delete(folder_id=...)`                           | `DELETE /api/v1/folders/{folder_id}` |

All parameters are keyword-only. Parameters left as `None` are not sent. The Tines docs do not
state which key types or permissions these endpoints need. A key without access to a resource
receives a 404.

## The folder

`data` of `get`, `create` and `update` is a folder, and `list` returns a list of them under
`folders`. A folder has:

| Field              | Meaning                                                                      |
| ------------------ | ---------------------------------------------------------------------------- |
| `id`               | The ID of the folder.                                                        |
| `name`             | The name of the folder.                                                      |
| `team_id`          | The ID of the team the folder belongs to.                                    |
| `content_type`     | The type of content the folder holds. See [Content types](#content-types).   |
| `size`             | The number of items in the folder. Subfolders are not counted.               |
| `parent_folder_id` | The ID of the parent folder, or `null` for a folder at the root level.       |

## `list()`

Paginated: one call returns one page; see [Pagination](../pagination.md). `data` holds `folders`
and `meta`.

| Parameter      | Type  | Meaning                                                                          |
| -------------- | ----- | -------------------------------------------------------------------------------- |
| `team_id`      | `int` | Only folders of this team.                                                       |
| `content_type` | `str` | Only folders that hold this type of content. See [Content types](#content-types). |
| `per_page`     | `int` | Results per page. Tines defaults to 20.                                          |
| `page`         | `int` | The page, starting at 1. Tines defaults to 1.                                    |

## `get()`

`folder_id` is required.

## `create()`

The reply has a 201 status and `data` is the created folder.

| Parameter          | Type  | Meaning                                                               |
| ------------------ | ----- | --------------------------------------------------------------------- |
| `name`             | `str` | The name of the folder. Required.                                     |
| `content_type`     | `str` | The type of content the folder holds. Required. See below.            |
| `team_id`          | `int` | The team the folder is created in. Required.                          |
| `parent_folder_id` | `int` | The folder to create it in. Tines defaults to `null`, the root level. |

Folders were tested nested one level deep. Tines does not state a depth limit, and deeper nesting
was not tested.

## `update()`

Renames or moves a folder. `folder_id` and `name` are required, because the OpenAPI document
requires `name`, so a folder cannot be moved without also giving its name. `parent_folder_id` moves
the folder into another folder.

- The content type and the team of a folder cannot be changed. `update` does not accept them, and
  a `content_type` sent to the server in an update is ignored: the reply is `200` and the folder
  keeps its type.
- Tines moves a folder to the root level when `parent_folder_id` is `null`, as its docs say, and
  also when it is an empty string, as the OpenAPI document says. Because `None` means "not sent",
  tapi cannot send either yet.
- The Tines docs show this operation as `PUT`. The OpenAPI document lists the same operation under
  `PUT` and `PATCH`, and tapi uses `PATCH`.

## `delete()`

`folder_id` is required. The reply has a 204 status and `data` is `None`.

A folder with contents cannot be deleted. Tines answers with a `422` whose `data` is
`['Cannot delete this folder, please remove all contents first.']`, and nothing is deleted. Remove
the contents first, subfolders included.

## Content types

`content_type` is `CREDENTIAL`, `RESOURCE` or `STORY`, in `create()` and in the filter of `list()`.

## Errors

| Status | When                                                                                        |
| ------ | ------------------------------------------------------------------------------------------- |
| `404`  | The folder does not exist, or the key has no access to it. `data` is a list of messages.    |
| `422`  | A value is invalid, such as an unknown `content_type` filter, or a folder with contents is deleted. `data` is a list of messages or of objects naming the field. |