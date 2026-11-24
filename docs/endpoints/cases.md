# Cases

Cases track work that needs people, such as an incident or an investigation. The module is available
as `tines.cases`, and the class is `tapi.cases.Cases`. Every method returns a
[`Response`](../responses.md).

The module covers the cases themselves and the sub-areas [`activities`](#activities),
[`assignees`](#assignees), [`comments`](#comments), [`notes`](#notes), [`tasks`](#tasks),
[`field_values`](#field_values), [`metadata`](#metadata), [`files`](#files), [`blocks`](#blocks),
[`linked_cases`](#linked_cases), [`records`](#records), [`subscribers`](#subscribers),
[`actions`](#actions), [`fields`](#fields), [`statuses`](#statuses), [`templates`](#templates) and
[`webhooks`](#webhooks). Fields, statuses, templates and webhooks are under `/api/v1`.

| Method                                           | HTTP route                           |
| ------------------------------------------------ | ------------------------------------ |
| `list(...)`                                      | `GET /api/v2/cases`                  |
| `get(case_id=...)`                               | `GET /api/v2/cases/{case_id}`        |
| `create(team_id=..., name=...)`                  | `POST /api/v2/cases`                 |
| `update(case_id=...)`                            | `PATCH /api/v2/cases/{case_id}`      |
| `delete(case_id=...)`                            | `DELETE /api/v2/cases/{case_id}`     |
| `append_description(case_id=..., description=...)` | `POST /api/v2/cases/{case_id}/description` |
| `search(...)`                                    | `POST /api/v3/cases/search`          |
| `bulk_update_fields(case_ids=..., fields=...)`   | `POST /api/v2/cases/bulk/fields`     |
| `get_pdf(case_id=...)`                           | `GET /api/v2/cases/{case_id}/pdf`    |
| `activities.list(case_id=..., ...)`              | `GET /api/v2/cases/{case_id}/activities` |
| `activities.get(case_id=..., activity_id=...)`   | `GET /api/v2/cases/{case_id}/activities/{activity_id}` |
| `assignees.list(case_id=..., ...)`               | `GET /api/v2/cases/{case_id}/assignees` |

All parameters are keyword-only. Parameters left as `None` are not sent. The Tines docs show the
Cases API documentation under Stories, and the OpenAPI document of Cases is a separate file.

## The case

`data` of `get`, `create`, `update` and `append_description` is a case, and `list` returns the same
32 fields for each case. `search` returns a shorter form: `case_id`, `name`, `description`,
`status`, `sub_status`, `priority`, `url`, `author`, `opened_by`, `resolved_by`, `assignees`, `tags`,
`team` and the four timestamps. A case has:

| Field                                  | Meaning                                                          |
| -------------------------------------- | ---------------------------------------------------------------- |
| `case_id`, `name`, `description`       | The ID, the name and the Markdown description (`null` if none).  |
| `status`, `sub_status`, `priority`     | `OPEN` or `CLOSED`, the case status object, and the priority.    |
| `url`                                  | The address of the case in Tines.                                |
| `author`, `opened_by`, `resolved_by`   | Users, or `null`. A user has `user_id`, `first_name`, `last_name`, `email`, `avatar_url` and `is_service_account`. |
| `assignees`, `tags`, `team`            | The assigned users, the tags and the team.                       |
| `metadata`, `fields`                   | The key-value pairs and the field values of the case.            |
| `sla`, `slas`                          | The service level agreement details.                             |
| `closure_conditions`                   | The conditions that must be true to close the case.              |
| `linked_cases`, `records`, `actions`, `blocks`, `tasks`, `activities` | The related items, as lists.         |
| `activities_meta`, `records_meta`, `blocks_meta`, `linked_cases_meta` | The pagination details of those lists. |
| `opened_at`, `resolved_at`, `created_at`, `updated_at` | ISO 8601 timestamps (`null` if not set). |

## `list()`

Paginated: one call returns one page; see [Pagination](../pagination.md). `data` holds `cases` and
`meta`. Tines recommends [`search()`](#search) for new integrations.

| Parameter  | Type          | Meaning                                                              |
| ---------- | ------------- | -------------------------------------------------------------------- |
| `team_id`  | `int`         | Only cases of this team. An unknown team is a `404`, `['Team not found']`. |
| `filters`  | `CaseFilters` | The filters, see below.                                              |
| `order`    | `str`         | `RECENTLY_EDITED`, `LEAST_RECENTLY_EDITED`, `PRIORITY_ASC`, `PRIORITY_DESC`, `OPENED_ASC`, `OPENED_DESC`, `CREATED_ASC` or `CREATED_DESC`. A value that is none of them was ignored. |
| `per_page` | `int`         | Results per page. Tines defaults to 20 and caps it at 500. `0` is a `400`. |
| `page`     | `int`         | The page, starting at 1. Tines defaults to 1.                        |

### Filters

`filters` is an object, typed as `tapi.cases.CaseFilters`, with any of these keys. tapi sends it as a
JSON body, which is how the Tines docs show it, and the server reads it from the query too. An
unknown key is a `400` with `Unsupported filter parameters: <key>`.

| Keys                                                                 | Value                                              |
| -------------------------------------------------------------------- | -------------------------------------------------- |
| `search`, `name`, `comment`, `note`                                  | Text to look for.                                  |
| `status`                                                             | `OPEN` or `CLOSED`, one value. A list is a `400`.  |
| `priority`, `exclude_priorities`                                     | Lists of `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO`. |
| `assignees`, `authors`                                               | Lists of user IDs or emails. `assignees` also takes `unassigned`, and `authors` takes `tines`. |
| `and_assignees`, `exclude_assignees`, `exclude_authors`              | Lists of user IDs.                                 |
| `assigned_to_me`, `subscribed`, `my_open_tasks`                      | `True` or `False`.                                 |
| `tags`, `and_tags`, `or_tags`, `exclude_tags`                        | Lists of tag names.                                |
| `sub_status_names`, `exclude_sub_status_names`, `records`            | Lists of names.                                    |
| `sla_status`, `and_sla_status`, `exclude_sla_status`                 | Lists of `WARNING` or `EXCEEDED`.                  |
| `sla_type`, `and_sla_type`, `exclude_sla_type`                       | Lists of `resolution` or `response`.               |
| `case_ids`, `child_team_ids`                                         | Lists of IDs.                                      |
| `metadata`                                                           | An object of key-value pairs.                      |
| `and_metadata`, `or_metadata`, `fields`, `and_fields`, `or_fields`   | Lists of objects with a `key` and a `value`.       |
| `record_field`                                                       | An object with an `id` and a `value`.              |
| `start_date`, `end_date`, `opened_at_start_date`, `opened_at_end_date`, `resolved_at_start_date`, `resolved_at_end_date`, `updated_at_start_date`, `updated_at_end_date` | A `datetime` or an ISO 8601 string. A string that is not a date is a `400`. |
| `relative_date`, `opened_at_relative_date`, `resolved_at_relative_date`, `updated_at_relative_date` | `today`, `yesterday` or a number of days, weeks, months or years, such as `7 days`. |
| `time_range`                                                         | A time of day range such as `09:00-17:00`.         |

The server accepted a single value in place of a list of one, and the values of `status`,
`priority` and the SLA filters in any case.

## `get()`

`case_id` is required. `resolve_mentions` (`bool`) replaces user mentions with display names.

## `create()`

`team_id` and `name` are required, and the reply has a 201 status.

| Parameter                  | Type                          | Meaning                                         |
| -------------------------- | ----------------------------- | ----------------------------------------------- |
| `team_id`, `name`          | `int`, `str`                  | The team and the name of the case.              |
| `template_id`              | `int` or `str`                | The ID or the slug of a case template.          |
| `description`              | `str`                         | Markdown. Mentions are written `<@user-2435>`.  |
| `priority`                 | `str`                         | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` or `INFO`.  |
| `status`                   | `str`                         | `OPEN` or `CLOSED`.                             |
| `sub_status_id`            | `int`                         | A case status of the team.                      |
| `author_email`             | `str`                         | The user creating the case.                     |
| `assignee_emails`, `tag_names` | `Sequence[str]`           | Users to assign and tags to add.                |
| `opened_at`, `resolved_at` | `datetime` or `str`           | ISO 8601.                                       |
| `metadata`                 | `Mapping`                     | Key-value pairs.                                |
| `closure_conditions`       | `Sequence[ClosureCondition]`  | Objects with a `name` and a `formula`.          |
| `field_values`             | `Mapping`                     | Field values keyed by the ID of the field.      |
| `tasks`                    | `Sequence[CaseTask]`          | Objects with a `description`, `assignee_ids` and `assignee_emails`. |
| `blocks`                   | `Sequence[CaseBlock]`         | Objects with a `title`, a `block_type` and `elements`. |

The Tines docs write `priority` and `status` in lower case for `create` and the OpenAPI document
writes `status` in upper case. The server accepted both and a case shows the upper case, which is
what tapi offers. A new case is `OPEN` with the priority `LOW` unless told otherwise. A `priority`,
a `status` or an `opened_at` that is not valid is a `422` that names the field, and a `team_id` that
does not exist is a `404`. An assignee email that is not a user and a `sub_status_id` that does not
exist were ignored. The Tines docs say that the user of the key is assigned when no assignee is
given, and the case that was tried had no assignee.

## `update()`

`case_id` is required, and the rest are the parameters of `create` with `add_assignee_emails`,
`remove_assignee_emails`, `add_tag_names` and `remove_tag_names` and without `template_id`,
`metadata`, `field_values`, `tasks` and `blocks`. The Tines docs show `PUT`, and the OpenAPI
document lists `PUT` and `PATCH`, so tapi uses `PATCH`, and `PUT` worked too. `assignee_emails`,
which replaces the assignees, is in the Tines docs only, and was not tried. Closing a case sets
`resolved_at` and `resolved_by`, and opening it again clears `resolved_at`. Closing a case whose
closure condition is not true is a `422` with `['Cannot close case as all case requirements have not
been met']`. A call that sends nothing is a `200`.

## `delete()` and `append_description()`

`delete` takes `case_id` and the reply has a 204 status and no data. `append_description` takes
`case_id` and `description`, adds the text and returns the case.

## `search()`

Search is the newer way to find cases, with composable filters and cursor pagination. It is available
on Tines Cloud only, and the OpenAPI document does not list it.

| Parameter       | Type                     | Meaning                                                |
| --------------- | ------------------------ | ------------------------------------------------------ |
| `filter`        | `SearchNode`             | A condition, a group or a nested filter. All cases match if it is left out. |
| `sort`          | `Sequence[SearchSort]`   | Up to three objects with a `field` and a `direction`.  |
| `page`          | `SearchPage`             | `size` (1 to 50, 20 by default) and `token`.           |
| `include_total` | `bool`                   | Adds `total` to the reply.                             |
| `timezone`      | `str`                    | An IANA time zone, UTC by default.                     |

- A condition is `{"field": ..., "operator": ..., "value": ..., "key": ...}`. The fields are
  `access_restricted`, `applicable_sla_type`, `assignee`, `assignees`, `author`, `authors`,
  `case_field`, `case_id`, `comment.author`, `comment.created_at`, `comment.text`, `comment_count`,
  `created_at`, `description`, `group`, `linked_cases_count`, `metadata`, `name`, `note.created_at`,
  `note.text`, `opened_at`, `opened_by`, `priority`, `record.value`, `recorded_sla_status`,
  `resolved_at`, `resolved_by`, `restricted`, `search`, `severity`, `sla`, `sla_time`, `status`,
  `sub_status`, `subscriber`, `subscribers`, `tag`, `tags`, `task.assignee`, `task.completed`,
  `task.text`, `task_count`, `team` and `updated_at`. The server lists them in its error for an
  unknown field, and the Tines docs name fewer of them.
- The operators are `IS`, `IS_NOT`, `IS_ANY_OF`, `IS_ALL_OF`, `IS_NONE_OF`, `CONTAINS`,
  `NOT_CONTAINS`, `CONTAINS_ALL`, `NOT_CONTAINS_ALL`, `CONTAINS_PHRASE`, `NOT_CONTAINS_PHRASE`,
  `STARTS_WITH`, `ENDS_WITH`, `FUZZY`, `BEFORE`, `AFTER`, `ON`, `BETWEEN`, `IN_THE_LAST`, `IS_EMPTY`
  and `IS_NOT_EMPTY`. Each field supports some of them, and a field that does not support the
  operator is a `400` that lists the ones it supports. The Tines docs name 19 of the 21.
- A group is `{"op": "AND", "nodes": [...]}`, with `OR` and `NOT` too. Its `nodes` cannot be empty,
  `NOT` takes one node, and the Tines docs allow four levels and 50 nodes.
- A nested filter is `{"op": "NESTED", "path": "task", "filter": {"field": "text", ...}}`, with
  `path` one of `comment`, `note`, `record` and `task`. Inside it the fields have no prefix: a task
  has `text`, `completed` and `assignee`.
- `sort` takes the fields `created_at`, `name`, `opened_at`, `priority`, `resolved_at` and
  `updated_at`, with the direction `ASC` or `DESC` in any case.

`data` holds `cases`, `total` when `include_total` is true, and `next_page_token` when there is
another page, which goes in `page["token"]` with the same filter and sort. Errors are a `400`, or a
`403` when the tenant has no access to Cases, with `data` set to `{"error": {"type", "message",
"field", "hint"}}`, where `hint` lists the values the server accepts. A sort with a fourth key is a
`400`.

The search index is not updated at once. A case that was created a moment ago may not be found for
several seconds, and one that was deleted a moment ago may still be found, while `list` shows
either change immediately.

## `bulk_update_fields()`

`case_ids` and `fields` are required. Each item of `fields` has an `input_id`, a `value` and
optionally `upsert`: by default only the cases that already have the field are updated, and `upsert`
adds the field to the others. A field that allows several values takes one string separated by `|`.
The OpenAPI document shows `case_id` inside each item, and the Tines docs show `case_ids` apart,
which tapi follows. The OpenAPI document gives the status `201`.

## `get_pdf()`

`case_id` is required. `data` is the PDF, as `bytes`, and the content type is `application/pdf`. The
Tines docs show a JSON object with the file Base64 encoded in `base64encodedcontents`, which is what
Tines returns to one of its own HTTP actions, and the OpenAPI document declares no content type. A
case that does not exist is a `404` with the odd message `[' not found']`.

## `activities`

The activity log of a case. Tines writes the activities, and they cannot be changed through the API.
An activity has `id`, `activity_type`, `value`, `file`, `user`, `created_at` and, for a comment,
`reactions`.

- **`activities.list(case_id=...)`** is paginated and returns `case_id`, `activities` and `meta`.
  `activity_types` filters by type and is sent as `activity_type[]`, and the server accepted
  `activity_type` with a single value too. A type that does not exist is a `422` that lists the
  valid ones. The Tines docs give `per_page` a maximum of 50, and the server accepted 51.
  `resolve_mentions` replaces mentions in comments. The types are `CREATED`, `ASSIGNED`,
  `UNASSIGNED`, `STATUS_UPDATED`, `SUB_STATUS_UPDATED`, `SEVERITY_UPDATED`, `COMMENTED`,
  `DELETED_COMMENT`, `COMMENT_UPDATED`, `DESCRIPTION_UPDATED`, `FIELD_UPDATED`, `FILE_ATTACHED`,
  `FILE_ATTACHED_AND_COMMENTED`, `FILE_DELETED`, `TAGS_ADDED`, `TAGS_REMOVED`,
  `RECORD_RESULT_SET_ADDED`, `RECORD_RESULT_SET_REMOVED`, `CHECKLIST_ITEM_COMPLETED`,
  `CHECKLIST_ITEM_INCOMPLETE`, `LINKED_CASE_ADDED`, `LINKED_CASE_REMOVED`, `METADATA_UPDATED`,
  `NOTE_ADDED`, `NOTE_DELETED`, `NOTE_UPDATED`, `SLA_WARNING`, `SLA_EXCEEDED`, `TASK_CREATED`,
  `TASK_DELETED`, `TASK_COMPLETED`, `TASK_INCOMPLETE`, `TASK_UPDATED`, `TASK_ASSIGNED`,
  `TASK_UNASSIGNED`, `TEAM_UPDATED` and `TITLE_UPDATED`.
- **`activities.get(case_id=..., activity_id=...)`** returns one activity, optionally with
  `resolve_mentions`. An activity that does not exist is a `404` with `['TeamCaseAction not
  found']`, and the ID of an activity of another case is a `500`.

## `assignees`

**`assignees.list(case_id=...)`** is paginated and returns `case_id`, `assignees`, a list of users,
and `meta`. Assignees are changed with `update`.

## `comments`

A comment is an activity of the case, with `id`, `activity_type`, `value` (the Markdown text),
`created_at`, `user` and `reactions`, a list of objects with an `emoji` and its `reactants`.

| Method                                                       | HTTP route                                              |
| ------------------------------------------------------------ | ------------------------------------------------------- |
| `comments.list(case_id=..., ...)`                            | `GET /api/v2/cases/{case_id}/comments`                  |
| `comments.get(case_id=..., comment_id=...)`                  | `GET /api/v2/cases/{case_id}/comments/{comment_id}`     |
| `comments.create(case_id=..., value=...)`                    | `POST /api/v2/cases/{case_id}/comments`                 |
| `comments.update(case_id=..., comment_id=..., value=...)`    | `PATCH /api/v2/cases/{case_id}/comments/{comment_id}`   |
| `comments.delete(case_id=..., comment_id=...)`               | `DELETE /api/v2/cases/{case_id}/comments/{comment_id}`  |
| `comments.add_reaction(case_id=..., comment_id=..., value=...)` | `POST /api/v2/cases/{case_id}/comments/{comment_id}/reactions` |
| `comments.remove_reaction(case_id=..., comment_id=..., value=...)` | `DELETE /api/v2/cases/{case_id}/comments/{comment_id}/reactions` |

`list` is paginated and holds `case_id` (repeated as `caseId`), `comments` and `meta`. `create` has
a 201 status and takes the `value` and optionally an `author_email`. `value` supports Markdown and
user mentions such as `<@user-2435>`. A missing `value` is a `422`, and an empty one was accepted for
`create` and is a `422` (`Comment cannot be blank`) for `update`. An `author_email` that is not a user
was ignored. The Tines docs show `update` as `PUT`, and tapi uses `PATCH`, which the OpenAPI document
lists too, and `PUT` worked as well. `delete` has a 204 status, and the Tines docs say that only the
author of a comment or an admin can delete it.

The reaction is one of `+1`, `-1`, `eyes`, `heart` and `white_check_mark`, and any other value is a
`422` that lists them. `add_reaction` has a 201 status and returns the comment with its `reactions`,
a list of objects with an `emoji` such as `:+1:` and its `reactants`. The same reaction twice was a
201 as well.

`remove_reaction` sends the reaction as the JSON body of a `DELETE`, as the Tines docs show, and it
did not work on the tenant that tapi was tried on: the server answered every request with a `404` and
`['User not found']`, however the value was sent (in the body, in the query, with an `author_email`, a
`user_email` or a `user_id`), and the reaction stayed. The deprecated v1 route that Tines removes on
December 1, 2026 did remove it.

## `notes`

A note has `id`, `title`, `content` (Markdown), `color`, `sensitive` (left out of exports), `hidden`,
`author`, `created_at` and `updated_at`.

| Method                                                    | HTTP route                                           |
| --------------------------------------------------------- | ---------------------------------------------------- |
| `notes.list(case_id=..., ...)`                            | `GET /api/v2/cases/{case_id}/notes`                  |
| `notes.get(case_id=..., note_id=...)`                     | `GET /api/v2/cases/{case_id}/notes/{note_id}`        |
| `notes.create(case_id=..., title=...)`                    | `POST /api/v2/cases/{case_id}/notes`                 |
| `notes.update(case_id=..., note_id=...)`                  | `PATCH /api/v2/cases/{case_id}/notes/{note_id}`      |
| `notes.delete(case_id=..., note_id=...)`                  | `DELETE /api/v2/cases/{case_id}/notes/{note_id}`     |
| `notes.append_content(case_id=..., note_id=..., content=...)` | `POST /api/v2/cases/{case_id}/notes/{note_id}/content` |

`create` has a 201 status and takes `title`, `content`, `color`, `position` (zero-based), `sensitive`,
`hidden` and `author_email`. The Tines docs require `title` and the OpenAPI document does not, and
the server refuses a note without one with a `422`, so it is required. An empty title was accepted.
`color` is one of `white` (the default), `gold`, `magenta`, `green`, `blue`, `red`, `mint` and
`indigo`, in lower case, and anything else is a `422`. A new note is not sensitive and not hidden. The
server accepted `position` and `author_email` (an address that is not a user too), which only the
Tines docs list, and the replies show no position.

`update` takes the same and `PUT` worked as well. A call that sends nothing is a `200`.
`append_content` adds text and returns the note, and an empty text was accepted. `list` and `get`
take `resolve_mentions`, and `list` holds `case_id`, `notes`, including the hidden ones, and `meta`.
A note that does not exist is a `404`, with `Note not found` for `get` and `TeamCaseNote not found`
for a second `delete`, which has a 204 status.

## `tasks`

A task has `id`, `description`, `completed`, `assignees` (objects with `id`, `email`, `first_name`
and `last_name`), `created_at` and `updated_at`.

| Method                                                | HTTP route                                         |
| ----------------------------------------------------- | -------------------------------------------------- |
| `tasks.list(case_id=..., ...)`                        | `GET /api/v2/cases/{case_id}/tasks`                |
| `tasks.get(case_id=..., task_id=...)`                 | `GET /api/v2/cases/{case_id}/tasks/{task_id}`      |
| `tasks.create(case_id=..., description=...)`          | `POST /api/v2/cases/{case_id}/tasks`               |
| `tasks.batch_create(case_id=..., tasks=...)`          | `POST /api/v2/cases/{case_id}/tasks/batch`         |
| `tasks.update(case_id=..., task_id=...)`              | `PATCH /api/v2/cases/{case_id}/tasks/{task_id}`    |
| `tasks.delete(case_id=..., task_id=...)`              | `DELETE /api/v2/cases/{case_id}/tasks/{task_id}`   |

`get`, `create` and `update` return an object with `task`, and `list` holds `tasks` and `meta`, without
`case_id`. `create` and `batch_create` have a 201 status. `batch_create` takes at most 25 tasks, each
with a `description` and optionally `assignee_emails`, and returns `tasks`. `update` takes
`description`, `completed` and `assignee_emails`, which replaces the assignees, and `PUT` worked as
well. A call that sends nothing is a `200`.

An assignee email that is not a user is a `400` with `Users <email> not found`, unlike for a case,
where it is ignored. A blank description is a `422` with `Description cannot be blank`, an empty
`batch_create` is a `400` with `tasks must be a non-empty array`, and 26 tasks are a `400` with
`Cannot create more than 25 tasks at once`. `delete` has a 204 status and no data, as the OpenAPI
document says, and the Tines docs show a JSON object with `destroyed_id`. A task that does not exist
is a `404` with `Task not found`. The server accepted a `per_page` of 51, although the Tines docs
give a maximum of 50.

## `field_values`

A field is a custom value that a team defines for its cases. These methods read and set the value
that one case holds for one field. A field value has `id`, `value` and `case_input`, the field, with
`id`, `key`, `name`, `validation_type` and `validation_options`.

| Method                                                    | HTTP route                                        |
| --------------------------------------------------------- | ------------------------------------------------- |
| `field_values.list(case_id=..., ...)`                     | `GET /api/v2/cases/{case_id}/fields`              |
| `field_values.get(case_id=..., field_id=...)`             | `GET /api/v2/cases/{case_id}/fields/{field_id}`   |
| `field_values.create(case_id=..., input_id=..., value=...)` | `POST /api/v2/cases/{case_id}/fields`           |
| `field_values.update(case_id=..., field_id=..., value=...)` | `PATCH /api/v2/cases/{case_id}/fields/{field_id}` |
| `field_values.delete(case_id=..., field_id=...)`          | `DELETE /api/v2/cases/{case_id}/fields/{field_id}` |

`field_id` is the ID of the field value, the `id` in the reply, and `input_id` is the ID of the field
itself. `value` is a string, and a field that allows several values takes them in one string
separated by `|`. `get`, `create` and `update` return an object with `case_id` and `field`, and `list`
holds `case_id`, `fields` and `meta`. These calls were tried only on a tenant with no field
definition, so what they do for a field that exists is not known, and the errors are: `create` with
a field that does not exist is a `404` with `['TeamCaseInput not found']`, `get` and `update` with an
unknown field value are `404` with `['Field not found']`, and `delete` is a `404` with
`['TeamCaseInputValue not found']`.

## `metadata`

Metadata is a set of key-value pairs that a case holds.

| Method                                              | HTTP route                                       |
| --------------------------------------------------- | ------------------------------------------------ |
| `metadata.list(case_id=..., ...)`                   | `GET /api/v2/cases/{case_id}/metadata`           |
| `metadata.get(case_id=..., key=...)`                | `GET /api/v2/cases/{case_id}/metadata/{key}`     |
| `metadata.create(case_id=..., metadata=...)`        | `POST /api/v2/cases/{case_id}/metadata`          |
| `metadata.update(case_id=..., metadata=...)`        | `PUT /api/v2/cases/{case_id}/metadata`           |
| `metadata.delete(case_id=..., metadata=...)`        | `DELETE /api/v2/cases/{case_id}/metadata`        |

`list` and `get` return an object with `case_id` and `metadata`, which for `get` holds only the pair
asked for, and an empty object for a case without metadata. The server returns every pair, and `list`
takes no `per_page` or `page`. A value is a string, a number, a boolean or `null`: an object or a list is a `422`.

`create` adds keys and has a 201 status. When a key already has a value the reply is a `409` with
`Metadata key <key> already exists`, and none of the pairs are set. `update` sets keys and creates
the missing ones, and `PUT` is the only verb: a `PATCH` is a `404`, so tapi does not use `PATCH`. An
empty `metadata` is a `400` with `Invalid metadata` for both.

`delete` takes the keys to delete and sends them as the JSON body named `metadata`, with a 204
status. The OpenAPI document calls the property `keys` and says that leaving it out deletes
everything, and the server answered a body with `keys` and a request without a body with a `400` and
`Invalid metadata keys`. An empty list deleted nothing, and a key that does not exist is a `404` with
`Metadata key <key> does not exist`, which `get` answers too.

## `files`

A file is attached to a case by an activity. The activity has `id` (the `file_id` of the other
methods), `activity_type` (`FILE_ATTACHED` or `FILE_ATTACHED_AND_COMMENTED`), `value`, `created_at`,
`file` (with the `filename` and a `url`) and `user`.

| Method                                                   | HTTP route                                         |
| -------------------------------------------------------- | -------------------------------------------------- |
| `files.list(case_id=..., ...)`                           | `GET /api/v2/cases/{case_id}/files`                |
| `files.get(case_id=..., file_id=...)`                    | `GET /api/v2/cases/{case_id}/files/{file_id}`      |
| `files.create(case_id=..., filename=..., file_contents=...)` | `POST /api/v2/cases/{case_id}/files`           |
| `files.delete(case_id=..., file_id=...)`                 | `DELETE /api/v2/cases/{case_id}/files/{file_id}`   |
| `files.download(case_id=..., file_id=...)`               | `GET /api/v2/cases/{case_id}/files/{file_id}/download` |
| `files.info(case_id=..., file_id=...)`                   | `GET /api/v2/cases/{case_id}/files/{file_id}/info` |

`create` has a 201 status and sends the file as Base64 text in a JSON body, `file_contents`, and not
as a multipart upload: use `base64.b64encode(data).decode()`. It also takes `value`, a comment to
add, which makes the activity `FILE_ATTACHED_AND_COMMENTED`, `author_email` (an address that is not
a user was accepted) and `team_case_block_id`, a file block, which adds a `block_id` to the reply and
an element to the block. A missing `file_contents` is a `422`, a block that does not exist is a `404`
with `['TeamCaseBlock not found']`, and the server accepted text that is not Base64 and an empty
filename.

`list` holds `files` and `meta`, without `case_id`. `get` returns the activity. `download` returns
the file, decoded by its content type: the text file that was tried came back as a `str` with
`text/plain` and `Content-Disposition: attachment`. `info` returns `filename`, `content_type`, `guid`,
`md5`, `sha256`, `sizeinbytes` and `base64encodedcontents`, which only the OpenAPI document lists. A
file that does not exist is a `404` with `['File not found']` (`['TeamCaseAction not found']` for
`info`). `delete` has a 204 status, and the same file again is a `422` with `['You must provide a
valid file attachment']`. The Tines docs say that only the user who attached a file or an admin can
delete it.

## `blocks`

A block is a section of the case page, with `id`, `slug` (`blk_...`), `title`, `block_type`, `color`,
`position`, `hidden`, `default_collapsed`, `block_group_id`, `elements`, `created_at` and
`updated_at`. A method that takes `block_id` accepts the number or the slug.

| Method                                                              | HTTP route                                                   |
| ------------------------------------------------------------------- | ------------------------------------------------------------ |
| `blocks.list(case_id=..., ...)`                                     | `GET /api/v2/cases/{case_id}/blocks`                         |
| `blocks.get(case_id=..., block_id=...)`                             | `GET /api/v2/cases/{case_id}/blocks/{block_id}`              |
| `blocks.create(case_id=..., title=..., block_type=...)`             | `POST /api/v2/cases/{case_id}/blocks`                        |
| `blocks.update(case_id=..., block_id=...)`                          | `PATCH /api/v2/cases/{case_id}/blocks/{block_id}`            |
| `blocks.delete(case_id=..., block_id=...)`                          | `DELETE /api/v2/cases/{case_id}/blocks/{block_id}`           |
| `blocks.get_element(case_id=..., block_id=..., element_id=...)`     | `GET /api/v2/cases/{case_id}/blocks/{block_id}/elements/{element_id}` |
| `blocks.update_element(case_id=..., block_id=..., element_id=...)`  | `PATCH /api/v2/cases/{case_id}/blocks/{block_id}/elements/{element_id}` |
| `blocks.append_element_content(case_id=..., block_id=..., element_id=..., content=...)` | `POST /api/v2/cases/{case_id}/blocks/{block_id}/elements/{element_id}/content` |

`block_type` is `note`, `file`, `linked_cases`, `metadata`, `closure_conditions`, `case_action`,
`block_group` or `html`, and the OpenAPI document names only four of them. A new case has a
metadata block already, and a second is a `422`. `color` is `primary`, `white`, `gold`, `magenta`,
`green`, `blue`, `red`, `mint` or `indigo`, in lower case, and only note, file, block group and HTML
blocks have one. `primary` is stored as `white`, which is what a new block shows too.

`create` has a 201 status and takes `title`, which the server requires, as the Tines docs say and the
OpenAPI document does not, `block_type`, `color`, `elements`, `position`, `hidden`,
`default_collapsed`, `block_group_id` and `author_email` (an address that is not a user was
accepted). `elements` are note elements (`content`, `note_type` and `color`) or file elements
(`filename`, `file_contents` and `annotation`). A note block needs a note element and an HTML block an
HTML element, and a block without one is a `422` such as `Block "x": Note block is missing note
element`. `position` is a non-negative integer, a number past the end puts the block last, and
`top`, `bottom` and `-1` are a `400`, although the OpenAPI document names `top` and `bottom`.
`block_group_id` takes the ID or the slug of a block group.

`get` returns an object with `block`, by ID or by slug. `list` holds `blocks` and `meta`, and takes
`block_type` and `block_group_id`. A `block_type` that does not exist is a `422` that lists the
valid ones. `update` takes `title`, `color`, `position`, `hidden`, `default_collapsed` and
`block_group_id`, and `PUT` worked as well. The server took `block_group_id` as `null` to take a
block out of its group, which tapi cannot send. `delete` has a 204 status. Without
`include_children`, deleting a block group leaves its blocks in the case, outside any group, and
with `include_children` set to true it deletes them too. A block that does not exist is a `404` with
`['TeamCaseBlock not found']`.

The methods for elements take the `element_id` of the element, which is a different number from its
`id`: the `id` was a `404` with `['TeamCaseBlockElement not found']`. A slug in place of the block ID
was a `404` as well. `update_element` takes `content`, `author_email` and `annotation` (only the
Tines docs list the last two, and `annotation` works for a file element). `append_element_content`
adds text to a note element, and a file element is a `422` with
`['Element type does not support append']`.

## `linked_cases`

| Method                                                   | HTTP route                                            |
| -------------------------------------------------------- | ----------------------------------------------------- |
| `linked_cases.list(case_id=..., ...)`                    | `GET /api/v2/cases/{case_id}/linked_cases`            |
| `linked_cases.create(case_id=..., id=...)`               | `POST /api/v2/cases/{case_id}/linked_cases`           |
| `linked_cases.batch_create(case_id=..., ids=...)`        | `POST /api/v2/cases/{case_id}/linked_cases/batch`     |
| `linked_cases.delete(case_id=..., linked_case_id=...)`   | `DELETE /api/v2/cases/{case_id}/linked_cases/{linked_case_id}` |

A link is shown as a `linked_case`, with the `case_id` and the `name` of the other case, and it
shows on both cases. `list` holds `case_id`, `name`, `linked_cases` and `meta`. The body properties of
`create` and `batch_create` are `id` and `ids`, as the Tines docs say. The OpenAPI document calls
them `linked_case_id` and `linked_case_ids`, and the server did not read those: the first was a `404`
with `['TeamCase not found']` and the second a `500`.

`create` and `batch_create` have a 201 status and return `case_id`, `name` and the `linked_case` or
the `linked_cases`. Linking cases that are linked already, and an empty `ids`, are a 201 that changes
nothing. Linking a case to itself is a `422` with `['Cannot link case to itself']`, a case that does
not exist is a `404` with `['TeamCase not found']` (`['Target cases not found']` for `batch_create`),
and a request without a body is a `500`. `delete` has a 204 status, removes the link from both cases,
and is a 204 for a case that is not linked. The Tines docs give `ids` a limit of 150, which was not
tried.

## `records`

| Method                                           | HTTP route                                          |
| ------------------------------------------------ | --------------------------------------------------- |
| `records.list(case_id=..., ...)`                 | `GET /api/v2/cases/{case_id}/records`               |
| `records.get(case_id=..., record_id=...)`        | `GET /api/v2/cases/{case_id}/records/{record_id}`   |
| `records.create(case_id=..., record_id=...)`     | `POST /api/v2/cases/{case_id}/records`              |
| `records.delete(case_id=..., record_id=...)`     | `DELETE /api/v2/cases/{case_id}/records/{record_id}` |

A record has `id`, `record_type`, `results`, `created_at` and `linked_at`. `list` holds `case_id`,
`records` and `meta`. The Tines docs name the body property of `create` `record_id` and the OpenAPI
document `record_result_set_id`. The server read `record_id`, and for `record_result_set_id` it
answered `422` with `[{'record_result_set_id': 'Expected value to not be null'}]`, so tapi sends
`record_id`. A record that does not exist is a `404` with `['RecordResultSet not found']`, for `get`,
`create` and `delete`. The tenant that tapi was tried on had no records, so what these methods do
for a record that exists was not tried.

## `subscribers`

| Method                                                     | HTTP route                                               |
| ---------------------------------------------------------- | -------------------------------------------------------- |
| `subscribers.list(case_id=..., ...)`                       | `GET /api/v2/cases/{case_id}/subscribers`                |
| `subscribers.create(case_id=..., user_email=...)`          | `POST /api/v2/cases/{case_id}/subscribers`               |
| `subscribers.batch_create(case_id=..., user_emails=...)`   | `POST /api/v2/cases/{case_id}/subscribers/batch`         |
| `subscribers.delete(case_id=..., subscriber_id=...)`       | `DELETE /api/v2/cases/{case_id}/subscribers/{subscriber_id}` |

A new case has one subscriber already. `list` holds `case_id`, `subscribers` and `meta`, and each
subscriber has `id`, `user_id`, `first_name`, `last_name`, `email` and `avatar_url`, flat, where the
Tines docs show the user inside a `user` object (which `create` returns). `create` takes the email
address of a user, and an address that is not a user is a `404` with `['User not found']`.
`batch_create` takes at most 50 emails according to the Tines docs, and answers `404` with
`['Users not found']` when an address is not a user, `201` for an empty list, and `400` with
`['user_emails must be an array of strings']` for a string. A subscribing that works was not tried,
because it would email a user.

`delete` was `404` for the subscriber that a new case has: `['User not found']` with the `id` of the
listing, and `['Subscriber not found']` with its `user_id`. So the number that `delete` takes is not
known. A subscriber that does not exist is a `404` with `['Subscriber not found']`.

## `actions`

A case action is a button on the case that opens a page or calls a webhook. These are not the actions
of a story, which are [`tines.stories.actions`](stories_actions.md).

| Method                                                          | HTTP route                                          |
| --------------------------------------------------------------- | --------------------------------------------------- |
| `actions.list(case_id=..., ...)`                                | `GET /api/v2/cases/{case_id}/actions`               |
| `actions.get(case_id=..., action_id=...)`                       | `GET /api/v2/cases/{case_id}/actions/{action_id}`   |
| `actions.create(case_id=..., url=..., label=..., action_type=...)` | `POST /api/v2/cases/{case_id}/actions`           |
| `actions.update(case_id=..., action_id=...)`                    | `PATCH /api/v2/cases/{case_id}/actions/{action_id}` |
| `actions.delete(case_id=..., action_id=...)`                    | `DELETE /api/v2/cases/{case_id}/actions/{action_id}` |
| `actions.batch_update(case_id=..., actions=...)`                | `PUT /api/v2/cases/{case_id}/actions/batch`         |

An action has `id`, `case_id`, `url`, `label`, `action_type`, `action_text` (the button text, `Run`
for a webhook that has none), `query_params` (key-value pairs added to the address, `null` if none),
`story_name`, `story_emoji`, `page_emoji`, `created_at` and `updated_at`, and the fields
`query_param_key`, `query_param_value` and `three_b_reference`. `list` holds `case_id`, `actions` and
`meta`.

`create` has a 201 status. `url`, `label` and `action_type` are required, as the Tines docs say and
the OpenAPI document does not: each missing one is a `422`, and a `url` that is not a URL is a `422`
with `['Validation failed: Url is not a valid URL']`. The Tines docs give `action_type` the values
`webhook` and `page`, and the server lists `webhook`, `page`, `chat`, `story` and `app`, of which only
the first two were tried. `query_params` that is not an object is a `400`. `update` takes the same,
all optional, and a call that sends nothing is a `200`. `PUT` worked as well. An action that does not
exist is a `404` with `['Action not found']`, and `delete` has a 204 status.

`batch_update` replaces the actions of the case with the ones that it is given, and `PUT` is its only
verb. An action without a label is a `422` with `["Validation failed: Label can't be blank"]`, and an
empty list removes every action of the case.

## `fields`

A field is a custom value that the cases of a team can hold. This is the definition of the field,
and [`field_values`](#field_values) are the values. A field has `id`, `name`, `key` (a slug),
`input_type`, `sensitive`, `validation_type`, `validation_options`, `team`, `team_case_input_group`,
`created_at` and `updated_at`.

| Method                                                          | HTTP route                                   |
| --------------------------------------------------------------- | -------------------------------------------- |
| `fields.list(...)`                                              | `GET /api/v1/case_inputs`                    |
| `fields.get(field_id=...)`                                      | `GET /api/v1/case_inputs/{field_id}`         |
| `fields.create(name=..., input_type=..., team_id=...)`          | `POST /api/v1/case_inputs`                   |
| `fields.update(field_id=...)`                                   | `PATCH /api/v2/case_inputs/{field_id}`       |
| `fields.delete(field_id=...)`                                   | `DELETE /api/v2/case_inputs/{field_id}`      |
| `fields.list_values(field_id=..., ...)`                         | `GET /api/v1/case_inputs/{field_id}/fields`  |

A new field has `sensitive` false, `validation_type` `none`, `validation_options` `{}` and no group.
`create` has a 201 status and returns an object with one key, `team_case_input`, while `get` and
`update` return the field as it is. The Tines docs show `get` inside an object with `case_input`, which
the server does not do. `update` and `delete` are under `/api/v2` and the other routes under
`/api/v1`, and a `PATCH` on the `/api/v1` route is a `404`. The Tines docs let `group_name` be `null`
to take a field out of its group, which tapi cannot send.

`input_type` is `string`, `number`, `boolean`, `timestamp`, `email`, `url` or `ip_address`. The Tines
docs name the first four. Tines checks a value against the type when a case gets it: `5` is a number,
`a@example.com` an email, `https://example.com` a url, `1.2.3.4` an ip address and `true` a boolean,
and a value that does not fit is a `422`. The check of a `timestamp` is loose.

`validation_type` is `none`, `options` or `regex`, for a `string` field. `validation_options` is an
object, as the OpenAPI document types it. The Tines docs say a list for `options` and a string for
`regex`, and the server answers `422` with `Validation options must be an array of values` to a list,
and `500` to a string for `regex`:

| `validation_type` | `validation_options`                | A value that does not fit                      |
| ----------------- | ----------------------------------- | ---------------------------------------------- |
| `options`         | `{"options": ["low", "high"]}`      | `422` with `Value must be one of low, high`    |
| `regex`           | `{"regex": "^T-[0-9]+$"}`           | `422` with `Value must match ^T-[0-9]+$`       |

The server accepts other keys for `regex`, such as `pattern`, and an empty object, and does not check
anything then. `tapi.cases.FieldOptions` and `tapi.cases.FieldRegex` type the two objects. Updating a
field back to `none` leaves its old `validation_options` in place.

`list` takes `team_id`, which is optional, and holds `case_inputs` and `meta`. `list_values` holds
`fields`, each with `id`, `value`, `case` and `case_input`, and `meta`. A name that the team already
has is a `422` with `A field named "..." already exists in this team`, a team that does not exist is a
`404` with `Team not found`, and a field that does not exist is a `404` with `TeamCaseInput not found`
(`CaseInput not found` for `list_values`).

## `statuses`

A case is open or closed, and a case status refines that. A status has `id`, `name`, `slug`,
`description`, `parent_status` (`OPEN` or `CLOSED`), `default`, `team`, `created_at` and `updated_at`.
A case takes a status with `sub_status_id`.

| Method                                                   | HTTP route                                         |
| -------------------------------------------------------- | -------------------------------------------------- |
| `statuses.list(team_id=..., ...)`                        | `GET /api/v1/case_sub_statuses`                    |
| `statuses.get(status_id=...)`                            | `GET /api/v1/case_sub_statuses/{status_id}`        |
| `statuses.create(team_id=..., name=...)`                 | `POST /api/v1/case_sub_statuses`                   |
| `statuses.update(status_id=...)`                         | `PATCH /api/v1/case_sub_statuses/{status_id}`      |
| `statuses.delete(status_id=..., fallback_status_id=...)` | `DELETE /api/v1/case_sub_statuses/{status_id}`     |

Every team starts with four statuses that have `default` set: `to_do` and `in_progress` under `OPEN`,
and `done` and `canceled` under `CLOSED`.

`list` needs `team_id`, which is a `400` with `team_id is required` when it is missing, and takes
`parent_status`, `search` (the name contains the text, in any case) and the pagination. It holds
`case_sub_statuses` and `meta`. `create` has a 201 status and returns the status as it is, and takes
`parent_status`, `OPEN` unless told otherwise and also accepted in lower case, and `description`. A
`parent_status` that is not valid is a `422`, a name that the team already has is a `422` with `A
status named "..." already exists in this team.`, and a team that does not exist is a `404`. `update`
takes `name`, which changes the slug, and `description`, and `PUT` works too.

`delete` needs `fallback_status_id`, the status that its cases move to, in the query, and a missing
one is a `400` with `fallback_status_id is required`. A fallback that does not exist is a `404`, and
one under the other parent status is a `422` with `Fallback status must be of the same parent
status`. The status itself is accepted as its own fallback. The cases of the deleted status move to the
fallback. A status that does not exist is a `404` with `Case sub status not found` for `get` and
`TeamCaseSubStatus not found` for `update`.

## `templates`

A template fills in a case when a case is created from it, with `template_id` of `create`. A template
has `id`, `name`, `emoji`, `team`, `created_at` and `updated_at`, and its options come back only from
`export`.

| Method                                              | HTTP route                                              |
| --------------------------------------------------- | ------------------------------------------------------- |
| `templates.list(team_id=..., ...)`                  | `GET /api/v1/case_templates`                            |
| `templates.get(template_id=...)`                    | `GET /api/v1/case_templates/{template_id}`              |
| `templates.create(team_id=..., name=...)`           | `POST /api/v1/case_templates`                           |
| `templates.update(template_id=...)`                 | `PATCH /api/v1/case_templates/{template_id}`            |
| `templates.delete(template_id=...)`                 | `DELETE /api/v1/case_templates/{template_id}`           |
| `templates.export(template_id=...)`                 | `GET /api/v1/case_templates/{template_id}/export`       |
| `templates.import_(team_id=..., data=...)`          | `POST /api/v1/case_templates/import`                    |
| `templates.preview(template_id=...)`                | `GET /api/v1/case_templates/{template_id}/preview`      |

`list` needs `team_id` and takes `search` and the pagination, and holds `case_templates` and `meta`.
The Tines docs give a maximum of 100 per page, which the server does not enforce. A missing `team_id`
is a `400`. `create` has a 201 status and returns the template as it is, and takes `emoji`, a shortcode
such as `:mag:` that Tines picks at random when it is left out, and `options`, an object typed as
`tapi.cases.TemplateOptions`: `name` and `description` (which can hold formulas and field mentions),
`status`, `priority` (both accepted in upper and lower case), `sub_status_id`, `assignee_emails`,
`tag_names`, `team_case_buttons`, `tasks`, `closure_conditions`, `blocks`, `field_values` and
`metadata`. An option that is not valid is a `400` with `Template contains a malformed ...` followed by
`status`, `priority`, `buttons`, `case requirements` or `sub-status`, and a field ID that does not
exist is a `400` too. A name that the team already has is a `422` with `A template named "..." already
exists.`, and a team that does not exist is a `404`.

`update` takes the same. An option that is left out keeps its value and one that is sent replaces the
old value as a whole. `PUT` is listed too and tapi uses `PATCH`. A template that does not exist is a
`404` with `Case template not found`.

`export` returns `schema_version`, `exported_at` and `templates`, each with `emoji`,
`field_definitions`, `input_values`, `name` and `options`. The `options` use other names than `create`
does: `case_name`, `case_description`, `team_case_tasks`, `team_case_buttons`, `sub_status`,
`tag_names`, `assignee_emails`, `blocks`, `closure_conditions`, `metadata`, `priority` and `status`,
the last two in lower case. `import_` takes that as `data`, has a 201 status and returns an object with
`case_templates`. Importing an export into the team it came from creates a copy under a changed name.
`data` without a templates array is a `422` with `Missing or invalid templates array`, and an empty one
creates nothing. `preview` returns `actions`, `assignees`, `blocks`, `closure_conditions`,
`description`, `fields`, `metadata`, `name`, `priority`, `status`, `sub_status`, `tags` and `tasks`,
with formulas not evaluated.

A case created with `template_id` gets the priority, tasks, blocks, actions, metadata and closure
conditions of the template. A `template_id` that does not exist is a `404` with `Template not found`.

## `webhooks`

A case webhook sends a request to an address when something happens to a case of the team. A webhook
has `id`, `name` (`null` when none was given), `url`, `version_number`, `notifications` and `team`. The
Tines docs say that a team can have at most five.

| Method                                               | HTTP route                                       |
| ---------------------------------------------------- | ------------------------------------------------ |
| `webhooks.list(...)`                                 | `GET /api/v1/case_webhooks`                      |
| `webhooks.get(webhook_id=...)`                       | `GET /api/v1/case_webhooks/{webhook_id}`         |
| `webhooks.create(team_id=..., url=...)`              | `POST /api/v1/case_webhooks`                     |
| `webhooks.update(webhook_id=...)`                    | `PATCH /api/v1/case_webhooks/{webhook_id}`       |
| `webhooks.delete(webhook_id=...)`                    | `DELETE /api/v1/case_webhooks/{webhook_id}`      |

`list` takes `team_id` and the pagination, with a maximum of 50 per page in the Tines docs, though 51
was accepted, and holds `webhooks` and `meta`. `get`, `create` and `update` return an object with
`webhook`, and `create` has a 201 status. `notifications` is `["ALL"]`, which is the default, or a list
of events such as `CREATED`, `ASSIGNED`, `COMMENTED`, `STATUS_UPDATED`, `TAGS_ADDED`, `FILE_ATTACHED`,
`LINKED_CASE_ADDED`, `NOTE_ADDED`, `TASK_CREATED` and `SLA_EXCEEDED`. See
`tapi.cases.types.WebhookNotification` for all 37. `update` replaces them, and an empty `name` is
accepted.

A `url` that is not valid is a `422` with `Url is not a valid URL`, and a notification that is not
valid is a `422` whose message lists the valid ones. An `update` that sends nothing is a `422` with
`At least one of url, name, version_number, or notifications must be provided`. A webhook that does
not exist is a `404` with `TeamCaseWebhook not found`. `PUT` works as well as `PATCH`.

## Errors

| Status | When                                                                                       |
| ------ | ------------------------------------------------------------------------------------------ |
| `400`  | `per_page` is not a positive integer, a filter or a value is not valid, or `search` is refused. `data` is a list of messages, and for `search` an `error` object. |
| `403`  | `search`, when the tenant has no access to Cases.                                          |
| `404`  | The case or the team does not exist or is not visible to the key. The messages are `['TeamCase not found']` and `['Team not found']`. `bulk_update_fields` answers `['TeamCaseInput not found']` for a field and `['One or more cases not found']` for the cases. |
| `408`  | `list`, when the search takes too long (OpenAPI document).                                 |
| `422`  | A value is not valid (`create`, `update` and `activities.list`), closing a case whose closure condition is not true, and `list` for a filter of the wrong shape, such as `and_metadata` as an object. `data` is a list of objects naming the field, or of messages. |
| `409`  | `metadata.create`, when a key already has a value.                                         |
| `500`  | `activities.get` with the ID of an activity of another case.                               |

`delete` answers `404` for a case that is already gone, and a deleted case is gone from `get` and
`list` at once. `bulk_update_fields` answers `400` with `['case_ids is required']` and `['fields is
required']`.

## Not tried

Everything above was tried on 2026-11-23 against a tenant that had no cases, with throwaway cases
that were deleted afterwards. These were not:

- assigning users: `assignee_emails`, `add_assignee_emails` and `remove_assignee_emails` with a real
  user, which makes Tines email them, and the assignees of a task;
- subscribing a user and unsubscribing one, and a record that exists;
- tags, moving a case to another team, and `author_email` with a real user;
- the case action types `chat`, `story` and `app`, the same button types of a template, an HTML
  element, a file larger than a few bytes, and the limits of 150 linked cases and 50 subscribers;
- `filters` with `assigned_to_me`, `subscribed`, `my_open_tasks` and the SLA filters on cases that
  match;
- a case webhook that fires, that is, a request arriving at its `url`, the limit of five webhooks per
  team, and what `version_number` takes;
- a sensitive field read by a key without the permission, and `group_name` of a field;
- the 500 that an update of a field to `regex` with a string gives, which was seen once and is not a
  case that tapi sends.
