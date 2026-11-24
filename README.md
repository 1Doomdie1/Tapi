# tapi

Unofficial Python wrapper for the [Tines REST API](https://www.tines.com/stories/docs/api/welcome/).

tapi covers every area of the Tines API that the Tines docs list: `info`, `admin`, `ai`, `apps`,
`audit_logs`, `cases`, `change_requests`, `credentials`, `dashboards`, `folders`, `records`,
`reporting`, `resources`, `skills`, `stories`, `tags`, `teams` and `workbench`. Each is an attribute
of the `Tines` client, and the [endpoints overview](https://github.com/1Doomdie1/Tapi/blob/main/docs/endpoints/README.md) maps every method to its
route.

Requires Python 3.11 or newer.

## Installation

```powershell
pip install tapi
```

## Quick start

### The `Tines` client

`Tines` is the main class. It holds the tenant and the API key, and every module is an attribute of
it.

```python
from tapi import Tines

tines = Tines(tenant_domain="acme.tines.com", api_key="<your API key>")

response = tines.stories.list(per_page=10)
print(response.status_code)
print(response.data["stories"])
```

The tenant domain and the API key can also come from the `TINES_TENANT_DOMAIN` and `TINES_API_KEY`
environment variables. [Getting started](https://github.com/1Doomdie1/Tapi/blob/main/docs/getting-started.md) has the details.

### A module on its own

Each API area is a class of its own that takes a `Transport`, which sends the requests. Use one when
you need only that area.

```python
from tapi.core import Transport
from tapi.stories import Stories

transport = Transport(base_url="https://acme.tines.com", api_key="<your API key>")
stories = Stories(transport=transport)

response = stories.list(per_page=10)
print(response.status_code)
```

The sub-areas come with the class: `stories.versions` works like `tines.stories.versions`.

## Documentation

The [documentation overview](https://github.com/1Doomdie1/Tapi/blob/main/docs/README.md) lists every page and says where to start.

| Page                                                 | Covers                                              |
| ---------------------------------------------------- | --------------------------------------------------- |
| [Getting started](https://github.com/1Doomdie1/Tapi/blob/main/docs/getting-started.md)           | Installing and making a first call                  |
| [Architecture](https://github.com/1Doomdie1/Tapi/blob/main/docs/architecture.md)                 | How the core, the modules and `Tines` fit together  |
| [Conventions](https://github.com/1Doomdie1/Tapi/blob/main/docs/conventions.md)                   | Naming, parameters and docstrings                   |
| [Testing](https://github.com/1Doomdie1/Tapi/blob/main/docs/testing.md)                           | Running the tests and writing the tests of a module |
| [OpenAPI drift](https://github.com/1Doomdie1/Tapi/blob/main/docs/openapi-drift.md)               | Comparing tapi's routes with the Tines OpenAPI file |
| [Responses](https://github.com/1Doomdie1/Tapi/blob/main/docs/responses.md)                       | The `Response` class, body decoding, non-2xx        |
| [Pagination](https://github.com/1Doomdie1/Tapi/blob/main/docs/pagination.md)                     | Walking pages yourself                              |
| [Endpoints](https://github.com/1Doomdie1/Tapi/tree/main/docs/endpoints)                         | Each module: its methods, arguments and response codes |

## How to contribute

1. Fork the repository, clone your fork and create a branch for your change.
2. Create a virtual environment and install tapi with its development tools:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -e ".[dev]"
   ```

   On macOS and Linux, activate it with `source .venv/bin/activate`.
3. Read [Architecture](https://github.com/1Doomdie1/Tapi/blob/main/docs/architecture.md) and [Conventions](https://github.com/1Doomdie1/Tapi/blob/main/docs/conventions.md). Every method
   takes keyword-only arguments, names its parameters as the Tines API does, and has a short
   docstring that starts with the route that it calls.
4. Make the change, with its tests and its page in [`docs/endpoints/`](https://github.com/1Doomdie1/Tapi/tree/main/docs/endpoints). Each method
   needs a row in the table of cases of its module, and
   [Testing](https://github.com/1Doomdie1/Tapi/blob/main/docs/testing.md) shows how to write one. The tests never reach a tenant.
5. Run the checks. All of them must pass:

   ```powershell
   ruff check . ; ruff format .
   mypy
   python -m pytest
   python tools/check_openapi_drift.py
   ```

   The last one compares the routes of tapi with the Tines OpenAPI documents. Its notes are in
   [OpenAPI drift](https://github.com/1Doomdie1/Tapi/blob/main/docs/openapi-drift.md).
6. Open a pull request against the `dev` branch and say what changed and why.

Never put an API key or the domain of a tenant in the code, the tests, the docs or a commit. The live
tests, which need a dedicated test tenant, are opt-in and described in [Testing](https://github.com/1Doomdie1/Tapi/blob/main/docs/testing.md).
