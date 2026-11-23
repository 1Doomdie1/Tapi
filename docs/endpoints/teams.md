# Teams

Teams group users and the content they work on. The module is available as `tines.teams`, and the
class is `tapi.teams.Teams`. The members of a team are a sub-area, available as
`tines.teams.members` and as the class `tapi.teams.Members`. Every method returns a
[`Response`](../responses.md).

| Method                                                | HTTP route                                               |
| ----------------------------------------------------- | -------------------------------------------------------- |
| `list(...)`                                           | `GET /api/v1/teams`                                      |
| `get(team_id=...)`                                    | `GET /api/v1/teams/{team_id}`                            |
| `create(name=...)`                                    | `POST /api/v1/teams`                                     |
| `update(team_id=..., name=...)`                       | `PATCH /api/v1/teams/{team_id}`                          |
| `delete(team_id=...)`                                 | `DELETE /api/v1/teams/{team_id}`                         |
| `destroy_static_external_id(team_id=...)`             | `POST /api/v1/teams/{team_id}/destroy_static_external_id` |
| `members.list(team_id=..., ...)`                      | `GET /api/v1/teams/{team_id}/members`                    |
| `members.invite(team_id=..., ...)`                    | `POST /api/v1/teams/{team_id}/invite_member`             |
| `members.resend_invitation(team_id=..., user_id=...)` | `POST /api/v1/teams/{team_id}/resend_invitation`         |
| `members.remove(team_id=..., user_id=...)`            | `POST /api/v1/teams/{team_id}/remove_member`             |

All parameters are keyword-only. Parameters left as `None` are not sent. The Tines docs do not state
which key types or permissions these endpoints need. The OpenAPI document says that personal,
service, team and tenant owner keys are all accepted, and that a key without access to a resource
receives a 404.

## The team

`data` of `get`, `create` and `update` is a team, and `list` returns a list of them under `teams`. A
team has:

| Field    | Meaning                                                                               |
| -------- | ------------------------------------------------------------------------------------- |
| `id`     | The ID of the team.                                                                   |
| `name`   | The name of the team.                                                                 |
| `groups` | The groups of the team, as a list of objects with `id` and `name`. It can be empty.   |

The Tines docs show `groups` only in the replies of `get` and `list`, and describe `get` and
`delete` as acting on "a team or case group". The OpenAPI document gives every team reply the same
three fields, and so did the live tenant, `create` and `update` included.

## The member

`data` of `members.invite` is a member, and `members.list` returns a list of them under `members`.
A member has:

