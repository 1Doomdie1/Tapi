# Checking tapi against the OpenAPI documents

tapi is written by hand against an API whose documentation is not always consistent, and Tines adds
and changes routes over time. `tools/check_openapi_drift.py` compares the routes that tapi sends with
the routes in the Tines OpenAPI document, so a new, removed or renamed route shows up as a difference
and not as a surprise.

The tool is for the people who work on tapi. It is not part of the installed package.

## Running it

From the project root, with the virtual environment active:

```
python tools/check_openapi_drift.py
```

It needs the network. It downloads the OpenAPI document into memory each time and never writes it to
disk, so there is no copy of it in the repository.

| Option         | Meaning                                                                            |
| -------------- | ---------------------------------------------------------------------------------- |
| `--spec URL`   | An OpenAPI document to read. Repeat it for several. Defaults to the Stories document, `https://www.tines.com/stories/docs/api/openapi.json`, and the Cases document, `https://www.tines.com/cases/docs/api/openapi.json`. |
| `--known PATH` | The file of known differences. Defaults to `tools/openapi_known_differences.toml`. |

The exit code is `0` when there are no unexpected differences, `1` when there are, and `2` when a
document could not be read.

## What it compares

For every operation it takes the verb and the path, with each placeholder written as `{}` and without
a trailing slash, so `/api/v1/stories/{id}` and `/api/v1/stories/{story_id}` are the same route. tapi's
side is read from the first line of each method's docstring, the route that the tests already check
against what is sent.

A `PUT` in the document counts as the `PATCH` that tapi sends, because tapi updates with `PATCH`. A
`PUT` is also ignored when the document lists a `PATCH` for the same path.

It compares routes only. It does not compare parameters, allowed values or replies.

## Reading the report

```
Routes in the OpenAPI documents: 217
Routes in tapi: 101
Matched: 101
Known, not offered by tapi on purpose: 17
Known, not built yet:
  /api/v1/admin/...: 47
  ...

No unexpected differences.
```

An unexpected difference is one of these, listed under its own heading:

- **In the OpenAPI documents, missing from tapi.** A route that tapi does not send and nobody has said
  that it should not. Build it, or add it to the known differences with a reason.
- **In tapi, missing from the OpenAPI documents.** A route that tapi sends and the document does not
  list. It may be a typo, or a route that Tines has removed.
- **Known differences that no longer apply.** An entry that now says something untrue, such as an
  area that has been built since. Remove it.
- **Methods of tapi whose docstring states no route.** Fix the docstring.

## The known differences

`tools/openapi_known_differences.toml` lists the differences that are accepted, each with a reason. It
has three tables, and each entry names either one `route` or a `prefix` that covers every route below it:

```toml
[[not_offered]]
prefix = "/api/v1/agents"
reason = "A copy of the /api/v1/actions routes under their old name."

[[not_built]]
prefix = "/api/v1/admin"
reason = "The admin module is not built yet."

[[not_in_spec]]
route = "GET /api/v1/example/{id}"
reason = "Documented on the Tines pages, but not in the OpenAPI document."
```

| Table         | Meaning                                                                      |
| ------------- | ---------------------------------------------------------------------------- |
| `not_offered` | A route of the document that tapi leaves out on purpose.                     |
| `not_built`   | A route of an area that has no module yet.                                   |
| `not_in_spec` | A route of tapi that the document does not list.                             |

When you build a module, delete its `not_built` entries. The tool reminds you: it reports an entry
whose routes are all covered by tapi as no longer applying.

## What it cannot tell you

It tells you that something changed, not which side is right. The OpenAPI document is wrong in places,
and the server does not always do what either source says. Use the [live tests](testing.md#live-tests)
to find out how the server behaves.

## When to run it

Run it when you add or change a module, and before a release. Because it needs the network and the
upstream document changes by itself, it is a poor fit for every pull request. A scheduled run, such as
once a week, suits it better.
