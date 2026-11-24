# Stories: actions

Actions are the steps of a story. The Tines docs list them in the Stories section, and tapi follows
that: they are a sub-area of [stories](stories.md), available as `tines.stories.actions`, and the
class is `tapi.stories.Actions`. The page is separate because it is long. Every method returns a
[`Response`](../responses.md).

| Method                                                 | HTTP route                                         |
| ------------------------------------------------------ | -------------------------------------------------- |
| `actions.list(...)`                                    | `GET /api/v1/actions`                              |
| `actions.get(action_id=..., ...)`                      | `GET /api/v1/actions/{action_id}`                  |
| `actions.create(type=..., name=..., ...)`              | `POST /api/v1/actions`                             |
| `actions.update(action_id=..., ...)`                   | `PATCH /api/v1/actions/{action_id}`                |
| `actions.delete(action_id=...)`                        | `DELETE /api/v1/actions/{action_id}`               |
| `actions.list_events(action_id=..., ...)`              | `GET /api/v1/actions/{action_id}/events`           |
| `actions.list_logs(action_id=..., ...)`                | `GET /api/v1/actions/{action_id}/logs`             |
| `actions.delete_events(action_id=..., ...)`            | `DELETE /api/v1/actions/{action_id}/remove_events` |
| `actions.delete_logs(action_id=...)`                   | `DELETE /api/v1/actions/{action_id}/remove_logs`   |
| `actions.clear_memory(action_id=...)`                  | `DELETE /api/v1/actions/{action_id}/clear_memory`  |

The sections below name the methods without the `actions.` prefix.

All parameters are keyword-only. Parameters left as `None` are not sent, but `False` and `""` are.
The Tines docs do not state which key types or permissions these endpoints need. The OpenAPI
document says that personal, service, team and tenant owner keys are all accepted, and that a key
without access to a resource receives a 404.

## Events

