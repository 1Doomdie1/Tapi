# Tags

- **Access:** `tines.tags`
- **Import:** `from tapi.tags import Tags`

Tags that classify content. A tag created after February 2025 belongs to a single team.

Every method returns a [`Response`](../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the tags that the key can access, optionally of one team. | `GET /api/v1/tags` |
| [`get`](#get) | Get a tag. | `GET /api/v1/tags/{tag_id}` |
| [`create`](#create) | Create a tag. | `POST /api/v1/tags` |
| [`update`](#update) | Update a tag. | `PATCH /api/v1/tags/{tag_id}` |
| [`delete`](#delete) | Delete a tag, or remove it from one team with `team_id`. | `DELETE /api/v1/tags/{tag_id}` |

## Methods breakdown

### `list`

`GET /api/v1/tags`

List the tags that the key can access, optionally of one team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | no | — | Only tags of this team. |
| `per_page` | `int` | no | 1 to 500 | Results per page. Tines defaults to 20 and caps it at 500. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. Tines defaults to 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `tags`, the tags of the page that your key has access to, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |

### `get`

`GET /api/v1/tags/{tag_id}`

Get a tag.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `tag_id` | `int` | yes | — | The ID of the tag to retrieve. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the tag. |
| 404 | The tag does not exist or the key has no access to it. |

### `create`

`POST /api/v1/tags`

Create a tag.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `name` | `str` | yes | — | The name of the tag. It must be unused. |
| `team_id` | `int` | yes | — | The ID of the team the tag belongs to. |
| `color` | `str` | yes | `purple`, `blue`, `gold`, `green`, `magenta`, `red`, `orange`, `mint`, or `#RRGGBB` | The color of the tag: a name or a `#RRGGBB` hex value. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the created tag. |
| 404 | `team_id` does not exist. |
| 422 | The name is in use, or the color is missing or not valid. |

### `update`

`PATCH /api/v1/tags/{tag_id}`

Update a tag.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `tag_id` | `int` | yes | — | The ID of the tag to update. |
| `name` | `str` | no | — | The new name of the tag. |
| `color` | `str` | no | `purple`, `blue`, `gold`, `green`, `magenta`, `red`, `orange`, `mint`, or `#RRGGBB` | The color of the tag: a name or a `#RRGGBB` hex value. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated tag. |
| 404 | The tag does not exist or the key has no access to it. |
| 422 | The name is in use, or the color is not valid. |

### `delete`

`DELETE /api/v1/tags/{tag_id}`

Delete a tag, or remove it from one team with `team_id`.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `tag_id` | `int` | yes | — | The ID of the tag to delete. |
| `team_id` | `int` | no | — | Remove the tag from this team only. Without it the tag is deleted entirely. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The tag does not exist or the key has no access to it. `team_id` does not exist. |
