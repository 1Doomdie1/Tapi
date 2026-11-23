# AI

AI providers and AI usage. The module is available as `tines.ai`, with one attribute per area:
`tines.ai.providers` and `tines.ai.usage`. The classes are `tapi.ai.AI`, `tapi.ai.Providers` and
`tapi.ai.Usage`; `Providers` and `Usage` can also be used on their own with a `Transport`. Every
method returns a [`Response`](../responses.md).

| Method                        | HTTP route                 |
| ----------------------------- | -------------------------- |
| `tines.ai.providers.list()`   | `GET /api/v1/ai_providers` |
| `tines.ai.usage.get(...)`     | `GET /api/v1/ai_usage`     |

## Providers

### `list()`

Lists the AI providers and models available to you. Administrators get every AI provider
configured for the tenant. Other users get the providers that belong to one of their teams, are
shared with one of their teams or are available to the whole tenant. Enabled and disabled
providers are both included. The method takes no arguments and the endpoint is not paginated.

`data` is an object with an `ai_providers` list. Each provider has:

| Field               | Meaning                                                                            |
| ------------------- | ---------------------------------------------------------------------------------- |
| `guid`              | The unique identifier of the provider.                                             |
| `enabled`           | Whether the provider is enabled.                                                   |
| `name`              | The configured name, or the default name of the provider.                          |
| `provider_type`     | `ANTHROPIC`, `OPEN_AI`, `AWS_BEDROCK`, `ORACLE_COHERE`, `MISTRAL` or `GOOGLE_VERTEX`. |
| `provisioning_type` | `customer_provisioned` or `tines_provisioned`.                                     |
| `models`            | The models available through the provider.                                         |

Each model has:

| Field          | Meaning                                                                                  |
| -------------- | ---------------------------------------------------------------------------------------- |
| `display_name` | The display name of the model.                                                           |
| `api_model_id` | The identifier to use when configuring Tines AI features through the API.                |
| `description`  | A description of the model, or `null` if there is none.                                  |
| `cost_tier`    | `LOW`, `MEDIUM`, `HIGH` or `null`.                                                       |
| `legacy`       | Whether the model is a legacy model.                                                     |

```python
response = tines.ai.providers.list()
for provider in response.data["ai_providers"]:
    print(provider["name"], [model["api_model_id"] for model in provider["models"]])
```

## Usage

### `get()`

Aggregated AI usage for the tenant: tokens, credits and cost in US dollars. Administrators see the
usage of the whole tenant. Other users see the usage of the teams they belong to, plus usage that
is not attributed to any team. When a filter names a team, story, user or action that a non
administrator may not see, the reply holds zeroed usage and is not an error.

| Parameter       | Type                | Meaning                                                                                 |
| --------------- | ------------------- | --------------------------------------------------------------------------------------- |
| `relative_date` | `str`               | A window relative to now. See [Choosing the time window](#choosing-the-time-window).    |
| `start_date`    | `datetime` or `str` | The start of a custom window. Must be paired with `end_date`.                           |
| `end_date`      | `datetime` or `str` | The end of a custom window. Must be paired with `start_date`.                           |
| `team_id`       | `int`               | Only usage attributed to this team.                                                     |
| `model_id`      | `str`               | Only usage attributed to this model.                                                    |
| `provider_id`   | `int`               | Only usage attributed to this AI provider.                                              |
| `feature`       | `str`               | Only usage attributed to this feature: `workbench`, `workbench_storyboard`, `ai_agents`, `workbench_cases`, `workbench_apps` or `other`. |
| `story_id`      | `int`               | Only runtime usage from AI actions and AI agents in this story.                         |
| `user_id`       | `int`               | Only usage initiated by this user.                                                      |
| `action_id`     | `int`               | Only runtime usage from this AI action or AI agent. An AI action that an agent uses as a tool reports its usage under its own ID. |
| `group_by`      | `str`               | Split the usage by one of `model`, `provider`, `team`, `feature`, `story`, `user`, `action` or `day`. Without it, only the totals are returned. |

All parameters are optional and keyword-only. Parameters left as `None` are not sent.

#### Choosing the time window

Use `relative_date`, or `start_date` and `end_date`, but not both. With none of them, the last 30
days are used.

- `relative_date` is `today`, `yesterday`, or a count followed by `day`, `week`, `month` or
  `year`, singular or plural, such as `7 days` or `1 year`.
- `start_date` and `end_date` take a `datetime` or an ISO 8601 string. A datetime without a
  timezone is treated as UTC. Both must be given, `end_date` must be after `start_date`, and the
  window cannot be longer than one year.

#### The reply

`data` is an object with:

| Key                   | Meaning                                                                      |
| --------------------- | ---------------------------------------------------------------------------- |
| `range`               | The resolved time window, with `start` and `end`.                            |
| `totals`              | The usage of the whole window.                                               |
| `group_by`, `groups`  | Only when `group_by` was given: the grouping, and one entry per value of it. |

`totals` and every group hold `input_tokens`, `cached_read_input_tokens`,
`cached_write_input_tokens`, `output_tokens`, `credits_used`, `usage_count` and `billed_cost`.
`billed_cost` is an object with `currency` and `amount`, a string with two decimals. Each group
also holds the keys of its grouping:

| `group_by`  | Extra keys in each group                                              |
| ----------- | --------------------------------------------------------------------- |
| `model`     | `model_id`                                                            |
| `provider`  | `provider_id`, `provider_name`                                        |
| `team`      | `team_id`, `team_name`                                                |
| `story`     | `story_id`, `story_name`                                              |
| `user`      | `user_id`, `user_email`, `user_name`, `is_service_account`            |
| `action`    | `action_id`, `action_name`, `story_id`                                |
| `feature`   | `feature`                                                             |
| `day`       | `day`, an ISO 8601 date                                               |

An identifier is `null` for usage that does not belong to anything of that kind, such as Workbench
usage with no story, and for things you cannot see.

#### Errors

An invalid request is answered with a 400 whose `data` is a list of messages. This happens when
`relative_date` is combined with `start_date` or `end_date`, when only one of those two is given,
when a date cannot be parsed or `relative_date` is unknown, when `end_date` is not after
`start_date` or the window is longer than a year, when `feature` is invalid, or when AI usage is
unavailable on the tenant.

```python
from datetime import UTC, datetime, timedelta

tines.ai.usage.get()
tines.ai.usage.get(relative_date="7 days", group_by="model")

now = datetime.now(UTC)
tines.ai.usage.get(start_date=now - timedelta(days=7), end_date=now, team_id=3)
```
