# Roles

- **Access:** `tines.admin.roles`
- **Import:** `from tapi.admin import Roles`
- **Part of:** [Admin](admin.md)

Manage the roles of the tenant. A role is a set of permissions that a user can have in a team. Tines has default roles, such as `TEAM_ADMIN`, and a tenant can add custom roles.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the default and the custom roles. | `GET /api/v1/admin/roles` |
| [`get`](#get) | Get a role. | `GET /api/v1/admin/roles/{role_id}` |
| [`create`](#create) | Create a custom role. | `POST /api/v1/admin/roles` |
| [`update`](#update) | Change the description or the permissions of a custom role. | `PATCH /api/v1/admin/roles/{role_id}` |
| [`delete`](#delete) | Delete a custom role. | `DELETE /api/v1/admin/roles/{role_id}` |

## Methods breakdown

### `list`

`GET /api/v1/admin/roles`

List the default and the custom roles.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `admin/roles`, the roles of the page, and `meta`, the pagination details. |

### `get`

`GET /api/v1/admin/roles/{role_id}`

Get a role.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `role_id` | `str` | yes | — | The ID or the name of the role, default or custom. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the role. |
| 404 | The role does not exist. |

### `create`

`POST /api/v1/admin/roles`

Create a custom role.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `name` | `str` | yes | — | The name of the role. It must be unique among the custom roles. |
| `permissions` | `Sequence[str]` | yes | — | The names of the permissions to give the role, such as `STORY_CREATE`. It cannot be empty. |
| `description` | `str` | no | — | A description of the role. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the created role. |
| 422 | The name is taken by another custom role, a permission does not exist or the list is empty. |

### `update`

`PATCH /api/v1/admin/roles/{role_id}`

Change the description or the permissions of a custom role. The name cannot be changed.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `role_id` | `str` | yes | — | The ID or the name of a custom role. |
| `description` | `str` | no | — | A new description. |
| `permissions` | `Sequence[str]` | no | — | The permissions, which replace the old ones. It cannot be empty. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated role. |
| 404 | The role does not exist. |
| 422 | `permissions` is an empty list. |

### `delete`

`DELETE /api/v1/admin/roles/{role_id}`

Delete a custom role.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `role_id` | `str` | yes | — | The ID or the name of a custom role. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | The role is deleted. No data. |
| 404 | The role does not exist. |
