# Teams

- **Access:** `tines.teams`
- **Import:** `from tapi.teams import Teams`

Teams, which own stories and other content. List, create, rename and delete them, and manage their members.

Every method returns a [`Response`](../../responses.md).

## Sub-endpoints

| Class | Access | Description |
| --- | --- | --- |
| [`Members`](members.md) | `tines.teams.members` | The members of a team. |

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the teams, optionally of one scope. | `GET /api/v1/teams` |
| [`get`](#get) | Get a team. | `GET /api/v1/teams/{team_id}` |
| [`create`](#create) | Create a team. | `POST /api/v1/teams` |
| [`update`](#update) | Rename a team. | `PATCH /api/v1/teams/{team_id}` |
| [`delete`](#delete) | Delete a team. | `DELETE /api/v1/teams/{team_id}` |
| [`destroy_static_external_id`](#destroy_static_external_id) | Destroy the static external ID of a team. | `POST /api/v1/teams/{team_id}/destroy_static_external_id` |

## Methods breakdown

### `list`

`GET /api/v1/teams`

List the teams, optionally of one scope.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `scope` | `TeamScope` | no | `all`, `standard`, `personal_only` | Which teams to list: `standard` for shared teams, `personal_only` for personal teams or `all` for both. Tines defaults to `standard`. |
| `per_page` | `int` | no | Positive integer | The number of results per page. Tines defaults to 20 and caps it at 500. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. Tines defaults to 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `teams`, the teams of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 422 | `scope` is not a valid value. |

### `get`

`GET /api/v1/teams/{team_id}`

Get a team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | yes | — | The ID of the team to retrieve. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the team. |
| 404 | The team does not exist or the key has no access to it. |

### `create`

`POST /api/v1/teams`

Create a team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `name` | `str` | yes | — | The name of the team. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the created team. |

### `update`

`PATCH /api/v1/teams/{team_id}`

Rename a team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | yes | — | The ID of the team to update. |
| `name` | `str` | yes | — | The new name of the team. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated team. |
| 404 | The team does not exist or the key has no access to it. |

### `delete`

`DELETE /api/v1/teams/{team_id}`

Delete a team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | yes | — | The ID of the team to delete. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The team does not exist or the key has no access to it. |

### `destroy_static_external_id`

`POST /api/v1/teams/{team_id}/destroy_static_external_id`

Destroy the static external ID of a team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | yes | — | The ID of the team whose static external ID is destroyed. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | The request succeeded.. |
| 404 | The team does not exist or the key has no access to it. |
| 422 | The team has no static external ID. |
