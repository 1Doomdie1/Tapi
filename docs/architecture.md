# Architecture

## Layers

```
Tines                  src/tapi/client.py           entry point, one per tenant
└── Transport          src/tapi/core/transport.py   one HTTP call in, one Response out
    └── httpx.Client
```

Endpoint modules (`tapi.info`, `tapi.stories`, `tapi.tags`, ...) each take the `Transport` and send
their requests through `Transport.request`. `Tines` builds one `Transport` and hands it to every
module, which then becomes an attribute such as `tines.info`.

Implemented so far: `info`, `ai`, `apps`, `audit_logs`, `cases`, `change_requests`, `credentials`,
`folders`, `reporting`, `resources`, `stories`, `tags`, `teams` and `workbench`. The other module
folders exist but are still empty.

## The core layer

`src/tapi/core/` holds everything the modules share. It depends on nothing else in the package.

| File            | Contents                                                                           |
| --------------- | ---------------------------------------------------------------------------------- |
| `exceptions.py` | `TinesError`, `TinesConfigurationError` and `TinesConnectionError`                 |
| `response.py`   | `Response` and `decode_body`, which turns a reply body into `Response.data`        |
| `transport.py`  | `Transport`, which sends requests and returns a `Response` for every reply         |
| `auth.py`       | `ApiKeyAuth`, which sends the API key in the `X-User-Token` header                 |
| `config.py`     | Resolution of the tenant domain and the API key from arguments or the environment  |
| `params.py`     | `omit_none` (drops `None` values), `to_iso` (formats datetimes) and `to_list` (turns a sequence into a repeated parameter) |

## Life of a request

1. `Tines` resolves the tenant domain and the API key (`config.py`) and creates a `Transport`.
2. A module method calls `Transport.request(method=..., path=..., params=..., json=...)`.
3. `httpx` sends the request. `ApiKeyAuth` adds the `X-User-Token` header.
4. The reply becomes a `Response`: its status code, its decoded body and its lower-cased headers.
5. If no reply arrives, `TinesConnectionError` is raised instead.

## Anatomy of a module

`info` is the smallest complete module and the pattern for the others:

| Part                                | Role                                                                                       |
| ----------------------------------- | ------------------------------------------------------------------------------------------ |
| `src/tapi/info/api.py`              | The `Info` class. Its constructor takes a `Transport` (`Info(transport=...)`); each method sends one request and returns the `Response`. |
| `src/tapi/info/__init__.py`         | Exports the class, so `from tapi.info import Info` works.                                  |
| `src/tapi/client.py`                | Creates the module in `Tines.__init__` with the shared `Transport`.                        |
| `tests/info/test_api.py`            | A table of calls and the request each must send, checked against mocked HTTP. See [Testing](testing.md). |
| `docs/endpoints/info.md`            | Maps each method to its HTTP route and describes what it returns.                          |

A module that groups several areas has an `api.py` class that only creates the area classes. In
`ai`, `AI` creates `Providers` and `Usage`, which live in `providers.py` and `usage.py`, so the
calls read `tines.ai.providers.list()` and `tines.ai.usage.get()`. Each area class can also be
used on its own with a `Transport`.

A module can also have methods of its own and a sub-area beside them. `Teams` has `list`, `get` and
the other team methods in `api.py`, and creates `Members` from `members.py`, so the calls read
`tines.teams.get(team_id=4)` and `tines.teams.members.list(team_id=4)`. `Stories` does the same
with eleven sub-areas, such as `tines.stories.versions.list(story_id=4)` and
`tines.stories.actions.get(action_id=4)`. Values that several of its files accept, such as the
story filters and orders and the types of actions, live in `stories/types.py`.

Every method has keyword-only, typed parameters named as the API names them, and a docstring that
starts with what it does and the route it calls, then describes each parameter and the values it
accepts. See [Conventions](conventions.md).

## Design decisions

- **Replies are returned as they are.** No status code is treated as an error, so the caller always
  decides how to react. See [Responses](responses.md).
- **No retries, no pagination, no redirects.** `Transport` performs exactly one request per call.
- **Few exceptions.** Only a missing configuration and a missing reply raise.
- **The API key is kept in one place.** It lives in `ApiKeyAuth`, whose `repr` hides it, and is
  never part of the `repr` of `Tines` or `Transport`.
- **Modules depend on `tapi.core` only.** They do not import each other, so each can be used on its
  own with a `Transport`.
