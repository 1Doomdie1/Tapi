# SyncDestinations

- **Access:** `tines.admin.sync_destinations`
- **Import:** `from tapi.admin import SyncDestinations`
- **Part of:** [Admin](admin.md)

Manage the sync destinations. A destination delivers stories of this tenant to a team of another tenant, or to another team of the same tenant. The stories must use change control, and draft syncing must be enabled for the source tenant.

> **Careful:** `create` can send stories, and an API key, to another tenant. `delete` deletes the synced stories on the destination unless `keep_stories=True`. `manual_sync` and `sync_story` replace the live story on a `live_readonly` destination.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the sync destinations. | `GET /api/v1/admin/sync_destinations` |
| [`get`](#get) | Get a sync destination. | `GET /api/v1/admin/sync_destinations/{sync_destination_id}` |
| [`create`](#create) | Create a sync destination and subscribe it to the stories. | `POST /api/v1/admin/sync_destinations` |
| [`update`](#update) | Change the API key, the stories or the manual sync setting of a destination. | `PATCH /api/v1/admin/sync_destinations/{sync_destination_id}` |
| [`delete`](#delete) | Delete a destination. | `DELETE /api/v1/admin/sync_destinations/{sync_destination_id}` |
| [`manual_sync`](#manual_sync) | Queue the delivery of every subscribed story to the destination. | `POST /api/v1/admin/sync_destinations/{sync_destination_id}/manual_sync` |
| [`sync_story`](#sync_story) | Queue the delivery of one subscribed story to the destination. | `POST /api/v1/admin/sync_destinations/{sync_destination_id}/story/{story_id}/sync` |

## Methods breakdown

### `list`

`GET /api/v1/admin/sync_destinations`

List the sync destinations.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `per_page` | `int` | no | 1 to 500 | Results per page. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `sync_destinations`, the destinations of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |

### `get`

`GET /api/v1/admin/sync_destinations/{sync_destination_id}`

Get a sync destination.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `sync_destination_id` | `int` | yes | — | The ID of the sync destination. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the destination. |
| 404 | The destination does not exist. |

### `create`

`POST /api/v1/admin/sync_destinations`

Create a sync destination and subscribe it to the stories.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `destination_tenant_url` | `str` | yes | — | The base URL of the destination tenant. For a team of this tenant, use the URL of this tenant. |
| `destination_team_id` | `int` | yes | — | The team on the destination tenant that owns the synced stories. |
| `team_id` | `int` | yes | — | The team of this tenant that creates the sync. |
| `story_ids` | `Sequence[int]` | yes | — | The stories of this tenant to sync. They must use change control. |
| `destination_tenant_api_key` | `str` | no | — | A Tines API key for the destination tenant, needed only for another tenant. It needs `STORY_CREATE` and `STORY_UPDATE` on the destination team. |
| `manual_sync_only` | `bool` | no | `True`, `False` | Whether the stories are synced only by `manual_sync` or `sync_story`. |
| `sync_mode` | [`SyncMode`](#syncmode) | no | `live_readonly`, `draft_editable` | How deliveries reach the destination. Tines defaults to `live_readonly`, and the mode cannot be changed afterwards. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the created destination. |

### `update`

`PATCH /api/v1/admin/sync_destinations/{sync_destination_id}`

Change the API key, the stories or the manual sync setting of a destination. The teams, the URL and the sync mode cannot be changed: delete the destination and create it again.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `sync_destination_id` | `int` | yes | — | The ID of the sync destination. |
| `destination_tenant_api_key` | `str` | no | — | A new API key. The old one is kept when left out. |
| `story_ids` | `Sequence[int]` | no | — | The stories to sync. An empty list removes every subscription, and they are kept when left out. |
| `manual_sync_only` | `bool` | no | `True`, `False` | Whether the stories are synced only by hand. Kept when left out. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated destination. |

### `delete`

`DELETE /api/v1/admin/sync_destinations/{sync_destination_id}`

Delete a destination. The synced stories on the destination are deleted too, unless `keep_stories=True`.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `sync_destination_id` | `int` | yes | — | The ID of the sync destination. |
| `keep_stories` | `bool` | no | `True`, `False` | `True` keeps the synced stories on the destination, detached from the source, instead of deleting them. Tines defaults to `False`. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | The destination is deleted. No data. |

### `manual_sync`

`POST /api/v1/admin/sync_destinations/{sync_destination_id}/manual_sync`

Queue the delivery of every subscribed story to the destination.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `sync_destination_id` | `int` | yes | — | The ID of the sync destination. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `sync_initiated`. |

### `sync_story`

`POST /api/v1/admin/sync_destinations/{sync_destination_id}/story/{story_id}/sync`

Queue the delivery of one subscribed story to the destination.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `sync_destination_id` | `int` | yes | — | The ID of the sync destination. |
| `story_id` | `int` | yes | — | The ID of one of the subscribed stories. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `story_sync_initiated`. |

## Types

### `SyncMode`

| Value | Meaning |
| --- | --- |
| `live_readonly` | Each delivery replaces the live story on the destination. |
| `draft_editable` | The first delivery creates a blank live story and an editable draft, and each later one creates a new draft. |
