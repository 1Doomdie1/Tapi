# Admin: templates

A template is an action that can be reused in stories. This sub-area manages the private templates of
the tenant. It is a sub-area of [`admin`](admin.md), available as `tines.admin.templates`, and the
class is `tapi.admin.Templates`. Every method returns a [`Response`](../responses.md).

| Method                                                                        | HTTP route                                          |
| ----------------------------------------------------------------------------- | --------------------------------------------------- |
| `list(...)`                                                                   | `GET /api/v1/admin/templates`                       |
| `get(template_id=...)`                                                        | `GET /api/v1/admin/templates/{template_id}`         |
| `create(name=..., agent_type=..., agent_options=..., product=..., description=..., vendor=...)` | `POST /api/v1/admin/templates` |
| `update(template_id=..., name=..., description=..., agent_type=..., agent_options=..., vendor=..., product=...)` | `PATCH /api/v1/admin/templates/{template_id}` |
| `delete(template_id=...)`                                                     | `DELETE /api/v1/admin/templates/{template_id}`      |
| `move(template_id=..., team_id=...)`                                          | `POST /api/v1/admin/templates/{template_id}/move`   |

## The template

| Field               | Meaning                                                                               |
| ------------------- | ------------------------------------------------------------------------------------- |
| `id`                | The ID of the template.                                                               |
| `name`              | The name.                                                                             |
| `description`       | A description.                                                                        |
| `agent_type`        | The type of action, such as `Agents::EventTransformationAgent`.                       |
| `agent_options`     | The options of the action, as an object.                                              |
| `vendor`            | The name of the vendor.                                                               |
| `product`           | The name of the product.                                                              |
| `team_id`           | The ID of the team that the template belongs to, or `null` for a template without a team. |
| `folder_id`         | The ID of the template folder, or `null` when it is not in a folder.                  |
| `read_access`       | `TEAM`, `GLOBAL` or `SPECIFIC_TEAMS`.                                                 |
| `shared_team_slugs` | The slugs of the teams where it can be used, empty unless `read_access` is `SPECIFIC_TEAMS`. |
| `action_inputs`     | The input parameters, a list of objects.                                              |

## `agent_type`

`AgentType` is `tapi.admin.AgentType`. The Tines docs and the OpenAPI document give eight values:
`Agents::EmailAgent`, `Agents::EventTransformationAgent`, `Agents::HTTPRequestAgent`,
`Agents::IMAPAgent`, `Agents::LLMAgent`, `Agents::TriggerAgent`, `Agents::WebhookAgent` and
`Agents::SendToStoryAgent`. The error of a value that is not valid lists the action types that Tines
knows: `eventTransformation`, `trigger`, `webhook`, `httpRequest`, `sendToStory`, `email`, `imap`,
`grpcRequest`, `mcpRequest`, `group`, `groupInput`, `groupOutput`, `form`, `file`, `record`, `case`,
`runScript` and `llm`. Both kinds are typed. `eventTransformation` was accepted in place of
`Agents::EventTransformationAgent`, and the reply holds the `Agents::` name. The options are checked
against the type: a `webhook` without a `path` and a `secret` is a `422`.

## `list()`

The endpoint is paginated, and one call returns one page; see [Pagination](../pagination.md).

| Parameter   | Type  | Meaning                                                                          |
| ----------- | ----- | -------------------------------------------------------------------------------- |
| `search`    | `str` | Only templates that match this text in the name, description, vendor, product or action options. |
| `folder_id` | `int` | Only templates in this folder.                                                   |
| `per_page`  | `int` | The number of results per page. Tines defaults to 20 and caps it at 500.         |
| `page`      | `int` | The page to return, starting at 1. Tines defaults to 1.                          |

`data` is an object with `admin/templates`, the templates of the page, and `meta`, the pagination
details. The Tines docs show `search` in a JSON body in one example and as a query parameter in the
table. tapi sends it in the query, which worked.

## `create()`

| Parameter           | Type                      | Meaning                                                              |
| ------------------- | ------------------------- | -------------------------------------------------------------------- |
| `name`              | `str`                     | The name. Required. Tines does not require it to be unique.          |
| `agent_type`        | `AgentType`               | The type of action. Required.                                        |
| `agent_options`     | mapping                   | The options of the action. Required.                                 |
| `product`           | `str`                     | The name of the product. Required.                                   |
| `description`       | `str`                     | A description. Required.                                             |
| `vendor`            | `str`                     | The name of the vendor. Required.                                    |
| `team_id`           | `int`                     | The team of the template. Without it the template has no team and `read_access` is `GLOBAL`. |
| `folder_id`         | `int`                     | A template folder of the same team.                                  |
| `read_access`       | `ReadAccess`              | Where the template can be used. Tines defaults to `TEAM` when `team_id` is sent, and to `GLOBAL` otherwise. |
| `shared_team_slugs` | sequence of `str`         | The slugs of the teams. Needed for `SPECIFIC_TEAMS`.                 |
| `action_inputs`     | sequence of `ActionInput` | The input parameters.                                                |

