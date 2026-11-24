# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project
aims to follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [3.0.0] - 2026-11-24

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
  `records`, `subscribers`, `actions`, `fields`, `statuses`, `templates` and `webhooks`.
- `change_requests` module (`tines.change_requests`): `list`, filterable by teams and statuses, and
  `get`. The operations on the change request of one story stay in `stories.change_control`.
- `workbench` module (`tines.workbench`): `list`, filterable by title, favorite, creator, type and
  creation time, and `get`, which returns a conversation with its usage and transcript.
- `reporting` module (`tines.reporting`): `flow_usage`, the flow usage of the tenant by team, and
  `time_saved`, the time saved grouped by hour, day, week or month.
- `dashboards` module (`tines.dashboards`): `list`, `delete`, `export` and `import_`.
- `skills` module (`tines.skills`): `list`, `get`, `create`, `update` and `delete`. A skill is found
  by its name and the ID of its team.
- `admin` module (`tines.admin`): the sub-areas `users` (`list`, `get`, `create`, `update`,
  `delete`, `list_signin_activities`, `resend_invitation` and `expire_session`), `roles`,
  `templates` (with `move`) and `tunnels` (`health`), the sub-areas `ip_access_control_rules`,
  `action_egress_control_rules` and `sync_destinations` (with `manual_sync` and `sync_story`), and
  the sub-areas `license`, `smtp` and `custom_certificate_authority` (`set`) for self-hosted
  tenants, and `jobs` for dedicated tenants (four lists and six deletes).
- `records` module (`tines.records`): `create` (with an idempotency key), `get`, `update`, `delete`,
  `search`, `aggregate`, `list_cases`, `link_case`, `unlink_case`, `list_child_record_ids` and
  `list_child_records`, and the sub-areas `record_types` (`list`, `get`, `create`, `update` and
  `delete`), `record_views` (`list`, `delete`, `export` and `import_`), `fields` (`get`) and
  `artifacts` (`get`).
- `tags` module (`tines.tags`): `list`, `get`, `create`, `update` and `delete`.
- `teams` module (`tines.teams`): `list`, `get`, `create`, `update`, `delete` and
  `destroy_static_external_id`, and `members` (`tines.teams.members`): `list`, `invite`,
  `resend_invitation` and `remove`.
- Request parameter helpers in `core/params.py`: `omit_none`, `to_iso` and `to_list`.
- `Transport.request` takes extra request `headers`.
- `print(response)` shows a `Response` as indented JSON. Binary data is shown as its size.
- `tools/check_openapi_drift.py`, which compares the routes of tapi with the Tines OpenAPI documents
  and fails when tapi offers a route that they mark as deprecated. The differences that are accepted
  are listed in `tools/openapi_known_differences.toml`.
- Opt-in live tests in `tests/live`, for a dedicated test tenant. The default `pytest` run leaves
  them out.
- Documentation in `docs/`: the guides, and for each module a page in `docs/endpoints/`, in a
  folder with a page for each sub-endpoint when the module has some. A page lists the methods
  and, for each one, its arguments, the values they accept and its response codes. The README has
  an installation, a quick start and how to contribute.
- `requirements.txt` with the runtime dependencies, `httpx` and `pydantic`.

### Changed

- tapi 3.0.0 is a rewrite and is not compatible with 0.2.x. The classes of each endpoint, such as
  `TenantAPI(DOMAIN, API_KEY)` and `StoriesAPI(DOMAIN, API_KEY)`, are replaced by the `Tines` client
  and its modules, such as `tines.stories`.
- Every call returns a `Response` with `status_code`, `data` and `headers`. A reply with a status
  other than 2xx is returned, not raised. Only `TinesConnectionError` and `TinesConfigurationError`
  are raised.
- Every function takes keyword-only arguments, and the parameters are named as the Tines API names
  them.
- tapi requires Python 3.11 or newer, and depends on `httpx` and `pydantic`.
- The package has a `src/` layout and is built with `hatchling`. The version is 3.0.0, the license is
  GPL-3.0 and the development status is production stable.
- The routes, parameters and values of tapi are the ones that the Tines docs list, and none that
  Tines deprecates.

### Removed

- The 0.2.x implementation, with `setup.py` and `MANIFEST.in`.

[Unreleased]: https://github.com/1Doomdie1/Tapi/compare/v3.0.0...HEAD
[3.0.0]: https://github.com/1Doomdie1/Tapi/releases/tag/v3.0.0
