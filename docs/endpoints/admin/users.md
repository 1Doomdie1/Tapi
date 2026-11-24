# Users

- **Access:** `tines.admin.users`
- **Import:** `from tapi.admin import Users`
- **Part of:** [Admin](admin.md)

Manage the users of the tenant: list, read, create, update and delete them, read their sign-in activity, resend an invitation and end their sessions.

> **Careful:** `create` is an upsert by email address: calling it with the address of an existing user overwrites that user instead of failing.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the users, optionally only the tenant owners or those that match a search. | `GET /api/v1/admin/users` |
| [`get`](#get) | Get a user by ID or email address. | `GET /api/v1/admin/users/{user_id}` |
| [`create`](#create) | Create a user. | `POST /api/v1/admin/users` |
| [`update`](#update) | Change a user. | `PATCH /api/v1/admin/users/{user_id}` |
| [`delete`](#delete) | Delete a user. | `DELETE /api/v1/admin/users/{user_id}` |
| [`list_signin_activities`](#list_signin_activities) | List the sign-ins of a user, a subset of the audit logs. | `GET /api/v1/admin/users/{user_id}/signin_activities` |
| [`resend_invitation`](#resend_invitation) | Resend the invitation to the platform to a user. | `POST /api/v1/admin/users/{user_id}/resend_invitation` |
| [`expire_session`](#expire_session) | Sign a user out of the tenant on all devices. | `POST /api/v1/admin/users/{user_id}/expire_session` |

## Methods breakdown

### `list`

`GET /api/v1/admin/users`

List the users, optionally only the tenant owners or those that match a search.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `filter` | `UserFilter` | no | `TENANT_OWNER` | Lists only the tenant owners. |
| `search` | `str` | no | — | Only users whose name or email contains this text, in any case. |
| `include` | `UserInclude` | no | `team_memberships` | Adds the teams of each user. |
| `per_page` | `int` | no | 1 to 500 | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `admin/users`, the users of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 422 | `filter` is not a valid value. |

### `get`

`GET /api/v1/admin/users/{user_id}`

Get a user by ID or email address.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `user_id` | `int \| str` | yes | User ID, or email address | The ID or the email address of the user. |
| `include` | `UserInclude` | no | `team_memberships` | Adds the teams of the user. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the user. |
| 404 | The user does not exist. |

### `create`

`POST /api/v1/admin/users`

Create a user. An email address that already belongs to a user updates that user instead of failing.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `email` | `str` | yes | — | The email address of the user. |
| `first_name` | `str` | no | — | The first name. |
| `last_name` | `str` | no | — | The last name. |
| `admin` | `bool` | no | `True`, `False` | Whether the user is a tenant owner. |
| `tenant_permissions` | `Sequence[str]` | no | — | The tenant permissions to grant, such as `AUDIT_LOG_READ`. |
| `is_active` | `bool` | no | `True`, `False` | Whether the user is active. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the created user. |
| 422 | The email address is missing or not valid, or a tenant permission does not exist. |

### `update`

`PATCH /api/v1/admin/users/{user_id}`

Change a user. Only the arguments that are passed are sent.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `user_id` | `int` | yes | — | The ID of the user. |
| `email` | `str` | no | — | A new email address. |
| `first_name` | `str` | no | — | A new first name. |
| `last_name` | `str` | no | — | A new last name. |
| `admin` | `bool` | no | `True`, `False` | Whether the user is a tenant owner. |
| `tenant_permissions` | `Sequence[str]` | no | — | The tenant permissions, which replace the old ones. |
| `is_active` | `bool` | no | `True`, `False` | Whether the user is active. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated user. |
| 404 | The user does not exist. |

### `delete`

`DELETE /api/v1/admin/users/{user_id}`

Delete a user.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `user_id` | `int` | yes | — | The ID of the user. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | The user is deleted. No data. |
| 404 | The user does not exist. |

### `list_signin_activities`

`GET /api/v1/admin/users/{user_id}/signin_activities`

List the sign-ins of a user, a subset of the audit logs.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `user_id` | `int` | yes | — | The ID of the user. |
| `before` | `datetime \| str` | no | ISO 8601 string, or `datetime` | Only sign-ins before this time. A datetime without a timezone is treated as UTC. |
| `after` | `datetime \| str` | no | ISO 8601 string, or `datetime` | Only sign-ins after this time. |
| `per_page` | `int` | no | 1 to 500 | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `admin/login_activities`, the sign-ins of the page, and `meta`. |
| 400 | `per_page` or `page` is not a positive integer. |
| 422 | `before` or `after` cannot be read. |

### `resend_invitation`

`POST /api/v1/admin/users/{user_id}/resend_invitation`

Resend the invitation to the platform to a user.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `user_id` | `int` | yes | — | The ID of the user. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an empty object, or has a `message` when the user already accepted the invitation. |
| 404 | The user does not exist. |

### `expire_session`

`POST /api/v1/admin/users/{user_id}/expire_session`

Sign a user out of the tenant on all devices.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `user_id` | `int` | yes | — | The ID of the user. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | The sessions are ended. No data. |
| 422 | The user does not exist. |
