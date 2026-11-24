# Admin: roles

A role is a set of permissions that a user can have in a team. Tines has default roles, such as
`TEAM_ADMIN`, and a tenant can add custom roles. The roles are a sub-area of [`admin`](admin.md),
available as `tines.admin.roles`, and the class is `tapi.admin.Roles`. Every method returns a
[`Response`](../responses.md).

| Method                                             | HTTP route                           |
| -------------------------------------------------- | ------------------------------------ |
| `list(...)`                                        | `GET /api/v1/admin/roles`            |
| `get(role_id=...)`                                 | `GET /api/v1/admin/roles/{role_id}`  |
| `create(name=..., permissions=...)`                | `POST /api/v1/admin/roles`           |
| `update(role_id=...)`                              | `PATCH /api/v1/admin/roles/{role_id}` |
| `delete(role_id=...)`                              | `DELETE /api/v1/admin/roles/{role_id}` |

## The role

| Field         | Meaning                                                                                    |
| ------------- | ------------------------------------------------------------------------------------------ |
| `id`          | The identifier. For a default role it is the name, such as `TEAM_ADMIN`. A custom role has a number, which `list` and `get` return as a string and `create` returns as an integer. |
| `name`        | The name of the role.                                                                      |
| `type`        | `default` or `custom`.                                                                     |
| `description` | A description.                                                                             |
| `permissions` | A list of permission names, such as `STORY_CREATE` or `CASE_READ`. `ALLOW_ALL` is a permission of its own. |
| `created_at`  | An ISO 8601 timestamp, or `null` for a default role.                                       |
| `updated_at`  | An ISO 8601 timestamp, or `null` for a default role.                                       |
| `builder`     | Whether the role grants permission to build and edit stories.                              |

The tenant had seven default roles: `CASE_MANAGER`, `DASHBOARD_MANAGER`, `DASHBOARD_VIEWER`,
`EDITOR`, `TEAM_ADMIN`, `VIEWER` and `WORKBENCH_USER`. The Tines docs link a table of the permission
names, and the permissions of the default roles show many of them. Whether Tines refuses a name that
does not exist was not tried.

## `list()`

Lists the default and the custom roles. The endpoint is paginated, and one call returns one page; see
[Pagination](../pagination.md).

| Parameter  | Type  | Meaning                                                              |
| ---------- | ----- | -------------------------------------------------------------------- |
| `per_page` | `int` | The number of results per page. Tines defaults to 20.                |
| `page`     | `int` | The page to return, starting at 1. Tines defaults to 1.              |

`data` is an object with `admin/roles`, the roles of the page, and `meta`, the pagination details.
Unlike the other lists, this one does not refuse a `per_page` of `0` and gives the default, does not
cap a large `per_page`, and accepts a `page` of `0`.

## `get()`, `update()` and `delete()`

`role_id` is the ID or the name of the role. A default role was found by its name in lower case too,
and a role that does not exist is a `404` with `['Role not found']`.

- `get(role_id=...)` returns the role, default or custom.
- `update(role_id=..., description=..., permissions=...)` changes a custom role, and `permissions`
  replaces the old list. The name cannot be changed. The Tines docs show the operation as `PATCH`, and
  the OpenAPI document also lists `PUT`.
- `delete(role_id=...)` deletes a custom role and has a `204` status.

## `create()`

| Parameter     | Type              | Meaning                                                                |
| ------------- | ----------------- | ---------------------------------------------------------------------- |
| `name`        | `str`             | The name of the role. Required.                                        |
| `permissions` | sequence of `str` | The names of the permissions, such as `STORY_CREATE`. Required.        |
| `description` | `str`             | A description.                                                         |

The reply has a `201` status, and `data` is the created role. The name is unique among the custom roles,
and the list of permissions cannot be empty. A name that is not a permission is refused.

## Errors

| Status | When                                                                                          |
| ------ | --------------------------------------------------------------------------------------------- |
| `404`  | `get`, `update` and `delete` with a role that does not exist (`['Role not found']`).           |
| `422`  | `create` with a name that another custom role has (`['Validation failed: Name ... is already being used by another custom role']`), with a permission that does not exist (`['NOT_A_PERMISSION is not a valid permission']`) and with an empty list (`["Validation failed: Permissions can't be blank"]`). `update` with an empty list of permissions. |

## Behaviors worth knowing

- `update` with no argument besides `role_id` is a `200` and changes nothing. A `name` in the body is
  ignored, so a role cannot be renamed. `PUT` worked as well as `PATCH`.
- `get` finds a role by its ID or by its name, with either type of ID, and `update` takes the integer
  that `create` returned.
- A deleted role is a `404` afterwards, and so is a second `delete`.

## Not tried

Everything above was tried on 2026-11-24 with a custom role that was created for the purpose and
deleted afterwards. These were not run:

- `update` and `delete` of a default role, which the docs say is not possible for `delete`;
- `delete` of a role that users still have.
