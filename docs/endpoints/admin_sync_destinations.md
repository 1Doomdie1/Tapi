# Admin: sync destinations

A sync destination delivers stories of this tenant to a team of another tenant, or to another team of
the same tenant. The source stories must use change control, and draft syncing must be enabled for the
source tenant. The destinations are a sub-area of [`admin`](admin.md), available as
`tines.admin.sync_destinations`, and the class is `tapi.admin.SyncDestinations`. Every method returns a
[`Response`](../responses.md).

**Be careful with writes.** `create` can send stories, and an API key, to another tenant, and `delete`
deletes the synced stories on the destination by default. `manual_sync` and `sync_story` replace the
live story on a `live_readonly` destination.

| Method                                                                        | HTTP route                                                      |
| ----------------------------------------------------------------------------- | --------------------------------------------------------------- |
| `list(...)`                                                                   | `GET /api/v1/admin/sync_destinations`                           |
| `get(sync_destination_id=...)`                                                | `GET /api/v1/admin/sync_destinations/{sync_destination_id}`     |
| `create(destination_tenant_url=..., destination_team_id=..., team_id=..., story_ids=...)` | `POST /api/v1/admin/sync_destinations`            |
| `update(sync_destination_id=...)`                                             | `PATCH /api/v1/admin/sync_destinations/{sync_destination_id}`   |
| `delete(sync_destination_id=..., ...)`                                        | `DELETE /api/v1/admin/sync_destinations/{sync_destination_id}`  |
| `manual_sync(sync_destination_id=...)`                                        | `POST /api/v1/admin/sync_destinations/{sync_destination_id}/manual_sync` |
| `sync_story(sync_destination_id=..., story_id=...)`                           | `POST /api/v1/admin/sync_destinations/{sync_destination_id}/story/{story_id}/sync` |

## The destination

| Field                    | Meaning                                                                          |
| ------------------------ | -------------------------------------------------------------------------------- |
| `id`                     | The ID of the destination.                                                       |
| `destination_tenant_url` | The base URL of the destination tenant.                                          |
| `destination_team_id`    | The team on the destination tenant that owns the synced stories.                 |
| `manual_sync_only`       | Whether the stories are synced only by hand.                                     |
| `sync_mode`              | `live_readonly` or `draft_editable`.                                             |
| `origin_team_id`         | The team of this tenant where the destination was created.                       |
| `subscriptions`          | One object for each story: `story` (its `id` and `name`), `status` (`synced`, `failed` or `requires_sync`) and `error_message` (`null` unless it failed). |

With `live_readonly`, each delivery replaces the live story on the destination. With `draft_editable`,
the first delivery creates a blank live story and an editable draft, and each later one creates a new
draft and leaves the live story alone. `SyncMode` is `tapi.admin.SyncMode`. The Tines docs show a
destination inside an object with `sync_destination` for `get`, `create` and `update`, and the OpenAPI
document shows it as it is. Neither was seen, because the tenant had no destination.

## `list()`

The endpoint is paginated, and one call returns one page; see [Pagination](../pagination.md).
`per_page` is capped at 500, and `0` is a `400`. `data` is an object with `sync_destinations`, the
destinations of the page, and `meta`, the pagination details.

## `create()`

| Parameter                    | Type                | Meaning                                                      |
| ---------------------------- | ------------------- | ------------------------------------------------------------ |
| `destination_tenant_url`     | `str`               | The base URL of the destination tenant. For a team of this tenant, use the URL of this tenant. Required. |
| `destination_team_id`        | `int`               | The team on the destination tenant that owns the stories. Required. |
| `team_id`                    | `int`               | The team of this tenant that creates the sync. Required.     |
| `story_ids`                  | sequence of `int`   | The stories of this tenant to sync, which must use change control. Required. |
| `destination_tenant_api_key` | `str`               | A Tines API key for the destination tenant, needed only for another tenant. It needs `STORY_CREATE` and `STORY_UPDATE` on the destination team. |
| `manual_sync_only`           | `bool`              | Whether stories are synced only by hand.                     |
| `sync_mode`                  | `SyncMode`          | `live_readonly`, the default, or `draft_editable`. It cannot be changed afterwards. |

The reply has a `201` status.

## `update()`

| Parameter                    | Type              | Meaning                                                        |
| ---------------------------- | ----------------- | -------------------------------------------------------------- |
| `sync_destination_id`        | `int`             | The ID of the destination. Required.                           |
| `destination_tenant_api_key` | `str`             | A new API key. The old one is kept when it is left out.        |
| `story_ids`                  | sequence of `int` | The stories to sync. An empty list removes every subscription, and they are kept when it is left out. |
| `manual_sync_only`           | `bool`            | Whether stories are synced only by hand. Kept when left out.   |

The two teams, the URL and the sync mode cannot be changed: delete the destination and create it again.
The Tines docs show the operation as `PUT`, and the OpenAPI document lists `PUT` and `PATCH`.

## `delete()`, `manual_sync()` and `sync_story()`

- `delete(sync_destination_id=..., keep_stories=...)` has a `204` status. By default the synced
  stories on the destination are deleted, in the background. `keep_stories=True` detaches them and
  keeps them, and the stories of a `draft_editable` destination are always kept. `keep_stories` goes
  in the body of the `DELETE`, and nothing is sent when it is left out.
- `manual_sync(sync_destination_id=...)` queues the delivery of every subscribed story, and `data` is an
  object with `sync_initiated`.
- `sync_story(sync_destination_id=..., story_id=...)` queues one story, and `data` is an object with
  `story_sync_initiated`. A `live_readonly` story that is already `synced` is not sent again.

## Errors

| Status | When                                                                                          |
| ------ | --------------------------------------------------------------------------------------------- |
| `400`  | `list` with a `per_page` or `page` that is not a positive integer (`['Invalid per_page: 0. per_page must be a positive integer.']`). |
| `404`  | `get` with a destination that does not exist (`['Sync destination not found']`).               |

## Not tried

Everything above was read from a tenant that had no sync destinations, so no destination has been
seen. These were not run: `create`, `update`, `delete`, `manual_sync` and `sync_story`, which send
stories to another team or delete them, and the messages of a refused request. Their shapes come from
the Tines docs and the OpenAPI document, which also differ on whether a destination is wrapped.
