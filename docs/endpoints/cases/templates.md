# Templates

- **Access:** `tines.cases.templates`
- **Import:** `from tapi.cases import Templates`
- **Part of:** [Cases](cases.md)

The case templates of a team: the values that a new case starts with.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the case templates of a team. | `GET /api/v1/case_templates` |
| [`get`](#get) | Get a case template. | `GET /api/v1/case_templates/{template_id}` |
| [`create`](#create) | Create a case template in a team. | `POST /api/v1/case_templates` |
| [`update`](#update) | Change a case template. | `PATCH /api/v1/case_templates/{template_id}` |
| [`delete`](#delete) | Delete a case template. | `DELETE /api/v1/case_templates/{template_id}` |
| [`export`](#export) | Export a case template in a form that `import_` takes. | `GET /api/v1/case_templates/{template_id}/export` |
| [`import_`](#import_) | Import case templates into a team. | `POST /api/v1/case_templates/import` |
| [`preview`](#preview) | Preview the case that a template would create. | `GET /api/v1/case_templates/{template_id}/preview` |

## Methods breakdown

### `list`

`GET /api/v1/case_templates`

List the case templates of a team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | yes | — | The ID of the team. |
| `search` | `str` | no | — | Only templates whose name matches this text. |
| `per_page` | `int` | no | Positive integer | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `case_templates`, the templates of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The team does not exist or is not visible to the key. |

### `get`

`GET /api/v1/case_templates/{template_id}`

Get a case template.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `template_id` | `int` | yes | — | The ID of the template. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the template. |
| 404 | The template does not exist or is not visible to the key. |

### `create`

`POST /api/v1/case_templates`

Create a case template in a team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | yes | — | The ID of the team that gets the template. |
| `name` | `str` | yes | — | The name of the template. It is unique within the team. |
| `emoji` | `str` | no | — | The emoji of the template, as a shortcode such as `:mag:`. |
| `options` | [`TemplateOptions`](#templateoptions) | no | — | What a case created from the template gets. A name and a description can hold formulas and field mentions. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the created template. |
| 404 | The team does not exist or is not visible to the key. |

### `update`

`PATCH /api/v1/case_templates/{template_id}`

Change a case template. Cases that were created from it before are not changed.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `template_id` | `int` | yes | — | The ID of the template. |
| `name` | `str` | no | — | A new name. |
| `emoji` | `str` | no | — | A new emoji, as a shortcode. |
| `options` | [`TemplateOptions`](#templateoptions) | no | — | New options. An option that is sent replaces the old value as a whole, and one that is left out keeps its value. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated template. |
| 404 | The template does not exist or is not visible to the key. |

### `delete`

`DELETE /api/v1/case_templates/{template_id}`

Delete a case template. Cases created from it are not changed.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `template_id` | `int` | yes | — | The ID of the template. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The template does not exist or is not visible to the key. |

### `export`

`GET /api/v1/case_templates/{template_id}/export`

Export a case template in a form that `import_` takes.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `template_id` | `int` | yes | — | The ID of the template. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the template in a form that `import_` takes, to copy it to another team or tenant: an object with `schema_version`, `exported_at` and `templates`, each with `name`, `emoji`, `options`, `input_values` and `field_definitions`. |
| 404 | The template does not exist or is not visible to the key. |

### `import_`

`POST /api/v1/case_templates/import`

Import case templates into a team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | yes | — | The ID of the team that gets the templates. |
| `data` | `Mapping[str, Any]` | yes | — | What `export` returned. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is an object with `case_templates`, the templates that were created. |
| 404 | The team does not exist or is not visible to the key. |
| 422 | `data` is not a valid export. |

### `preview`

`GET /api/v1/case_templates/{template_id}/preview`

Preview the case that a template would create.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `template_id` | `int` | yes | — | The ID of the template. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the case that the template would create, with `name`, `description`, `status`, `priority`, `sub_status`, `assignees`, `tags`, `fields`, `actions`, `blocks`, `tasks`, `closure_conditions` and `metadata`. |
| 404 | The template does not exist or is not visible to the key. |

## Types

### `TemplateOptions`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `name` | `str` | no | — | The name of the case. It can hold formulas and field mentions. |
| `description` | `str` | no | — | The description of the case. It can hold formulas and field mentions. |
| `status` | `CaseStatus` | no | `OPEN`, `CLOSED` | The status of the case. |
| `priority` | `CasePriority` | no | `CRITICAL`<br>`HIGH`<br>`MEDIUM`<br>`LOW`<br>`INFO` | The priority of the case. |
| `sub_status_id` | `int` | no | — | The ID of a case status of the team. |
| `assignee_emails` | `Sequence[str]` | no | — | The email addresses of the users to assign. |
| `tag_names` | `Sequence[str]` | no | — | The names of the tags to add. |
| `team_case_buttons` | [`Sequence[TemplateButton]`](#templatebutton) | no | — | The buttons of the case. |
| `tasks` | [`Sequence[TaskInput]`](#taskinput) | no | — | The tasks to create with the case. |
| `closure_conditions` | [`Sequence[ClosureCondition]`](#closurecondition) | no | — | The conditions that must be true to close the case. |
| `blocks` | [`Sequence[CaseBlock]`](#caseblock) | no | — | The blocks to create with the case. |
| `field_values` | `Mapping[str, Any]` | no | — | The values of the case fields, keyed by the ID of the field. |
| `metadata` | `Mapping[str, Any]` | no | — | Key-value pairs to store on the case. |

### `TemplateButton`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `button_type` | `CaseActionType` | yes | `webhook`<br>`page`<br>`chat`<br>`story`<br>`app` | The type of the button. |
| `url` | `str` | yes | — | The address that the button opens or calls. |
| `label` | `str` | yes | — | The name that identifies the button. |
| `button_text` | `str` | no | — | The text of the button. |

### `TaskInput`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `description` | `str` | yes | — | The description of the task. |
| `assignee_emails` | `Sequence[str]` | no | — | The email addresses of the users to assign. |

### `ClosureCondition`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `name` | `str` | yes | — | The name of the condition. |
| `formula` | `str` | yes | — | A formula that must be true, such as `=SIZE(team_case.assignees) > 0`. |

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
