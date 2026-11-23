# Apps

Apps are small web applications built inside Tines. The module is available as `tines.apps`, and
the class is `tapi.apps.Apps`. Every method returns a [`Response`](../responses.md).

| Method                                       | HTTP route                           |
| -------------------------------------------- | ------------------------------------ |
| `list(...)`                                  | `GET /api/v1/apps`                   |
| `get(app_id=...)`                            | `GET /api/v1/apps/{app_id}`          |
| `create(team_id=..., ...)`                   | `POST /api/v1/apps`                  |
| `delete(app_id=...)`                         | `DELETE /api/v1/apps/{app_id}`       |
| `export(app_id=..., ...)`                    | `GET /api/v1/apps/{app_id}/export`   |
| `replace_files(app_id=..., files=...)`       | `PUT /api/v1/apps/{app_id}/files`    |
| `publish(app_id=..., ...)`                   | `POST /api/v1/apps/{app_id}/publish` |

All parameters are keyword-only. Parameters left as `None` are not sent, but `""` is sent.

The Tines docs do not state which key types or permissions these endpoints need. Apps are not
available on every Tines plan. Where they are unavailable or switched off, the endpoints answer with
a `404` and `['Not found']`.

## The app

`data` of `get`, `create` and `publish` is an app, and `list` returns a list of them under `apps`.
An app has:

| Field               | Meaning                                                                          |
| ------------------- | -------------------------------------------------------------------------------- |
| `id`                | The ID of the app.                                                               |
| `guid`              | The unique identifier of the app. It can be `null`.                              |
| `name`              | The name of the app.                                                             |
| `description`       | A user-defined description. It can be `null`.                                    |
| `emoji`             | The emoji associated with the app.                                               |
| `created_at`        | When the app was created, as an ISO 8601 timestamp.                              |
| `updated_at`        | When the app was last updated, as an ISO 8601 timestamp.                         |
| `team`              | The team the app belongs to, as an object with `id` and `name`.                  |
| `published_version` | An object with the `id` of the published version, or `null` if it is unpublished. |

The files of an app are not part of the app. Read them with `export`.

## `list()`

Paginated: one call returns one page; see [Pagination](../pagination.md). `data` holds `apps` and
`meta`.

| Parameter  | Type  | Meaning                                        |
| ---------- | ----- | ---------------------------------------------- |
| `per_page` | `int` | Results per page. Tines defaults to 20.        |
| `page`     | `int` | The page, starting at 1. Tines defaults to 1.  |

## `get()`

`app_id` is required. When no app with that ID is visible to the key, the reply is a `404` with
`['App not found']`.

## `create()`

`team_id` is required, and the reply has a 201 status.

| Parameter     | Type  | Meaning                                       |
| ------------- | ----- | --------------------------------------------- |
| `team_id`     | `int` | The team the app belongs to. Required. It must not be a personal team. |
| `name`        | `str` | The name of the app.                          |
| `description` | `str` | A description of the app.                     |

An app cannot be created in a personal team. The reply is a `422` with
`['Validation failed: Cannot create app in a personal team']`. On the tenant used for the live
check, `GET /api/v1/teams` returned only the standard team, and the personal teams appeared only
with `scope` set to `personal_only` or `all`. See [Teams](teams.md).

There is no endpoint to rename an app or change its description afterwards. A new app starts with a
single file, `package.json`, and gets its other files through `replace_files`.

## `delete()`

`app_id` is required. It deletes the app and all of its versions. The reply has a 204 status and
`data` is `None`.

## `export()`

Returns the name, the description and the files of an app.

| Parameter    | Type  | Meaning                                                                  |
| ------------ | ----- | ------------------------------------------------------------------------ |
| `app_id`     | `int` | The app to export. Required.                                             |
| `version_id` | `int` | The version to export. Tines defaults to the current draft.              |

`data` is an object with `name`, `description` (`null` if there is none) and `files`, a list of
objects with a `path` and `contents`. It uses the same format as `replace_files`, so an export can
be sent back as it is. The reply is a `404` when no app is visible or the version does not belong to
the app, and a `413` when the files are too large to export.

## `replace_files()`

Replaces all the draft files of an app. `app_id` and `files` are required.

`files` is a sequence of files, and each file is a `dict`, typed as `tapi.apps.AppFile`:

| Key        | Type  | Meaning                                                              |
| ---------- | ----- | -------------------------------------------------------------------- |
| `path`     | `str` | The path of the file. Required.                                      |
| `contents` | `str` | The contents of the file. Optional, and an empty string by default.  |

```python
tines.apps.replace_files(
    app_id=42,
    files=[
        {"path": "App.tsx", "contents": "export default function App() { return <h1>Hi</h1>; }"},
        {"path": "styles.css", "contents": "h1 { color: red; }"},
    ],
)
```

- `files` is the complete set. An existing file that is left out is deleted.
- One file must have the path `App.tsx`. Without it, and for an empty list, the reply is a `422`
  with `['Missing required entry file App.tsx']` and nothing is replaced.
- A file without `contents` is stored with an empty string.
- This does not build the app. To build it, open it in the Tines UI or use `publish`.
- A single file instead of a sequence of files is rejected with a `TypeError` before any request is
  sent.
- `data` is an object with `files`, the complete set of draft files of the app.

## `publish()`

Builds the current draft and publishes it as a new version. If the draft has not changed since the
latest version, that version is published instead.

| Parameter     | Type  | Meaning                                |
| ------------- | ----- | -------------------------------------- |
| `app_id`      | `int` | The app to publish. Required.          |
| `name`        | `str` | A name for the published version.      |
| `description` | `str` | A description of the published version. |

`data` is the published app, with `published_version` set. The reply does not echo the name or the
description of the version.

Tines documents a `422` with the build error when the build fails, and does not describe the shape
of that body. A syntax error in `App.tsx` was answered with a `500` instead, and nothing was
published.

## Errors

| Status | When                                                                                       |
| ------ | ------------------------------------------------------------------------------------------ |
| `400`  | A request is malformed or a parameter is invalid. `data` is a list of messages.            |
| `404`  | Apps are unavailable on the plan or switched off (`['Not found']`), or the app (`['App not found']`) or the version (`['AppVersion not found']`) is not visible. |
| `413`  | `export` of an app whose files are too large.                                              |
| `422`  | `create` in a personal team, and `replace_files` without an `App.tsx`. Tines documents it for a failed `publish` build as well. |
| `500`  | `publish` when the build fails on a syntax error in `App.tsx`.                             |
