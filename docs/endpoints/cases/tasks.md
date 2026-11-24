# Tasks

- **Access:** `tines.cases.tasks`
- **Import:** `from tapi.cases import Tasks`
- **Part of:** [Cases](cases.md)

The tasks of a case.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the tasks of a case. | `GET /api/v2/cases/{case_id}/tasks` |
| [`get`](#get) | Get a task. | `GET /api/v2/cases/{case_id}/tasks/{task_id}` |
| [`create`](#create) | Add a task to a case. | `POST /api/v2/cases/{case_id}/tasks` |
| [`batch_create`](#batch_create) | Add several tasks to a case. | `POST /api/v2/cases/{case_id}/tasks/batch` |
| [`update`](#update) | Change a task. | `PATCH /api/v2/cases/{case_id}/tasks/{task_id}` |
| [`delete`](#delete) | Delete a task. | `DELETE /api/v2/cases/{case_id}/tasks/{task_id}` |

## Methods breakdown

### `list`

`GET /api/v2/cases/{case_id}/tasks`

List the tasks of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. Tines defaults to 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `tasks`, the tasks of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The case does not exist or is not visible to the key. |

### `get`

`GET /api/v2/cases/{case_id}/tasks/{task_id}`

Get a task.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `task_id` | `int` | yes | — | The ID of the task. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `task`. |
| 404 | The case or the task does not exist or is not visible to the key. |

### `create`

`POST /api/v2/cases/{case_id}/tasks`

Add a task to a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `description` | `str` | yes | — | The description of the task. |
| `assignee_emails` | `Sequence[str]` | no | — | The email addresses of the users to assign. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is an object with `task`. |
| 400 | An assignee is not a user. |
| 404 | The case does not exist or is not visible to the key. |
| 422 | The description is blank. |

### `batch_create`

`POST /api/v2/cases/{case_id}/tasks/batch`

Add several tasks to a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `tasks` | [`Sequence[TaskInput]`](#taskinput) | yes | At most 25 tasks | The tasks to add. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is an object with `tasks`, the created tasks. |
| 400 | `tasks` is empty or has more than 25 tasks, or an assignee is not a user. |
| 404 | The case does not exist or is not visible to the key. |

### `update`

`PATCH /api/v2/cases/{case_id}/tasks/{task_id}`

Change a task.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `task_id` | `int` | yes | — | The ID of the task. |
| `description` | `str` | no | — | A new description. |
| `completed` | `bool` | no | `True`, `False` | Whether the task is completed. |
| `assignee_emails` | `Sequence[str]` | no | — | The email addresses of the users to assign. They replace the assignees of the task. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `task`. |
| 404 | The case or the task does not exist or is not visible to the key. |

### `delete`

`DELETE /api/v2/cases/{case_id}/tasks/{task_id}`

Delete a task.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `task_id` | `int` | yes | — | The ID of the task. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The case or the task does not exist or is not visible to the key. |

## Types

### `TaskInput`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `description` | `str` | yes | — | The description of the task. |
| `assignee_emails` | `Sequence[str]` | no | — | The email addresses of the users to assign. |
