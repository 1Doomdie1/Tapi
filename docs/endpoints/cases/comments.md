# Comments

- **Access:** `tines.cases.comments`
- **Import:** `from tapi.cases import Comments`
- **Part of:** [Cases](cases.md)

The comments on a case, with reactions.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the comments of a case. | `GET /api/v2/cases/{case_id}/comments` |
| [`get`](#get) | Get a comment. | `GET /api/v2/cases/{case_id}/comments/{comment_id}` |
| [`create`](#create) | Add a comment to a case. | `POST /api/v2/cases/{case_id}/comments` |
| [`update`](#update) | Change a comment. | `PATCH /api/v2/cases/{case_id}/comments/{comment_id}` |
| [`delete`](#delete) | Delete a comment. | `DELETE /api/v2/cases/{case_id}/comments/{comment_id}` |
| [`add_reaction`](#add_reaction) | React to a comment. | `POST /api/v2/cases/{case_id}/comments/{comment_id}/reactions` |
| [`remove_reaction`](#remove_reaction) | Remove a reaction. | `DELETE /api/v2/cases/{case_id}/comments/{comment_id}/reactions` |

## Methods breakdown

### `list`

`GET /api/v2/cases/{case_id}/comments`

List the comments of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. Tines defaults to 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `case_id`, `comments`, the comments of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The case does not exist or is not visible to the key. |

### `get`

`GET /api/v2/cases/{case_id}/comments/{comment_id}`

Get a comment.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `comment_id` | `int` | yes | — | The ID of the comment. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the comment, with `case_id` added. |
| 404 | The case or the comment does not exist or is not visible to the key. |

### `create`

`POST /api/v2/cases/{case_id}/comments`

Add a comment to a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `value` | `str` | yes | — | The text of the comment, as Markdown. User mentions are written `<@user-2435>`. |
| `author_email` | `str` | no | — | The email address of the user who comments. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the created comment. |
| 404 | The case does not exist or is not visible to the key. |
| 422 | `value` is missing. |

### `update`

`PATCH /api/v2/cases/{case_id}/comments/{comment_id}`

Change a comment.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `comment_id` | `int` | yes | — | The ID of the comment. |
| `value` | `str` | yes | — | The new text of the comment, as Markdown. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated comment. |
| 404 | The case or the comment does not exist or is not visible to the key. |
| 422 | `value` is empty. |

### `delete`

`DELETE /api/v2/cases/{case_id}/comments/{comment_id}`

Delete a comment.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `comment_id` | `int` | yes | — | The ID of the comment. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The case or the comment does not exist or is not visible to the key. |

### `add_reaction`

`POST /api/v2/cases/{case_id}/comments/{comment_id}/reactions`

React to a comment.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `comment_id` | `int` | yes | — | The ID of the comment. |
| `value` | `Reaction` | yes | `+1`<br>`-1`<br>`eyes`<br>`heart`<br>`white_check_mark` | The reaction. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the comment with its `reactions`. |
| 404 | The case or the comment does not exist or is not visible to the key. |
| 422 | The reaction is not one of the supported values. |

### `remove_reaction`

`DELETE /api/v2/cases/{case_id}/comments/{comment_id}/reactions`

Remove a reaction.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `comment_id` | `int` | yes | — | The ID of the comment. |
| `value` | `Reaction` | yes | `+1`<br>`-1`<br>`eyes`<br>`heart`<br>`white_check_mark` | The reaction to remove. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The case or the comment does not exist or is not visible to the key. |
