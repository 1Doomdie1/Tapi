# Resources

Resources are named values, such as text, JSON and files, that actions and stories can use. The
module is available as `tines.resources`, and the class is `tapi.resources.Resources`. Tines calls
them global resources in its API paths. Every method returns a [`Response`](../responses.md).

| Method                                          | HTTP route                                            |
| ----------------------------------------------- | ----------------------------------------------------- |
| `list(...)`                                     | `GET /api/v1/global_resources`                        |
| `get(resource_id=..., ...)`                     | `GET /api/v1/global_resources/{resource_id}`          |
| `create(name=..., value=..., team_id=..., ...)` | `POST /api/v1/global_resources`                       |
| `update(resource_id=..., value=..., ...)`       | `PATCH /api/v1/global_resources/{resource_id}`        |
| `delete(resource_id=...)`                       | `DELETE /api/v1/global_resources/{resource_id}`       |
| `append(resource_id=..., value=..., ...)`       | `POST /api/v1/global_resources/{resource_id}/append`  |
| `remove(resource_id=..., ...)`                  | `POST /api/v1/global_resources/{resource_id}/remove`  |
| `replace(resource_id=..., value=..., ...)`      | `POST /api/v1/global_resources/{resource_id}/replace` |
| `set_locked(resource_id=..., locked=...)`       | `PUT /api/v1/global_resources/{resource_id}/locked`   |

All parameters are keyword-only. Parameters left as `None` are not sent, but `0`, `False` and `""`
are sent. The Tines docs do not state which key types these endpoints need, other than that locking
needs the `RESOURCE_MANAGE` permission. A key without access to a resource receives a 404.

## The resource

`data` of `get`, `create` and `update` is a resource, and `list` returns a list of them under
`global_resources`. A resource has:

| Field                      | Meaning                                                                           |
| -------------------------- | --------------------------------------------------------------------------------- |
| `id`, `name`, `slug`       | The ID, the name and an underscored form of the name.                             |
| `value`                    | The contents. A string unless `typed_value` is true. For a file resource it holds `name`, `contents` and `type`. |
| `team_id`, `folder_id`     | The team and the folder. `folder_id` is `null` at the root.                       |
| `user_id`                  | The user associated with the resource.                                            |
| `read_access`              | Where the resource can be used: `TEAM`, `GLOBAL` or `SPECIFIC_TEAMS`.            |
| `shared_team_slugs`        | The teams' slugs when `read_access` is `SPECIFIC_TEAMS`, otherwise empty.         |
| `description`              | The description.                                                                  |
| `created_at`, `updated_at` | ISO 8601 timestamps.                                                              |
| `test_resource_enabled`    | Whether the resource can use a test resource.                                     |
| `test_resource`            | The test resource, with `value`, `created_at` and `updated_at`. Present only when it is enabled. |
| `referencing_action_ids`   | The IDs of the actions that use the resource.                                     |

A resource has no field that tells you whether it is locked.

## Values

A value, as taken by `value` and `if_value`, is a string, a number, a boolean, a JSON object (a
`dict`) or a JSON array (a `list`).

- A string that is not JSON is stored as text.
- A `dict` or a `list` creates a JSON resource.
- A file resource takes a `dict` with `name` (the file name), `contents` (the Base64-encoded
  contents) and optionally `type` (the MIME type). Reading it returns the same three fields in
  `value`.

By default Tines returns every `value` as a string, so a JSON array comes back as compact JSON
text, such as `'["a","b","c"]'`. With `typed_value=True`, `value` is returned as a boolean, a number,
an array or an object where it holds one. `typed_value` is available on `list`, `get`, `create` and
`update`, and it only changes the reply.

## `list()`

Paginated: one call returns one page; see [Pagination](../pagination.md). `data` holds
`global_resources` and `meta`.

| Parameter                        | Type   | Meaning                                                                      |
| -------------------------------- | ------ | ---------------------------------------------------------------------------- |
| `team_id`                        | `int`  | Only resources of this team.                                                 |
| `folder_id`                      | `int`  | Only resources in this folder.                                               |
| `filter`                         | `str`  | `UNUSED_IN_ACTIONS` keeps the resources that no action uses. |
| `include_referencing_action_ids` | `bool` | Whether each resource has `referencing_action_ids`. Tines defaults to true.  |
| `include_value`                  | `bool` | Whether each resource has `value` and `test_resource.value`. Tines defaults to true. |
| `typed_value`                    | `bool` | Return typed values. Tines defaults to false.                                |
| `per_page`                       | `int`  | Results per page. Tines defaults to 20.                                      |
| `page`                           | `int`  | The page, starting at 1. Tines defaults to 1.                                |

## `get()`

`resource_id` is required. `include_referencing_action_ids` and `typed_value` work as in `list`.

## `create()`

`name`, `value` and `team_id` are required, and the reply has a 201 status.

