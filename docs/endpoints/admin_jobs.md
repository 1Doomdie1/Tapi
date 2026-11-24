# Admin: jobs

The background jobs of a dedicated tenant. They are a sub-area of [`admin`](admin.md), available as
`tines.admin.jobs`, and the class is `tapi.admin.Jobs`. Every method returns a
[`Response`](../responses.md). The Tines docs say that the routes are relevant for dedicated tenants
only, and they are in the docs but not in the OpenAPI document.

**Be careful with deletes.** Each `delete_*` method removes jobs for good, and the three `delete_all_*`
methods remove them for the whole tenant.

| Method                                | HTTP route                                                       |
| ------------------------------------- | ---------------------------------------------------------------- |
| `list_dead(...)`                      | `GET /api/v1/admin/dead_jobs`                                    |
| `list_in_progress(...)`               | `GET /api/v1/admin/in_progress_jobs`                             |
| `list_queued(...)`                    | `GET /api/v1/admin/queued_jobs`                                  |
| `list_retry(...)`                     | `GET /api/v1/admin/retry_jobs`                                   |
| `delete_all_dead()`                   | `DELETE /api/v1/admin/delete_all_dead_jobs`                      |
| `delete_all_queued()`                 | `DELETE /api/v1/admin/delete_all_queued_jobs`                    |
| `delete_all_retry()`                  | `DELETE /api/v1/admin/delete_all_retry_jobs`                     |
| `delete_dead_by_action(action_id=...)`   | `DELETE /api/v1/admin/actions/{action_id}/delete_all_dead_jobs`   |
| `delete_queued_by_action(action_id=...)` | `DELETE /api/v1/admin/actions/{action_id}/delete_all_queued_jobs` |
| `delete_retry_by_action(action_id=...)`  | `DELETE /api/v1/admin/actions/{action_id}/delete_all_retry_jobs`  |

## The lists

Each list is paginated, and one call returns one page; see [Pagination](../pagination.md).

| Parameter  | Type  | Meaning                                                  |
| ---------- | ----- | -------------------------------------------------------- |
| `per_page` | `int` | The number of results per page. Tines defaults to 20.   |
| `page`     | `int` | The page to return, starting at 1. Tines defaults to 1.  |

The Tines docs describe the reply as an array, and their samples show an object with the jobs under
`admin/dead_jobs`, `admin/in_progress_jobs`, `admin/queued_jobs` or `admin/retry_jobs`, and `meta`, the
pagination details. A job has these fields.

| Field         | Meaning                                                                                       |
| ------------- | --------------------------------------------------------------------------------------------- |
| `id`          | The ID of the job.                                                                            |
| `type`        | The type of the job, such as `AgentReceiveJob` or `CredentialRefreshJob`.                     |
| `agent`       | For an `AgentReceiveJob`, an object with the `id` and `name` of the action. For a `CredentialRefreshJob`, the ID of the action. |
| `events`      | The ID of the event.                                                                          |
| `retry_count` | How many times the job was retried. Dead and retry jobs.                                      |
| `last_retry`  | The time of the last retry, as a timestamp. Dead and retry jobs.                              |
| `error_class` | The type of the error. Dead and retry jobs.                                                   |
| `started_at`  | The time the job started, as a timestamp. In-progress jobs.                                   |

The sample of the queued jobs shows `retry_count`, `last_retry` and `error_class`, and its field table
lists `started_at`.

## The deletes

Every delete has a `204` status and no data. The ones with `_by_action` take `action_id`, the ID of the
action, and delete the jobs of that action only. The Tines docs do not give the type of the ID, and tapi
takes an integer, like every other action ID.

## Errors

A tenant that is not dedicated answers the lists with `403` and an object whose `error` is
`Endpoint not available on this tenant`. The Tines docs list no other status code for these routes.

## Not tried

The tenant used to check this module is not dedicated, so the four lists answered `403`, and nothing
else was run. The shape of a job, the `meta` of a page and the deletes come from the Tines docs, whose
samples are not consistent with their descriptions.
