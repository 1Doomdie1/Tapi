# Documentation

This is the overview of the tapi documentation. The pages are Markdown files that are read on
GitHub or in an editor. The docstring of every method documents its arguments and what `Response.data`
holds, so the pages here cover what a docstring cannot: how the pieces fit together, and the routes
of each module.

## Using tapi

Start here if you want to call the Tines API.

| Page                                  | Covers                                                                   |
| ------------------------------------- | ------------------------------------------------------------------------ |
| [Getting started](getting-started.md) | Installing tapi, creating a client and closing it.                       |
| [Responses](responses.md)             | The `Response` class, how a body is decoded, and what a non-2xx reply is. |
| [Pagination](pagination.md)           | The paging parameters, the `meta` object and walking the pages yourself. |
| [Endpoints](endpoints/README.md)      | Each module and sub-endpoint: its methods, arguments and response codes. |

## How tapi is built

Read these before you change the code or add a module.

| Page                              | Covers                                                                        |
| --------------------------------- | ----------------------------------------------------------------------------- |
| [Architecture](architecture.md)   | The layers, the life of a request, what a module consists of and the design decisions. |
| [Conventions](conventions.md)     | Named arguments, parameters, methods, docstrings and comments.                |

## Testing and keeping tapi correct

| Page                                | Covers                                                                         |
| ----------------------------------- | ------------------------------------------------------------------------------ |
| [Testing](testing.md)               | The mocked tests, how to write the tests of a module, and the opt-in live tests. |
| [OpenAPI drift](openapi-drift.md)   | Comparing the routes in the docstrings with the Tines OpenAPI documents.       |

## Where to start

- To make a first call: [Getting started](getting-started.md), then [Responses](responses.md).
- To find the method for a Tines route: [Endpoints](endpoints/README.md).
- To add a module: [Architecture](architecture.md), [Conventions](conventions.md) and
  [Testing](testing.md), in that order.
