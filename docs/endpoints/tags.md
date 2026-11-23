# Tags

Tags classify content in Tines. The module is available as `tines.tags`, and the class is
`tapi.tags.Tags`. Every method returns a [`Response`](../responses.md).

| Method                          | HTTP route                      |
| ------------------------------- | ------------------------------- |
| `list(...)`                     | `GET /api/v1/tags`              |
| `get(tag_id=...)`               | `GET /api/v1/tags/{tag_id}`     |
| `create(name=..., team_id=..., color=...)` | `POST /api/v1/tags`  |
| `update(tag_id=..., ...)`       | `PATCH /api/v1/tags/{tag_id}`   |
| `delete(tag_id=..., ...)`       | `DELETE /api/v1/tags/{tag_id}`  |

All parameters are keyword-only. Parameters left as `None` are not sent. The Tines docs do not state
which key types or permissions these endpoints need. The OpenAPI document says that personal,
service, team and tenant owner keys are all accepted, and that a key without access to a resource
receives a 404.

The OpenAPI document shows stories being tagged by name, not by tag ID: with `tags` when a story is
created, with `add_tag_names` and `remove_tag_names` when one is updated, and with `tags[]` when
stories are listed. Those parameters belong to the stories module.

## The tag

`data` of `get`, `create` and `update` is a tag, and `list` returns a list of them under `tags`. A
tag has:

| Field        | Meaning                                                                                 |
| ------------ | --------------------------------------------------------------------------------------- |
| `id`         | The ID of the tag.                                                                      |
| `name`       | The name of the tag.                                                                    |
| `color`      | The color of the tag, as a `#RRGGBB` hex value. See [Colors](#colors).                  |
| `teams`      | The teams the tag belongs to, as a list of objects with `id` and `name`.                |
| `created_at` | When the tag was created, as an ISO 8601 timestamp.                                     |
| `updated_at` | When the tag was last updated, as an ISO 8601 timestamp.                                |

The Tines docs say that a tag created after February 2025 belongs to a single team.

## `list()`

Paginated: one call returns one page; see [Pagination](../pagination.md). `data` holds `tags`, the
tags your key has access to, and `meta`.

| Parameter  | Type  | Meaning                                                    |
| ---------- | ----- | ---------------------------------------------------------- |
| `team_id`  | `int` | Only tags of this team.                                    |
| `per_page` | `int` | Results per page. Tines defaults to 20 and caps it at 500. |
| `page`     | `int` | The page, starting at 1. Tines defaults to 1.              |

## `get()`

`tag_id` is required. When no tag with that ID is visible to the key, the reply is a `404` with
`['Tag not found']`.

## `create()`

`name`, `team_id` and `color` are required, and the reply has a 201 status. The Tines docs do not
say which parameters are required, and the OpenAPI document requires `name` and `team_id` only.
Tines refuses a tag without a `color`, so tapi requires it too.

| Parameter | Type  | Meaning                                                      |
| --------- | ----- | ------------------------------------------------------------ |
| `name`    | `str` | The name of the tag. Required. It must not be in use.        |
| `team_id` | `int` | The team the tag belongs to. Required.                       |
| `color`   | `str` | The color of the tag. Required. See [Colors](#colors).       |

Creating a tag whose name is already used by a tag of the same team is a `422` with
`['Tag <name> already exists.']`. Whether the same name can be used in another team has not been
tried.

## `update()`

`tag_id` is required. `name` and `color` are optional, and the Tines docs mark both as optional.
Without either of them nothing changes and the reply is the tag. The team of a tag cannot be
changed: `update` does not accept a `team_id`.

The Tines docs show this operation as `PUT`. The OpenAPI document lists the same operation under
`PUT` and `PATCH`, and tapi uses `PATCH`.

## `delete()`

`tag_id` is required. The reply has a 204 status and `data` is `None`.

| Parameter | Type  | Meaning                                                                   |
| --------- | ----- | ------------------------------------------------------------------------- |
| `tag_id`  | `int` | The tag to delete. Required.                                              |
| `team_id` | `int` | Remove the tag from this team only. Without it the tag is deleted entirely. |

The Tines docs list `team_id` as a query parameter, but their sample sends it in a JSON body. The
OpenAPI document says query parameter. Tines reads it from both, and tapi sends it in the query.

With a `team_id` of a team that does not exist, the reply is a `404` with `['Team not found']` and
the tag is kept. A tag was also deleted entirely when `team_id` was another team that exists but
that the tag did not belong to, so `team_id` does not protect a tag from being deleted. A tag
created after February 2025 belongs to one team, so removing it from its team and deleting it come
to the same thing, and removing a tag from one of several teams has not been tried.

## Colors

`color` is a string: one of the eight names below, or a `#RRGGBB` hex value. Tines returns the
color as a hex value:

| Name      | Hex       |
| --------- | --------- |
| `purple`  | `#8D75E6` |
| `blue`    | `#4BBFFF` |
| `gold`    | `#FABE25` |
| `green`   | `#6DD888` |
| `magenta` | `#DF99FF` |
| `red`     | `#FF8888` |
| `orange`  | `#FAA666` |
| `mint`    | `#4DDBBB` |

A hex value is returned in the case it was sent in. `#fff` and `ff0000` are refused, so a hex value
needs the `#` and six digits.

## Errors

| Status | When                                                                                       |
| ------ | ------------------------------------------------------------------------------------------ |
| `400`  | A pagination parameter is invalid. `data` is a list of messages.                           |
| `404`  | The tag does not exist or the key has no access to it (`['Tag not found']`), or a `team_id` names an unknown team (`['Team not found']`). |
| `422`  | A tag name is in use, or the color is missing, empty or not valid. `data` is a list of messages, or a list of objects naming the field. |
