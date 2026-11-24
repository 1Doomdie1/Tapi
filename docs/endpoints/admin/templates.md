# Templates

- **Access:** `tines.admin.templates`
- **Import:** `from tapi.admin import Templates`
- **Part of:** [Admin](admin.md)

Manage the private templates of the tenant. A template is an action that can be reused in stories.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the private templates, optionally filtered by text or by folder. | `GET /api/v1/admin/templates` |
| [`get`](#get) | Get a template. | `GET /api/v1/admin/templates/{template_id}` |
| [`create`](#create) | Create a template. | `POST /api/v1/admin/templates` |
| [`update`](#update) | Change a template. | `PATCH /api/v1/admin/templates/{template_id}` |
| [`delete`](#delete) | Delete a template. | `DELETE /api/v1/admin/templates/{template_id}` |
| [`move`](#move) | Move a template to another team. | `POST /api/v1/admin/templates/{template_id}/move` |

## Methods breakdown

### `list`

`GET /api/v1/admin/templates`

List the private templates, optionally filtered by text or by folder.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `search` | `str` | no | — | Only templates that match this text in the name, description, vendor, product or action options. |
| `folder_id` | `int` | no | — | Only templates in this template folder. |
| `per_page` | `int` | no | 1 to 500 | Results per page. Tines defaults to 20. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `admin/templates`, the templates of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | `folder_id` does not exist. |

### `get`

`GET /api/v1/admin/templates/{template_id}`

Get a template.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `template_id` | `int` | yes | — | The ID of the template. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the template. |
| 404 | The template does not exist. |

### `create`

`POST /api/v1/admin/templates`

Create a template.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `name` | `str` | yes | — | The name of the template. |
| `agent_type` | `AgentType` | yes | `Agents::EmailAgent`<br>`Agents::EventTransformationAgent`<br>`Agents::HTTPRequestAgent`<br>`Agents::IMAPAgent`<br>`Agents::LLMAgent`<br>`Agents::TriggerAgent`<br>`Agents::WebhookAgent`<br>`Agents::SendToStoryAgent` | The type of action to create. |
| `agent_options` | `Mapping[str, Any]` | yes | — | The options of the action, as an object. |
| `product` | `str` | yes | — | The name of the product. |
| `description` | `str` | yes | — | A description of the template. |
| `vendor` | `str` | yes | — | The name of the vendor. |
| `team_id` | `int` | no | — | The team that the template belongs to. Without it the template has no team and `read_access` is `GLOBAL`. |
| `folder_id` | `int` | no | — | A template folder of the same team. |
| `read_access` | `ReadAccess` | no | `TEAM`, `GLOBAL`, `SPECIFIC_TEAMS` | Where the template can be used. Tines defaults to `TEAM` when `team_id` is sent, and to `GLOBAL` otherwise. `SPECIFIC_TEAMS` is a premium feature. |
| `shared_team_slugs` | `Sequence[str]` | no | — | The slugs of the teams where the template can be used. Needed for `SPECIFIC_TEAMS`. |
| `action_inputs` | [`Sequence[ActionInput]`](#actioninput) | no | List of [`ActionInput`](#actioninput) objects | The input parameters of the template. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the created template. |
| 404 | `team_id` or `folder_id` does not exist. |
| 422 | A required argument is missing, or `agent_type`, `agent_options` or an input is not valid. |

### `update`

`PATCH /api/v1/admin/templates/{template_id}`

Change a template. It is a full update: send the name, description, type, options, vendor and product every time. To change the team, use `move`.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `template_id` | `int` | yes | — | The ID of the template. |
| `name` | `str` | yes | — | The name of the template. |
| `description` | `str` | yes | — | A description of the template. |
| `agent_type` | `AgentType` | yes | `Agents::EmailAgent`<br>`Agents::EventTransformationAgent`<br>`Agents::HTTPRequestAgent`<br>`Agents::IMAPAgent`<br>`Agents::LLMAgent`<br>`Agents::TriggerAgent`<br>`Agents::WebhookAgent`<br>`Agents::SendToStoryAgent` | The type of action. It cannot be changed. |
| `agent_options` | `Mapping[str, Any]` | yes | — | The options of the action, as an object. |
| `vendor` | `str` | yes | — | The name of the vendor. |
| `product` | `str` | yes | — | The name of the product. |
| `folder_id` | `int` | no | — | A template folder of the same team. |
| `read_access` | `ReadAccess` | no | `TEAM`, `GLOBAL`, `SPECIFIC_TEAMS` | Where the template can be used. |
| `shared_team_slugs` | `Sequence[str]` | no | — | The slugs of the teams where the template can be used. Needed for `SPECIFIC_TEAMS`. |
| `action_inputs` | [`Sequence[ActionInput]`](#actioninput) | no | List of [`ActionInput`](#actioninput) objects | The input parameters, which replace the old ones. An empty list removes them. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated template. |
| 404 | `folder_id` does not exist. |
| 422 | A required argument is missing, the type changed, an option or an input is not valid, or the template does not exist. |

### `delete`

`DELETE /api/v1/admin/templates/{template_id}`

Delete a template.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `template_id` | `int` | yes | — | The ID of the template. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | The template is deleted. No data. |
| 404 | The template does not exist. |

### `move`

`POST /api/v1/admin/templates/{template_id}/move`

Move a template to another team. The access of the template is reset to the team only.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `template_id` | `int` | yes | — | The ID of the template. |
| `team_id` | `int` | yes | — | The team to move the template to. |
| `folder_id` | `int` | no | — | A template folder of the target team. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated template. |
| 404 | The template, the team or the folder does not exist. |

## Types

### `ActionInput`

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `name` | `str` | yes | — | The name of the input. |
| `type` | `ActionInputType` | yes | `TEXT`<br>`NUMBER`<br>`BOOLEAN`<br>`DATE`<br>`OBJECT`<br>`OPTION`<br>`CODE`<br>`CREDENTIAL` | The type of the input. |
| `required` | `bool` | no | `True`, `False` | Whether a value is needed. |
| `description` | `str` | no | — | A description of the input. |
| `default_value` | `Any` | no | — | The default value: a string for `TEXT`, `DATE` and `CODE`, a number for `NUMBER`, a boolean for `BOOLEAN`, any JSON for `OBJECT` and an array for `OPTION`. A string that starts with `=` is a formula. |
| `data` | `Mapping[str, Any]` | no | — | Extra settings: `json_schema` for `OBJECT`, `options` and `multi_select_enabled` for `OPTION`, and `code_language` for `CODE`. |

- A template takes at most 300 inputs, with unique names, and at most one `CREDENTIAL`.
- A `CREDENTIAL` input needs `required` set to `True` and takes no other field.
