# Conventions

The rules every module follows.

## Arguments are named

Every function, method and class in tapi takes keyword-only arguments, and every call names what
it passes. This applies to your own calls and to the calls inside the library:

```python
tines.info.get()
self._transport.request(method="GET", path="/api/v1/info")
```

A positional call is rejected with a `TypeError`, so the rule cannot be broken by accident:

```python
transport.request("GET", "/api/v1/info")  # TypeError
```

The rule includes identifiers that appear in a URL path, so a call on a module that takes one
looks like `tines.stories.get(story_id=42)`.

There are two exceptions. The message of tapi's own exceptions is positional
(`TinesConnectionError("...")`), and calls into the standard library, builtins and third-party
libraries follow their normal style.

Keyword arguments are written without spaces around `=`, as `ruff format` enforces:
`method="GET"`, not `method = "GET"`.

## Parameters

- Parameters are typed and named as the Tines API names them, such as `team_id` and `per_page`.
- Optional parameters default to `None` and are not sent when they are `None`. This means tapi
  cannot send an explicit `null`, so a field that Tines lets you clear with `null` cannot be
  cleared yet.
- Date and time parameters accept a `datetime` as well as an ISO 8601 string. A datetime without
  a timezone is treated as UTC.
- Array parameters, which the API names with a `[]` suffix such as `user_id[]`, take a sequence and
  use the plural of the API name: `user_ids`. A single string or mapping is rejected, because it
  would be split into characters or reduced to its keys.
- Paginated endpoints take `page` and `per_page` and return one page per call. Walking the pages is
  left to the caller. See [Pagination](pagination.md).
- There is no catch-all `**kwargs`. Every parameter a method accepts is in its signature and is
  described in its docstring.

## Methods

- A method sends exactly one request and returns the `Response`.
- Methods are named `get`, `list`, `create`, `update` and `delete` for the usual operations, and
  with a verb for anything else, such as `export` or `disable`.

## Docstrings

Docstrings use the Google style:

- The first line says what the method does and which route it calls.
- `Args` describes each parameter: what it does and which values it accepts.
- `Returns` describes what `Response.data` holds.
- `Raises` appears only where something is raised. In tapi that means configuration errors and
  `TinesConnectionError`.

The docstring is the reference for a method's parameters. The pages in
[`endpoints/`](endpoints/) map each method to its route and add whatever a reader needs beyond the
docstring.

## Comments

There are no inline comments. Names and docstrings explain what the code does, and these pages
explain why.