The events of the whole tenant, at `/api/v1/events`, are not part of this page: they are the
sub-area `tines.stories.events`, described on the [stories page](stories.md#events). `list_events`
lists the events of one action.

## The action

`data` of `get`, `create`, `update`, `delete_events`, `delete_logs` and `clear_memory` is an action,
and `list` returns a list of them under `agents`, which is the old name. An action has:

| Field                                                         | Meaning                                                                    |
| ------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `id`, `guid`, `slug`                                          | The ID, the unique identifier and the underscored name of the action.      |
| `type`                                                        | The type, such as `Agents::HTTPRequestAgent`. See [Types](#types).         |
| `name`, `description`                                         | The name, and the description, which is `null` when there is none.         |
| `user_id`                                                     | The owner.                                                                 |
| `options`                                                     | The options block, an object whose keys depend on the type.                |
| `position`                                                    | The coordinates on the story diagram, an object with `x` and `y`.          |
| `story_id`, `story_mode`                                      | The story, and its mode, `LIVE` or `TEST`.                                 |
| `group_id`, `nested_group_id`                                 | The group, and the nested group. Both are `null` for an action in no group. |
| `team_id`                                                     | The team.                                                                  |
| `disabled`                                                    | Whether the action is disabled.                                            |
| `schedule`                                                    | A list of objects with a `cron` and a `timezone`, or `null`.               |
| `sources`, `receivers`                                        | The IDs of the actions it receives events from, and emits events to.       |
| `links_to_sources`, `links_to_receivers`                      | The same links, as objects with `source_id` or `receiver_id` and a `link_type`. See [Links](#links). |
| `monitor_failures`, `monitor_all_events`                      | Whether failures and all events are monitored.                             |
| `monitor_no_events_emitted`                                   | Seconds without an event after which Tines notifies, or `null`.            |
| `created_at`, `updated_at`                                    | ISO 8601 timestamps.                                                       |
| `last_check_at`, `last_receive_at`, `last_event_at`, `last_error_log_at` | When the action last ran on its schedule, received an event, emitted an event and logged an error. `null` if never. |
| `blended_events_count`, `logs_count`                          | The number of events emitted in `TEST` and `LIVE` mode, and the number of logs. |
| `time_saved_unit`, `time_saved_value`                         | The time saved by the action.                                              |
| `page`                                                        | The page of a page action, or `null`.                                      |
| `action_memory_contents`                                      | An object with `values`, a list of the values the action keeps in memory.  |
| `story_run_save_setting`                                      | How many story runs to save. Only for Receive Email and Webhook actions.   |

The live tenant also returned `integration`, which neither the Tines docs nor the OpenAPI document
list. It was `null`, or an object with `action_inputs`. The docs list `draft_id` and `draft_name`
in the replies of `create` and `list`, and the replies seen did not have them. None of the stories
had change control. With `include_live_activity`, an action also has `pending_action_runs_count`.

## `list()`

Paginated: one call returns one page; see [Pagination](../pagination.md). `data` holds `agents` and
`meta`.

| Parameter               | Type   | Meaning                                                                       |
| ----------------------- | ------ | ----------------------------------------------------------------------------- |
| `story_id`              | `int`  | Only actions of this story.                                                   |
| `story_mode`            | `str`  | `LIVE` or `TEST`. The docs say to use it with `story_id`.                     |
| `team_id`               | `int`  | Only actions of this team.                                                    |
| `group_id`              | `int`  | Only actions of this group.                                                   |
| `action_type`           | `str`  | Only actions of this type. See [Types](#types).                               |
| `draft_id`              | `int`  | Only actions of this draft. It needs `story_id`.                              |
| `include_live_activity` | `bool` | Adds `pending_action_runs_count` to each action. Tines defaults to `False`.   |
| `per_page`              | `int`  | Results per page. Tines defaults to 20 and caps it at 500.                    |
| `page`                  | `int`  | The page, starting at 1. Tines defaults to 1.                                 |

## `get()`

`action_id` is required, and `include_live_activity` is optional. When no action with that ID is
visible to the key, the reply is a `404` with `['Agent not found']`.

## `create()`

`type` and `name` are required, and the reply has a 201 status. A story or a group must be given. If
change control is enabled on the story and no `draft_id` is given, Tines adds the action to a draft
called `test`.

| Parameter                   | Type                   | Meaning                                                           |
| --------------------------- | ---------------------- | ----------------------------------------------------------------- |
| `type`                      | `str`                  | The type of the action. Required. See [Types](#types).            |
| `name`                      | `str`                  | The name of the action. Required.                                 |
| `options`                   | `dict`                 | The options block. See [Options](#options).                       |
| `position`                  | `dict`                 | `{"x": 100, "y": 200}`, the coordinates on the story diagram.     |
| `story_id`, `group_id`      | `int`                  | The story or the group the action is added to.                    |
| `description`               | `str`                  | A description of the action.                                      |
| `disabled`                  | `bool`                 | Whether the action is disabled. Tines defaults to `False`.        |
| `source_ids`                | `Sequence[int]`        | The actions that this action receives events from. Not with `links_to_sources`. |
| `links_to_sources`          | `Sequence[dict]`       | Links from source actions. See [Links](#links). Not with `source_ids`. |
| `receiver_ids`              | `Sequence[int]`        | The actions that this action emits events to. Not with `links_to_receivers`. |
| `links_to_receivers`        | `Sequence[dict]`       | Links to receiver actions. See [Links](#links). Not with `receiver_ids`. |
| `schedule`                  | `dict` or `Sequence[dict]` | The cron schedule: an object with `cron` and `timezone`, or a list of them. |
| `monitor_failures`          | `bool`                 | Whether Tines notifies when the action fails.                     |
| `monitor_all_events`        | `bool`                 | Whether all events are monitored.                                 |
| `monitor_no_events_emitted` | `int`                  | Seconds without an event after which Tines notifies.              |
| `draft_id`                  | `int`                  | The draft the action is added to.                                 |

The OpenAPI document requires `type` and `name` only, and the Tines docs table does not mark
`options` and `position` as optional. tapi follows the OpenAPI document, and the live tenant agrees:
an action created without them got default options and a position of its own. An Event
Transformation action got the `message_only` mode.

Tines moved the position by 5 on the tenant: `{"x": 100, "y": 100}` came back as
`{"x": 105, "y": 105}`. An update keeps the position it is given.

`schedule` is documented as an object, and the replies show a list of objects with a `cron` and a
`timezone`. Tines accepted both forms, and answered with a list each time.

Without a story and without a group the reply is a `404` with `['Story or Group ID must be
provided']`. A `type` that does not exist is a `422` with
`[{'agents.0.type': 'Expected value to not be null'}]`.

## `update()`

`action_id` is required and every other parameter is optional. The type, the story and the group of
an action cannot be changed: `update` does not accept them. The Tines docs show this operation as
`PUT`. The OpenAPI document lists the same operation under `PUT` and `PATCH`, and tapi uses `PATCH`.

The parameters are `name`, `description`, `options`, `position`, `source_ids`, `links_to_sources`,
`receiver_ids`, `links_to_receivers`, `schedule`, `disabled`, `monitor_failures`,
`monitor_all_events`, `monitor_no_events_emitted` and `num_runs_to_save`, as in `create`.
`num_runs_to_save` is the number of story runs to save, and only applies to Receive Email and
Webhook actions. The Tines docs say that `monitor_failures` and `monitor_all_events` must be sent
together, and that `monitor_no_events_emitted` needs both. Tines enforces that for the first two:
each one alone is a `422`, with `[{'actions.0.monitor_all_events': 'Expected value to not be
null'}]` or `[{'actions.0.monitor_failures': 'Expected value to not be null'}]`.

- `source_ids`, `links_to_sources`, `receiver_ids` and `links_to_receivers` only add links. An empty
  list removed nothing, and `source_ids=[a1]` did not remove the other sources of the action. Links
  are deleted with [`tines.stories.links.delete`](stories.md#links).
- `num_runs_to_save` on an action that is not a Receive Email or Webhook action is a `400`, with
  `['This action type is not supported for saving runs']`. A success has not been seen.
- An update without any field is a `200`, and the action is unchanged.
- An action that does not exist is a `404` with `['Agent not found']`.

## `delete()`

`action_id` is required. The reply has a 204 status and no data. `get` answered `404` at once, the
action was gone from `list`, and the links to it were gone from the other actions. A second `delete`
is a `404` with `['Agent not found']`.

## `list_events()`

Lists the events that an action emitted. Paginated.

| Parameter                         | Type              | Meaning                                                             |
| --------------------------------- | ----------------- | ------------------------------------------------------------------- |
| `action_id`                       | `int`             | The action. Required.                                               |
| `since_id`, `until_id`            | `int`             | Only events after this event ID, or until and including it.         |
| `since`, `until`                  | `datetime`, `str` | Only events created after this time, or until it. A naive `datetime` is treated as UTC. |
| `show_reemitted_events_only`      | `bool`            | Only events that were re-emitted. Tines defaults to `False`.        |
| `exclude_previous_event_payloads` | `bool`            | Keeps only the output of the action in each payload, without the payloads from upstream events of the run. Tines defaults to `False`. |
| `per_page`                        | `int`             | Results per page. Tines defaults to 20 and caps it at 500.          |
| `page`                            | `int`             | The page, starting at 1. Tines defaults to 1.                       |

`data` holds `events` and `meta`. An event has `id`, `agent_id` (the action), `team_id`, `payload`,
`created_at`, `updated_at` (always equal to `created_at`), `story_run_guid`, `previous_events_ids`
and `re_emitted`. A `since` or `until` that is not a time is a `400`. A page whose payloads add up
to more than 200 MB is a `422`, and a lower `per_page` helps.

## `list_logs()`

Lists the logs of an action. Paginated.

| Parameter  | Type            | Meaning                                                                          |
| ---------- | --------------- | -------------------------------------------------------------------------------- |
| `action_id`| `int`           | The action. Required.                                                            |
| `levels`   | `Sequence[int]` | Only logs of these levels: `2` is a warning, `3` is info and `4` is an error. Sent as `level[]`, once per level. |
| `per_page` | `int`           | Results per page. Tines defaults to 20.                                          |
| `page`     | `int`           | The page, starting at 1. Tines defaults to 1.                                    |

`data` holds `action_logs` and `meta`. A log has `id`, `level`, `message`, `created_at` and
`inbound_event`, the inbound event of the run, which was an object with an `id`. The docs show the
single form `level=4` as well, and the server accepts it, but `levels` sends the list form.

## `delete_events()`, `delete_logs()` and `clear_memory()`

All three take `action_id`, and `data` is the action.

- `delete_events` deletes all the events that the action emitted. `async_deletion=True` does it in a
  background job instead of before the reply. A value that is not a boolean is a `400`.
- `delete_logs` deletes all the logs that the action emitted.
- `clear_memory` clears all the values the action keeps in its memory, shown on its status tab. It
  applies to Event Transformation actions in the `deduplicate` or `implode` mode. It was also
  accepted for an action in the `message_only` mode, with `200`.

The Tines docs do not say whether these deletions can be undone. All three answered `200` with the
action, which had 36 fields. A `delete_events` or `delete_logs` of an action that does not exist is a
`404` with `['Agent not found']`, and a `clear_memory` of one is a `422`, with a message such as
``['No object found for `actionId: "..."`']``. A `delete_events` with an `async_deletion` that is
not a boolean is a `400`, with `['Invalid value for async_deletion. Must be true or false.']`.

## Types

`create` takes ten types: `Agents::EmailAgent`, `Agents::EventTransformationAgent`,
`Agents::HTTPRequestAgent`, `Agents::IMAPAgent`, `Agents::LLMAgent`, `Agents::TriggerAgent`,
`Agents::WebhookAgent`, `Agents::SendToStoryAgent`, `Agents::GroupAgent` and
`Agents::RunScriptAgent`. The Condition action was called Trigger, and Tines still names it
`Agents::TriggerAgent` in the API.

The `action_type` filter of `list` takes thirteen: those ten, plus `Agents::CaseAgent`,
`Agents::FormAgent` and `Agents::RecordAgent`. The docs do not say whether `create` accepts those
three.

## Options

`options` is an object that depends on the type. Neither source describes the keys. The Tines docs
show only Event Transformation actions, such as `{"mode": "deduplicate", "path": "...", "lookback":
"1"}` and `{"mode": "extract", "matchers": [...]}`. Read the options of an existing action with
`get` to see the keys of a type.

The `message_only` mode of an Event Transformation action took `{"mode": "message_only",
"message": "..."}`, and came back as it was sent. Without `options`, Tines made it
`{"mode": "message_only", "loop": false, "payload": {"message": "..."}}`. The `path` of a
`deduplicate` action was sent as `{{.message}}` and came back as `<<message>>`, and the `message`
of a `message_only` action kept its `{{.name}}`.

## Links

A link has the ID of the other action and a type: `DEFAULT`, `NO_MATCH` or `FAILURE`. A request
sends it as `{"source_id": 11, "type": "NO_MATCH"}` or `{"receiver_id": 12, "type": "FAILURE"}`,
and the reply has `link_type` where the request has `type`. `type` is `DEFAULT` when it is left out.
Links and the ID lists are mutually exclusive: `source_ids` with `links_to_sources`, and
`receiver_ids` with `links_to_receivers`. The Tines docs sample for `create` sends both anyway, and
Tines answers a request that does with a `400` and `['links_to_sources and source_ids cannot be used
together']`. A link type that does not exist is a `400` and `['links_to_sources type must be
DEFAULT, NO_MATCH, or FAILURE']`.

A `NO_MATCH` link needs a Condition action (`Agents::TriggerAgent`) on one end. From an Event
Transformation action it was a `422`, with `['Cannot create a no-match link with a non-trigger
action source']`, as a source link and as a receiver link. `FAILURE` and `DEFAULT` were accepted.
A Condition action has not been created, so `NO_MATCH` links have not been seen to work.

A link to an action that does not exist in `source_ids` was ignored: `201`, and the action had no
sources. `create` and `update` only add links, and the other actions gain the link at once: the
`receivers` of a source listed the new action. A link is removed with
[`tines.stories.links.delete`](stories.md#links) or by deleting one of its actions.

## Errors

| Status | When                                                                                       |
| ------ | ------------------------------------------------------------------------------------------ |
| `400`  | A pagination parameter is invalid, a time is not valid, `async_deletion` is not a boolean, the links of `create` or `update` are mixed with the ID lists or have a type that does not exist, or `num_runs_to_save` is used with an unsupported type. `data` is a list of messages. |
| `404`  | The action (`['Agent not found']`), the story, the group or the team (`['Story not found']`, `['Group not found']`, `['Team not found']`) does not exist or is not visible to the key. `list` with a `draft_id` and no `story_id` is a `404` with `['Story ID must be provided with Draft ID']`, and `create` with neither a story nor a group one with `['Story or Group ID must be provided']`. |
| `422`  | `list_events`, when the payloads of a page are too large. Also a `create` with a type that does not exist, a `NO_MATCH` link without a Condition action, an `update` with `monitor_failures` or `monitor_all_events` alone, and a `clear_memory` of an action that does not exist. |
