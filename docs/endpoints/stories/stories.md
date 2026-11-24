# Stories

- **Access:** `tines.stories`
- **Import:** `from tapi.stories import Stories`

Stories, the automations built in Tines. List, create, change, delete, import and export stories, draw them as an image, and manage what belongs to them in the sub-endpoints.

Every method returns a [`Response`](../../responses.md).

## Sub-endpoints

| Class | Access | Description |
| --- | --- | --- |
| [`Actions`](actions.md) | `tines.stories.actions` | The actions of stories, with their events and logs. |
| [`Events`](events.md) | `tines.stories.events` | The events of the tenant. |
| [`Links`](links.md) | `tines.stories.links` | The links between the actions of a story. |
| [`Notes`](notes.md) | `tines.stories.notes` | The notes on the storyboard of a story. |
| [`Drafts`](drafts.md) | `tines.stories.drafts` | The drafts of a story that uses change control. |
| [`Owners`](owners.md) | `tines.stories.owners` | The owners of a story. |
| [`Recipients`](recipients.md) | `tines.stories.recipients` | The monitoring recipients of a story. |
| [`Runs`](runs.md) | `tines.stories.runs` | The runs of a story. |
| [`Groups`](groups.md) | `tines.stories.groups` | The runs of the groups of a story. |
| [`Versions`](versions.md) | `tines.stories.versions` | The versions of a story. |
| [`ChangeControl`](change_control.md) | `tines.stories.change_control` | The change request of a story. |

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the stories, optionally filtered by team, folder, tags, name or condition. | `GET /api/v1/stories` |
| [`get`](#get) | Get a story, optionally in test mode or as a draft. | `GET /api/v1/stories/{story_id}` |
| [`create`](#create) | Create a story in a team. | `POST /api/v1/stories` |
| [`update`](#update) | Change a story: its name, settings, tags, access, place or entry and exit actions. | `PATCH /api/v1/stories/{story_id}` |
| [`delete`](#delete) | Delete a story. | `DELETE /api/v1/stories/{story_id}` |
| [`batch_delete`](#batch_delete) | Delete several stories. | `DELETE /api/v1/stories/batch` |
| [`export`](#export) | Export a story in a form that `import_` takes. | `GET /api/v1/stories/{story_id}/export` |
| [`import_`](#import_) | Import a story into a team. | `POST /api/v1/stories/import` |
| [`diagram`](#diagram) | Get an image of a story. | `GET /api/v1/stories/{story_id}/diagram` |
| [`disable`](#disable) | Disable or enable a story. | `POST /api/v1/stories/{story_id}/disable` |
| [`list_pending_actions`](#list_pending_actions) | List the actions of a story that have pending runs. | `GET /api/v1/stories/{story_id}/pending_actions` |

## Methods breakdown

### `list`

`GET /api/v1/stories`

List the stories, optionally filtered by team, folder, tags, name or condition.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | no | — | Only stories of this team. |
| `folder_id` | `int` | no | — | Only stories in this folder. |
| `tags` | `Sequence[str]` | no | — | Only stories with these tag names. |
| `search` | `str` | no | — | Only stories whose name matches this text. |
| `filter` | `StoryFilter` | no | `SEND_TO_STORY_ENABLED`<br>`HIGH_PRIORITY`<br>`API_ENABLED`<br>`FAVORITE`<br>`CHANGE_CONTROL_ENABLED`<br>`CHANGE_CONTROL_DISABLED`<br>`ENABLED`<br>`DISABLED`<br>`LOCKED` | Only stories that match this condition. |
| `order` | `StoryOrder` | no | `NAME`<br>`NAME_DESC`<br>`RECENTLY_EDITED`<br>`LEAST_RECENTLY_EDITED`<br>`ACTION_COUNT_ASC`<br>`ACTION_COUNT_DESC`<br>`CONCURRENT_RUNS_COUNT_DESC`<br>`PENDING_ACTION_RUNS_COUNT_DESC`<br>`NOT_WORKING_ACTIONS_COUNT_DESC` | How to sort the stories. |
| `include_live_activity` | `bool` | no | `True`, `False` | Adds `pending_action_runs_count`, `concurrent_runs_count`, `tokens_used_percentage` and `not_working_actions_count` to each story. |
| `per_page` | `int` | no | Positive integer | Results per page. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `stories`, the stories of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 422 | `filter` is not a valid value. |

### `get`

`GET /api/v1/stories/{story_id}`

Get a story, optionally in test mode or as a draft.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story to retrieve. |
| `story_mode` | `StoryMode` | no | `TEST`, `LIVE` | The mode of the story to retrieve. |
| `draft_id` | `int` | no | — | The ID of the draft to retrieve. |
| `include_live_activity` | `bool` | no | `True`, `False` | Adds `pending_action_runs_count`, `concurrent_runs_count` and `tokens_used_percentage` to the story. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the story. |
| 400 | `story_mode` is `TEST` or a draft is asked for on a story without change control. |
| 404 | The story does not exist or is not visible to the key. |

### `create`

`POST /api/v1/stories`

Create a story in a team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | yes | — | The ID of the team the story is added to. |
| `name` | `str` | no | — | The name of the story. |
| `description` | `str` | no | — | A description of the story. |
| `keep_events_for` | `KeepEventsFor` | no | Seconds: 3600, 21600, 86400, 259200, 604800, 1209600, 2592000, 5184000, 7776000, 15552000 or 31536000 | How long events are kept, in seconds. |
| `folder_id` | `int` | no | — | The ID of the folder the story is added to. |
| `tags` | `Sequence[str]` | no | — | Tag names that classify the story. They must exist on the team. |
| `disabled` | `bool` | no | `True`, `False` | Whether the story is disabled. |
| `priority` | `bool` | no | `True`, `False` | Whether the story is high priority. It needs a plan with priority processing. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the created story. |
| 404 | `team_id` or `folder_id` does not exist. |
| 422 | A value is not valid, a tag does not exist, or `priority` is used on a plan without it. |

### `update`

`PATCH /api/v1/stories/{story_id}`

Change a story: its name, settings, tags, access, place or entry and exit actions.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `name` | `str` | no | — | The new name. |
| `description` | `str` | no | — | The new description. |
| `add_tag_names` | `Sequence[str]` | no | — | Tag names to add. They must exist on the team of the story. |
| `remove_tag_names` | `Sequence[str]` | no | — | Tag names to remove. |
| `keep_events_for` | `KeepEventsFor` | no | Seconds: 3600, 21600, 86400, 259200, 604800, 1209600, 2592000, 5184000, 7776000, 15552000 or 31536000 | How long events are kept, in seconds. |
| `disabled` | `bool` | no | `True`, `False` | Whether the story is disabled. |
| `locked` | `bool` | no | `True`, `False` | Whether the story is locked. |
| `priority` | `bool` | no | `True`, `False` | Whether the story runs with high priority. |
| `webhook_api_enabled` | `bool` | no | `True`, `False` | Whether the story can be run through its webhook API. Needs `api_entry_action_id` and `api_exit_action_ids`. |
| `api_entry_action_id` | `int` | no | — | The entry action of an API-enabled story, a webhook action. |
| `api_exit_action_ids` | `Sequence[int]` | no | — | The exit actions of an API-enabled story. |
| `send_to_story_access_source` | `SendToStoryAccessSource` | no | `STS`, `STS_AND_WORKBENCH`, `WORKBENCH`, `OFF` | Where the story can be used as a skill. Enabling it needs `entry_action_id` and `exit_action_ids`. |
| `entry_action_id` | `int` | no | — | The entry action of a Send to Story story, a webhook action. |
| `exit_action_ids` | `Sequence[int]` | no | — | The exit actions of a Send to Story story. |
| `send_to_story_access` | `SendToStoryAccess` | no | `TEAM`, `GLOBAL`, `SPECIFIC_TEAMS` | Which teams may send to the story. `SPECIFIC_TEAMS` needs `shared_team_slugs`. |
| `shared_team_slugs` | `Sequence[str]` | no | — | The slugs of the teams that may send to the story. |
| `send_to_story_skill_use_requires_confirmation` | `bool` | no | `True`, `False` | Whether Workbench asks before it runs the story. |
| `team_id` | `int` | no | — | The ID of the team to move the story to. |
| `folder_id` | `int` | no | — | The ID of the folder to move the story to. |
| `change_control_enabled` | `bool` | no | `True`, `False` | Whether change control is enabled. |
| `draft_id` | `int` | no | — | The ID of the draft to update. |
| `monitor_failures` | `bool` | no | `True`, `False` | Whether failures are monitored. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated story. |
| 400 | A required field is missing, or a draft is asked for on a story without change control. |
| 404 | The story does not exist or is not visible to the key. |
| 422 | A value is not valid, or a tag does not exist. |

### `delete`

`DELETE /api/v1/stories/{story_id}`

Delete a story.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story to delete. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The story does not exist or is not visible to the key. |

### `batch_delete`

`DELETE /api/v1/stories/batch`

Delete several stories.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `ids` | `Sequence[int]` | yes | — | The IDs of the stories to delete. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | A story does not exist. |

### `export`

`GET /api/v1/stories/{story_id}/export`

Export a story in a form that `import_` takes.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story to export. |
| `randomize_urls` | `bool` | no | `True`, `False` | Whether the page and webhook URLs of the story are randomized. |
| `clear_recipients` | `bool` | no | `True`, `False` | Whether the monitoring and email recipient fields of the story are cleared. |
| `draft_id` | `int` | no | — | The ID of the draft to export. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the story in exported form, a JSON object that `import_` takes as `data`. |
| 404 | The story does not exist or is not visible to the key. |

### `import_`

`POST /api/v1/stories/import`

Import a story into a team.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `new_name` | `str` | yes | — | The name of the imported story. |
| `data` | `Mapping[str, Any]` | yes | — | The story in exported form, as `export` returns it. |
| `team_id` | `int` | yes | — | The ID of the team the story is added to. |
| `folder_id` | `int` | no | — | The ID of the folder the story is added to. |
| `mode` | `ImportMode` | no | `new`, `versionReplace` | `new` creates a story, and `versionReplace` updates the story of the same name. |
| `draft_name` | `str` | no | — | The name of the draft when change control is enabled. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the imported story. |
| 404 | `team_id` or `folder_id` does not exist. |

### `diagram`

`GET /api/v1/stories/{story_id}/diagram`

Get an image of a story.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story to draw. |
| `format` | `DiagramFormat` | no | `png`, `svg` | The image format. |
| `content` | `DiagramContent` | no | `full`, `actions` | What to draw: `full` is the actions, links, notes and sections, and `actions` is the actions and links only. |
| `draft_id` | `int` | no | — | The ID of the draft to draw. Without it the live story is drawn. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the image: the raw `bytes` of a PNG (`image/png`), or the text, a `str`, of an SVG (`image/svg+xml`). |
| 404 | The story does not exist or is not visible to the key. |

### `disable`

`POST /api/v1/stories/{story_id}/disable`

Disable or enable a story.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story to update. |
| `disabled` | `bool` | yes | `True`, `False` | `True` disables the story and `False` enables it. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `disabled`, the new state. |
| 404 | The story does not exist or is not visible to the key. |

### `list_pending_actions`

`GET /api/v1/stories/{story_id}/pending_actions`

List the actions of a story that have pending runs.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `story_id` | `int` | yes | — | The ID of the story. |
| `search` | `str` | no | — | Only actions whose name matches this text. |
| `story_mode` | `StoryMode` | no | `TEST`, `LIVE` | The mode of the story. |
| `draft_id` | `int` | no | — | Only actions of this draft. |
| `per_page` | `int` | no | Positive integer | Results per page. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `pending_actions`, a list of objects with `id`, `name`, `type` and `pending_action_runs_count`, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 404 | The story does not exist or is not visible to the key. |
