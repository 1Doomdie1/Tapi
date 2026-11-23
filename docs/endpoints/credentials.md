# Credentials

Credentials hold the secrets that actions use. The module is available as `tines.credentials`, and
the class is `tapi.credentials.Credentials`. Every method returns a
[`Response`](../responses.md).

| Method                                    | HTTP route                                      |
| ----------------------------------------- | ----------------------------------------------- |
| `list(...)`                               | `GET /api/v1/user_credentials`                  |
| `get(credential_id=..., ...)`             | `GET /api/v1/user_credentials/{credential_id}`  |
| `create(name=..., mode=..., team_id=...)` | `POST /api/v1/user_credentials`                 |
| `update(credential_id=..., mode=..., ...)` | `PATCH /api/v1/user_credentials/{credential_id}` |
| `delete(credential_id=...)`               | `DELETE /api/v1/user_credentials/{credential_id}` |

All parameters are keyword-only. Parameters left as `None` are not sent. The Tines docs do not
state which key types or permissions these endpoints need, other than that `SPECIFIC_TEAMS` read
access is a premium feature. A key without access to a resource receives a 404.

## Secrets

Secrets are write-only. `value`, `aws_secret_key`, `jwt_private_key`, `oauth_client_secret` and
the other secret inputs are sent to Tines and appear in no documented field of a reply.
tapi does not log requests.

## The credential

`data` of `get`, `create` and `update` is a credential, and `list` returns a list of them under
`user_credentials`. A credential has:

| Field                                        | Meaning                                                                       |
| -------------------------------------------- | ----------------------------------------------------------------------------- |
| `id`, `name`, `slug`                         | The ID, the name and an underscored form of the name.                         |
| `mode`                                       | `TEXT`, `JWT`, `OAUTH`, `AWS`, `MTLS`, `HTTP_REQUEST_AGENT` or `MULTI_REQUEST`. |
| `team_id`, `folder_id`                       | The team and the folder. `folder_id` is `null` at the root.                   |
| `read_access`                                | Where the credential can be used: `TEAM`, `GLOBAL` or `SPECIFIC_TEAMS`.      |
| `shared_team_slugs`                          | The teams' slugs when `read_access` is `SPECIFIC_TEAMS`, otherwise empty.     |
| `description`                                | The description.                                                              |
| `allowed_hosts`                              | The domains where the credential can be used in HTTP requests.                |
| `metadata`                                   | Key/value metadata.                                                           |
| `restriction_type`                           | `RESTRICTED`, `RESTRICTED_TO_CREDENTIALS` or `UNRESTRICTED`. The meaning is not documented. |
| `test_credential_enabled`                    | Whether the credential can use a test credential.                             |
| `test_credential`                            | The test credential, with `created_at` and `updated_at`. Present only when it is enabled. |
| `owner`                                      | The owning user: `user_id`, `first_name`, `last_name` and `email`.            |
| `expires_at`, `expiry_notifications_enabled` | When it expires, or `null`, and whether expiry notifications are on.          |
| `credential_notification_recipient_user_ids` | The users who receive credential notifications.                               |
| `created_at`, `updated_at`                   | ISO 8601 timestamps.                                                          |
| `aws_authentication_type`, `aws_assumed_role_external_id`, `aws_assumed_role_source_identity`, `use_static_external_id` | AWS settings. They are `null` or false for other modes. |
| `references`                                 | Only with `include_references`. See below.                                    |

With `include_references=True`, each credential also has `references`: the stories that use it,
each as `story_id`, `team_id` and `action_ids`. Tines limits this to 100 visible actions per
credential in `list` and to 500 in `get`, `create` and `update`.

## `list()`

Paginated: one call returns one page; see [Pagination](../pagination.md). `data` holds
`user_credentials` and `meta`.

| Parameter            | Type   | Meaning                                                                        |
| -------------------- | ------ | ------------------------------------------------------------------------------ |
| `team_id`            | `int`  | Only credentials of this team.                                                 |
| `folder_id`          | `int`  | Only credentials in this folder.                                               |
| `filter`             | `str`  | `UNUSED_IN_ACTIONS`, `UNRESTRICTED`, `RESTRICTED` or `ALL`. Tines does not document what they match. |
| `include_references` | `bool` | Add `references` to each credential.                                           |
| `per_page`           | `int`  | Results per page. Tines defaults to 20.                                        |
| `page`               | `int`  | The page, starting at 1. Tines defaults to 1.                                  |

## `get()`

`credential_id` is required. `include_references` adds `references`.

## `create()`

`name`, `mode` and `team_id` are required, and the reply has a 201 status. `mode` decides which of
the mode-specific parameters apply.

