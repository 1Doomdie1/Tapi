# Actions

- **Access:** `tines.stories.actions`
- **Import:** `from tapi.stories import Actions`
- **Part of:** [Stories](stories.md)

The actions of stories: create, change and delete them, and read or delete their events and logs.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the actions, optionally of a story, a team, a group, a draft or a type. | `GET /api/v1/actions` |
| [`get`](#get) | Get an action. | `GET /api/v1/actions/{action_id}` |
| [`create`](#create) | Create an action in a story or a group. | `POST /api/v1/actions` |
| [`update`](#update) | Update an action. | `PATCH /api/v1/actions/{action_id}` |
| [`delete`](#delete) | Delete an action. | `DELETE /api/v1/actions/{action_id}` |
| [`list_events`](#list_events) | List the events that an action emitted. | `GET /api/v1/actions/{action_id}/events` |
| [`list_logs`](#list_logs) | List the logs of an action. | `GET /api/v1/actions/{action_id}/logs` |
| [`delete_events`](#delete_events) | Delete the events of an action. | `DELETE /api/v1/actions/{action_id}/remove_events` |
| [`delete_logs`](#delete_logs) | Delete the logs of an action. | `DELETE /api/v1/actions/{action_id}/remove_logs` |
| [`clear_memory`](#clear_memory) | Clear the memory of an action. | `DELETE /api/v1/actions/{action_id}/clear_memory` |

## Methods breakdown

### `list`

`GET /api/v1/actions`

List the actions, optionally of a story, a team, a group, a draft or a type.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | no | — | Only actions of this story. |
| `story_mode` | `StoryMode` | no | `TEST`, `LIVE` | Only actions of the story in this mode. Use it with `story_id`. |
| `team_id` | `int` | no | — | Only actions of this team. |
| `group_id` | `int` | no | — | Only actions of this group. |
| `action_type` | `ActionFilterType` | no | `Agents::CaseAgent`, `Agents::EmailAgent`, `Agents::EventTransformationAgent`, `Agents::FormAgent`, `Agents::GroupAgent`, `Agents::HTTPRequestAgent`, `Agents::IMAPAgent`, `Agents::LLMAgent`, `Agents::RecordAgent`, `Agents::RunScriptAgent`, `Agents::SendToStoryAgent`, `Agents::TriggerAgent`, `Agents::WebhookAgent` | Only actions of this type. |
| `draft_id` | `int` | no | — | Only actions of this draft. |
| `include_live_activity` | `bool` | no | `True`, `False` | Adds `pending_action_runs_count` to each action. |
| `per_page` | `int` | no | Positive integer | Results per page. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `agents`, the actions of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | `story_id`, `group_id` or `team_id` does not exist, or `draft_id` is sent without `story_id`. |

### `get`

`GET /api/v1/actions/{action_id}`

Get an action.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `action_id` | `int` | yes | — | The ID of the action to retrieve. |
| `include_live_activity` | `bool` | no | `True`, `False` | Adds `pending_action_runs_count` to the action. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the action. |
| 404 | The action does not exist or is not visible to the key. |

### `create`

`POST /api/v1/actions`

Create an action in a story or a group.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `type` | `ActionType` | yes | `Agents::EmailAgent`<br>`Agents::EventTransformationAgent`<br>`Agents::HTTPRequestAgent`<br>`Agents::IMAPAgent`<br>`Agents::LLMAgent`<br>`Agents::TriggerAgent`<br>`Agents::WebhookAgent`<br>`Agents::SendToStoryAgent`<br>`Agents::GroupAgent`<br>`Agents::RunScriptAgent` | The type of the action. |
| `name` | `str` | yes | — | The name of the action. |
| `options` | `Mapping[str, Any]` | no | — | The options of the action. Its keys depend on the type. |
| `position` | [`ActionPosition`](#actionposition) | no | — | The coordinates of the action on the story diagram. |
| `story_id` | `int` | no | — | The ID of the story. Send `story_id` or `group_id`. |
| `group_id` | `int` | no | — | The ID of the group. Send `story_id` or `group_id`. |
| `description` | `str` | no | — | A description of the action. |
| `disabled` | `bool` | no | `True`, `False` | Whether the action is disabled. |
| `source_ids` | `Sequence[int]` | no | — | The IDs of the actions that it receives events from. Not with `links_to_sources`. |
| `links_to_sources` | [`Sequence[SourceLink]`](#sourcelink) | no | — | Links from source actions. Not with `source_ids`. `NO_MATCH` needs a Condition action as the source. |
| `receiver_ids` | `Sequence[int]` | no | — | The IDs of the actions that it emits events to. Not with `links_to_receivers`. |
| `links_to_receivers` | [`Sequence[ReceiverLink]`](#receiverlink) | no | — | Links to receiver actions. Not with `receiver_ids`. `NO_MATCH` needs the receiver to be a Condition action. |
| `schedule` | `Mapping[str, Any] \| Sequence[Mapping[str, Any]]` | no | An object with `cron` and `timezone`, or a list of them | The cron schedule: an object with `cron` and `timezone`, or a list of them. |
| `monitor_failures` | `bool` | no | `True`, `False` | Whether Tines sends a notification when the action fails. |
| `monitor_all_events` | `bool` | no | `True`, `False` | Whether all events are monitored. |
| `monitor_no_events_emitted` | `int` | no | — | Seconds without an event after which Tines sends a notification. |
| `draft_id` | `int` | no | — | The ID of the draft. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the created action. |
| 400 | The links are mixed with the ID lists, a link has a type that does not exist, or `num_runs_to_save` is used with an unsupported type. |
| 404 | Neither a story nor a group is given, or one of them does not exist. |
| 422 | `type` does not exist, or a `NO_MATCH` link has no Condition action. |

### `update`

`PATCH /api/v1/actions/{action_id}`

Update an action.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `action_id` | `int` | yes | — | The ID of the action. |
| `name` | `str` | no | — | The new name. |
| `description` | `str` | no | — | The new description. |
| `options` | `Mapping[str, Any]` | no | — | The new options block. |
| `position` | [`ActionPosition`](#actionposition) | no | — | The new coordinates on the story diagram. |
| `source_ids` | `Sequence[int]` | no | — | The IDs of the actions that it receives events from. Not with `links_to_sources`. |
| `links_to_sources` | [`Sequence[SourceLink]`](#sourcelink) | no | — | Links from source actions. Not with `source_ids`. |
| `receiver_ids` | `Sequence[int]` | no | — | The IDs of the actions that it emits events to. Not with `links_to_receivers`. |
| `links_to_receivers` | [`Sequence[ReceiverLink]`](#receiverlink) | no | — | Links to receiver actions. Not with `receiver_ids`. |
| `schedule` | `Mapping[str, Any] \| Sequence[Mapping[str, Any]]` | no | An object with `cron` and `timezone`, or a list of them | The cron schedule, as for `create`. |
| `disabled` | `bool` | no | `True`, `False` | Whether the action is disabled. |
| `monitor_failures` | `bool` | no | `True`, `False` | Whether Tines sends a notification when the action fails. Send it with `monitor_all_events`. |
| `monitor_all_events` | `bool` | no | `True`, `False` | Whether all events are monitored. Send it with `monitor_failures`. |
| `monitor_no_events_emitted` | `int` | no | — | Seconds without an event after which Tines sends a notification. Send it with the two others. |
| `num_runs_to_save` | `int` | no | — | The number of story runs to save, for Receive Email and Webhook actions. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated action. |
| 400 | The links are mixed with the ID lists, or `num_runs_to_save` is used with an unsupported type. |
| 404 | The action does not exist or is not visible to the key. |
| 422 | `monitor_failures` or `monitor_all_events` is sent alone. |

### `delete`

`DELETE /api/v1/actions/{action_id}`

Delete an action. The links to it disappear from the other actions.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `action_id` | `int` | yes | — | The ID of the action to delete. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The action does not exist or is not visible to the key. |

### `list_events`

`GET /api/v1/actions/{action_id}/events`

List the events that an action emitted.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `action_id` | `int` | yes | — | The ID of the action. |
| `since_id` | `int` | no | — | Only events after this event ID. |
| `until_id` | `int` | no | — | Only events until and including this event ID. |
| `since` | `datetime \| str` | no | ISO 8601 string, or `datetime` | Only events created after this time. A naive `datetime` is treated as UTC. |
| `until` | `datetime \| str` | no | ISO 8601 string, or `datetime` | Only events created until this time. A naive `datetime` is treated as UTC. |
| `show_reemitted_events_only` | `bool` | no | `True`, `False` | Only events that were re-emitted. |
| `exclude_previous_event_payloads` | `bool` | no | `True`, `False` | Keep only the output of the action in the payload of each event, without the payloads that came from upstream events of the story run. |
| `per_page` | `int` | no | Positive integer | Results per page. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `events`, the events of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. A time is not valid. |
| 404 | The action does not exist or is not visible to the key. |
| 422 | The payloads of a page are too large. |

### `list_logs`

`GET /api/v1/actions/{action_id}/logs`

List the logs of an action.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `action_id` | `int` | yes | — | The ID of the action. |
| `levels` | `Sequence[ActionLogLevel]` | no | `2`, `3`, `4` | Only logs of these severity levels: `2` is a warning, `3` is info and `4` is an error. |
| `per_page` | `int` | no | Positive integer | Results per page. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `action_logs`, the logs of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The action does not exist or is not visible to the key. |

### `delete_events`

`DELETE /api/v1/actions/{action_id}/remove_events`

Delete the events of an action.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `action_id` | `int` | yes | — | The ID of the action. |
| `async_deletion` | `bool` | no | `True`, `False` | Whether to delete in a background job, and not before the reply. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the action. |
| 400 | `async_deletion` is not a boolean. |
| 404 | The action does not exist or is not visible to the key. |

### `delete_logs`

`DELETE /api/v1/actions/{action_id}/remove_logs`

Delete the logs of an action.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `action_id` | `int` | yes | — | The ID of the action. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the action. |
| 404 | The action does not exist or is not visible to the key. |

### `clear_memory`

`DELETE /api/v1/actions/{action_id}/clear_memory`

Clear the memory of an action.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `action_id` | `int` | yes | — | The ID of the action. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the action. |
| 422 | The action does not exist. |

## Types

### `ActionPosition`

The coordinates of an action on the story diagram.

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `x` | `float` | yes | — | The horizontal coordinate. |
| `y` | `float` | yes | — | The vertical coordinate. |

### `SourceLink`

A link from a source action: its `source_id` and, optionally, the link `type`.

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `source_id` | `int` | yes | — | The ID of the source action. |
| `type` | `LinkType` | no | `DEFAULT`, `NO_MATCH`, `FAILURE` | The type of the link. Tines defaults to `DEFAULT`. |

### `ReceiverLink`

A link to a receiver action: its `receiver_id` and, optionally, the link `type`.

| Field | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `receiver_id` | `int` | yes | — | The ID of the receiver action. |
| `type` | `LinkType` | no | `DEFAULT`, `NO_MATCH`, `FAILURE` | The type of the link. Tines defaults to `DEFAULT`. |
