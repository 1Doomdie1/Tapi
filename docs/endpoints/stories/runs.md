# Runs

- **Access:** `tines.stories.runs`
- **Import:** `from tapi.stories import Runs`
- **Part of:** [Stories](stories.md)

The runs of a story: list them, read one and list its events.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the runs of a story. | `GET /api/v1/stories/{story_id}/runs` |
| [`list_events`](#list_events) | List the events of a story run. | `GET /api/v1/stories/{story_id}/runs/{story_run_guid}` |
| [`get_summary`](#get_summary) | Get the summary of a story run. | `GET /api/v1/stories/{story_id}/runs/{story_run_guid}/summary` |

## Methods breakdown

### `list`

`GET /api/v1/stories/{story_id}/runs`

List the runs of a story.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `story_mode` | `StoryMode` | no | `TEST`, `LIVE` | The mode of the story. |
| `draft_id` | `int` | no | — | Only runs of this draft. |
| `since` | `datetime \| str` | no | ISO 8601 string, or `datetime` | Only runs that started after this time. A naive `datetime` is treated as UTC. |
| `until` | `datetime \| str` | no | ISO 8601 string, or `datetime` | Only runs that started until this time. A naive `datetime` is treated as UTC. |
| `per_page` | `int` | no | Positive integer | The number of results per page. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `story_runs`, the runs of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The story does not exist or is not visible to the key. |

### `list_events`

`GET /api/v1/stories/{story_id}/runs/{story_run_guid}`

List the events of a story run.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `story_run_guid` | `str` | yes | — | The guid of the story run. |
| `story_mode` | `StoryMode` | no | `TEST`, `LIVE` | The mode of the story. |
| `draft_id` | `int` | no | — | Only events of this draft. |
| `per_page` | `int` | no | Positive integer | The number of results per page. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `story_run_events`, a list of objects with `id`, `action_id` (the action that emitted the event), `created_at` and `is_reemitted`, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The story or the run does not exist or is not visible to the key. |

### `get_summary`

`GET /api/v1/stories/{story_id}/runs/{story_run_guid}/summary`

Get the summary of a story run.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `story_run_guid` | `str` | yes | — | The guid of the story run. |
| `story_mode` | `StoryMode` | no | `TEST`, `LIVE` | The mode of the story. |
| `draft_id` | `int` | no | — | The draft the run belongs to. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `story_run`, the run. |
| 404 | The story or the run does not exist or is not visible to the key. |
