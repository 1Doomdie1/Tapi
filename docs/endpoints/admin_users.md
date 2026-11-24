# Admin: users

The users of the tenant are a sub-area of [`admin`](admin.md), available as `tines.admin.users`, and
the class is `tapi.admin.Users`. Every method returns a [`Response`](../responses.md).

| Method                                    | HTTP route                                                |
| ----------------------------------------- | --------------------------------------------------------- |
| `list(...)`                               | `GET /api/v1/admin/users`                                 |
| `get(user_id=...)`                        | `GET /api/v1/admin/users/{user_id}`                       |
| `create(email=...)`                       | `POST /api/v1/admin/users`                                |
| `update(user_id=...)`                     | `PATCH /api/v1/admin/users/{user_id}`                     |
| `delete(user_id=...)`                     | `DELETE /api/v1/admin/users/{user_id}`                    |
| `list_signin_activities(user_id=..., ...)` | `GET /api/v1/admin/users/{user_id}/signin_activities`    |
| `resend_invitation(user_id=...)`          | `POST /api/v1/admin/users/{user_id}/resend_invitation`    |
| `expire_session(user_id=...)`             | `POST /api/v1/admin/users/{user_id}/expire_session`       |

## The user

| Field                | Meaning                                                                              |
| -------------------- | ------------------------------------------------------------------------------------ |
| `id`                 | The ID of the user.                                                                  |
| `scim_uid`           | The SCIM ID, or `null` for a user that did not come from SCIM.                       |
| `email`              | The email address.                                                                   |
| `first_name`         | The first name.                                                                      |
| `last_name`          | The last name.                                                                       |
| `admin`              | Whether the user is a tenant owner.                                                  |
| `is_active`          | Whether the user is active.                                                          |
| `tenant_permissions` | A list of tenant permission names, or `null` when the user has none granted.         |
| `last_seen`          | An ISO 8601 timestamp.                                                               |
| `created_at`         | An ISO 8601 timestamp.                                                               |
| `updated_at`         | An ISO 8601 timestamp.                                                               |
| `team_memberships`   | Only with `include="team_memberships"`: a list of objects with `team_id`, `team_name` and `role`. |

## `list()`

The endpoint is paginated, and one call returns one page; see [Pagination](../pagination.md).

| Parameter  | Type         | Meaning                                                                          |
| ---------- | ------------ | -------------------------------------------------------------------------------- |
| `filter`   | `UserFilter` | `TENANT_OWNER` to list only the tenant owners.                                   |
| `search`   | `str`        | Only users whose name or email contains this text, in any case.                  |
| `include`  | `UserInclude`| `team_memberships` to add the teams of each user.                                |
| `per_page` | `int`        | The number of results per page. Tines defaults to 20 and caps it at 500.         |
| `page`     | `int`        | The page to return, starting at 1. Tines defaults to 1.                          |

The value of `filter` is case-sensitive, and another one is a `422` that lists the values that the
server knows. A value of `include` that is not `team_memberships` is ignored.

`data` is an object with `admin/users`, the users of the page, and `meta`, the pagination details.

## `get()`

`user_id` is the ID of the user or the email address of the user. `include="team_memberships"` adds
the teams. A user that does not exist is a `404` with `['User not found']`.

## `create()` and `update()`

| Parameter            | Type              | Meaning                                                             |
| -------------------- | ----------------- | ------------------------------------------------------------------- |
| `email`              | `str`             | The email address. Required by `create`.                            |
| `first_name`         | `str`             | The first name.                                                     |
| `last_name`          | `str`             | The last name.                                                      |
| `admin`              | `bool`            | Whether the user is a tenant owner. Tines defaults to `False`.      |
| `tenant_permissions` | sequence of `str` | The tenant permissions, such as `AUDIT_LOG_READ`. `update` replaces the old ones. |
| `is_active`          | `bool`            | Whether the user is active. Tines defaults to `True`.               |

