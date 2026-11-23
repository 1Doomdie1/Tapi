# Change requests

A change request asks to promote the changes of a draft to the live story. This module reads the
change requests of every story that the API key can access. It is available as
`tines.change_requests`, and the class is `tapi.change_requests.ChangeRequests`. Every method
returns a [`Response`](../responses.md).

| Method                           | HTTP route                                         |
| -------------------------------- | -------------------------------------------------- |
| `list(...)`                      | `GET /api/v1/change_requests`                      |
| `get(change_request_id=...)`     | `GET /api/v1/change_requests/{change_request_id}`  |

## Where the other change request operations are

The Tines docs list change requests in two places, and the OpenAPI document tags them in two ways, so
tapi keeps them in two places too.

| Operation                                                                            | In tapi                                              |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------- |
| Listing change requests, and getting one by its ID                                   | `tines.change_requests`, on this page                |
| Creating, viewing, generating a description for, approving, cancelling, rejecting and promoting a change request of one story | `tines.stories.change_control`, on the [stories page](stories.md#change_control) |

## `list()`

Lists change requests across the stories that the key can access, newest first. Only the latest
change request of each draft is returned. The endpoint is paginated, and one call returns one page;
see [Pagination](../pagination.md).

All parameters are optional and keyword-only. Parameters left as `None` are not sent.

| Parameter  | Type                                | Sent as     | Meaning                                                                                  |
| ---------- | ----------------------------------- | ----------- | ---------------------------------------------------------------------------------------- |
| `team_ids` | sequence of `int`                   | `team_id[]` | Only change requests of stories in these teams.                                          |
| `statuses` | sequence of `ChangeRequestStatus`   | `status[]`  | Only change requests with one of these statuses. Tines returns every status except `PUSHED` when it is left out. |
| `per_page` | `int`                               | `per_page`  | The number of results per page. Tines defaults to 20, and a value above 500 is capped at 500. |
| `page`     | `int`                               | `page`      | The page to return, starting at 1. Tines defaults to 1.                                  |

`ChangeRequestStatus` is `tapi.change_requests.ChangeRequestStatus`: `PENDING`, `APPROVED`,
`REJECTED`, `PUSHED` or `IN_PROGRESS`, in upper case. `IN_PROGRESS` is what the author cancelling a
change request leaves.

A sequence is sent once per value, as in `status[]=PENDING&status[]=APPROVED`. An empty sequence
sends nothing. A single string raises `TypeError`, because it would be split into characters.

```python
response = tines.change_requests.list(statuses=["PENDING"], per_page=100)
```

## `get()`

Gets one change request in any status, with the export of the live story and the export of the
draft.

| Parameter           | Type  | Meaning                           |
| ------------------- | ----- | --------------------------------- |
| `change_request_id` | `int` | The ID of the change request.     |

## The reply

`list` returns an object with `change_requests`, the change requests of the page, and `meta`, the
pagination details. `get` returns the change request itself. A change request has:

| Field               | Meaning                                                                                   |
| ------------------- | ----------------------------------------------------------------------------------------- |
| `id`                | The ID of the change request.                                                             |
| `name`              | Its name.                                                                                 |
| `description`       | Its description.                                                                          |
| `status`            | `PENDING`, `APPROVED`, `REJECTED`, `PUSHED` or `IN_PROGRESS`.                             |
| `story_id`          | The ID of the story.                                                                      |
| `story_name`        | The name of the story.                                                                    |
| `team_id`           | The ID of the team of the story.                                                          |
| `draft_id`          | The ID of the draft, or `null` when the draft no longer exists.                           |
| `draft_name`        | The name of the draft, or `null` when the draft no longer exists.                         |
| `user_id`           | The ID of a user, as the Tines docs list it.                                              |
| `participants`      | A list of user IDs.                                                                       |
| `created_at`        | An ISO 8601 timestamp.                                                                    |
| `updated_at`        | An ISO 8601 timestamp.                                                                    |
| `live_story_export` | The live story as a string that holds JSON. Only in `get`.                                |
| `draft_export`      | The draft as a string that holds JSON, or `null` when the draft no longer exists. Only in `get`. |

`meta` holds `current_page`, `previous_page` and `next_page` (links), `next_page_number`, `per_page`,
`pages` and `count`. See [Pagination](../pagination.md).

## Errors

| Status | When                                                                                          |
| ------ | --------------------------------------------------------------------------------------------- |
| `400`  | `per_page` is not a positive integer. `data` is a list with the message, such as `Invalid per_page: 0. per_page must be a positive integer.` |
| `404`  | `list` with a team that does not exist or that the key cannot access (`['Team not found']`), and `get` with an ID that does not exist or is not visible (`['StoryChangeRequest not found']`). |
| `422`  | `list` with a status that is not valid, including one in lower case. `data` is a list with an object that names the value and lists the valid ones. The OpenAPI document gives a `400` for this. |

## Not tried

The tenant had no change requests when this was checked on 2026-11-23, so these calls were not read
live with a change request in the tenant:

- the items of `list` and the reply of `get` for a change request that exists. Their fields are the
  ones that the Tines docs list, and they match the change request that `stories.change_control`
  returned when it was run earlier (`id`, `name`, `description`, `status`, `participants` and the two
  exports);
- `list` filtered by a team that has change requests, and a page beyond the first.