| Parameter                                    | Type                | Meaning                                                              |
| -------------------------------------------- | ------------------- | -------------------------------------------------------------------- |
| `name`                                       | `str`               | The name of the credential.                                          |
| `mode`                                       | `str`               | The type of credential. See above.                                   |
| `team_id`                                    | `int`               | The team the credential belongs to.                                  |
| `value`                                      | `str`               | The value of a `TEXT` credential.                                    |
| `folder_id`                                  | `int`               | The folder to put the credential in.                                 |
| `read_access`                                | `str`               | `TEAM` (the default), `GLOBAL` or `SPECIFIC_TEAMS`. OAuth credentials accept only `TEAM` and `GLOBAL`. |
| `shared_team_slugs`                          | sequence of `str`   | The teams that can use it. Needed for `SPECIFIC_TEAMS`.              |
| `description`                                | `str`               | Defaults to an empty string.                                         |
| `metadata`                                   | `dict`              | Key/value metadata, referenced through the `INFO` path.              |
| `allowed_hosts`                              | sequence of `str`   | Domains where it can be used. Wildcards are supported.               |
| `live_credential_id`                         | `int`               | For a test credential in the TEST mode of change control: the live credential it corresponds to. |
| `expires_at`                                 | `datetime` or `str` | When it expires. A datetime without a timezone is treated as UTC.    |
| `expiry_notifications_enabled`               | `bool`              | Defaults to false.                                                   |
| `credential_notification_recipient_user_ids` | sequence of `int`   | The users who receive notifications, such as expiry notifications.   |
| `include_references`                         | `bool`              | Add `references` to the reply. Sent as a query parameter.            |

### Mode-specific parameters

The Tines docs list these under each mode, and `create` and `update` accept all of them. Tines does
not state their types or which are required, apart from what is noted here.

| Mode                 | Parameters                                                                                                         |
| -------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `AWS`                | `aws_authentication_type` (`KEY`, `ROLE` or `INSTANCE_PROFILE`), `aws_access_key`, `aws_secret_key`, `aws_assumed_role_arn` (required for role-based access), `aws_assumed_role_source_identity`, `use_static_external_id` (`bool`) |
| `HTTP_REQUEST_AGENT` | `http_request_options`, `http_request_location_of_token`, `http_request_secret`, `http_request_ttl` (seconds)     |
| `MULTI_REQUEST`      | `credential_requests` (two objects, each with `options` and `http_request_secret`, run in order), `http_request_location_of_token`, `http_request_ttl` |
| `JWT`                | `jwt_algorithm` (such as `RS256`), `jwt_payload` (`dict`), `jwt_auto_generate_time_claims` (`bool`), `jwt_private_key` |
| `MTLS`               | `mtls_client_certificate`, `mtls_client_private_key`, `mtls_root_certificate`                                      |
| `OAUTH`              | `oauth_url`, `oauth_token_url`, `oauth_client_id`, `oauth_client_secret`, `oauth_scope`, `oauth_grant_type` (`client_credentials` or `authorization_code`), `oauthPkceCodeChallengeMethod` (`S256` or `plain`), `oauth_authorization_code`, `oauth_redirect_uri`, `oauth_code_verifier` |

Notes from the Tines docs:

- `oauth_url` is required when `oauth_grant_type` is `authorization_code`, unless you send
  `oauth_authorization_code`.
- `oauth_authorization_code` is a code that your own OAuth app got from the provider. Tines
  exchanges it for tokens instead of returning a `redirect_url`. It needs `oauth_redirect_uri`
  (required with it, and only accepted with it), and the grant type must be `authorization_code`.
  If the exchange fails, Tines does not create the credential and answers with a 422.
- `oauthPkceCodeChallengeMethod` cannot be used with `oauth_authorization_code`; send
  `oauth_code_verifier` instead, which takes 43 to 128 characters from letters, numbers and `-._~`.
  The docs spell the name in camel case, and tapi sends it as written.
- `aws_assumed_role_source_identity` takes 2 to 64 characters from letters, numbers, underscores and
  `+=,.@-`, and needs `sts:SetSourceIdentity` in the IAM policies described in the Tines docs.
- An OAuth credential that still has to be authorized comes back with a `redirect_url` in `data`.

## `update()`

`credential_id` and `mode` are required. Only the other parameters you give are sent. It accepts
everything `create` accepts except `team_id` and `live_credential_id`, and also:

| Parameter                 | Type   | Meaning                                                                          |
| ------------------------- | ------ | -------------------------------------------------------------------------------- |
| `name`                    | `str`  | The new name.                                                                    |
| `test_credential_enabled` | `bool` | Whether the credential is enabled for using a test credential.                   |
| `is_test`                 | `bool` | Whether the test credential is the one to update. It needs `test_credential_enabled` to be true and a test credential to exist. |

Differences and limits to know about:

- The Tines docs show this operation as `PUT`. The OpenAPI document lists the same operation under
  `PUT` and `PATCH`, and tapi uses `PATCH`.
- The OpenAPI document requires `mode`. The Tines docs do not say whether it is required.
- Tines documents that not sending `http_request_ttl` during an update sets it to `null`.
- For `aws_assumed_role_source_identity`, leaving it out keeps the value, and an empty string
  clears it.
- Because `None` means "not sent", tapi cannot send an explicit `null`, and cannot move a credential
  to the root folder, which Tines does with an empty value.
- For OAuth credentials, changing `oauth_url`, `oauth_token_url`, `oauth_client_id`,
  `oauth_client_secret`, `oauth_scope` or `oauth_grant_type` can answer with a `redirect_url` to
  authorize the credential again. Credentials authorized with `oauth_authorization_code` never
  get one.

## `delete()`

`credential_id` is required. The reply has a 204 status and `data` is `None`.

## Errors

| Status | When                                                                                       |
| ------ | ------------------------------------------------------------------------------------------ |
| `404`  | The credential does not exist, or the key has no access to it. `data` is a list of messages. |
| `422`  | A value is invalid, such as an unknown `filter`, or an OAuth code exchange failed.         |
