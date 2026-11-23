# Responses

Every call returns a `Response` with exactly three fields. The examples on this page use
`tines.info.get()`, which is implemented, and `tines.stories.get`, which is not implemented yet
but returns a `Response` like every other module method.

| Field         | Type             | Meaning                                                       |
| ------------- | ---------------- | ------------------------------------------------------------- |
| `status_code` | `int`            | The HTTP status code.                                         |
| `data`        | `Any`            | The decoded body. See [Body decoding](#body-decoding).        |
| `headers`     | `dict[str, str]` | The response headers, with lower-cased names.                 |

A `Response` is immutable.

```python
response = tines.info.get()

response.status_code
response.data
response.headers["content-type"]
```

## Printing

`print(response)` shows the whole response as indented JSON, so a call can be inspected at a
glance:

```python
print(tines.info.get())
```

```json
{
  "status_code": 200,
  "data": {
    "stack": {
      "name": "example-stack",
      "type": "shared",
      "region": "eu-west-1",
      "egress_ips": [
        "203.0.113.10"
      ]
    }
  },
  "headers": {
    "content-type": "application/json; charset=utf-8"
  }
}
```

The example shows only one header. A real reply has more.

Binary data cannot be written as JSON, so it is printed as its size, such as `<2048 bytes>`.
`response.data` itself still holds the bytes. `repr(response)` stays on one line, which suits a
debugger or a log line.

## Status codes

Every status code is returned as a `Response`, including 4xx and 5xx. tapi never raises because of
a status code, so check `status_code` and decide what to do:

```python
response = tines.stories.get(42)

if response.status_code == 404:
    ...
elif response.status_code == 429:
    retry_after = int(response.headers["retry-after"])
```

Error payloads are decoded like any other body. Tines answers many 4xx errors with a JSON list of
messages, and a rate-limited request with a plain text message, so `data` is a `list` or a `str`
respectively.

tapi does not retry requests and does not follow redirects. A 3xx reply is returned with its
`location` header.

## Body decoding

`data` depends on the `Content-Type` of the reply:

| Reply                                                                                                  | `data`                                  |
| ------------------------------------------------------------------------------------------------------ | --------------------------------------- |
| Empty body, such as a 204                                                                              | `None`                                  |
| `application/json` or any `+json` type                                                                 | The parsed JSON                         |
| `text/*`, `application/xml`, `application/yaml`, `application/x-yaml` or any `+xml` or `+yaml` type    | A `str`                                 |
| Any other type, such as images, archives and binary downloads                                          | The raw `bytes`                         |
| No `Content-Type` header                                                                               | Parsed JSON, else UTF-8 text, else `bytes` |

Text uses the charset declared in the `Content-Type` header and defaults to UTF-8. A body that does
not match its declared type falls back to text and then to `bytes`, so no reply is ever lost.

Repeated headers are joined into one comma-separated value.

## Exceptions

Only two situations raise an exception. Both derive from `TinesError`.

| Exception                  | Raised when                                                                                                                                  |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `TinesConfigurationError`  | The tenant domain or API key is missing or invalid. Raised when the client is created.                                                       |
| `TinesConnectionError`     | No HTTP reply was received: the connection was refused or reset, DNS or TLS failed, or the request timed out. The original error is `__cause__`. |

```python
from tapi import TinesConnectionError

try:
    response = tines.info.get()
except TinesConnectionError as error:
    print(error.__cause__)
```
