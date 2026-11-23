# Reporting

Reports about the tenant: its flow usage and the time that Tines saved. The module is available as
`tines.reporting`, and the class is `tapi.reporting.Reporting`. Every method returns a
[`Response`](../responses.md).

| Method            | HTTP route                           |
| ----------------- | ------------------------------------ |
| `flow_usage(...)` | `GET /api/v1/reporting/flow_usage`   |
| `time_saved(...)` | `GET /api/v1/reporting/time_saved`   |

## `flow_usage()`

Returns the flow usage of the tenant against its licensed flow limit, broken down by team. Tines
recalculates the counts when a story changes, not on each request. Only tenant owners can call it,
and only tenants on the flows pricing model can use it. The teams are paginated, and one call
returns one page; see [Pagination](../pagination.md).

Both parameters are optional and keyword-only.

| Parameter  | Type  | Meaning                                                                     |
| ---------- | ----- | --------------------------------------------------------------------------- |
| `per_page` | `int` | The number of teams per page. Tines defaults to 20 and caps it at 500.      |
| `page`     | `int` | The page to return, starting at 1. Tines defaults to 1.                     |

`data` is an object with `flows`, `teams` and `meta`.

| Field                 | Meaning                                                                            |
| --------------------- | ---------------------------------------------------------------------------------- |
| `flows.used`          | The flows in use across the tenant.                                                |
| `flows.limit`         | The licensed flow limit.                                                           |
| `flows.allocated`     | The flows given to specific teams.                                                 |
| `flows.unallocated`   | The flows that teams without an allocation share.                                  |
| `teams[].id`          | The ID of the team.                                                                |
| `teams[].name`        | The name of the team.                                                              |
| `teams[].flows_used`  | The flows used by the stories of the team.                                         |
| `teams[].flows_allocated` | The flows given to the team, or `null` when it has no allocation and draws from the unallocated flows. |
| `teams[].flows_available` | The allocated flows that the team has not used, or `null` when it has no allocation. |

`meta` holds `current_page`, `previous_page` and `next_page` (links), `next_page_number`, `per_page`,
`pages` and `count`.

## `time_saved()`

Returns the time that Tines saved, as dated records. The endpoint is paginated, and one call returns
one page.

All parameters are optional and keyword-only. Parameters left as `None` are not sent.

| Parameter    | Type                | Meaning                                                                              |
| ------------ | ------------------- | ------------------------------------------------------------------------------------ |
| `start_date` | `datetime` or `str` | Only records after this time. Without it the reply holds no records.                 |
| `end_date`   | `datetime` or `str` | Only records before this time. Tines defaults to the current time.                   |
| `date_unit`  | `DateUnit`          | How to group the records: `hour`, `day`, `week` or `month`. Tines defaults to `day`. |
| `fill_gaps`  | `bool`              | Whether to fill the groups that have no data with a value of 0. Tines defaults to `True`. `False` is sent. |
| `team_id`    | `int`               | Only records of this team.                                                           |
| `story_id`   | `int`               | Only records of this story.                                                          |
| `action_id`  | `int`               | Only records of this action.                                                         |
| `per_page`   | `int`               | The number of results per page. Tines defaults to 20 and caps it at 500.             |
| `page`       | `int`               | The page to return, starting at 1. Tines defaults to 1.                              |

`DateUnit` is `tapi.reporting.DateUnit`. `start_date` and `end_date` take a `datetime` or an ISO 8601
string, and a datetime without a timezone is treated as UTC. Tines also accepted a date without a
time, such as `2026-11-01`.

```python
from datetime import UTC, datetime, timedelta

response = tines.reporting.time_saved(
    start_date=datetime.now(UTC) - timedelta(days=30),
    date_unit="week",
)
```

`data` is an object with `time_saved`, the records of the page, and `meta`, the pagination details.
A record has two fields:

| Field   | Meaning                                                                                     |
| ------- | ------------------------------------------------------------------------------------------- |
| `date`  | A UTC timestamp, rounded down to the `date_unit`, such as `2026-11-23T00:00:00Z`. For hours Tines writes `2026-11-23T21:00:00+00:00`. |
| `value` | The time saved in seconds, as a number.                                                     |

Some behaviors worth knowing:

- Without `start_date`, `data["time_saved"]` is an empty list. With it, the records run from the
  start to `end_date`, one per `date_unit`, so a `start_date` 30 days back gives 31 daily records.
- `end_date` can be in the future, and the records then run to it. It must be later than
  `start_date`, and the check applies when `end_date` is left out too.
- `date_unit` is case-sensitive. A value in upper case, such as `DAY`, is not refused, and the
  reply holds no records.
- With `fill_gaps=False`, only the groups that have data are returned. The reply is empty for a
  period with no time saved.

## Errors

| Status | When                                                                                          |
| ------ | --------------------------------------------------------------------------------------------- |
| `400`  | `flow_usage` on a tenant that is not on the flows pricing model. `time_saved` with a `date_unit` that is not valid (`["Bad request: date_unit must be one of 'hour', 'day', 'week', 'month', got 'year'"]`) and with an `end_date` that is not later than the start (`['Bad request: end_date must be later than start_date, got start_date: ..., end_date: ...']`). Both with a `per_page` or `page` that is not a positive integer (`['Invalid per_page: 0. per_page must be a positive integer.']`). |
| `404`  | `time_saved` with a `team_id`, `story_id` or `action_id` that does not exist or is not visible to the key: `['Team not found']`, `['Story not found']` or `['Action not found']`. |
| `422`  | `time_saved` with a date that cannot be read. `data` is a list holding an object that names the parameter, such as `Could not coerce value "not a date" to ISO8601DateTime`. The OpenAPI document gives a `400` for this. |

## Not tried

Everything above was tried on 2026-11-23, on a tenant that is on the flows pricing model and has
one team with stories. These were not seen:

- `flow_usage` on a tenant that is not on the flows pricing model, which the Tines docs say is a
  `400`, and with a key that is not a tenant owner;
- a team with an allocation, so `flows_allocated` and `flows_available` as numbers;
- `time_saved` with time saved in it. Every record that the tenant returned had a `value` of `0.0`,
  and `fill_gaps=False` returned nothing, so the values in seconds and the filters by team, story
  and action are not checked against data;
- an offset in a timestamp. `2026-11-20T00:00:00+05:00` returned the same first record as
  `2026-11-20T00:00:00`, so Tines may ignore the offset.