| Field                 | Meaning                                                                          |
| --------------------- | -------------------------------------------------------------------------------- |
| `id`                  | The ID of the user.                                                              |
| `first_name`          | The first name of the user.                                                      |
| `last_name`           | The last name of the user.                                                       |
| `email`               | The email address of the user.                                                   |
| `is_admin`            | Whether the user is an admin.                                                    |
| `created_at`          | When the user was created, as an ISO 8601 timestamp.                             |
| `last_seen`           | When the user was last seen, as an ISO 8601 timestamp, or `null`.                |
| `invitation_accepted` | Whether the user accepted the invitation to join the team.                       |
| `role`                | The role of the user on the team. See [Roles](#roles).                           |

The reply of `members.resend_invitation` has the same fields except `role`.

## `list()`

Paginated: one call returns one page; see [Pagination](../pagination.md). `data` holds `teams` and
`meta`.

| Parameter  | Type  | Meaning                                                                          |
| ---------- | ----- | -------------------------------------------------------------------------------- |
| `scope`    | `str` | Which teams to list: `standard`, `personal_only` or `all`. Tines defaults to `standard`. |
| `per_page` | `int` | Results per page. Tines defaults to 20 and caps it at 500.                       |
| `page`     | `int` | The page, starting at 1. Tines defaults to 1.                                    |

By default only standard teams, the shared ones, are listed. Personal teams are listed with
`scope="personal_only"` or `scope="all"`. The server accepts the values in either case.

Tines also accepts the deprecated parameters `include_personal_teams` and `include_drafts`, which
`scope` replaces. tapi does not offer them.

## `get()`

`team_id` is required. When no team with that ID is visible to the key, the reply is a `404` with
`['Team not found']`.

## `create()`

`name` is required, and the reply has a 201 status.

| Parameter | Type  | Meaning                  |
| --------- | ----- | ------------------------ |
| `name`    | `str` | The name of the team.    |

## `update()`

Renames a team. `team_id` and `name` are required. The Tines docs show this operation as `PUT`. The
OpenAPI document lists the same operation under `PUT` and `PATCH`, and tapi uses `PATCH`.

Neither source says whether `name` is required, because it is the only field. An update without it
was answered with a `500` on the live tenant and the team was left as it was, so tapi requires it.

## `delete()`

`team_id` is required. The reply has a 204 status and `data` is `None`.

## `destroy_static_external_id()`

Destroys the static external ID of a team. `team_id` is required and no body is sent. The Tines
docs say that the reply has a 200 status and that the body is the ID of the destroyed static
external ID, and show it as a bare number, `12`. The OpenAPI document describes the reply without a
body. Neither source says what a static external ID is or when a team has one. For a team that has
none, the reply is a `422` with `['Team static external ID not found']`. A successful call has not
been seen.

## `members.list()`

Paginated like `list`. `data` holds `members` and `meta`.

| Parameter  | Type  | Meaning                                                    |
| ---------- | ----- | ---------------------------------------------------------- |
| `team_id`  | `int` | The team. Required.                                        |
| `per_page` | `int` | Results per page. Tines defaults to 20 and caps it at 500. |
| `page`     | `int` | The page, starting at 1. Tines defaults to 1.              |

## `members.invite()`

Invites a user to a team. `team_id` is required. Give either `email` or `user_id`, but not both.
Tines enforces that, so tapi sends whatever it is given and returns the reply.

| Parameter | Type  | Meaning                                                                      |
| --------- | ----- | ---------------------------------------------------------------------------- |
| `team_id` | `int` | The team. Required.                                                          |
| `email`   | `str` | The email address of the user to invite.                                     |
| `user_id` | `int` | The ID of an existing user in the tenant.                                    |
| `role`    | `str` | The role the user gets on the team. See [Roles](#roles).                     |

`data` is the invited member.

## `members.resend_invitation()`

Resends the invitation to a user. `team_id` and `user_id` are required. `data` is the user, with the
fields of a member except `role`. When no user has that ID, the reply is a `404` with
`['User not found']`.

## `members.remove()`

Removes a user from a team. `team_id` and `user_id` are required. The reply has a 200 status and
`data` is an object with `deleted_id`, which the OpenAPI document calls the ID of the removed
membership. When no user has that ID, the reply is a `404` with `['User not found']`.

## Roles

`role` is a string. Tines accepts default and custom roles and does not list the allowed values. The
samples in the Tines docs show `TEAM_ADMIN` and `VIEWER`, and every member found on the live tenant
had `TEAM_ADMIN`. The docs link to a page about team roles, which was not read.

## Errors

| Status | When                                                                                       |
| ------ | ------------------------------------------------------------------------------------------ |
| `400`  | The OpenAPI document lists it for `list` and `members.list`: a malformed request or a parameter that failed validation. |
| `404`  | The team does not exist or the key has no access to it (`['Team not found']`), or the user of `members.resend_invitation` or `members.remove` does not exist (`['User not found']`). |
| `422`  | A value is invalid, such as an unknown `scope`, in which case `data` is a list of objects naming the field. Also `destroy_static_external_id` for a team without one (`['Team static external ID not found']`). |
| `500`  | An update without a `name`. tapi always sends one.                                         |

Neither source documents error responses for the other methods.
