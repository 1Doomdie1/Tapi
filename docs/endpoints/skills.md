# Skills

A skill is a set of instructions that AI agents can load. Agents are shown only the `name` and the
`description` of a skill, and match a task against them to decide whether to load it. The `body`, the
full instructions, is loaded only after that. The module is available as `tines.skills`, and the
class is `tapi.skills.Skills`. Every method returns a [`Response`](../responses.md).

A skill belongs to a team, and its name is unique only within the team. So a skill is found by its
name and the ID of its team, and `get`, `update` and `delete` take both.

| Method                                  | HTTP route                                 |
| --------------------------------------- | ------------------------------------------ |
| `list(...)`                             | `GET /api/v1/skills`                       |
| `get(skill_name=..., team_id=...)`      | `GET /api/v1/skills/{skill_name}`          |
| `create(team_id=..., name=..., description=..., body=...)` | `POST /api/v1/skills`   |
| `update(skill_name=..., team_id=...)`   | `PATCH /api/v1/skills/{skill_name}`        |
| `delete(skill_name=..., team_id=...)`   | `DELETE /api/v1/skills/{skill_name}`       |

## The skill

A skill, as listed by `list` and returned by the other methods, has:

| Field           | Meaning                                                                                  |
| --------------- | ---------------------------------------------------------------------------------------- |
| `name`          | The name: lowercase letters and digits with hyphens, such as `triage-alerts`. See below. |
| `description`   | What the skill does and when to use it.                                                  |
| `body`          | The full instructions, as Markdown.                                                      |
| `license`       | The license that the skill is distributed under, or `null`.                              |
| `compatibility` | A free-text note on what the skill is compatible with, or `null`.                        |
| `metadata`      | A flat object of string keys and string values, empty when none is set.                  |
| `team_id`       | The ID of the team that owns the skill.                                                  |
| `created_at`    | An ISO 8601 timestamp.                                                                   |
| `updated_at`    | An ISO 8601 timestamp.                                                                   |

A name has at most 64 characters, and Tines refused upper case, underscores, spaces, characters that
are not ASCII, a double hyphen and a hyphen at the end. `create` leaves `license` and `compatibility`
as `null` when they are not sent, and `metadata` as an empty object.

## `list()`

Lists the skills that the key has access to. The endpoint is paginated, and one call returns one
page; see [Pagination](../pagination.md).

All parameters are optional and keyword-only. Parameters left as `None` are not sent.

| Parameter  | Type  | Meaning                                                                   |
| ---------- | ----- | ------------------------------------------------------------------------- |
| `team_id`  | `int` | Only skills owned by this team.                                           |
| `search`   | `str` | Only skills whose name contains this text, in any case.                   |
| `per_page` | `int` | The number of results per page. Tines defaults to 20 and caps it at 500.  |
| `page`     | `int` | The page to return, starting at 1. Tines defaults to 1.                   |

`data` is an object with `skills`, the skills of the page, and `meta`, the pagination details:
`current_page`, `previous_page` and `next_page` (links), `next_page_number`, `per_page`, `pages` and
`count`.

## `get()` and `delete()`

| Parameter    | Type  | Meaning                                                      |
| ------------ | ----- | ------------------------------------------------------------ |
| `skill_name` | `str` | The name of the skill.                                       |
| `team_id`    | `int` | The ID of the team that owns the skill. Sent in the query.   |

`get` returns the skill. `delete` has a `204` status and no data, and a second `delete` of the same
skill is a `404`.

## `create()`

| Parameter       | Type                | Meaning                                                                     |
| --------------- | ------------------- | --------------------------------------------------------------------------- |
| `team_id`       | `int`               | The ID of the team that gets the skill. Required.                           |
| `name`          | `str`               | The name of the skill. It is unique within the team. Required.              |
| `description`   | `str`               | What the skill does and when to use it. Required, and not empty.            |
| `body`          | `str`               | The full instructions, as Markdown. Required, and not empty.                |
| `license`       | `str`               | The license that the skill is distributed under, such as `Apache-2.0`.      |
| `compatibility` | `str`               | A free-text note on what the skill is compatible with.                      |
| `metadata`      | mapping of `str` to `str` | A flat object of string keys and string values.                       |

The reply has a `201` status, and `data` is the created skill.

```python
response = tines.skills.create(
    team_id=42,
    name="triage-alerts",
    description="Triage inbound security alerts. Use when a new alert needs a severity assessment.",
    body="# Triage alerts\n\nStart by checking the alert severity.",
    license="Apache-2.0",
    metadata={"source_repo": "runbooks"},
)
```

## `update()`

Changes a skill. Only what is sent changes, and what is left out keeps its value. The skill has to
exist: a name that no skill has is a `404`, and `create` adds a new one. The Tines docs show this
operation as `PUT`. The OpenAPI document lists it under `PUT` and `PATCH`, and tapi uses `PATCH`.

| Parameter       | Type                | Meaning                                                                     |
| --------------- | ------------------- | --------------------------------------------------------------------------- |
| `skill_name`    | `str`               | The current name of the skill. Required.                                    |
| `team_id`       | `int`               | The ID of the team that owns the skill. Required, and sent in the body.     |
| `name`          | `str`               | A new name. Tines also rewrites it in every AI action that references the skill. |
| `description`   | `str`               | A new description.                                                          |
| `body`          | `str`               | New instructions.                                                           |
| `license`       | `str`               | A new license.                                                              |
| `compatibility` | `str`               | A new compatibility note.                                                   |
| `metadata`      | mapping of `str` to `str` | New metadata. It replaces the whole object, so include every key that should stay. An empty mapping is sent, and clears it. |

`data` is the updated skill, with `updated_at` moved and `created_at` kept. A call that sends only
`team_id` is a `200` and changes nothing. A rename takes effect at once: the old name is a `404`
afterwards. `PUT`, which the Tines docs show, worked as well as `PATCH`.

tapi cannot send `null`, so `license` and `compatibility` cannot be set back to `null`. An empty
string is accepted for them and stored as an empty string. An empty `metadata` object clears the
metadata, since it replaces the whole object.

## Errors

| Status | When                                                                                          |
| ------ | --------------------------------------------------------------------------------------------- |
| `400`  | `get`, `update` and `delete` without a `team_id` (`['team_id is required']`; the OpenAPI document says `team_id is missing.`). `list` with a `per_page` or `page` that is not a positive integer (`['Invalid per_page: 0. per_page must be a positive integer.']`). |
| `404`  | `list` or `create` with a `team_id` that does not exist (`['Team not found']`). `get`, `update` and `delete` with a name that no skill has in the team, or with a team that does not exist (`['Skill not found']`). |
| `422`  | `create` or `update` with a name that is not valid (`['Validation failed: Name must be lowercase alphanumeric with hyphens']`), longer than 64 characters (`['Validation failed: Name is too long (maximum is 64 characters)']`) or already taken in the team (`['Validation failed: Name has already been taken']`). `create` with a `description` or `body` that is empty (`["Validation failed: Description can't be blank"]`) and with `metadata` that is not a flat object of strings (`['Validation failed: Metadata must be a flat string-to-string map']`). A required field that is missing is also a `422`, as a list holding an object such as `{'body': 'Expected value to not be null'}`. |

## Not tried

Everything above was tried on 2026-11-23 with skills that were created for the purpose and deleted
afterwards, in a tenant that had none. These were not seen:

- a name that starts with a hyphen, and the rename of a skill that an AI action references, which
  Tines says rewrites the name in that action;
- a body or a description of a large size, and a key that has access to only some teams.
