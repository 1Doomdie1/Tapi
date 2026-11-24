# Events

- **Access:** `tines.stories.events`
- **Import:** `from tapi.stories import Events`
- **Part of:** [Stories](stories.md)

The events of the tenant: list them, read one and emit one again.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the events, optionally of a team or a story. | `GET /api/v1/events` |
| [`get`](#get) | Get an event. | `GET /api/v1/events/{event_id}` |
| [`reemit`](#reemit) | Emit an event again. | `POST /api/v1/events/{event_id}/reemit` |

## Methods breakdown

### `list`

`GET /api/v1/events`

List the events, optionally of a team or a story.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | no | — | Only events of this team. Do not combine it with `story_id`. |
| `story_id` | `int` | no | — | Only events of this story. |
| `story_mode` | `str` | no | `test` | `test` lists the events of the default test story. Only with `story_id`. |
| `include_groups` | `bool` | no | `True`, `False` | Whether to include the events of groups in the story. Only with `story_id`. |
| `since_id` | `int` | no | — | Only events after this event ID. |
| `until_id` | `int` | no | — | Only events until and including this event ID. |
| `since` | `datetime \| str` | no | ISO 8601 string, or `datetime` | Only events created after this time. A naive `datetime` is treated as UTC. |
| `until` | `datetime \| str` | no | ISO 8601 string, or `datetime` | Only events created until this time. A naive `datetime` is treated as UTC. |
| `show_reemitted_events_only` | `bool` | no | `True`, `False` | Only events that were re-emitted. |
| `exclude_previous_event_payloads` | `bool` | no | `True`, `False` | Keep only the output of the action in the payload of each event, without the payloads that came from upstream events of the story run. |
| `per_page` | `int` | no | Positive integer | The number of results per page. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `events`, the events of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. `story_id` or `team_id` is not valid. |
| 404 | The story does not exist or is not visible to the key. |
| 422 | The payloads of a page are too large. |

### `get`

`GET /api/v1/events/{event_id}`

Get an event.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `event_id` | `int` | yes | — | The ID of the event to retrieve. |
| `exclude_previous_event_payloads` | `bool` | no | `True`, `False` | Keep only the output of the action in the payload, without the payloads of the upstream events of the story run. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the event. |
| 404 | The event does not exist or is not visible to the key. |

### `reemit`

`POST /api/v1/events/{event_id}/reemit`

Emit an event again.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `event_id` | `int` | yes | — | The ID of the event to re-emit. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The event does not exist or is not visible to the key. |
