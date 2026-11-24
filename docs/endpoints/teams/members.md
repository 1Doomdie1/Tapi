# Members

- **Access:** `tines.teams.members`
- **Import:** `from tapi.teams import Members`
- **Part of:** [Teams](teams.md)

The members of a team: list them, invite users, resend invitations and remove users.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the members of a team. | `GET /api/v1/teams/{team_id}/members` |
| [`invite`](#invite) | Invite a user to a team. | `POST /api/v1/teams/{team_id}/invite_member` |
| [`resend_invitation`](#resend_invitation) | Resend the invitation to a team. | `POST /api/v1/teams/{team_id}/resend_invitation` |
| [`remove`](#remove) | Remove a user from a team. | `POST /api/v1/teams/{team_id}/remove_member` |

## Methods breakdown

### `list`

`GET /api/v1/teams/{team_id}/members`

List the members of a team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | yes | — | The ID of the team. |
| `per_page` | `int` | no | Positive integer | The number of results per page. Tines defaults to 20 and caps it at 500. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. Tines defaults to 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `members`, the members of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The team does not exist or the key has no access to it. |

### `invite`

`POST /api/v1/teams/{team_id}/invite_member`

Invite a user to a team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | yes | — | The ID of the team. |
| `email` | `str` | no | — | The email address of the user to invite. |
| `user_id` | `int` | no | — | The ID of an existing user in the tenant. |
| `role` | `str` | no | A default role, such as `TEAM_ADMIN` or `VIEWER`, or a custom role | The role the user gets on the team. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the invited member. |
| 404 | The team does not exist or the key has no access to it. `user_id` does not exist. |

### `resend_invitation`

`POST /api/v1/teams/{team_id}/resend_invitation`

Resend the invitation to a team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | yes | — | The ID of the team. |
| `user_id` | `int` | yes | — | The ID of the user to invite again. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the invited user, with the fields of a member except `role`. |
| 404 | The team does not exist or the key has no access to it. The user does not exist. |

### `remove`

`POST /api/v1/teams/{team_id}/remove_member`

Remove a user from a team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | yes | — | The ID of the team. |
| `user_id` | `int` | yes | — | The ID of the user to remove. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `deleted_id`, the ID of the removed membership. |
| 404 | The team does not exist or the key has no access to it. The user does not exist. |
