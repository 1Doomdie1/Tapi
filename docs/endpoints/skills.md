# Skills

- **Access:** `tines.skills`
- **Import:** `from tapi.skills import Skills`

Skills that AI agents can load. A skill is found by its name and the ID of its team.

Every method returns a [`Response`](../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the skills, optionally of one team or by name. | `GET /api/v1/skills` |
| [`get`](#get) | Get a skill. | `GET /api/v1/skills/{skill_name}` |
| [`create`](#create) | Create a skill. | `POST /api/v1/skills` |
| [`update`](#update) | Change a skill. | `PATCH /api/v1/skills/{skill_name}` |
| [`delete`](#delete) | Delete a skill. | `DELETE /api/v1/skills/{skill_name}` |

## Methods breakdown

### `list`

`GET /api/v1/skills`

List the skills, optionally of one team or by name.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | no | — | Only skills owned by this team. |
| `search` | `str` | no | — | Only skills whose name contains this text, in any case. |
| `per_page` | `int` | no | Positive integer | The number of results per page. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `skills`, the skills of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | `team_id` does not exist. |

### `get`

`GET /api/v1/skills/{skill_name}`

Get a skill.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `skill_name` | `str` | yes | — | The name of the skill. Names are unique only within a team. |
| `team_id` | `int` | yes | — | The ID of the team that owns the skill. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the skill. |
| 400 | `team_id` is missing. |
| 404 | No skill has that name in the team, or the team does not exist. |

### `create`

`POST /api/v1/skills`

Create a skill.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | yes | — | The ID of the team that gets the skill. |
| `name` | `str` | yes | Lowercase letters, digits and hyphens, such as `triage-alerts`: up to 64 characters, no double hyphen and none at the end | The name of the skill. It is unique within the team. |
| `description` | `str` | yes | — | What the skill does and when to use it. AI agents match a task against it to decide whether to load the skill. It cannot be empty. |
| `body` | `str` | yes | — | The full instructions of the skill, as Markdown. Agents load it only after the description matches the task. It cannot be empty. |
| `license` | `str` | no | — | The license that the skill is distributed under, such as `Apache-2.0`. |
| `compatibility` | `str` | no | — | A free-text note on what the skill is compatible with. |
| `metadata` | `Mapping[str, str]` | no | — | A flat object of string keys and string values. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the created skill. |
| 404 | `team_id` does not exist. |
| 422 | The name is not valid, too long or taken in the team, a required field is empty, or `metadata` is not a flat object of strings. |

### `update`

`PATCH /api/v1/skills/{skill_name}`

Change a skill.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `skill_name` | `str` | yes | — | The current name of the skill. |
| `team_id` | `int` | yes | — | The ID of the team that owns the skill. It is sent in the body. |
| `name` | `str` | no | As for `create` | A new name. Tines also rewrites the name in every AI action that references the skill. |
| `description` | `str` | no | — | A new description. |
| `body` | `str` | no | — | New instructions, as Markdown. |
| `license` | `str` | no | — | A new license. |
| `compatibility` | `str` | no | — | A new compatibility note. |
| `metadata` | `Mapping[str, str]` | no | — | New metadata, which replaces the whole object, so include every key that should stay. An empty object clears it. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated skill, with `updated_at` moved and `created_at` kept. |
| 400 | `team_id` is missing. |
| 404 | No skill has that name in the team, or the team does not exist. |
| 422 | The name is not valid, too long or taken in the team, a required field is empty, or `metadata` is not a flat object of strings. |

### `delete`

`DELETE /api/v1/skills/{skill_name}`

Delete a skill.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `skill_name` | `str` | yes | — | The name of the skill. |
| `team_id` | `int` | yes | — | The ID of the team that owns the skill. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 400 | `team_id` is missing. |
| 404 | No skill has that name in the team, or the team does not exist. |
