# Testing

The tests never reach a Tines tenant. [`respx`](https://lundberg.github.io/respx/) intercepts every
HTTP request that `httpx` would send, so a test can check which request tapi built and what tapi
returns for a given reply. The whole suite takes about a minute and needs no network and no
credentials.

A separate, opt-in layer of [live tests](#live-tests) runs against a dedicated Tines test tenant. It
is left out of every normal run.

Because the library is a thin wrapper, almost everything worth testing is the same question: *does
this method send the right verb, route, query and body?* That question is written once, in
`tests/support.py`, and every module answers it with a table of cases. You add rows to a table; you
do not write a test function per method.

## Running the tests

From the project root, with the virtual environment active:

```
python -m pytest
```

To run part of the suite:

```
python -m pytest tests/tags
python -m pytest tests/stories/test_api.py
python -m pytest tests -k "tags.get or teams.members"
```

Each case is named after its method and the arguments it passes, such as
`test_request[tags.list(team_id, per_page, page)]`, so `-k` can pick out one method. When the names of
the arguments add up to more than 40 characters, the case is shown as `tags.create(...)`. A case that
has a `name` is shown with it instead, such as
`test_request[tags.delete: team_id is sent in the query, not in the body]`.

Before a change is finished, three commands must pass. Ruff lints the tests too, including the
pytest style rules.

```
ruff check . ; ruff format .
mypy
python -m pytest
```

## How the suite is laid out

| Path                       | Contents                                                                              |
| -------------------------- | ------------------------------------------------------------------------------------- |
| `tests/conftest.py`        | The shared fixtures (see [Fixtures](#fixtures)).                                      |
| `tests/support.py`         | `Case`, `assert_sent`, `assert_covers` and the helpers they use.                      |
| `tests/<area>/test_api.py` | The table of cases of one module, and its two tests. Sub-areas share the parent's file. |
| `tests/test_conventions.py`| Rules that hold for every method, checked by looking at the classes.                  |
| `tests/test_client.py`     | `Tines` itself: configuration, wiring of the modules, one call from end to end.       |
| `tests/test_packaging.py`  | The release metadata: the files that the sdist may hold, and the changelog heading.   |
| `tests/core/`              | The foundation: `Transport`, `Response`, configuration, authentication and `params`.  |
| `tests/live/`              | The opt-in tests against a test tenant. See [Live tests](#live-tests).                |

## Writing the test for a module

This is the whole test file of the `tags` module. Every module's file has the same shape:

```python
import pytest

from tests.support import Case, assert_covers, assert_sent, case_id

CASES = [
    Case(target="tags.list", arguments={}, route="GET /api/v1/tags"),
    Case(
        target="tags.list",
        arguments={"team_id": 3, "per_page": 100, "page": 2},
        route="GET /api/v1/tags",
        params={"team_id": 3, "per_page": 100, "page": 2},
    ),
    Case(target="tags.get", arguments={"tag_id": 17}, route="GET /api/v1/tags/17"),
    Case(
        target="tags.create",
        arguments={"name": "priority-high", "team_id": 1, "color": "red"},
        route="POST /api/v1/tags",
        body={"name": "priority-high", "team_id": 1, "color": "red"},
    ),
    Case(
        target="tags.update",
        name="required arguments send an empty JSON body",
        arguments={"tag_id": 17},
        route="PATCH /api/v1/tags/17",
        body={},
    ),
    Case(
        target="tags.update",
        arguments={"tag_id": 17, "name": "priority-critical", "color": "#9B61FF"},
        route="PATCH /api/v1/tags/17",
        body={"name": "priority-critical", "color": "#9B61FF"},
    ),
    Case(target="tags.delete", arguments={"tag_id": 17}, route="DELETE /api/v1/tags/17"),
    Case(
        target="tags.delete",
        name="team_id is sent in the query, not in the body",
        arguments={"tag_id": 17, "team_id": 5},
        route="DELETE /api/v1/tags/17",
        params={"team_id": 5},
    ),
]


@pytest.mark.parametrize("case", CASES, ids=case_id)
def test_request(tines, router, case):
    assert_sent(tines=tines, router=router, case=case)


def test_every_method_and_argument_has_a_case(tines):
    assert_covers(tines=tines, area="tags", cases=CASES)
```

Every call into tapi's own code names its arguments, in the tests as everywhere else, and `Case` and
the helpers of `tests/support.py` accept nothing else: `Case("tags.get", ...)` raises a `TypeError`.
The exceptions are the calls into the standard library and into third-party libraries
(`pytest.param`, `httpx.Response`, `router.get(path)`), and the functions that pytest calls itself:
the tests, the fixtures, and `case_id`, which is passed as `ids=`.

### The rule for the cases

For every method, write two cases:

1. **The minimal case** passes only the required arguments (the path IDs and the parameters without a
   default). It shows that nothing optional is sent by default.
2. **The full case** passes every argument. It shows that each parameter ends up in the right place,
   under the right name.

A method whose parameters are all required needs only one case, as `tags.get` does, because the
minimal case and the full case are then the same.

### The fields of a `Case`

| Field       | Meaning                                                                                      |
| ----------- | -------------------------------------------------------------------------------------------- |
| `target`    | The method, as the attribute path from `Tines`: `"tags.get"`, `"teams.members.list"`.        |
| `arguments` | The keyword arguments the method is called with.                                             |
| `route`     | The verb and the path that must be sent, such as `"GET /api/v1/tags/17"`.                    |
| `params`    | The query string that must be sent, as a dict. Empty by default, meaning none.               |
| `body`      | The JSON body that must be sent. `None` by default, meaning no body at all.                  |
| `name`      | Optional. What the case checks, in a few words. See [Naming a case](#naming-a-case).         |

### Naming a case

Most cases are the minimal case or the full case of a method, and the arguments they pass already
say that, so they need no name. Give a `name` to a case that checks something a reader would not see
at a glance:

- a conversion, such as a tuple that is sent as a list, a `datetime` that is sent as ISO 8601, or a
  list that is sent as `level[]`;
- a value that must be sent although it looks empty, such as `False` or `0`;
- a parameter that goes in the query when a reader would expect the body, or the other way round;
- a method that sends an empty JSON body when it has nothing to send;
- any case that is neither the minimal nor the full case of its method, such as the third case of
  `audit_logs.list`.

Write what the case shows, not the method it calls: the target is already part of the test name.
`"empty sequences send nothing"` is a good name. `"audit logs with empty lists"` is not.

The name is only a label for the person who reads a failure, and nothing checks that it matches the
case. Change it when you change what the case does. `assert_covers` fails on an empty name and on a
name that two cases of the same method share.

### Writing the expected values

- **Path IDs belong in the route.** `{"tag_id": 17}` becomes `/api/v1/tags/17`. It is not in `params`
  or `body`.
- **Query parameters** go in `params`, under the names the API uses. A repeated parameter is a list:
  `"user_ids": (1, 2)` is sent as `user_id[]=1&user_id[]=2`, so write `"user_id[]": [1, 2]`. Booleans are
  written as Python booleans and are compared as `true` and `false`.
- **The body** goes in `body`. A method that sends a JSON body with nothing in it, because every
  optional parameter was left out, is checked with `body={}`, as in the minimal `tags.update` case.
  `body=None` means that the request has no body.
- **A parameter that tapi renames** is written with the name tapi takes in `arguments` and the name the
  API uses in `params` or `body`.
- **Dates** can be passed as a `datetime` or as an ISO 8601 string. A string is sent unchanged, and a
  `datetime` is sent as ISO 8601, with a naive one taken as UTC:

  ```python
  {"before": datetime(2026, 11, 22, tzinfo=UTC), "after": "2026-11-01T00:00:00Z"}
  ```

  is expected as

  ```python
  {"before": "2026-11-22T00:00:00+00:00", "after": "2026-11-01T00:00:00Z"}
  ```
- **Sequences** can be passed as a list, a tuple or a `range`. They are sent as a list, so a tuple in
  `arguments` is a list in `params` or `body`.
- **Empty sequences** are worth a case when the method has one. An empty sequence in a query adds
  nothing to the query string; see the third case of `audit_logs.list`.

### Reusing the arguments

When a case sends exactly what it was given, define the dict once and use it for both:

```python
LIST = {"team_id": 3, "per_page": 100, "page": 2}

Case(target="tags.list", arguments=LIST, route="GET /api/v1/tags", params=LIST)
```

When the body is the arguments minus a few, use `wire`. It copies the arguments, turns tuples and
ranges into lists, and drops the names you give it. Drop the path IDs and the arguments that are sent
in the query:

```python
Case(
    target="credentials.update",
    arguments=UPDATE,
    route="PATCH /api/v1/user_credentials/21",
    params={"include_references": True},
    body=wire(arguments=UPDATE, drop=["credential_id", "include_references"]),
)
```

`wire` copies the arguments into the expectation, so it only proves that every argument is sent under
its own name. When a parameter is renamed or reshaped on its way to the API, write that part of the
body out by hand.

## What the two helpers check

`assert_sent(tines=..., router=..., case=...)` registers the route of the case, makes the call and
checks that:

- exactly one request was sent, with the verb and the path of the case;
- the query string equals `params`, and the JSON body equals `body`, or there is none;
- the call returned a `Response` with the mocked reply, a `200` with `{}`;
- the route in the first line of the method's docstring, such as ``GET /api/v1/tags/{tag_id}``, is the
  route that was sent. This keeps the documentation and the code from drifting apart.

`assert_covers(tines=..., area="<area>", cases=CASES)` finds every public method of the area and its
sub-areas, and fails if a method has no case, if a case names something that is not a method, or if a parameter is
not passed by any case. A new method or parameter therefore cannot be added without a test.

## Adding the tests of a new module

1. Create `tests/<area>/__init__.py`, empty. Every area has one, because the files are all called
   `test_api.py`.
2. Create `tests/<area>/test_api.py` from the `tags` example above: the cases, then the two tests, with
   the area name in `assert_covers`.
3. For a sub-area, such as `teams.members`, put its cases in the parent's file and use the full path as
   the target, for example `target="teams.members.list"`. `assert_covers` is called once, with the
   name of the parent.
4. Run `python -m pytest tests/<area>`.

Nothing else needs to be registered. `tests/test_conventions.py` and `tests/test_client.py` find every
module that `Tines` exposes as an attribute, so a new module is checked by them as soon as it is
attached in `src/tapi/client.py`.

## Checks you do not write

Some rules hold for every method, and one test checks all of them. Do not repeat them per method.

| What                                                                 | Where it is checked                  |
| -------------------------------------------------------------------- | ------------------------------------ |
| Every method and constructor takes keyword-only arguments            | `tests/test_conventions.py`          |
| Every method documents each parameter in `Args` and has a `Returns`  | `tests/test_conventions.py`          |
| A single string is rejected for every `Sequence` parameter           | `tests/test_conventions.py`          |
| Every area uses the transport of the client                          | `tests/test_client.py`               |
| The public names of the package                                      | `tests/test_client.py`               |
| Non-2xx replies are returned, and not retried, raised or followed    | `tests/core/test_transport.py`       |
| The decoding of a reply body by its content type                     | `tests/core/test_response.py`        |
| Configuration, the API key header, connection errors                 | `tests/core/`                        |
| The parameter helpers (`omit_none`, `to_iso`, `to_list`, ...)        | `tests/core/test_params.py`          |

Do not test what is not the wrapper's: how Tines behaves, what its replies contain, or what `httpx`
does. The suite stays small because every test is about something tapi does.

## When a case is not enough

Add a separate test only for behavior that a case cannot show, such as a new helper in `core`, or a
method that does something with a reply. A case always receives a `200` with `{}`, so a test that
needs a particular reply mocks it itself. Use the `tines` and `router` fixtures:

```python
def test_a_call_through_the_client_authenticates_and_returns_the_reply(tines, router, api_key):
    route = router.get("/api/v1/info").mock(return_value=httpx.Response(200, json={"stack": {}}))

    response = tines.info.get()

    assert response.data == {"stack": {}}
    assert route.calls.last.request.headers["x-user-token"] == api_key
```

For a function with several inputs and outputs, parametrize and give each row an `id`:

```python
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(datetime(2026, 1, 2, 3, 4, 5), "2026-01-02T03:04:05+00:00", id="naive is utc"),
        pytest.param("2026-01-02T03:04:05Z", "2026-01-02T03:04:05Z", id="string unchanged"),
    ],
)
def test_to_iso(value, expected):
    assert to_iso(value=value) == expected
```

Style of a separate test:

- Name it after the behavior, as a sentence: `test_non_2xx_replies_are_returned_not_raised_nor_retried`.
- Test one behavior, and separate the setup, the call and the assertions with blank lines.
- Call tapi code with named arguments, as everywhere else: `to_iso(value=...)`.
- Do not write comments. The name of the test and the names of the values should explain it.

## Fixtures

All of them are in `tests/conftest.py`.

| Fixture                | What it gives you                                                                     |
| ---------------------- | ------------------------------------------------------------------------------------- |
| `router`               | A `respx` router for `https://acme.tines.com`. Mock a route with `router.get(path)`.  |
| `tines`                | A `Tines` client for that tenant, closed after the test.                              |
| `transport`            | A `Transport` for the same tenant, for tests of the core.                             |
| `api_key`              | The fake API key the client and the transport use.                                    |
| `base_url`             | `https://acme.tines.com`.                                                             |
| `isolated_environment` | Automatic. Removes `TINES_TENANT_DOMAIN` and `TINES_API_KEY` from the environment.    |

A test that needs those variables sets them with `monkeypatch.setenv`.

## Live tests

The mocked tests show that tapi sends what its author meant to send. They cannot show that Tines
agrees: the Tines docs, its OpenAPI document and the server do not always match, and a server that
ignores a parameter looks the same as one that received it. The live tests in `tests/live/` check the
real behavior against a **dedicated test tenant**.

Never point them at a production tenant. They create and delete objects, and every write shows up in
the tenant's audit logs.

### What they are

- They are marked `live` automatically, and the default `pytest` run leaves them out
  (`-m 'not live'` in `pyproject.toml`). Nothing in a normal run, or in CI without secrets, reaches a
  tenant.
- **Read tests** (`test_read.py`) call every `list` and `get` and check the status and the shape of the
  reply: the documented key is there and is a list, the pagination details are there. They skip a
  read that the tenant's plan does not offer, and a `get` when the list is empty.
- **Write tests** (`test_tags.py`, `test_folders.py`, and so on) are marked `writes`. Each creates
  throwaway objects, reads, lists, updates and deletes them, and checks the status and the fields that
  the docs promise. They do not compare whole replies, because those change.
- Operations with real side effects, such as re-emitting an event, promoting a change request or
  inviting a user, are only covered by the mocked tests.

### Running them

The live tests read their own variables, so the `TINES_TENANT_DOMAIN` and `TINES_API_KEY` of your real
tenant can never be used by accident.

| Variable                    | Meaning                                                                          |
| --------------------------- | -------------------------------------------------------------------------------- |
| `TINES_TEST_TENANT_DOMAIN`  | The domain of the test tenant. Required for every live test.                     |
| `TINES_TEST_API_KEY`        | An API key of the test tenant. Required for every live test.                     |
| `TINES_TEST_CONFIRM_WRITES` | Must be equal to `TINES_TEST_TENANT_DOMAIN`. Without it the write tests skip.    |
| `TINES_TEST_TEAM_ID`        | Optional. The team that throwaway objects are created in. Defaults to the first standard team. |

```
$env:TINES_TEST_TENANT_DOMAIN = "your-test-tenant.tines.com"
$env:TINES_TEST_API_KEY = "..."
python -m pytest -m live
$env:TINES_TEST_CONFIRM_WRITES = $env:TINES_TEST_TENANT_DOMAIN
python -m pytest -m live
```

The first run reads only, and the write tests report that they were skipped. The second also writes.
`-m live` on the command line replaces the default `-m 'not live'`. `-m "live and not writes"` runs the
reads alone, even when the confirmation is set.

A run that is interrupted can leave throwaway objects behind. Their names start with
`tapi-live-check-`. The next run of the write tests checks for them first, stops without touching
anything and lists them, so delete them by hand and run again.

### Writing a live test

- Put a read in the tables of `test_read.py`. Put a write in the file of its module, and give the
  file `pytestmark = pytest.mark.writes`.
- Ask for the fixtures you need, all from `tests/live/conftest.py`:

  | Fixture   | What it gives you                                                                       |
  | --------- | --------------------------------------------------------------------------------------- |
  | `live`    | A `Tines` client for the test tenant. The test skips if the variables are not set.      |
  | `team_id` | The ID of the team to create objects in.                                                |
  | `cleanup` | A registry of deletions. It runs them in reverse order, even when the test fails.       |

- Name every object with `throwaway(kind="tag")`, which gives `tapi-live-check-tag-1a2b3c4d`, and
  register its deletion right after it is created, before anything else can fail:

  ```python
  created = check(reply=live.tags.create(name=name, team_id=team_id, color="red"), status=201)
  cleanup.add(description="tag", action=lambda: live.tags.delete(tag_id=created["id"]))
  ```

- `check(reply=..., status=...)` asserts the status and returns `data`. `all_items(...)` walks every
  page of a list, and `wait_until_gone(read=...)` polls until a read answers `404`, for the deletions
  that Tines carries out a moment later, such as a story's.
- Assert what the docs promise and what tapi relies on: statuses, fields you sent coming back,
  an object being in a list. Do not assert whole replies, ordering or counts.
- Skip, do not fail, when the tenant's plan lacks a feature.
- Never print secrets or tenant data. A failed `check` shows the status and the reply body, so use
  throwaway values only.

## Test data

- Use made-up values: IDs such as `17`, the tenant `acme.tines.com`, the address
  `user@example.com`. Never put a real ID, name, address or credential in a test.
- The unit tests never read a `.env` file and never contact a real tenant.
- Only the [live tests](#live-tests) reach a tenant, and only the dedicated test tenant. Take its
  credentials from the environment, never write them in a file of the project, and never print or
  commit them.

## When a test fails

| Message                                                              | Cause and fix                                                                                   |
| -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `without a case: ['tags.create', ...]`                               | A method has no case. Add the minimal and the full case.                                        |
| `not a method: [...]`                                                | A case names a target that does not exist. Check the spelling and the sub-area.                 |
| `tags.delete: parameters without a case ['team_id']`                 | No case passes that parameter. Add it to the full case.                                         |
| `a case has an empty name`                                           | A `name` is empty or only spaces. Write what the case checks, or remove the `name`.             |
| `names used twice: [('tags.list', '...')]`                           | Two cases of one method have the same `name`. Make each say what is different.                  |
| `RESPX: <Request('GET', ...)> not mocked!`                           | The method sent another verb or path than the case says. Compare the request with `route`.      |
| An assertion on the query string or the body                         | The method sent something other than `params` or `body`. Pytest shows both in its diff.         |
| `tags.get documents /api/v1/tags/{tag_id}, but sends ...`            | The route in the docstring and the route the code sends differ. Fix whichever is wrong.         |
| `... does not state its route on the first docstring line`           | Start the docstring with what the method does, then the route in double backticks.              |
| An offender listed by `tests/test_conventions.py`                    | A parameter is not keyword-only, is not described in `Args`, or accepts a lone string.          |

## Checking that the tests can fail

A passing table proves little if it could never fail. After writing the cases, break the module on
purpose, in a copy or by undoing it afterwards: change a verb, a path or the name of a parameter in
`src/tapi/<area>/api.py` and run the tests of the area. A case must fail each time. If one does not,
the table does not pin that detail down, so add or tighten a case.
