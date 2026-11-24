# Subscribers

- **Access:** `tines.cases.subscribers`
- **Import:** `from tapi.cases import Subscribers`
- **Part of:** [Cases](cases.md)

The users that follow a case.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the subscribers of a case. | `GET /api/v2/cases/{case_id}/subscribers` |
| [`create`](#create) | Subscribe a user to a case. | `POST /api/v2/cases/{case_id}/subscribers` |
| [`batch_create`](#batch_create) | Subscribe several users to a case. | `POST /api/v2/cases/{case_id}/subscribers/batch` |
| [`delete`](#delete) | Unsubscribe a user from a case. | `DELETE /api/v2/cases/{case_id}/subscribers/{subscriber_id}` |

## Methods breakdown

### `list`

`GET /api/v2/cases/{case_id}/subscribers`

List the subscribers of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. Tines defaults to 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `case_id`, `subscribers`, the subscribers of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The case does not exist or is not visible to the key. |

### `create`

`POST /api/v2/cases/{case_id}/subscribers`

Subscribe a user to a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `user_email` | `str` | yes | — | The email address of the user to subscribe. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is an object with `case_id`, `id` and `user`. |
| 404 | The case does not exist or is not visible to the key. `user_email` is not a user. |

### `batch_create`

`POST /api/v2/cases/{case_id}/subscribers/batch`

Subscribe several users to a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `user_emails` | `Sequence[str]` | yes | At most 50 addresses | The email addresses of the users to subscribe, at most 50. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is an object with `case_id` and `subscribers`, also for an empty list. |
| 400 | `user_emails` is not valid, for example it has too many addresses. |
| 404 | The case does not exist or is not visible to the key. An address is not a user. |

### `delete`

`DELETE /api/v2/cases/{case_id}/subscribers/{subscriber_id}`

Unsubscribe a user from a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `subscriber_id` | `int` | yes | — | The ID of the subscriber. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The case or the subscriber does not exist or is not visible to the key. |
