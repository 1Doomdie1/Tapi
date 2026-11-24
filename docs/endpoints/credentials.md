# Credentials

- **Access:** `tines.credentials`
- **Import:** `from tapi.credentials import Credentials`

The credentials that actions use. Create, read, update and delete credentials of every mode: text, JWT, OAuth, AWS, mTLS and HTTP request. Secrets are sent to Tines and never returned.

Every method returns a [`Response`](../responses.md).

## Methods

| Method | Description | Route |
| --- | --- | --- |
| [`list`](#list) | List the credentials, optionally of a team or a folder. | `GET /api/v1/user_credentials` |
| [`get`](#get) | Get a credential. | `GET /api/v1/user_credentials/{credential_id}` |
| [`create`](#create) | Create a credential. | `POST /api/v1/user_credentials` |
| [`update`](#update) | Update a credential. | `PATCH /api/v1/user_credentials/{credential_id}` |
| [`delete`](#delete) | Delete a credential. | `DELETE /api/v1/user_credentials/{credential_id}` |

## Methods breakdown

### `list`

`GET /api/v1/user_credentials`

List the credentials, optionally of a team or a folder.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `team_id` | `int` | no | — | Only credentials of this team. |
| `folder_id` | `int` | no | — | Only credentials in this folder. |
| `filter` | `CredentialFilter` | no | `UNUSED_IN_ACTIONS`, `UNRESTRICTED`, `RESTRICTED` | Which credentials to list. |
| `include_references` | `bool` | no | `True`, `False` | When true, each credential has `references`: the stories and actions that use it, limited to 100 visible actions per credential. |
| `per_page` | `int` | no | 1 to 500 | Results per page. Tines defaults to 20 and caps it at 500. |
| `page` | `int` | no | Positive integer | The page to return, starting at 1. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is an object with `user_credentials`, the credentials of the page, and `meta`, the pagination details. |
| 400 | `per_page` or `page` is not a positive integer. |
| 422 | `filter` is not a valid value. |

### `get`

`GET /api/v1/user_credentials/{credential_id}`

Get a credential.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `credential_id` | `int` | yes | — | The ID of the credential to retrieve. |
| `include_references` | `bool` | no | `True`, `False` | When true, the credential has `references`: the stories and actions that use it, limited to 500 visible actions. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the credential. |
| 404 | The credential does not exist or the key has no access to it. |

### `create`

`POST /api/v1/user_credentials`

Create a credential. `name`, `mode` and `team_id` are always needed, and `mode` decides which of the mode-specific arguments apply.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `name` | `str` | yes | — | The name of the credential. |
| `mode` | `CredentialMode` | yes | `TEXT`<br>`JWT`<br>`OAUTH`<br>`AWS`<br>`MTLS`<br>`HTTP_REQUEST_AGENT`<br>`MULTI_REQUEST` | The mode of the credential. It decides which of the mode-specific arguments apply. |
| `team_id` | `int` | yes | — | The ID of the team the credential belongs to. |
| `value` | `str` | no | — | The value of a `TEXT` credential. |
| `folder_id` | `int` | no | — | The ID of the folder to put it in. |
| `read_access` | `ReadAccess` | no | `TEAM`, `GLOBAL`, `SPECIFIC_TEAMS` | Where the credential can be used. `SPECIFIC_TEAMS` is a premium feature, and OAuth takes `TEAM` and `GLOBAL` only. |
| `shared_team_slugs` | `Sequence[str]` | no | — | The slugs of the teams that can use it. Needed for `SPECIFIC_TEAMS`. |
| `description` | `str` | no | — | A description of the credential. |
| `metadata` | `dict[str, Any]` | no | — | Key-value metadata, referenced through the `INFO` path. |
| `allowed_hosts` | `Sequence[str]` | no | — | Domains where it can be used, with wildcards. It then works in HTTP requests only. |
| `live_credential_id` | `int` | no | — | For a test credential, the ID of the live credential. |
| `expires_at` | `datetime \| str` | no | ISO 8601 string, or `datetime` | When it expires: a `datetime` or an ISO 8601 string. |
| `expiry_notifications_enabled` | `bool` | no | `True`, `False` | Whether to send expiry notifications. |
| `credential_notification_recipient_user_ids` | `Sequence[int]` | no | — | The IDs of the users who get notifications. |
| `include_references` | `bool` | no | `True`, `False` | `True` adds `references`, the stories and actions that use it. |
| `aws_authentication_type` | `AwsAuthenticationType` | no | `KEY`, `ROLE`, `INSTANCE_PROFILE` | AWS: how Tines authenticates. |
| `aws_access_key` | `str` | no | — | AWS: the access key. |
| `aws_secret_key` | `str` | no | — | AWS: the secret key. |
| `aws_assumed_role_arn` | `str` | no | — | AWS: the ARN of the role to assume. Needed for role-based access. |
| `aws_assumed_role_source_identity` | `str` | no | 2 to 64 characters | AWS: a source identity of 2 to 64 characters. |
| `use_static_external_id` | `bool` | no | `True`, `False` | AWS: whether to use the team-scoped static external ID. |
| `http_request_options` | `dict[str, Any] \| str` | no | — | HTTP request: the options of the HTTP Request action that fetches the value, as a JSON object. |
| `http_request_location_of_token` | `str` | no | — | HTTP request and multi request: where the token is in the response. |
| `http_request_secret` | `str` | no | — | HTTP request: a secret for the request, referenced as `secret`. |
| `http_request_ttl` | `int` | no | — | HTTP request and multi request: how long, in seconds, the value is kept. |
| `credential_requests` | `Sequence[dict[str, Any]]` | no | — | Multi request: two objects, each with `options` and `http_request_secret`, that run in order. |
| `jwt_algorithm` | `str` | no | — | JWT: the signing algorithm, such as `RS256`. |
| `jwt_payload` | `dict[str, Any]` | no | — | JWT: the payload, as an object. |
| `jwt_auto_generate_time_claims` | `bool` | no | `True`, `False` | JWT: whether Tines generates `iat` and `exp`. |
| `jwt_private_key` | `str` | no | — | JWT: the private key. |
| `mtls_client_certificate` | `str` | no | — | MTLS: the client certificate. |
| `mtls_client_private_key` | `str` | no | — | MTLS: the private key of the client certificate. |
| `mtls_root_certificate` | `str` | no | — | MTLS: the root certificate of the CA. |
| `oauth_url` | `str` | no | — | OAuth: the authorization URL. Needed for `authorization_code` unless `oauth_authorization_code` is sent. |
| `oauth_token_url` | `str` | no | — | OAuth: the token URL. |
| `oauth_client_id` | `str` | no | — | OAuth: the client ID. |
| `oauth_client_secret` | `str` | no | — | OAuth: the client secret. |
| `oauth_scope` | `str` | no | — | OAuth: the scopes. |
| `oauth_grant_type` | `OAuthGrantType` | no | `client_credentials`, `authorization_code` | OAuth: the grant type. |
| `oauthPkceCodeChallengeMethod` | `PkceCodeChallengeMethod` | no | `S256`, `plain` | OAuth: the PKCE code challenge method, not with `oauth_authorization_code`. Written in camel case, as Tines does. |
| `oauth_authorization_code` | `str` | no | — | OAuth: a code from your own app. Needs `oauth_redirect_uri` and the grant type `authorization_code`. |
| `oauth_redirect_uri` | `str` | no | — | OAuth: needed with, and only with, `oauth_authorization_code`. |
| `oauth_code_verifier` | `str` | no | 43 to 128 characters | OAuth: 43 to 128 characters. Only with `oauth_authorization_code`. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 201 | `data` is the credential, with a `redirect_url` for an OAuth credential that still has to be authorized. |
| 422 | A value is not valid, or an OAuth code exchange failed. |

### `update`

`PATCH /api/v1/user_credentials/{credential_id}`

Update a credential. `credential_id` and `mode` are always needed.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `credential_id` | `int` | yes | — | The ID of the credential to update. |
| `mode` | `CredentialMode` | yes | `TEXT`<br>`JWT`<br>`OAUTH`<br>`AWS`<br>`MTLS`<br>`HTTP_REQUEST_AGENT`<br>`MULTI_REQUEST` | The mode of the credential. It decides which of the mode-specific arguments apply. |
| `name` | `str` | no | — | The new name. |
| `value` | `str` | no | — | The new value of a `TEXT` credential. |
| `folder_id` | `int` | no | — | The ID of the folder to move it to. |
| `read_access` | `ReadAccess` | no | `TEAM`, `GLOBAL`, `SPECIFIC_TEAMS` | Where the credential can be used. `SPECIFIC_TEAMS` is a premium feature. |
| `shared_team_slugs` | `Sequence[str]` | no | — | The slugs of the teams that can use it. Needed for `SPECIFIC_TEAMS`. |
| `description` | `str` | no | — | The new description. |
| `metadata` | `dict[str, Any]` | no | — | Key-value metadata for HTTP requests. |
| `allowed_hosts` | `Sequence[str]` | no | — | Domains where it can be used, with wildcards. It then works in HTTP requests only. |
| `test_credential_enabled` | `bool` | no | `True`, `False` | Whether the credential has a test credential. |
| `is_test` | `bool` | no | `True`, `False` | Whether to update the test credential. Needs `test_credential_enabled`. |
| `expires_at` | `datetime \| str` | no | ISO 8601 string, or `datetime` | When it expires: a `datetime` or an ISO 8601 string. |
| `expiry_notifications_enabled` | `bool` | no | `True`, `False` | Whether to send expiry notifications. |
| `credential_notification_recipient_user_ids` | `Sequence[int]` | no | — | The IDs of the users who get notifications. |
| `include_references` | `bool` | no | `True`, `False` | `True` adds `references`, the stories and actions that use it. |
| `aws_authentication_type` | `AwsAuthenticationType` | no | `KEY`, `ROLE`, `INSTANCE_PROFILE` | AWS: how Tines authenticates. |
| `aws_access_key` | `str` | no | — | AWS: the access key. |
| `aws_secret_key` | `str` | no | — | AWS: the secret key. |
| `aws_assumed_role_arn` | `str` | no | — | AWS: the ARN of the role to assume. Needed for role-based access. |
| `aws_assumed_role_source_identity` | `str` | no | 2 to 64 characters | AWS: a source identity of 2 to 64 characters. An empty string clears it. |
| `use_static_external_id` | `bool` | no | `True`, `False` | AWS: whether to use the team-scoped static external ID. |
| `http_request_options` | `dict[str, Any] \| str` | no | — | HTTP request: the options of the HTTP Request action that fetches the value. |
| `http_request_location_of_token` | `str` | no | — | HTTP request and multi request: where the token is in the response. |
| `http_request_secret` | `str` | no | — | HTTP request: a secret for the request. |
| `http_request_ttl` | `int` | no | — | HTTP request and multi request: how long, in seconds, the value is kept. |
| `credential_requests` | `Sequence[dict[str, Any]]` | no | — | Multi request: the requests, as for `create`. |
| `jwt_algorithm` | `str` | no | — | JWT: the signing algorithm. |
| `jwt_payload` | `dict[str, Any]` | no | — | JWT: the payload, as an object. |
| `jwt_auto_generate_time_claims` | `bool` | no | `True`, `False` | JWT: whether Tines generates `iat` and `exp`. |
| `jwt_private_key` | `str` | no | — | JWT: the private key. |
| `mtls_client_certificate` | `str` | no | — | MTLS: the client certificate. |
| `mtls_client_private_key` | `str` | no | — | MTLS: the private key of the client certificate. |
| `mtls_root_certificate` | `str` | no | — | MTLS: the root certificate of the CA. |
| `oauth_url` | `str` | no | — | OAuth: the authorization URL. |
| `oauth_token_url` | `str` | no | — | OAuth: the token URL. |
| `oauth_client_id` | `str` | no | — | OAuth: the client ID. |
| `oauth_client_secret` | `str` | no | — | OAuth: the client secret. |
| `oauth_scope` | `str` | no | — | OAuth: the scopes. |
| `oauth_grant_type` | `OAuthGrantType` | no | `client_credentials`, `authorization_code` | OAuth: the grant type. |
| `oauthPkceCodeChallengeMethod` | `PkceCodeChallengeMethod` | no | `S256`, `plain` | OAuth: the PKCE code challenge method, not with `oauth_authorization_code`. Written in camel case, as Tines does. |
| `oauth_authorization_code` | `str` | no | — | OAuth: a code from your own app, to authorize the credential again. Needs `oauth_redirect_uri` and the grant type `authorization_code`. |
| `oauth_redirect_uri` | `str` | no | — | OAuth: needed with, and only with, `oauth_authorization_code`. |
| `oauth_code_verifier` | `str` | no | 43 to 128 characters | OAuth: 43 to 128 characters. Only with `oauth_authorization_code`. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 200 | `data` is the updated credential, with a `redirect_url` when an OAuth credential has to be authorized again. |
| 404 | The credential does not exist or the key has no access to it. |
| 422 | A value is not valid, or an OAuth code exchange failed. |

### `delete`

`DELETE /api/v1/user_credentials/{credential_id}`

Delete a credential.

**Arguments**

| Name | Type | Required | Values | Description |
| --- | --- | --- | --- | --- |
| `credential_id` | `int` | yes | — | The ID of the credential to delete. |

**Response codes**

| Code | Meaning |
| --- | --- |
| 204 | No data. |
| 404 | The credential does not exist or the key has no access to it. |
