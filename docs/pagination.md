# Pagination

Tines paginates endpoints that return many items. tapi never paginates for you: one call returns
one page, and you decide whether to ask for the next one.

## Parameters

Paginated methods take two keyword-only parameters:

| Parameter  | Meaning                                                                          |
| ---------- | -------------------------------------------------------------------------------- |
| `page`     | The page to return, starting at 1. Tines defaults to 1.                          |
| `per_page` | The number of results per page. Tines defaults to 20 and allows at most 500.     |

A `per_page` above 500 is not rejected: Tines caps it at 500.

## The `meta` object

A paginated reply holds the list of items and a `meta` object next to it. Both are in
`Response.data`:

| Field              | Meaning                                                              |
| ------------------ | -------------------------------------------------------------------- |
| `current_page`     | A link to the current page.                                          |
| `previous_page`    | A link to the previous page, or `null`.                              |
| `next_page`        | A link to the next page, or `null`.                                  |
| `next_page_number` | The number of the next page, or `null` on the last page.             |
| `per_page`         | The number of items per page.                                        |
| `pages`            | The number of pages.                                                 |
| `count`            | The total number of items, across all pages.                         |

## Walking the pages

Read `next_page_number` from each reply and stop when it is `null`:

```python
page = 1
while page is not None:
    response = tines.audit_logs.list(per_page=500, page=page)
    if response.status_code != 200:
        break
    for entry in response.data["audit_logs"]:
        ...
    page = response.data["meta"]["next_page_number"]
```

Each page is one request, so a long walk counts against the Tines rate limits. A page past the end
is not an error: it is answered with `200` and an empty list.

## Other styles

Not every endpoint uses page numbers. Some use cursors, with `limit` and `after` parameters. The
page of each module says which style its endpoints use.
