# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project
aims to follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Project skeleton: package layout, documentation structure and tooling configuration.
- `Tines` client class, configured with a tenant domain and an API key, or from the
  `TINES_TENANT_DOMAIN` and `TINES_API_KEY` environment variables.
- Core layer: `Response`, response body decoding, `Transport`, API key authentication, and the
  `TinesConfigurationError` and `TinesConnectionError` exceptions.
- `info` module (`tines.info`): `get`, `web_stats` and `worker_stats`.
- `ai` module (`tines.ai`): `providers.list` and `usage.get`.
- `audit_logs` module (`tines.audit_logs`): `list`, filterable by time range, users, teams and
  operation names, with `page` and `per_page`.
- `credentials` module (`tines.credentials`): `list`, `get`, `create`, `update` and `delete`, with
  the parameters of every credential mode.
- `folders` module (`tines.folders`): `list`, `get`, `create`, `update` and `delete`.
- `resources` module (`tines.resources`): `list`, `get`, `create`, `update`, `delete`, `append`,
  `remove`, `replace` and `set_locked`.
- `apps` module (`tines.apps`): `list`, `get`, `create`, `delete`, `export`, `replace_files` and
  `publish`.
- `stories` module (`tines.stories`): `list`, `get`, `create`, `update`, `delete`, `batch_delete`,
  `export`, `import_`, `diagram`, `disable` and `list_pending_actions`, and the sub-areas
  `actions` (`list`, `get`, `create`, `update`, `delete`, `list_events`, `list_logs`,
  `delete_events`, `delete_logs` and `clear_memory`), `events` (`list`, `get` and `reemit`),
  `links` (`delete`), `notes` (`list`, `get`, `create`, `update` and `delete`), `drafts`, `owners`,
  `recipients`, `runs`, `groups`, `versions` and `change_control`.
- `cases` module (`tines.cases`): `list`, `get`, `create`, `update`, `delete`,
  `append_description`, `search`, `bulk_update_fields` and `get_pdf`, and the sub-areas
  `activities` (`list` and `get`), `assignees` (`list`), `comments` (with reactions), `notes`,
  `tasks`, `field_values`, `metadata`, `files`, `blocks` (with their elements), `linked_cases`,
  `records`, `subscribers`, `actions`, `fields`, `statuses`, `templates` and `webhooks`. Only the
  current API is offered: the v1 routes that Tines is removing are left out.
- `change_requests` module (`tines.change_requests`): `list`, filterable by teams and statuses, and
  `get`. The operations on the change request of one story stay in `stories.change_control`.
- `workbench` module (`tines.workbench`): `list`, filterable by title, favorite, creator, type and
  creation time, and `get`, which returns a conversation with its usage and transcript.
- `reporting` module (`tines.reporting`): `flow_usage`, the flow usage of the tenant by team, and
  `time_saved`, the time saved grouped by hour, day, week or month.
- `tags` module (`tines.tags`): `list`, `get`, `create`, `update` and `delete`.
- `teams` module (`tines.teams`): `list`, `get`, `create`, `update`, `delete` and
  `destroy_static_external_id`, and `members` (`tines.teams.members`): `list`, `invite`,
  `resend_invitation` and `remove`.
- Request parameter helpers in `core/params.py`: `omit_none`, `to_iso` and `to_list`.
- `print(response)` shows a `Response` as indented JSON. Binary data is shown as its size.
