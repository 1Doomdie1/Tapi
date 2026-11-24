# Providers

- **Access:** `tines.ai.providers`
- **Import:** `from tapi.ai import Providers`
- **Part of:** [AI](ai.md)

The AI providers that the tenant can use, and the models of each.

Every method returns a [`Response`](../../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the AI providers and models available to you. | `GET /api/v1/ai_providers` |

## Methods breakdown

### `list`

`GET /api/v1/ai_providers`

List the AI providers and models available to you.

**Arguments**

None.

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` has `ai_providers`. |
