# Stories

Stories are the automations built in Tines. The module is available as `tines.stories`, and the
class is `tapi.stories.Stories`. Eleven sub-areas hang off it: `actions`, `events`, `links`,
`notes`, `drafts`, `owners`, `recipients`, `runs`, `groups`, `versions` and `change_control`, each
also a class in `tapi.stories`. The methods of `actions` are on [their own page](stories_actions.md), and the
others are below. Every method returns a [`Response`](../responses.md).

| Method                                                    | HTTP route                                                            |
| --------------------------------------------------------- | --------------------------------------------------------------------- |
| `list(...)`                                               | `GET /api/v1/stories`                                                 |
| `get(story_id=...)`                                       | `GET /api/v1/stories/{story_id}`                                      |
| `create(team_id=..., ...)`                                | `POST /api/v1/stories`                                                |
| `update(story_id=..., ...)`                               | `PATCH /api/v1/stories/{story_id}`                                    |
| `delete(story_id=...)`                                    | `DELETE /api/v1/stories/{story_id}`                                   |
| `batch_delete(ids=...)`                                   | `DELETE /api/v1/stories/batch`                                        |
| `export(story_id=..., ...)`                               | `GET /api/v1/stories/{story_id}/export`                               |
| `import_(new_name=..., data=..., team_id=..., ...)`       | `POST /api/v1/stories/import`                                         |
| `diagram(story_id=..., ...)`                              | `GET /api/v1/stories/{story_id}/diagram`                              |
| `disable(story_id=..., disabled=...)`                     | `POST /api/v1/stories/{story_id}/disable`                             |
| `list_pending_actions(story_id=..., ...)`                 | `GET /api/v1/stories/{story_id}/pending_actions`                      |
| `drafts.list(story_id=..., ...)`                          | `GET /api/v1/stories/{story_id}/drafts`                               |
| `drafts.create(story_id=..., name=...)`                   | `POST /api/v1/stories/{story_id}/drafts`                              |
| `drafts.delete(story_id=..., draft_id=...)`               | `DELETE /api/v1/stories/{story_id}/drafts/{draft_id}`                 |
| `owners.add(story_id=..., user_id=...)`                   | `POST /api/v1/stories/{story_id}/owners`                              |
| `owners.remove(story_id=..., user_id=...)`                | `DELETE /api/v1/stories/{story_id}/owners`                            |
| `recipients.add(story_id=..., address=..., ...)`          | `POST /api/v1/stories/{story_id}/recipients`                          |
| `recipients.remove(story_id=..., address=..., ...)`       | `DELETE /api/v1/stories/{story_id}/recipients`                        |
| `runs.list(story_id=..., ...)`                            | `GET /api/v1/stories/{story_id}/runs`                                 |
| `runs.list_events(story_id=..., story_run_guid=..., ...)` | `GET /api/v1/stories/{story_id}/runs/{story_run_guid}`                |
| `runs.get_summary(story_id=..., story_run_guid=..., ...)` | `GET /api/v1/stories/{story_id}/runs/{story_run_guid}/summary`        |
| `groups.list_runs(group_id=..., ...)`                     | `GET /api/v1/groups/{group_id}/runs`                                  |
| `groups.list_run_events(group_id=..., group_run_guid=..., ...)` | `GET /api/v1/groups/{group_id}/runs/{group_run_guid}`           |
| `versions.list(story_id=..., ...)`                        | `GET /api/v1/stories/{story_id}/versions`                             |
| `versions.create(story_id=..., ...)`                      | `POST /api/v1/stories/{story_id}/versions`                            |
| `versions.get(story_id=..., version_id=...)`              | `GET /api/v1/stories/{story_id}/versions/{version_id}`                |
| `versions.update(story_id=..., version_id=..., name=...)` | `POST /api/v1/stories/{story_id}/versions/{version_id}`               |
| `versions.delete(story_id=..., version_id=...)`           | `DELETE /api/v1/stories/{story_id}/versions/{version_id}`             |
| `change_control.create(story_id=..., ...)`                | `POST /api/v1/stories/{story_id}/change_request`                      |
| `change_control.view(story_id=..., ...)`                  | `GET /api/v1/stories/{story_id}/change_request/view`                  |
| `change_control.generate_description(story_id=..., draft_id=...)` | `GET /api/v1/stories/{story_id}/change_request/ai_description` |
| `change_control.approve(story_id=..., change_request_id=...)` | `POST /api/v1/stories/{story_id}/change_request/approve`          |
| `change_control.cancel(story_id=..., change_request_id=..., ...)` | `POST /api/v1/stories/{story_id}/change_request/cancel`       |
| `change_control.reject(story_id=..., change_request_id=..., ...)` | `POST /api/v1/stories/{story_id}/change_request/reject`       |
| `change_control.promote(story_id=..., change_request_id=..., ...)` | `POST /api/v1/stories/{story_id}/change_request/promote`     |
| `events.list(...)`                                        | `GET /api/v1/events`                                                  |
| `events.get(event_id=..., ...)`                           | `GET /api/v1/events/{event_id}`                                       |
| `events.reemit(event_id=...)`                             | `POST /api/v1/events/{event_id}/reemit`                               |
| `links.delete(links=...)`                                 | `DELETE /api/v1/links`                                                |
| `notes.list(...)`                                         | `GET /api/v1/notes`                                                   |
| `notes.get(note_id=...)`                                  | `GET /api/v1/notes/{note_id}`                                         |
| `notes.create(...)`                                       | `POST /api/v1/notes`                                                  |
| `notes.update(note_id=..., ...)`                          | `PATCH /api/v1/notes/{note_id}`                                       |
| `notes.delete(note_id=...)`                               | `DELETE /api/v1/notes/{note_id}`                                      |