| Parameter                        | Type              | Meaning                                                                |
| -------------------------------- | ----------------- | ---------------------------------------------------------------------- |
| `name`                           | `str`             | The name of the resource.                                              |
| `value`                          | a value           | The contents. See [Values](#values).                                   |
| `team_id`                        | `int`             | The team the resource is created in.                                   |
| `folder_id`                      | `int`             | The folder to put it in.                                               |
| `read_access`                    | `str`             | `TEAM` (the default), `GLOBAL` or `SPECIFIC_TEAMS`, which is a premium feature. |
| `shared_team_slugs`              | sequence of `str` | The teams that can use it. Needed for `SPECIFIC_TEAMS`.                |
| `description`                    | `str`             | Defaults to an empty string.                                           |
| `live_resource_id`               | `int`             | For a test resource in the TEST mode of change control: the live resource it corresponds to. The other optional values then default to those of the live resource. |
| `include_referencing_action_ids` | `bool`            | Whether the reply has `referencing_action_ids`. Tines defaults to true. |
| `typed_value`                    | `bool`            | Return a typed `value` in the reply.                                   |

## `update()`

`resource_id` and `value` are required, and every other parameter is optional. Tines refuses an
update without `value` with a `422` and `['Value may not be null']`, even when only the name or the
description changes, so to change another field without changing the contents, pass the current
value. `update` accepts the same parameters as `create`, except `team_id` and `live_resource_id`, and
also:

| Parameter               | Type   | Meaning                                                                   |
| ----------------------- | ------ | ------------------------------------------------------------------------- |
| `test_resource_enabled` | `bool` | Whether the resource is enabled for using a test resource.                |
| `is_test`               | `bool` | Whether the test resource is the one to update. It needs `test_resource_enabled` to be true and a test resource to exist. |

Differences and limits to know about:

- The Tines docs show this operation as `PUT`. The OpenAPI document lists the same operation under
  `PUT` and `PATCH`, and tapi uses `PATCH`.
- The Tines docs do not mark `value` as optional, and the server requires it. The OpenAPI document
  requires no field.
- Because `None` means "not sent", tapi cannot send an explicit `null`, and cannot move a resource
  to the root folder, which Tines does with an empty value.

## `delete()`

`resource_id` is required. The reply has a 204 status and `data` is `None`. A locked resource can be
deleted. Tines does not say whether a resource that actions reference can be deleted.

## Changing part of a value

`append`, `remove` and `replace` change a resource without rewriting all of it. They take the ID of
the live resource, and each has an `is_test` parameter that points it at the test resource instead.

| Method    | What it does                                                          | The reply's `data`                             |
| --------- | --------------------------------------------------------------------- | ---------------------------------------------- |
| `append`  | Appends to the resource. `value` is required.                         | The updated value.                             |
| `remove`  | Removes an element from an array, or a key from an object.            | The removed item, or `None` if there was none. |
| `replace` | Replaces an element of an array, or a key of an object. `value` is required. | The updated value.                      |

How each one behaves, as observed on a live tenant:

- `append` on a text resource adds the string to the end of the text. On an array it adds a string
  as a new element, and an array adds its elements. On an object it is refused with a `422` and
  `['Append only supported for text or array type resources.']`.
- `remove` and `replace` address what they change with `key` for an object, or `index` for an array,
  counting from 0. `remove` without an `index` removes the last element of an array.
- `replace` with a `key` that does not exist adds that key to the object.
- `remove` of a key that does not exist is not an error: the reply is `200` with `data` equal to
  `None`, and nothing changes.
- An `index` beyond the end of the array is a `422` with `['Index out of bounds']`.
- On a text resource, `remove` and `replace` with an `index` change nothing and are not errors.
- A number given as `value` or `if_value` stays a number in an object, and an `if_value` of `5`
  matches a stored `5`.

`if_value` makes `remove` and `replace` conditional: the change only happens if the current value
at that key or index equals `if_value`, which can be any value. If it does not, Tines answers with
a `422` and the resource is unchanged. For that mismatch `data` is an object with `error` (`'Value
does not match expected value'`) and `current_value`, so a caller can retry against the value that is
there.

```python
tines.resources.replace(resource_id=9, key="count", value=6, if_value=5)
tines.resources.remove(resource_id=9, key="locked_by", if_value="run-123")
```

## `set_locked()`

Locks or unlocks a resource. It needs the `RESOURCE_MANAGE` permission. `data` is an object with
the `id` of the resource and its `locked` status.

- While a resource is locked, `update`, `append`, `remove` and `replace` are refused with a `422` and
  `['Resource is locked and cannot be modified']`. Reading it, and deleting it, still work.
- Locking a resource that is already locked is not an error.
- Locking or unlocking also applies to the test resource, and a test resource cannot be locked on
  its own. Unlocking through the API is permanent: the resource stays unlocked until it is locked
  again.

## Errors

| Status | When                                                                                       |
| ------ | ------------------------------------------------------------------------------------------ |
| `400`  | A request is malformed, for example when `team_id` is missing and no default team can be chosen. `data` is a list of messages. |
| `404`  | The resource does not exist, or the key has no access to it. `data` is a list of messages. |
| `422`  | An unknown `filter`, an `update` without `value`, a locked resource, an `append` on an object, an index out of bounds, or an `if_value` mismatch. |
