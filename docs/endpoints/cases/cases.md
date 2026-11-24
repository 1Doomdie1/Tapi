# Cases

- **Access:** `tines.cases`
- **Import:** `from tapi.cases import Cases`

Cases track work that needs attention. Create, read, update, delete and search cases. The sub-endpoints manage what a case holds, and the case settings of a team.

Every method returns a [`Response`](../../responses.md).

## Sub-endpoints

| Class | Access | Description |
| --- | --- | --- |
| [`Actions`](actions.md) | `tines.cases.actions` | The action buttons of a case. |
| [`Activities`](activities.md) | `tines.cases.activities` | The activity log of a case. |
| [`Assignees`](assignees.md) | `tines.cases.assignees` | The users assigned to a case. |
| [`Blocks`](blocks.md) | `tines.cases.blocks` | The blocks of a case, and their elements. |
| [`Comments`](comments.md) | `tines.cases.comments` | The comments on a case, with reactions. |
| [`FieldValues`](field_values.md) | `tines.cases.field_values` | The values that a case holds for the case fields of its team. |
| [`Fields`](fields.md) | `tines.cases.fields` | The case fields of a team. |
| [`Files`](files.md) | `tines.cases.files` | The files attached to a case. |
| [`LinkedCases`](linked_cases.md) | `tines.cases.linked_cases` | The cases that are linked to a case. |
| [`Metadata`](metadata.md) | `tines.cases.metadata` | The key-value metadata of a case. |
| [`Notes`](notes.md) | `tines.cases.notes` | The notes of a case. |
| [`Records`](records.md) | `tines.cases.records` | The records attached to a case. |
| [`Statuses`](statuses.md) | `tines.cases.statuses` | The case statuses of a team. |
| [`Subscribers`](subscribers.md) | `tines.cases.subscribers` | The users that follow a case. |
| [`Tasks`](tasks.md) | `tines.cases.tasks` | The tasks of a case. |
| [`Templates`](templates.md) | `tines.cases.templates` | The case templates of a team. |
| [`Webhooks`](webhooks.md) | `tines.cases.webhooks` | The webhooks of a team that are called when its cases change. |

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the cases, optionally of one team, filtered and sorted. | `GET /api/v2/cases` |
| [`get`](#get) | Get a case. | `GET /api/v2/cases/{case_id}` |
| [`create`](#create) | Create a case in a team, optionally from a template. | `POST /api/v2/cases` |
| [`update`](#update) | Change a case. | `PATCH /api/v2/cases/{case_id}` |
| [`delete`](#delete) | Delete a case. | `DELETE /api/v2/cases/{case_id}` |
| [`append_description`](#append_description) | Add text to the description of a case. | `POST /api/v2/cases/{case_id}/description` |
| [`search`](#search) | Search the cases with a filter tree, a sort and token pagination. | `POST /api/v3/cases/search` |
| [`bulk_update_fields`](#bulk_update_fields) | Set field values on several cases. | `POST /api/v2/cases/bulk/fields` |
| [`get_pdf`](#get_pdf) | Export a case as a PDF. | `GET /api/v2/cases/{case_id}/pdf` |

## Methods breakdown

### `list`

`GET /api/v2/cases`

List the cases, optionally of one team, filtered and sorted.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | no | — | Only cases of this team. |
| `filters` | [`CaseFilters`](#casefilters) | no | Any of the keys of `CaseFilters`; every key is optional | The filters to apply. Every key is optional. |
| `order` | `CaseOrder` | no | `RECENTLY_EDITED`<br>`LEAST_RECENTLY_EDITED`<br>`PRIORITY_ASC`<br>`PRIORITY_DESC`<br>`OPENED_ASC`<br>`OPENED_DESC`<br>`CREATED_ASC`<br>`CREATED_DESC` | How to sort the cases. |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, from 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` has `cases` and `meta`, the pagination details. |
| 400 | `per_page`, a filter or a value is not valid. |
| 404 | The team does not exist or is not visible to the key. |
| 422 | A filter has the wrong shape, such as `and_metadata` as an object. |

### `get`

`GET /api/v2/cases/{case_id}`

Get a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `resolve_mentions` | `bool` | no | `True`, `False` | Replaces user mentions with display names. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the case. |
| 404 | The case does not exist or is not visible to the key. |

### `create`

`POST /api/v2/cases`

Create a case in a team, optionally from a template.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | yes | — | The ID of the team the case belongs to. |
| `name` | `str` | yes | — | The name of the case. |
| `template_id` | `int \| str` | no | ID or slug | A case template. The values of the template fill the arguments that are left out. |
| `description` | `str` | no | — | The description, as Markdown. User mentions are written `<@user-2435>`. |
| `priority` | `CasePriority` | no | `CRITICAL`<br>`HIGH`<br>`MEDIUM`<br>`LOW`<br>`INFO` | The priority. Tines defaults to `LOW`. |
| `status` | `CaseStatus` | no | `OPEN`, `CLOSED` | The status. Tines defaults to `OPEN`. |
| `sub_status_id` | `int` | no | — | The ID of a case status of the team. |
| `author_email` | `str` | no | — | The email address of the user creating the case. |
| `assignee_emails` | `Sequence[str]` | no | — | The email addresses of the users to assign. |
| `tag_names` | `Sequence[str]` | no | — | The names of the tags to add. |
| `opened_at` | `datetime \| str` | no | ISO 8601 string, or `datetime` | When the case was opened: a `datetime` or an ISO 8601 string. |
| `resolved_at` | `datetime \| str` | no | ISO 8601 string, or `datetime` | When the case was resolved: a `datetime` or an ISO 8601 string. |
| `metadata` | `Mapping[str, Any]` | no | — | Key-value pairs to store on the case. |
| `closure_conditions` | [`Sequence[ClosureCondition]`](#closurecondition) | no | — | The conditions that must be true to close the case. |
| `field_values` | `Mapping[str, Any]` | no | — | The values of the case fields, keyed by the ID of the field. A field that allows several values takes one string separated by `\|`. |
| `tasks` | [`Sequence[CaseTask]`](#casetask) | no | — | Tasks to create with the case. |
| `blocks` | [`Sequence[CaseBlock]`](#caseblock) | no | — | Blocks to create with the case. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the created case. |
| 404 | The team or the template does not exist or is not visible to the key. |
| 422 | A value is not valid. |

### `update`

`PATCH /api/v2/cases/{case_id}`

Change a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `name` | `str` | no | — | A new name. |
| `team_id` | `int` | no | — | The team to move the case to. |
| `description` | `str` | no | — | A new description, as Markdown. To add to it, use `append_description`. |
| `priority` | `CasePriority` | no | `CRITICAL`<br>`HIGH`<br>`MEDIUM`<br>`LOW`<br>`INFO` | A new priority. |
| `status` | `CaseStatus` | no | `OPEN`, `CLOSED` | A new status. Closing a case sets `resolved_at`, and opening it again clears it. |
| `sub_status_id` | `int` | no | — | The ID of a case status of the team. |
| `author_email` | `str` | no | — | The email address of the user making the change. |
| `assignee_emails` | `Sequence[str]` | no | — | The email addresses of the users to assign. |
| `add_assignee_emails` | `Sequence[str]` | no | — | The email addresses of users to add as assignees. |
| `remove_assignee_emails` | `Sequence[str]` | no | — | The email addresses of users to remove as assignees. |
| `add_tag_names` | `Sequence[str]` | no | — | The names of tags to add. |
| `remove_tag_names` | `Sequence[str]` | no | — | The names of tags to remove. |
| `opened_at` | `datetime \| str` | no | ISO 8601 string, or `datetime` | When the case was opened: a `datetime` or an ISO 8601 string. |
| `resolved_at` | `datetime \| str` | no | ISO 8601 string, or `datetime` | When the case was resolved: a `datetime` or an ISO 8601 string. |
| `closure_conditions` | [`Sequence[ClosureCondition]`](#closurecondition) | no | — | The conditions that must be true to close the case. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated case. |
| 404 | The case or the team does not exist or is not visible to the key. |
| 422 | A value is not valid, or a closure condition is not true when the case is closed. |

### `delete`

`DELETE /api/v2/cases/{case_id}`

Delete a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The case does not exist or is not visible to the key. |

### `append_description`

`POST /api/v2/cases/{case_id}/description`

Add text to the description of a case.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |
| `description` | `str` | yes | — | The text to add, as Markdown. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated case. |
| 400 | The description is missing or empty. |
| 404 | The case does not exist or is not visible to the key. |

### `search`

`POST /api/v3/cases/search`

Search the cases with a filter tree, a sort and token pagination.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `filter` | [`SearchNode`](#searchnode) | no | — | A condition or a group of conditions. |
| `sort` | [`Sequence[SearchSort]`](#searchsort) | no | — | Up to three sort keys, in order of importance. Cases are sorted by ID if none is given. |
| `page` | [`SearchPage`](#searchpage) | no | Object with a `size` and a `token` | The page to return. |
| `include_total` | `bool` | no | `True`, `False` | `True` adds the number of cases that match. |
| `timezone` | `str` | no | IANA timezone name | The timezone of relative dates and times of day. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` has `cases`, `total` when `include_total` is true, and `next_page_token` when there are more pages. |
| 400 | The search is refused: a filter or a value is not valid. |
| 403 | The tenant has no access to Cases. |

### `bulk_update_fields`

`POST /api/v2/cases/bulk/fields`

Set field values on several cases.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_ids` | `Sequence[int]` | yes | — | The IDs of the cases to update. |
| `fields` | [`Sequence[BulkFieldUpdate]`](#bulkfieldupdate) | yes | — | The values to set. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `cases`, a list with the `case_id` and the `fields` of each updated case. |
| 404 | A case or a field does not exist. |

### `get_pdf`

`GET /api/v2/cases/{case_id}/pdf`

Export a case as a PDF. `data` is the PDF as `bytes`.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `case_id` | `int` | yes | — | The ID of the case. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the PDF, as `bytes`, with the content type `application/pdf`. |
| 404 | The case does not exist or is not visible to the key. |

## Types

### `CaseFilters`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `search` | `str` | no | — | Searches the name, the description and the ID of the case. |
| `name` | `str` | no | — | Only cases whose name contains this text. |
| `comment` | `str` | no | — | Only cases with a comment that contains this text. |
| `note` | `str` | no | — | Only cases with a note that contains this text. |
| `status` | `CaseStatus` | no | `OPEN`, `CLOSED` | Only cases with this status. |
| `sub_status_names` | `Sequence[str]` | no | — | Only cases with one of these case status names. |
| `exclude_sub_status_names` | `Sequence[str]` | no | — | Leave out cases with one of these case status names. |
| `priority` | `Sequence[CasePriority]` | no | `CRITICAL`<br>`HIGH`<br>`MEDIUM`<br>`LOW`<br>`INFO` | Only cases with one of these priorities. |
| `exclude_priorities` | `Sequence[CasePriority]` | no | `CRITICAL`<br>`HIGH`<br>`MEDIUM`<br>`LOW`<br>`INFO` | Leave out cases with one of these priorities. |
| `assignees` | `Sequence[int \| str]` | no | — | Only cases assigned to one of these users: IDs or email addresses. `unassigned` matches cases with no assignee. |
| `and_assignees` | `Sequence[int]` | no | — | Only cases assigned to all of these users: IDs. |
| `exclude_assignees` | `Sequence[int]` | no | — | Leave out cases assigned to these users: IDs. |
| `assigned_to_me` | `bool` | no | `True`, `False` | Only cases assigned to the current user. |
| `authors` | `Sequence[int \| str]` | no | — | Only cases created by one of these users: IDs or email addresses. `tines` matches the cases that automation created. |
| `exclude_authors` | `Sequence[int]` | no | — | Leave out cases created by these users: IDs. |
| `subscribed` | `bool` | no | `True`, `False` | Only cases that the current user follows. |
| `my_open_tasks` | `bool` | no | `True`, `False` | Only cases with open tasks that are assigned to the current user. |
| `tags` | `Sequence[str]` | no | — | Only cases that have all of these tags, like `and_tags`. |
| `and_tags` | `Sequence[str]` | no | — | Only cases with all of these tags. |
| `or_tags` | `Sequence[str]` | no | — | Only cases with at least one of these tags. |
| `exclude_tags` | `Sequence[str]` | no | — | Leave out cases with these tags. |
| `metadata` | `dict[str, Any]` | no | — | Only cases whose metadata holds these key-value pairs. |
| `and_metadata` | [`Sequence[FieldFilter]`](#fieldfilter) | no | — | Only cases that match all of these metadata pairs. |
| `or_metadata` | [`Sequence[FieldFilter]`](#fieldfilter) | no | — | Only cases that match at least one of these metadata pairs. |
| `fields` | [`Sequence[FieldFilter]`](#fieldfilter) | no | — | Only cases that match all of these field values, like `and_fields`. `key` is the slug of the field. |
| `and_fields` | [`Sequence[FieldFilter]`](#fieldfilter) | no | — | Only cases that match all of these field values. `key` is the slug of the field. |
| `or_fields` | [`Sequence[FieldFilter]`](#fieldfilter) | no | — | Only cases that match at least one of these field values. `key` is the slug of the field. |
| `record_field` | [`RecordFieldFilter`](#recordfieldfilter) | no | — | Only cases with a record whose field has this value. |
| `records` | `Sequence[str]` | no | — | Only cases that contain a record that matches any of these record values. Large text fields cannot be queried. |
| `sla_status` | `Sequence[SlaStatus]` | no | `WARNING`, `EXCEEDED` | Only cases with one of these SLA statuses. |
| `and_sla_status` | `Sequence[SlaStatus]` | no | `WARNING`, `EXCEEDED` | Only cases with all of these SLA statuses. |
| `exclude_sla_status` | `Sequence[SlaStatus]` | no | `WARNING`, `EXCEEDED` | Leave out cases with these SLA statuses. |
| `sla_type` | `Sequence[SlaType]` | no | `resolution`, `response` | Only cases with one of these SLA types. |
| `and_sla_type` | `Sequence[SlaType]` | no | `resolution`, `response` | Only cases with all of these SLA types. |
| `exclude_sla_type` | `Sequence[SlaType]` | no | `resolution`, `response` | Leave out cases with these SLA types. |
| `case_ids` | `Sequence[int]` | no | — | Only these cases. |
| `child_team_ids` | `Sequence[int]` | no | — | Only cases that belong to these child teams. |
| `start_date` | `datetime \| str` | no | — | Only cases created at or after this time. A date without a time starts at the beginning of the day. |
| `end_date` | `datetime \| str` | no | — | Only cases created at or before this time. A date without a time runs to the end of the day. |
| `relative_date` | `str` | no | — | Only cases created in this window before now: `today`, `yesterday` or a count and a unit, such as `7 days`. |
| `time_range` | `str` | no | — | A time of day range in 24-hour `HH:MM-HH:MM` format, such as `09:00-17:00`. A start later than the end spans midnight. Do not combine it with the date filters. |
| `opened_at_start_date` | `datetime \| str` | no | — | Only cases opened after this time. |
| `opened_at_end_date` | `datetime \| str` | no | — | Only cases opened before this time. |
| `opened_at_relative_date` | `str` | no | — | Only cases opened in this window before now, in the format of `relative_date`. |
| `resolved_at_start_date` | `datetime \| str` | no | — | Only cases resolved at or after this time. |
| `resolved_at_end_date` | `datetime \| str` | no | — | Only cases resolved at or before this time. |
| `resolved_at_relative_date` | `str` | no | — | Only cases resolved in this window before now, in the format of `relative_date`. |
| `updated_at_start_date` | `datetime \| str` | no | — | Only cases updated at or after this time. |
| `updated_at_end_date` | `datetime \| str` | no | — | Only cases updated at or before this time. |
| `updated_at_relative_date` | `str` | no | — | Only cases updated in this window before now, in the format of `relative_date`. |

### `FieldFilter`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `key` | `str` | yes | — | The key of the field or of the metadata pair. |
| `value` | `Any` | yes | — | The value to match. |

### `RecordFieldFilter`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `id` | `int` | yes | — | The ID of the record field. |
| `value` | `Any` | yes | — | The value to match. |

### `ClosureCondition`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `name` | `str` | yes | — | The name of the condition. |
| `formula` | `str` | yes | — | A formula that must be true, such as `=SIZE(team_case.assignees) > 0`. |

### `CaseTask`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `description` | `str` | yes | — | The description of the task. |
| `assignee_ids` | `Sequence[int]` | no | — | The IDs of the users to assign. |
| `assignee_emails` | `Sequence[str]` | no | — | The email addresses of the users to assign. |

### `CaseBlock`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `title` | `str` | yes | — | The title of the block. |
| `block_type` | `BlockType` | yes | `note`<br>`file`<br>`linked_cases`<br>`metadata`<br>`closure_conditions`<br>`case_action`<br>`block_group`<br>`html` | The type of the block. |
| `elements` | [`Sequence[NoteElement \| FileElement]`](#noteelement) | yes | — | The elements of the block: note elements or file elements. |
| `hidden` | `bool` | no | `True`, `False` | Whether the block is hidden. |
| `default_collapsed` | `bool` | no | `True`, `False` | Whether the block is collapsed by default. |
| `guid` | `str` | no | — | A GUID for the block. |
| `parent_block_guid` | `str` | no | — | The GUID of the block group that holds the block. |

### `NoteElement`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `content` | `str` | yes | — | The content of the note. |
| `note_type` | `NoteType` | yes | `html`, `text` | The format of the content. |
| `color` | `NoteColor` | no | `white`<br>`gold`<br>`magenta`<br>`green`<br>`blue`<br>`red`<br>`mint`<br>`indigo` | The color of the note. |
| `sensitive` | `bool` | no | `True`, `False` | Whether to leave the note out of exports. |

### `FileElement`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `filename` | `str` | yes | — | The name of the file. |
| `file_contents` | `str` | yes | — | The contents of the file, Base64 encoded. |
| `annotation` | `str` | no | — | A note about the file. |

### `SearchNode`

One of: [`SearchCondition`](#searchcondition), [`SearchGroup`](#searchgroup), [`SearchNested`](#searchnested).

### `SearchCondition`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `field` | `SearchField` | yes | `access_restricted`, `applicable_sla_type`, `assignee`, `assignees`, `author`, `authors`, `case_field`, `case_id`, `comment.author`, `comment.created_at`, `comment.text`, `comment_count`, `created_at`, `description`, `group`, `linked_cases_count`, `metadata`, `name`, `note.created_at`, `note.text`, `opened_at`, `opened_by`, `priority`, `record.value`, `recorded_sla_status`, `resolved_at`, `resolved_by`, `restricted`, `search`, `severity`, `sla`, `sla_time`, `status`, `sub_status`, `subscriber`, `subscribers`, `tag`, `tags`, `task.assignee`, `task.completed`, `task.text`, `task_count`, `team`, `updated_at` | The field to compare. |
| `operator` | `SearchOperator` | yes | `IS`, `IS_NOT`, `IS_ANY_OF`, `IS_ALL_OF`, `IS_NONE_OF`, `CONTAINS`, `NOT_CONTAINS`, `CONTAINS_ALL`, `NOT_CONTAINS_ALL`, `CONTAINS_PHRASE`, `NOT_CONTAINS_PHRASE`, `STARTS_WITH`, `ENDS_WITH`, `FUZZY`, `BEFORE`, `AFTER`, `ON`, `BETWEEN`, `IN_THE_LAST`, `IS_EMPTY`, `IS_NOT_EMPTY` | The comparison. |
| `value` | `Any` | no | — | The value to compare with. |
| `key` | `str` | no | — | For `case_field` and `metadata`: the key of the field or of the pair. |

### `SearchGroup`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `op` | `SearchGroupOperator` | yes | `AND`, `OR`, `NOT` | How the nodes combine. |
| `nodes` | [`Sequence[SearchNode]`](#searchnode) | yes | — | The conditions and groups of the group. |

### `SearchNested`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `op` | `str` | yes | `NESTED` | Always `NESTED`. |
| `path` | `SearchCollection` | yes | `comment`, `note`, `record`, `task` | The collection of the case to filter. |
| `filter` | [`SearchNode`](#searchnode) | yes | — | The condition or group that an item of the collection must match. |

### `SearchSort`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `field` | `SearchSortField` | yes | `created_at`<br>`name`<br>`opened_at`<br>`priority`<br>`resolved_at`<br>`updated_at` | The field to sort by. |
| `direction` | `SearchDirection` | yes | `ASC`, `DESC` | The direction of the sort. |

### `SearchPage`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `size` | `int` | no | — | The number of cases in a page, from 1 to 50. |
| `token` | `str` | no | — | The `next_page_token` of the previous reply. |

### `BulkFieldUpdate`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `input_id` | `int` | yes | — | The ID of the field. |
| `value` | `Any` | yes | — | The value to set. A field that allows several values takes one string separated by `\|`. |
| `upsert` | `bool` | no | `True`, `False` | `True` adds the field to the cases that do not have it. By default only the cases that have it are updated. |