All parameters are keyword-only. Parameters left as `None` are not sent, but `False` and `""` are.
The Tines docs do not state which key types or permissions these endpoints need. The OpenAPI
document says that personal, service, team and tenant owner keys are all accepted, and that a key
without access to a resource receives a 404.

## The actions of stories

The Tines docs list Actions under Stories, and they are the sub-area `tines.stories.actions`. It has
ten methods, and [its own page](stories_actions.md) describes them: `list`, `get`, `create`,
`update`, `delete`, `list_events`, `list_logs`, `delete_events`, `delete_logs` and
`clear_memory`.

## What is not here

The change request endpoints at `/api/v1/change_requests` belong to `change_requests`.
`change_control` holds only the operations that Tines routes under a story. The OpenAPI document
also lists `/api/v1/annotations` routes, which are copies of the `/api/v1/notes` routes, and tapi
offers the notes routes only.

## The story

`data` of `get`, `create`, `update`, `import_`, `owners.add` and `recipients.add` is a story, and
`list` returns a list of them under `stories`. A story has:

| Field                                             | Meaning                                                                                  |
| ------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `id`, `guid`, `slug`                              | The ID, the unique identifier and the underscored name of the story.                     |
| `name`, `description`                             | The name, and the description, which is `null` when there is none.                       |
| `user_id`                                         | The ID of the creator.                                                                   |
| `team_id`, `folder_id`                            | The team, and the folder, which is `null` at the root level.                             |
| `tags`                                            | The tag names of the story.                                                              |
| `owners`                                          | The IDs of the owners.                                                                   |
| `recipients`                                      | The monitoring recipients, as a list of objects with an `address`.                       |
| `keep_events_for`                                 | How long events are kept, in seconds.                                                    |
| `disabled`, `priority`, `published`, `locked`     | Whether the story is disabled, high priority, published and locked.                      |
| `change_control_enabled`                          | Whether change control is enabled.                                                       |
| `monitor_failures`, `actions_with_monitoring`     | Whether failures are monitored, and the IDs of the actions with monitoring.              |
| `entry_agent_id`, `exit_agents`                   | The entry action, which can be `null`, and the exit actions.                             |
| `mode`                                            | `LIVE` or `TEST`.                                                                        |
| `created_at`, `updated_at`, `edited_at`           | ISO 8601 timestamps. `edited_at` tracks changes to the story itself.                     |
| `send_to_story_enabled`                           | Whether Send to Story is enabled.                                                        |
| `send_to_story_access_source`                     | `STS`, `STS_AND_WORKBENCH`, `WORKBENCH` or `OFF`.                                        |
| `send_to_story_access`                            | `TEAM`, `GLOBAL`, `SPECIFIC_TEAMS`, or `null`.                                           |
| `send_to_story_referring_story_ids`               | The stories that call this one. Only present when Send to Story is enabled.              |
| `shared_team_slugs`                               | The team slugs for `SPECIFIC_TEAMS`, otherwise empty.                                    |
| `send_to_story_timeout_enabled`, `send_to_story_timeout_duration_seconds` | Whether Send to Story runs time out, and after how many seconds (`null` if unset). |
| `send_to_story_skill_use_requires_confirmation`   | Whether Workbench asks for confirmation before it runs the story.                        |
| `api_enabled`, `api_entry_actions`, `api_exit_actions`, `api_name` | The API fields of a story.                                              |

The live tenant also returned `change_control_require_owner_approval`, which neither the Tines
docs nor the OpenAPI document list. Replies of `list` and `get` had the same fields. With
`include_live_activity`, a story gets `pending_action_runs_count`, `concurrent_runs_count`,
`tokens_used_percentage` and `not_working_actions_count`.

A draft has the fields of a story plus `story_id` and `story_name`. Its `mode` is always `TEST`.

## `list()`

Paginated: one call returns one page; see [Pagination](../pagination.md). `data` holds `stories`
and `meta`. Only live stories are listed.