The OpenAPI document requires only the name, the type, the options and the product. Tines also refused
a template without a `description` or a `vendor`, as the Tines docs imply. The reply has a `200`
status, not a `201`, and `data` is the template. A second template with the same name was accepted.
`SPECIFIC_TEAMS` is a premium feature: on this tenant it was accepted with no error and had no effect,
and the template kept `TEAM`.

An `ActionInput` has `name` and `type`, and optionally `required`, `description`, `default_value`
and `data`. `type` is `ActionInputType`: `TEXT`, `NUMBER`, `BOOLEAN`, `DATE`, `OBJECT`, `OPTION`,
`CODE` or `CREDENTIAL`. The Tines docs set these limits:

- at most 300 inputs, with unique names, and at most one `CREDENTIAL`;
- a `CREDENTIAL` needs `required` set to true and takes no other field. Another field is a `422` with
  `Invalid key: description, for action input: c (CREDENTIAL)`;
- `default_value` is a string for `TEXT`, `DATE` and `CODE`, a number for `NUMBER`, a boolean for
  `BOOLEAN`, any JSON for `OBJECT` and an array for `OPTION`. A string that starts with `=` is a
  formula;
- `data` holds `json_schema` for `OBJECT`, `options` and `multi_select_enabled` for `OPTION`, and
  `code_language` for `CODE`.

## `update()`

`update` is a full update, as the Tines docs show it with `PUT`. The OpenAPI document lists `PUT` and
`PATCH` and requires only the name and the product, but every call that left out the name, the
description, the type, the options, the vendor or the product was a `422`. tapi sends `PATCH`, and
`PUT` worked as well.

| Parameter           | Type                      | Meaning                                                              |
| ------------------- | ------------------------- | -------------------------------------------------------------------- |
| `template_id`       | `int`                     | The ID of the template. Required.                                    |
| `name`              | `str`                     | The name. Required.                                                  |
| `description`       | `str`                     | A description. Required.                                             |
| `agent_type`        | `AgentType`               | The type of action. Required, and it cannot change: another type is a `422` with `Action type cannot be changed`. The camelCase name of the same type was accepted. |
| `agent_options`     | mapping                   | The options of the action. Required, and it must be an object.       |
| `vendor`            | `str`                     | The name of the vendor. Required.                                    |
| `product`           | `str`                     | The name of the product. Required.                                   |
| `folder_id`         | `int`                     | A template folder of the same team. Tines takes `null` to remove the folder, which tapi cannot send. |
| `read_access`       | `ReadAccess`              | Where the template can be used. Unchanged when left out.             |
| `shared_team_slugs` | sequence of `str`         | The slugs of the teams. Unchanged when left out.                     |
| `action_inputs`     | sequence of `ActionInput` | The input parameters. They replace the existing ones, are kept when the argument is left out, and an empty list removes them. |

A `team_id` in the body is ignored, so a template changes team only with `move`. `update` returns the
template with a `200` status. Renaming a template onto the name of another one was accepted.

## `get()`, `delete()` and `move()`

- `get(template_id=...)` returns the template.
- `delete(template_id=...)` has a `204` status.
- `move(template_id=..., team_id=..., folder_id=...)` moves the template to another team and returns it
  with a `200` status. The access of the template is reset to the team only, and the resources and
  credentials that it uses may not exist in the other team. `folder_id` is a template folder of the
  target team. Moving to the team that the template already has was accepted.

## Errors

| Status | When                                                                                          |
| ------ | --------------------------------------------------------------------------------------------- |
| `400`  | `list` with a `per_page` or `page` that is not a positive integer (`['Invalid per_page: 0. per_page must be a positive integer.']`). |
| `404`  | `get`, `move` and `delete` with a template that does not exist (`['Template not found']`). `list`, `create`, `update` and `move` with a folder that does not exist (`['Folder not found']`), and `create` and `move` with a team that does not exist (`['Team not found']`). |
| `422`  | `create` and `update` with a required field that is missing (a list of objects such as `{'description': 'Expected value to not be null'}`, where the type is named `action_type`), an `agent_type` that is not valid (the message lists the valid ones), options that are not valid for the type (`['Validation failed: ...']`) or that are not an object, and an input that is not valid. `update` with a template that does not exist is also a `422`, with an object `{'message': "Couldn't find Template with 'id'=..."}`. |

## Not tried

Everything above was tried on 2026-11-24 with a template that was created for the purpose and deleted
afterwards, in a tenant that had none. These were not seen:

- a template in a folder, since the tenant had no template folder;
- `SPECIFIC_TEAMS` where the feature is available, and the other action types with valid options;
- the items of `list` for a template that other teams share.
