# Activities

- **Access:** `tines.cases.activities`
- **Import:** `from tapi.cases import Activities`
- **Part of:** [Cases](cases.md)

The activity log of a case: the changes made to it.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the activities of a case. | `GET /api/v2/cases/{case_id}/activities` |
| [`get`](#get) | Get an activity of a case. | `GET /api/v2/cases/{case_id}/activities/{activity_id}` |

## Methods breakdown

### `list`

`GET /api/v2/cases/{case_id}/activities`

List the activities of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `activity_types` | `Sequence[ActivityType]` | no | `CREATED`, `ASSIGNED`, `UNASSIGNED`, `STATUS_UPDATED`, `SUB_STATUS_UPDATED`, `SEVERITY_UPDATED`, `COMMENTED`, `DELETED_COMMENT`, `COMMENT_UPDATED`, `DESCRIPTION_UPDATED`, `FIELD_UPDATED`, `FILE_ATTACHED`, `FILE_ATTACHED_AND_COMMENTED`, `FILE_DELETED`, `TAGS_ADDED`, `TAGS_REMOVED`, `RECORD_RESULT_SET_ADDED`, `RECORD_RESULT_SET_REMOVED`, `CHECKLIST_ITEM_COMPLETED`, `CHECKLIST_ITEM_INCOMPLETE`, `LINKED_CASE_ADDED`, `LINKED_CASE_REMOVED`, `METADATA_UPDATED`, `NOTE_ADDED`, `NOTE_DELETED`, `NOTE_UPDATED`, `SLA_WARNING`, `SLA_EXCEEDED`, `TASK_CREATED`, `TASK_DELETED`, `TASK_COMPLETED`, `TASK_INCOMPLETE`, `TASK_UPDATED`, `TASK_ASSIGNED`, `TASK_UNASSIGNED`, `TEAM_UPDATED`, `TITLE_UPDATED` | Only activities of these types. |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |
| `resolve_mentions` | `bool` | no | `True`, `False` | Replaces user mentions with display names. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `case_id`, `activities`, the activities of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The case does not exist or is not visible to the key. |
| 422 | A value is not valid. |

### `get`

`GET /api/v2/cases/{case_id}/activities/{activity_id}`

Get an activity of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `activity_id` | `int` | yes | — | The ID of the activity. |
| `resolve_mentions` | `bool` | no | `True`, `False` | Replaces user mentions with display names. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the activity, with `case_id` added. |
| 404 | The case or the activity does not exist or is not visible to the key. |
