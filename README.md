# tapi

Unofficial Python wrapper for the [Tines REST API](https://www.tines.com/stories/docs/api/welcome/).

> **Status: early development.** The `Tines` client and its core layer (responses, transport,
> configuration) are in place. Endpoint modules implemented so far: `info`, `ai`, `apps`,
> `audit_logs`, `cases`, `change_requests`, `credentials`, `folders`, `reporting`, `resources`,
> `stories`, `tags`, `teams` and `workbench`.

Requires Python 3.11 or newer.

## Design

- One module per Tines API area (`tapi.stories`, `tapi.tags`, `tapi.cases`, ...). Each module
  can be imported and used on its own.
- `Tines` is the umbrella class. An instance holds every module as an attribute, for example
  `Tines(...).stories`.
- Every call returns a `Response` with exactly three fields: `status_code`, `data` and `headers`.
- Non-2xx statuses are returned, not raised. The caller decides what to do with them.
- There are no automatic retries and no automatic pagination. Both are left to the caller.
- Only failures that produce no HTTP response raise an exception: `TinesConnectionError` for
  refused connections and timeouts, and `TinesConfigurationError` for a missing tenant domain or
  API key.

## Documentation

The [documentation overview](docs/README.md) lists every page and says where to start.

| Page                                                 | Covers                                              |
| ---------------------------------------------------- | --------------------------------------------------- |
| [Getting started](docs/getting-started.md)           | Installing and making a first call                  |
| [Architecture](docs/architecture.md)                 | How the core, the modules and `Tines` fit together  |
| [Conventions](docs/conventions.md)                   | Naming, parameters and docstrings                   |
| [Testing](docs/testing.md)                           | Running the tests and writing the tests of a module |
| [OpenAPI drift](docs/openapi-drift.md)               | Comparing tapi's routes with the Tines OpenAPI file |
| [Responses](docs/responses.md)                       | The `Response` class, body decoding, non-2xx        |
| [Pagination](docs/pagination.md)                     | Walking pages yourself                              |
| [Endpoints](docs/endpoints/)                         | One page per module, mapping methods to routes      |