`update` also takes `user_id`, and every other argument is optional. The Tines docs show it as `PUT`,
and the OpenAPI document lists `PUT` and `PATCH`, and both worked. `False` is sent, not left out.
`data` is the user, and a call that sends only `user_id` is a `200`. `tenant_permissions` is `[]` when
none is granted, and `update` replaces the list.

`create` has a `201` status, and `data` is the user. `create` has two behaviors that need care:

- **It is an upsert by email address.** Creating a user with an address that a user already has is not
  an error: Tines answers `201` with the ID of that user and overwrites the fields that were sent. The
  match ignores the case of the address. Never call `create` with the address of a user that must
  stay as it is.
- **A refused call can still create the user.** A `422` for a permission that does not exist left the
  user behind, inactive. Check the list after such a call.

**Every new user gets a personal team, and `delete` does not remove it.** Creating a user also creates
a team for the user, listed by `tines.teams.list(scope="personal_only")`, with one story called `Your
first story`. After the user is deleted, the team stays, with no members, and so does its story. To remove
them, delete the story with `tines.stories.delete` first, because `tines.teams.delete` refuses a team
with contents (`422`, `['Cannot delete a team with contents']`). Deleting a story is not immediate, and
the team is refused again with `['Stories scheduled for deletion are being deleted. Please try again in
a few minutes.']` until it is done, so retry the team. Each call of `create` that made a new user
leaves one team, including a call that was refused with a `422` or a `404` but left the user behind.

## The other methods

- `delete(user_id=...)` has a `204` status at once, and the user is still listed for about half a
  minute, after which it is gone. A second `delete` is a `404`.
- `list_signin_activities(user_id=..., before=..., after=..., per_page=..., page=...)` lists the
  sign-ins of a user, a subset of the audit logs. `before` and `after` take a `datetime` or an ISO 8601
  string. `data` is an object with `admin/login_activities` and `meta`, and a sign-in has `id`,
  `user_id`, `ip`, `user_agent` and `created_at`.
- `resend_invitation(user_id=...)` has a `200` status, and `data` is an empty object, or has a
  `message` when the user already accepted the invitation.
- `expire_session(user_id=...)` signs the user out on every device. The reply has a `200` status and
  no data, where the docs and the OpenAPI document say `204`. The Tines docs say `DELETE` in the
  request section of the page and use `POST` in the example. The OpenAPI document says `POST`, and
  `POST` is the one that works: `DELETE` is a `404`.

## Errors

| Status | When                                                                                          |
| ------ | --------------------------------------------------------------------------------------------- |
| `400`  | `list` and `list_signin_activities` with a `per_page` or `page` that is not a positive integer (`['Invalid per_page: 0. per_page must be a positive integer.']`). |
| `404`  | `get`, `update`, `delete` and `resend_invitation` with a user that does not exist (`['User not found']`). |
| `422`  | `list` with a `filter` that is not valid, and `list_signin_activities` with a `before` or `after` that cannot be read. `data` is a list holding an object that names the parameter. `create` with an email address that is missing or not valid (`['Validation failed: Email is not a valid email address']`) and with a permission that does not exist (`['Validation failed: Tenant permissions contains invalid permissions: NOT_A_PERMISSION']`). `expire_session` with a user that does not exist is also a `422`, not a `404` (`['User with ID ... not found.']`). |

`list_signin_activities` for a user that does not exist is a `200` with an empty list, not a `404`.

## Not tried

Everything above was tried on 2026-11-24 with a user that was created for the purpose with an
`example.invalid` address, and deleted afterwards. The two users of the tenant were not touched. These
were not seen:

- whether `create` or `resend_invitation` sends an email, which an address that cannot be delivered to
  cannot show;
- `update` with `admin` set to `True`, and a user that has signed in, so a sign-in activity with
  values from this route;
- what `delete` does with the stories and the other content of a user, and a user from SCIM.
