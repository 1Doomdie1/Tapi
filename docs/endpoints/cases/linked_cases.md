# LinkedCases

- **Access:** `tines.cases.linked_cases`
- **Import:** `from tapi.cases import LinkedCases`
- **Part of:** [Cases](cases.md)

The cases that are linked to a case. A link goes from both cases.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the cases linked to a case. | `GET /api/v2/cases/{case_id}/linked_cases` |
| [`create`](#create) | Link a case to another. | `POST /api/v2/cases/{case_id}/linked_cases` |
| [`batch_create`](#batch_create) | Link a case to several others. | `POST /api/v2/cases/{case_id}/linked_cases/batch` |
| [`delete`](#delete) | Unlink a case. | `DELETE /api/v2/cases/{case_id}/linked_cases/{linked_case_id}` |

## Methods breakdown

### `list`

`GET /api/v2/cases/{case_id}/linked_cases`

List the cases linked to a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. Tines defaults to 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `case_id`, `name`, `linked_cases`, the linked cases of the page, and `meta`. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The case does not exist or is not visible to the key. |

### `create`

`POST /api/v2/cases/{case_id}/linked_cases`

Link a case to another.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case that gets the link. |
| `id` | `int` | yes | — | The ID of the case to link to it. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is an object with the `case_id` and `name` of the case and the `linked_case`. |
| 404 | The case does not exist or is not visible to the key. |

### `batch_create`

`POST /api/v2/cases/{case_id}/linked_cases/batch`

Link a case to several others.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case that gets the links. |
| `ids` | `Sequence[int]` | yes | At most 150 IDs | The IDs of the cases to link. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is an object with `case_id`, `name` and the `linked_cases`, also for an empty list and for cases that are linked already. |
| 404 | The case does not exist or is not visible to the key. A case to link does not exist. |

### `delete`

`DELETE /api/v2/cases/{case_id}/linked_cases/{linked_case_id}`

Unlink a case. The link is removed from both cases.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `linked_case_id` | `int` | yes | — | The ID of the linked case to remove. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The case or the linked case does not exist or is not visible to the key. |