| Parameter               | Type       | Meaning                                                                      |
| ----------------------- | ---------- | ---------------------------------------------------------------------------- |
| `team_id`               | `int`      | Only stories of this team.                                                   |
| `folder_id`             | `int`      | Only stories in this folder.                                                 |
| `tags`                  | `Sequence[str]` | Only stories with these tag names. Sent as `tags[]`, once per name.     |
| `search`                | `str`      | Only stories whose name matches.                                             |
| `filter`                | `str`      | One condition. See [Filters and orders](#filters-and-orders).                |
| `order`                 | `str`      | How to sort. See [Filters and orders](#filters-and-orders).                  |
| `include_live_activity` | `bool`     | Adds the live activity fields. Tines defaults to `False`.                    |
| `per_page`              | `int`      | Results per page. Tines defaults to 20 and caps it at 500.                   |
| `page`                  | `int`      | The page, starting at 1. Tines defaults to 1.                                |

## `get()`

`story_id` is required.

| Parameter               | Type   | Meaning                                                                          |
| ----------------------- | ------ | -------------------------------------------------------------------------------- |
| `story_mode`            | `str`  | `TEST` or `LIVE`.                                                                |
| `draft_id`              | `int`  | The draft to retrieve.                                                           |
| `include_live_activity` | `bool` | Adds the live activity fields. Tines defaults to `False`.                        |

When no story with that ID is visible to the key, the reply is a `404` with `['Story not found']`.
`story_mode="TEST"` on a story without change control is a `400`.

## `create()`

`team_id` is required, and the reply has a 201 status.

| Parameter         | Type            | Meaning                                                             |
| ----------------- | --------------- | ------------------------------------------------------------------- |
| `team_id`         | `int`           | The team the story is added to. Required.                           |
| `name`            | `str`           | The name of the story.                                              |
| `description`     | `str`           | A description of the story.                                         |
| `keep_events_for` | `int`           | How long events are kept. See [Event retention](#event-retention).  |
| `folder_id`       | `int`           | The folder the story is added to.                                   |
| `tags`            | `Sequence[str]` | Tag names used to classify the story. See below.                    |
| `disabled`        | `bool`          | Whether the story is disabled. Tines defaults to `False`.           |
| `priority`        | `bool`          | Whether the story is high priority. Tines defaults to `False`. A tenant without priority processing refuses `True` with a `422`. |

The Tines docs say that Tines creates the tags named in `tags`. On the live tenant, a `create` with
`tags` was answered with a `500` and created nothing, both for tag names that did not exist and for
tags that did. Create the story without `tags`, and add the tags with `update` and
`add_tag_names`, which takes tags that already exist on the team of the story.

A new story had no owners and one recipient, which Tines added. The reply is the story, with
`published` set to `true`, `mode` `LIVE` and `folder_id` `null` for a story without a folder.

## `update()`

Updates a story. `story_id` is required and every other parameter is optional. If change control is
enabled on the story and no `draft_id` is given, Tines updates a draft called `test`.

| Parameter                                       | Type            | Meaning                                                                 |
| ----------------------------------------------- | --------------- | ----------------------------------------------------------------------- |
| `name`, `description`                           | `str`           | The new name and description.                                           |
| `add_tag_names`, `remove_tag_names`             | `Sequence[str]` | Tag names to add and to remove.                                         |
| `keep_events_for`                               | `int`           | See [Event retention](#event-retention).                                |
| `disabled`, `locked`, `priority`                | `bool`          | Whether the story is disabled from running, locked against edits, or high priority. |
| `webhook_api_enabled`                           | `bool`          | Whether the story can be run through its webhook API. Enabling it also needs `api_entry_action_id` and `api_exit_action_ids`, and `draft_id` if the story is not live. |
| `api_entry_action_id`                           | `int`           | The entry action of an API-enabled story. It must be a webhook action.  |
| `api_exit_action_ids`                           | `Sequence[int]` | The exit actions of an API-enabled story.                               |
| `send_to_story_access_source`                   | `str`           | `STS`, `STS_AND_WORKBENCH`, `WORKBENCH` or `OFF`. Enabling it also needs `entry_action_id` and `exit_action_ids`. |
| `entry_action_id`                               | `int`           | The entry action of a Send to Story story. It must be a webhook action. |
| `exit_action_ids`                               | `Sequence[int]` | The exit actions of a Send to Story story.                              |
| `send_to_story_access`                          | `str`           | `TEAM`, `GLOBAL` or `SPECIFIC_TEAMS`. Tines defaults to `TEAM`. `SPECIFIC_TEAMS` also needs `shared_team_slugs`. |
| `shared_team_slugs`                             | `Sequence[str]` | The slugs of the teams that may send to the story.                      |
| `send_to_story_skill_use_requires_confirmation` | `bool`          | Whether Workbench asks for confirmation before it runs the story.       |
| `team_id`                                       | `int`           | The team to move the story to.                                          |
| `folder_id`                                     | `int`           | The folder to move the story to.                                        |
| `change_control_enabled`                        | `bool`          | Whether change control is enabled.                                      |
| `draft_id`                                      | `int`           | The draft to update.                                                    |
| `monitor_failures`                              | `bool`          | Whether failures are monitored in the story.                            |

Tines moves a story to the root folder when `folder_id` is empty. Because `None` means "not sent",
tapi cannot do that yet. The Tines docs show this operation as `PUT`. The OpenAPI document lists
the same operation under `PUT` and `PATCH`, and tapi uses `PATCH`.

- `add_tag_names` must name tags that exist on the team of the story. A name that does not is a
  `422` with `["Error: The following tags don't exist on the team: <name>"]`. Create the tag first,
  with [`tines.tags.create`](tags.md).
- `priority=True` is a `422` on a tenant without priority processing, with
  `['This feature (PRIORITY_PROCESSING) is not enabled on this tenant. Please contact support to upgrade your plan']`.
- Sending `send_to_story_access_source="STS"` without entry and exit actions is a `422`, with
  `["Validation failed: Entry agent can't be blank, Exit agent ids can't be blank"]`.
- A `keep_events_for` that is not one of the listed values is a `422` whose message names the
  accepted values as `hour1`, `hours6`, `day1`, `days3` and so on, although the numbers are what
  Tines takes.
- An update of a locked story was accepted. The Tines docs say that locking prevents edits.
- With change control enabled and no `draft_id`, Tines updates the draft `test`: the reply has
  `draft_id` and `draft_name`, and the live story is unchanged.
- An update without any field is a `200`, and the story is unchanged.

## `delete()` and `batch_delete()`

`delete` takes `story_id`, and the reply has a 204 status and no data.

`batch_delete` takes `ids`, a sequence of story IDs, and sends them in a JSON body. The reply has a
204 status and no data. Tines skips stories that are sync sources and live read-only sync
destinations, and does not say which. A list holding only an ID that does not exist is a `404`
with `['StoryContainer not found']`.

A deleted story stays visible for a moment: `get` still answered `200` right after both calls, and
`404` about two seconds later. `list` and `export` had stopped showing it by then.

## `export()` and `import_()`

`export` takes `story_id`, and optionally `randomize_urls` (randomize the page and webhook URLs),
`clear_recipients` (clear the monitoring and email recipient fields) and `draft_id`. `data` is the
story in exported form, a JSON object without a documented schema. The Tines docs sample shows
`schema_version`, `name`, `description`, `guid`, `slug`, `agents`, `links`, `diagram_layout`,
`tags` and more.

`import_` takes the object that `export` returns as `data`.

| Parameter     | Type   | Meaning                                                                          |
| ------------- | ------ | -------------------------------------------------------------------------------- |
| `new_name`    | `str`  | The name of the imported story. Required.                                        |
| `data`        | `dict` | The story in exported form. Required.                                            |
| `team_id`     | `int`  | The team the story is added to. Required.                                        |
| `folder_id`   | `int`  | The folder the story is added to.                                                |
| `mode`        | `str`  | `new` creates a story, and `versionReplace` updates an existing one by name. Tines defaults to `new`. |
| `draft_name`  | `str`  | The name of the draft when change control is enabled. Tines defaults to `Imported story`. |

`data` is the story. The status is `200`, although the OpenAPI document says `201`. Embedded
substories are not imported. The tags of the exported story are kept, and `new_name` is the name of
the new story. An export lists its tags as objects with a `name`.

## `diagram()`

Draws a story. `story_id` is required.

| Parameter  | Type  | Meaning                                                                                   |
| ---------- | ----- | ----------------------------------------------------------------------------------------- |
| `format`   | `str` | `png` or `svg`. Tines defaults to `png`.                                                  |
| `content`  | `str` | `full` for actions, links, notes and sections, or `actions` for actions and links. Tines defaults to `full`. |
| `draft_id` | `int` | The draft to draw. Without it Tines draws the live story.                                 |

`data` is the image. A PNG (`image/png`) is the raw `bytes`, and an SVG (`image/svg+xml`) is
decoded as text, a `str`. Tines draws up to 1,000 items and 2,000 links, and scales a PNG to fit
within 2,000 by 2,000 pixels. The Tines docs list the errors: `404` for a story that is not visible
or a draft that does not belong to it, `422` for an unsupported `format` or `content` or a story
over the limits, and `503` when the diagram could not be rendered.

## `disable()`

`story_id` and `disabled` are required. `True` disables the story and `False` enables it. It works
on a story with change control enabled, bypassing the approval, and the live story was disabled at
once. `data` is an object with `disabled`.

## `list_pending_actions()`

Lists the actions of a story that have pending action runs, the highest count first. Paginated.
`story_id` is required.

| Parameter    | Type  | Meaning                                                        |
| ------------ | ----- | -------------------------------------------------------------- |
| `search`     | `str` | Only actions whose name matches.                               |
| `story_mode` | `str` | `TEST` or `LIVE`. Tines defaults to `LIVE`.                    |
| `draft_id`   | `int` | Only actions of this draft.                                    |
| `per_page`   | `int` | Results per page. Tines defaults to 20.                        |
| `page`       | `int` | The page, starting at 1. Tines defaults to 1.                  |

`data` holds `pending_actions`, a list of objects with `id`, `name`, `type` and
`pending_action_runs_count`, and `meta`.

## `drafts`

A draft belongs to a story with change control: `list` is refused for a story without it. All
three methods need `story_id`. When change control is enabled, Tines creates a draft called `test`.

- `list(story_id=..., per_page=..., page=...)` returns `drafts` and `meta`. The Tines docs show no
  pagination parameters on this endpoint, and the OpenAPI document lists `per_page` and `page`.
- `create(story_id=..., name=...)` creates a draft. The status is `200`, and the Tines docs and
  the OpenAPI document do not state one. `data` is the draft: the fields of a story plus `story_id`
  and `story_name`. A name that a draft of the story already has is a `422`, with
  `['A draft named "<name>" already exists for this live story.']`.
- `delete(story_id=..., draft_id=...)` has a 204 status and no data. A draft that does not exist,
  or that does not belong to the story, is a `404` with `['Draft not found']`.

The draft ID is what `draft_id` takes in the other methods. `get` with a `draft_id` returns the
draft, with `draft_id`, `draft_name` and `mode` `TEST`, `get` with `story_mode="TEST"` returns the
draft `test`, and `story_mode="LIVE"` returns the live story with a `draft_id` of `null`.

## `owners` and `recipients`

- `owners.add(story_id=..., user_id=...)` adds an owner, who must be a member of the team of the
  story. `data` is the story. A user that does not exist is a `404` with `['User not found']`. The
  success of this call has not been seen.
- `owners.remove(story_id=..., user_id=...)` removes an owner, who must be an existing one. The
  reply has a 204 status and no data. A user that does not exist is a `404` with
  `['User not found']`.
- `recipients.add(story_id=..., address=..., draft_id=...)` adds a recipient, an email address or a
  webhook URL that receives the monitoring communications. `data` is the story, with the new
  recipient in `recipients`.
- `recipients.remove(story_id=..., address=..., draft_id=...)` removes one. The status is `200` and
  `data` is `None`, although the Tines docs say `204`. An address that is not a recipient is a
  `404` with `['Recipient not found']`.

Both removals send their parameter in a JSON body, on a `DELETE`, as the Tines docs do.

## `runs`

A story run has `guid`, `story_id`, `team_id` (the team that owns the story now, which can differ
from the team at the time of the run), `start_time`, `end_time` (`null` while the run goes),
`duration` (seconds), `action_count`, `event_count`, `story_mode`, `draft_id` and `draft_name`.

- `list(story_id=..., story_mode=..., draft_id=..., since=..., until=..., per_page=..., page=...)`
  returns `story_runs` and `meta`. `since` and `until` take a `datetime` or an ISO 8601 string, and
  a naive `datetime` is treated as UTC.
- `list_events(story_id=..., story_run_guid=..., story_mode=..., draft_id=..., per_page=...,
  page=...)` returns `story_run_events`, a list of objects with `id`, `action_id`, `created_at` and
  `is_reemitted`, and `meta`.
- `get_summary(story_id=..., story_run_guid=..., story_mode=..., draft_id=...)` returns an object
  with `story_run`. A guid that does not exist is a `404` with `['Story run not found']`, and
  `list_events` answered `200` for one.

`story_mode="TEST"` and `draft_id` are accepted for a story with change control. For a story
without it they are a `400`.

## `groups`

A group run has the fields of a story run plus `group_id`.

- `list_runs(group_id=..., per_page=..., page=...)` returns `group_runs` and `meta`.
- `list_run_events(group_id=..., group_run_guid=..., per_page=..., page=...)` returns
  `group_run_events`, with the same fields as the events of a story run, and `meta`.

## `versions`

A version has `id`, `name` (`null` if it has none), `description` and `timestamp`.

- `list(story_id=..., draft_id=..., per_page=..., page=...)` returns `story_versions` and `meta`.
- `create(story_id=..., name=..., draft_id=...)` has a `200` status, although the OpenAPI document
  says `201`.
- `get(story_id=..., version_id=...)` returns the version with its `export_file`, the story in
  exported form.
- `update(story_id=..., version_id=..., name=...)` renames a version. Tines documents it as
  `POST`, and no other method is listed.
- `delete(story_id=..., version_id=...)` has a 200 status and `data` is an object with
  `destroyed_id`. Afterwards `get` answers `404` with `['StoryVersion not found']`.

The Tines docs show the version itself as `data` of `create`, `get` and `update`. The server wraps
it in an object with a `story_version` key. `list` is not wrapped.

## `change_control`

These are the change request operations that Tines groups under a story.

| Method                | Parameters                                                                                 | `data`                                                              |
| --------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------- |
| `create`              | `story_id`, and `title`, `description` and `draft_id`. A description can mention a user as `<@user-2435>`. | The change request: `id`, `draft_id`, `draft_name` and `change_request`. |
| `view`                | `story_id`, and `draft_id` in the query.                                                   | The current change request. `change_request` is `null` when a test story has changes but none has been submitted. |
| `generate_description`| `story_id` and `draft_id`, in the query. AI features must be enabled.                      | An object with `change_request_ai_description`.                     |
| `approve`             | `story_id` and `change_request_id`.                                                        | The status of the change request.                                   |
| `cancel`              | `story_id`, `change_request_id`, and `comment` (up to 1,000 characters, not for your own change request). | The status of the change request and the `comment`, or `null`. |
| `reject`              | The same as `cancel`.                                                                      | The same as `cancel`.                                               |
| `promote`             | `story_id`, `change_request_id`, and `bypass_approval`, `bypass_approval_reason` and `delete_draft`. | The updated live story.                                      |

The `change_request` object has `id` and `status`. `create` and `view` add `name`, `description`,
`participants` (a list of user IDs), `live_story_export` and `draft_export`, which are JSON
strings. The OpenAPI document lists the statuses `PENDING`, `APPROVED`, `REJECTED`, `PUSHED` and
`IN_PROGRESS`.

`cancel` and `reject` are the same operation under two routes: you cancel your own change request,
and when you are not the author, either rejects it. Tines answers a comment on your own change
request with a `400`. `promote` with `bypass_approval` needs the permission to manage the story on
its team, is recorded in the audit trail and sends a notification. Tines records
`Approval bypassed via API` when no `bypass_approval_reason` is given.

On the live tenant:

- `view` of a story with change control returned `200` with `change_request` `null` before any
  request, with a `draft_id` and without one. For a story without change control it is a `404`
  with `['Story not found']`.
- `create` returned `200`. The change request had `PENDING` as its `status`, `live_story_export`
  and `draft_export` were strings, and `participants` was a list.
- `generate_description` returned `200` with a text that described the difference between the
  draft and the live story. On a story without change control, a draft that does not exist and a
  call without a `draft_id` were both a `404` with `['Draft not found']`.
- `approve` by the author returned `200` with the status `APPROVED`. The tenant did not require
  another approver, so the `401` that the OpenAPI document lists was not seen. A change request
  that does not exist is a `404` with `['StoryChangeRequest not found']`.
- `cancel` of the author's own change request, which was `APPROVED`, returned `200` with the status
  `IN_PROGRESS` and `comment` `null`. `view` then showed `IN_PROGRESS`.
- `cancel` with a `comment`, as the author, is a `400` with
  `["You can't add a comment when canceling your own change request; omit comment"]`.
- `cancel` of a change request that is `IN_PROGRESS` is a `422` with
  `['This change request is in progress and must be pending or approved to be cancelled']`.

`reject` and `promote` have not been run.

## `events`

The events that actions emitted, across the tenant. `events.list` lists them, `events.get` returns
one and `events.reemit` emits one again. The events of one action are also available as
[`actions.list_events`](stories_actions.md#list_events).

An event has:

| Field                       | Meaning                                                                          |
| --------------------------- | -------------------------------------------------------------------------------- |
| `id`                        | The ID of the event.                                                             |
| `agent_id`                  | The ID of the action that emitted it.                                            |
| `team_id`                   | The team that owns the action now, which can differ from the team at the time.   |
| `payload`                   | The payload, an object.                                                          |
| `created_at`, `updated_at`  | ISO 8601 timestamps. `updated_at` is always equal to `created_at`.               |
| `story_run_guid`            | The unique identifier of the story run of the event.                             |
| `previous_events_ids`       | The IDs of the events of the upstream action in the same story run.              |
| `re_emitted`                | Whether the event was re-emitted.                                                |

The Tines docs samples also show a `user_id`, which the replies did not have.

**`events.list()`** is paginated: one call returns one page, the newest events first, and `data`
holds `events` and `meta`. A tenant can hold a very large number of events: the one tested had about
800,000. Narrow the list with `since` and `until`, with `agent_id`, or with a small `per_page`.

| Parameter                         | Type              | Meaning                                                              |
| --------------------------------- | ----------------- | -------------------------------------------------------------------- |
| `team_id`                         | `int`             | Only events of this team. With `story_id`, Tines ignores `story_id`. |
| `story_id`                        | `int`             | Only events of this story.                                           |
| `agent_id`                        | `int`             | Only events of this action. Neither source lists it. See below.      |
| `story_mode`                      | `str`             | `test`, for the default test story. Only with `story_id`.            |
| `include_groups`                  | `bool`            | Include the events of groups in the story. Only with `story_id`. Tines defaults to `False`. |
| `since_id`, `until_id`            | `int`             | Only events after this event ID, or until and including it.          |
| `since`, `until`                  | `datetime`, `str` | Only events created after this time, or until it. A naive `datetime` is treated as UTC. |
| `show_reemitted_events_only`      | `bool`            | Only events that were re-emitted. Tines defaults to `False`.         |
| `exclude_previous_event_payloads` | `bool`            | Keeps only the output of the action in each payload. Tines defaults to `False`. |
| `per_page`                        | `int`             | Results per page. Tines defaults to 20 and caps it at 500.           |
| `page`                            | `int`             | The page, starting at 1. Tines defaults to 1.                        |

`agent_id` is not in the Tines docs or the OpenAPI document, but the server accepts it, it returns
the events of that action, as the per-action route does, and a list that timed out says to "filter
by agent_id". `include_groups` with `story_id` and no `agent_id` took about 25 seconds and then
failed with a `504`.

**`events.get()`** takes `event_id`, and optionally `exclude_previous_event_payloads`, which keeps
the output of the action in the payload and drops the payloads of the upstream events. `data` is the
event. An event that does not exist is a `404` with `['Event not found']`.

**`events.reemit()`** takes `event_id` and emits the event again. The reply has a 204 status and no
data. Neither source says what happens to the actions that receive it.

On 2026-11-23, against a live tenant, only read-only calls were made, and a successful re-emit was
not tried: it would have sent an event to the real downstream actions, and no throwaway event could
be made.

- The list was newest first, and a page of events had the nine fields above.
- `team_id` of the standard team matched all the events, `team_id` of a personal team matched none,
  and a `team_id` that does not exist was a `404` with `['Team not found']`.
- `story_id` of a story that does not exist was a `200` with no events, not a `404`.
- `story_mode` was accepted with `test`, `TEST`, `live`, `LIVE` and `bogus`, and changed nothing for
  a story without change control. Without `story_id` it was ignored.
- `include_groups` with `story_id` was a `504` after about 25 seconds, with
  `['Listing events timed out; narrow since/until, reduce per_page, or filter by agent_id.']`. With
  `agent_id` as well it was a `200` at once, and without `story_id` it was accepted.
- `agent_id` returned the same events as `actions.list_events`, and an `agent_id` that does not
  exist was a `404` with `['Agent not found']`. A parameter named `action_id` was ignored.
- `since_id` and `until_id` filtered by ID. `since` and `until` took a full timestamp or a date
  only, and filtered. A `since` or an `until` that is not a time was a `400` with
  `['Invalid time argument passed for since/until']`.
- `show_reemitted_events_only` matched no events, as none had been re-emitted.
- `exclude_previous_event_payloads` made the payloads smaller. A value that is not a boolean was
  ignored.
- `per_page=0` and `page=0` were not refused: the page had the default 20 events, and a page past
  the end was an empty list.
- `get` of an event returned exactly the event in the list, and an ID that does not exist or is not
  a number was a `404` with `['Event not found']`. So was `reemit` of an ID that does not exist.

## `links`

A link connects a source action to a receiver action: the receiver gets the events that the source
emits. A link has no ID of its own, only the pair of the `source_id` and the `receiver_id`. The
Tines docs and the OpenAPI document have one operation for links, deleting them. They have no way to
list, get or create a link: links are created with `source_ids`, `links_to_sources`, `receiver_ids`
and `links_to_receivers` of [`actions.create` and `actions.update`](stories_actions.md#links).

`links.delete(links=...)` deletes one or more links in a single request. `links` is a sequence of
dicts, typed as `tapi.stories.Link`, each with the `source_id` and the `receiver_id` of the actions
it connects:

```python
tines.stories.links.delete(
    links=[
        {"source_id": 123, "receiver_id": 456},
        {"source_id": 456, "receiver_id": 789},
    ]
)
```

The links must all belong to the same story. The reply has a 204 status and `data` is `None`. Tines
checks every link before it deletes any, so a request that is refused deletes nothing.

| Reply | When |
| ----- | ---- |
| `400`, `['Links must be an array of objects with source_id and receiver_id']` | `links` is missing or is not a list of objects. |
| `400`, `['Each link must have source_id and receiver_id']` | An object has no `source_id` or no `receiver_id`, or one is `null`. |
| `400`, `['All links must belong to the same story']` | The links are in different stories. |
| `404`, `['Link not found between 1 and 2']` | A link does not exist, or is not visible to the key. The message names the first pair that was not found. |
| `500` | `links` is an empty list. |

The Tines docs sample shows the IDs as strings, and the server accepted digits in a string as well as
a number.

Tested on 2026-11-23 with two throwaway stories of Event Transformation actions, both deleted
afterwards. The tenant ended with the eight stories and the 246 actions it started with.

| Check | Result |
| ----- | ------ |
| `links.delete` of one link | `204`, no data and no content type. The `sources` of the receiver and the `receivers` of the source changed at once, and the other links were untouched. |
| The same link again | `404`, with `['Link not found between <source> and <receiver>']`. |
| The link the other way round | `404`, as above. A link from an action to itself: `404`. |
| A request with one link that exists and one that does not | `404`, and the link that exists was not deleted. |
| Links of two stories in one request | `400`, with `['All links must belong to the same story']`, and neither link was deleted. |
| Several links at once, one with its IDs as strings | `204`, and every link was deleted. The actions were not. |
| A link of type `FAILURE`, and a link of type `DEFAULT` | Both were deleted without naming the type. |
| The same link twice in one request | `204`. |
| A link made again with `actions.update` after it was deleted | `200`, and the link was back. |
| A malformed body, an empty list, and IDs that do not exist | The replies in the table above. |

## `notes`

Notes are Markdown text on the storyboard, the diagram of a story, with a position on it. A note
belongs to a story or to a group. A note has:

| Field                       | Meaning                                                                          |
| --------------------------- | -------------------------------------------------------------------------------- |
| `id`                        | The ID of the note.                                                              |
| `story_id`, `story_mode`    | The story, and its mode, `LIVE` or `TEST`.                                       |
| `group_id`                  | The group, or `null`.                                                            |
| `content`                   | The Markdown text.                                                               |
| `position`                  | The coordinates on the diagram, an object with the integers `x` and `y`.         |
| `draft_id`, `draft_name`    | The draft of the note, for a story with change control.                          |

The replies seen had no `draft_id` and `draft_name`, because none of the stories had change control.

**`notes.list()`** is paginated, and `data` holds `annotations`, which is the old name of the notes,
and `meta`.

| Parameter    | Type  | Meaning                                                                          |
| ------------ | ----- | -------------------------------------------------------------------------------- |
| `story_id`   | `int` | Only notes of this story.                                                        |
| `mode`       | `str` | `LIVE` or `TEST`. Use it with `story_id`.                                        |
| `team_id`    | `int` | Only notes of this team.                                                         |
| `group_id`   | `int` | Only notes of this group.                                                        |
| `draft_id`   | `int` | Only notes of this draft. Use it with `story_id`.                                |
| `per_page`   | `int` | Results per page. Tines defaults to 20 and caps it at 500.                       |
| `page`       | `int` | The page, starting at 1. Tines defaults to 1.                                    |

**`notes.get()`** takes `note_id`. **`notes.delete()`** takes `note_id`, with a 204 status and no
data.

**`notes.create()`** takes `story_id` or `group_id`, `content`, `position` and `draft_id`, as JSON,
and the reply has a 201 status. A story or a group must be given. The Tines docs say that if change
control is enabled and no `draft_id` is given, Tines adds the note to a draft called `test`. That
was not tried, because no story of the tenant had change control when notes were checked. The
OpenAPI document requires no parameter, and the Tines docs mark only `content` as not optional,
without saying that it is required. The server refuses a note without `content`, so `content` is a
required parameter of tapi. `story_id`, `group_id`, `position` and `draft_id` are optional, and
tapi cannot tell you at the call that neither a story nor a group was given: Tines answers that.

**`notes.update()`** takes `note_id`, `content` and `position`. The Tines docs show it as `PUT`. The
OpenAPI document lists `PUT` and `PATCH`, and tapi uses `PATCH`. A story, a group and a draft cannot
be changed.

On 2026-11-23 the notes were first read on a tenant with 6 notes in 2 stories, and then written on
a throwaway story, as described after the read-only findings. The contents of the existing notes are
not recorded here.

Read-only findings:

- A note had `id`, `story_id`, `story_mode`, `group_id`, `content` and `position`. `get` returned
  exactly the note in the list.
- `notes.list` with a `story_id` that does not exist, a `team_id` that does not exist or a `group_id`
  that does not exist was a `404`, with `['Story not found']`, `['Team not found']` and
  `['Group not found']`.
- `mode="LIVE"` worked with and without a `story_id`. `mode="TEST"` for a story without change
  control was a `404` with `['Story not found']`, and a `mode` that is neither was ignored. The
  server also read a parameter named `story_mode`: `story_mode="TEST"` was a `400` with
  `["Change control isn't enabled for this story"]`. tapi offers `mode`, which the docs list.
- `draft_id` with a `story_id` of a story without change control was a `400`, with
  `["Change control isn't enabled for this story; omit draft_id"]`. Alone, `draft_id` was ignored.
- `per_page=0` was a `400`, with `['Invalid per_page: 0. per_page must be a positive integer.']`,
  `per_page=501` was a `200` and `meta` showed a `per_page` of 500, and a page past the end was an
  empty list.
- `get` of a note that does not exist, or whose ID is not a number, was a `404` with
  `['DiagramNote not found']`.
- The route with a trailing slash, as the Tines docs write it for `create` and `list`, and the
  `/api/v1/annotations` copy of the route both worked.

Write findings, from one throwaway story called `tapi-live-check-story` in the standard team. The
story was deleted at the end, and the tenant ended with the 8 stories and the 6 notes it started
with.

| Check | Result |
| ----- | ------ |
| `create` with a story, `content` and a `position` | `201`, with the content type `application/json`. `data` had `id`, `story_id`, `story_mode` (`LIVE`), `group_id` (`null`), `content` and `position`, and no draft keys. The position came back as sent, `{'x': 100, 'y': 200}`. `get` returned exactly the same object. |
| `create` with a story and `content`, and no `position` | `201`, with the position `{'x': 0, 'y': 0}`. |
| `create` with an empty `content` | `201`. |
| `create` with a story and no `content`, and with a story and a `position` and no `content` | `422`, with `[{'diagram_notes.0.content': 'Expected value to not be null'}]`. This is why `content` is required in tapi. |
| `create` with a `content` that is a number (raw request) | `422`, with `[{'diagram_notes.0.content': 'Could not coerce value 123 to String'}]`. |
| `create` with a `content` of 20,000 characters (raw request) | `422`, with `['Validation failed: Content is too long (maximum is 8000 characters)']`. |
| `create` with a `position` of `{"x": 1.5, "y": -3}` (raw request) | `422`, with `[{'diagram_notes.0.position.x': 'Could not coerce value 1.5 to Int'}]`. |
| `create` with a `position` that has only `x` (raw request) | `422`, with `[{'diagram_notes.0.position.y': 'Expected value to not be null'}]`. |
| `create` with no story and no group | `404`, with `['Story or Group ID must be provided']`. |
| `create` with a story that does not exist, and with a group that does not exist | `404`, with `['Story not found']` and `['Group not found']`. A story that exists with a group that does not: `['Group not found']`. |
| `create` with a `draft_id` on a story without change control | `400`, with `["Change control isn't enabled for this story; omit draft_id"]`. |
| `list(story_id=...)` | `200`, with the 3 notes that had been created, in an order that was not newest first, and `meta` counted 3. `mode="LIVE"` returned the same 3, `mode="TEST"` was a `404` with `['Story not found']`, and `team_id` of the standard team contained them. Without filters `meta` counted 9, which was 6 plus the 3. |
| `update` of `content` only | `200`. The position was kept, and the reply had the same keys as the created note. |
| `update` of `position` only, with `{"x": 10, "y": 10}` | `200`, and the reply had the position `{'x': 15, 'y': 15}`, which is the change that the Tines docs sample shows. The content was kept. |
| `update` of `content` and a position of `{"x": 0, "y": 0}` | `200`, with both. |
| `update` with a `position` that has only `x`, `{"x": 7}` | `200`, and the reply had `{'x': 0, 'y': 0}`. |
| `update` as `PUT`, the verb the Tines docs show, with the position `{"x": 3, "y": 4}` (raw request) | `200`, the same as `PATCH`. The reply had the position `{'x': 0, 'y': 0}`. |
| `update` with an empty `content` | `200`. |
| `update` with nothing | `200`, with a note. |
| `update` with a `story_id` of a story that does not exist (raw request) | `200`, and the note stayed in its story: a story cannot be changed. |
| `update` of a note that does not exist | `404`, with `['DiagramNote not found']`. |
| `delete` | `204`, with no data and no content type. `get` answered `404` at once, and the story had one note less. |
| `delete` of the same note again, and of a note that does not exist | `404`, with `['DiagramNote not found']`. |
| `stories.delete` of the story | `204`, and `get` answered `200` and then `404`. Listing the notes of the story afterwards was a `404`, so its notes went with it. |

Only some of the positions that `update` returned were the ones sent: `{"x": 10, "y": 10}` came back
as `{"x": 15, "y": 15}`, and `{"x": 3, "y": 4}` and `{"x": 7}` came back as `{"x": 0, "y": 0}`, while
`create` returned `{"x": 100, "y": 200}` unchanged. Those values are consistent with `update` moving
a note to a multiple of 15, but only these values were tried, so read the position from `data` and
do not rely on that.

Not tried: a note in a group, a note in a draft of a story with change control, `mode="TEST"` with a
story that has change control, and the interaction of `story_id` and a `group_id` that exists.

## Filters and orders

`filter` takes one of: `SEND_TO_STORY_ENABLED`, `HIGH_PRIORITY`, `API_ENABLED`, `PUBLISHED` (which
Tines marks as deprecated), `FAVORITE`, `CHANGE_CONTROL_ENABLED`, `CHANGE_CONTROL_DISABLED`,
`ENABLED`, `DISABLED` and `LOCKED`. The server also accepts `ALL_STORIES`, `WORKBENCH_ENABLED` and
`TUNNELS_ENABLED`, which neither the Tines docs nor the OpenAPI document list, and tapi offers them.

`order` takes one of: `NAME`, `NAME_DESC`, `RECENTLY_EDITED`, `LEAST_RECENTLY_EDITED`,
`ACTION_COUNT_ASC`, `ACTION_COUNT_DESC`, `CONCURRENT_RUNS_COUNT_DESC`,
`PENDING_ACTION_RUNS_COUNT_DESC` and `NOT_WORKING_ACTIONS_COUNT_DESC`. On the live tenant
`ACTION_COUNT_ASC` and `ACTION_COUNT_DESC` were answered with a `500` after about 35 seconds, which
is longer than the default timeout of `Tines`, so they raise `TinesConnectionError` unless the
timeout is raised.

## Event retention

`keep_events_for` is a number of seconds: `3600` (1 hour), `21600` (6 hours), `86400` (1 day),
`259200` (3 days), `604800` (7 days), `1209600` (14 days), `2592000` (30 days), `5184000` (60
days), `7776000` (90 days), `15552000` (180 days) or `31536000` (365 days). The Tines docs list
them, and the OpenAPI document gives them in a description and not as an enumeration.

## Errors

| Status | When                                                                                       |
| ------ | ------------------------------------------------------------------------------------------ |
| `400`  | A pagination parameter is invalid, a required field is missing, or the test mode or a draft is asked for on a story without change control. `data` is a list of messages. |
| `401`  | The OpenAPI document lists it for `change_control.approve`, `cancel` and `reject`, when the key may not do it. It was not seen. |
| `404`  | The story, the group, the draft, the version, the run, the team, the folder, the user, the recipient, the note or the change request does not exist or is not visible to the key. The messages are `['Story not found']`, `['Group not found']`, `['StoryVersion not found']`, `['Draft not found']`, `['Story run not found']`, `['Team not found']`, `['Folder not found']`, `['User not found']`, `['Recipient not found']`, `['DiagramNote not found']`, `['StoryChangeRequest not found']` and, for `batch_delete`, `['StoryContainer not found']`. `notes.create` with no story and no group is a `404` too, with `['Story or Group ID must be provided']`. |
| `422`  | A value is invalid or refused: an unknown `filter`, a tag that does not exist, `priority` on a plan without it, a draft name that is in use, `drafts.list` on a story without change control, and `cancel` of a change request that is already in progress. Also `events.list`, when the payloads of a page are too large, and `notes.create`, for a `content` that is missing, is not text or is over 8000 characters, and for a `position` that is not made of two integers. `data` is a list of messages or of objects naming the field. |
| `500`  | `create` with `tags`, and `list` with `ACTION_COUNT_ASC` or `ACTION_COUNT_DESC`, after about 35 seconds. `data` is `{'errors': [{'message': "We're sorry, but something went wrong (500)"}]}`. |
| `503`  | `diagram`, when the diagram could not be rendered.                                         |
| `504`  | `events.list` with `include_groups` and a `story_id`, when the list takes too long.        |

`links.delete` has its own replies, in [`links`](#links).
