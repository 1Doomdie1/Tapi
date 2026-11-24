from collections.abc import Sequence
from datetime import datetime
from typing import Any, Literal

from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_iso, to_list

CredentialMode = Literal[
    "TEXT",
    "JWT",
    "OAUTH",
    "AWS",
    "MTLS",
    "HTTP_REQUEST_AGENT",
    "MULTI_REQUEST",
]
ReadAccess = Literal["TEAM", "GLOBAL", "SPECIFIC_TEAMS"]
CredentialFilter = Literal["UNUSED_IN_ACTIONS", "UNRESTRICTED", "RESTRICTED"]
AwsAuthenticationType = Literal["KEY", "ROLE", "INSTANCE_PROFILE"]
OAuthGrantType = Literal["client_credentials", "authorization_code"]
PkceCodeChallengeMethod = Literal["S256", "plain"]


class Credentials:
    """Credentials, available as ``tines.credentials``.

    A credential, as returned by every method except ``delete``, has ``id``, ``name``, ``mode``,
    ``team_id``, ``folder_id``, ``read_access``, ``shared_team_slugs``, ``slug``, ``created_at``,
    ``updated_at``, ``description``, ``allowed_hosts``, ``metadata``, ``restriction_type``,
    ``test_credential_enabled``, ``test_credential``, ``owner``, ``expires_at``,
    ``expiry_notifications_enabled`` and ``credential_notification_recipient_user_ids``. AWS
    credentials also have ``aws_authentication_type``, ``aws_assumed_role_external_id``,
    ``aws_assumed_role_source_identity`` and ``use_static_external_id``. ``references`` is present
    when ``include_references`` is true. None of these fields holds a secret value.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        team_id: int | None = None,
        folder_id: int | None = None,
        filter: CredentialFilter | None = None,
        include_references: bool | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List credentials. ``GET /api/v1/user_credentials``

        Args:
            team_id: Only credentials of this team.
            folder_id: Only credentials in this folder.
            filter: Only credentials matching ``UNUSED_IN_ACTIONS``, ``UNRESTRICTED`` or
                ``RESTRICTED``.
            include_references: When true, each credential has ``references``: the stories and
                actions that use it, limited to 100 visible actions per credential.
            per_page: The number of results per page.
            page: The page to return, starting at 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``user_credentials``, the credentials of
            the page, and ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/user_credentials",
            params=omit_none(
                values={
                    "team_id": team_id,
                    "folder_id": folder_id,
                    "filter": filter,
                    "include_references": include_references,
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )

    def get(
        self,
        *,
        credential_id: int,
        include_references: bool | None = None,
    ) -> Response:
        """Get a credential. ``GET /api/v1/user_credentials/{credential_id}``

        Args:
            credential_id: The ID of the credential to retrieve.
            include_references: When true, the credential has ``references``: the stories and
                actions that use it, limited to 500 visible actions.

        Returns:
            A ``Response`` whose ``data`` is the credential.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/user_credentials/{credential_id}",
            params=omit_none(values={"include_references": include_references}),
        )

    def create(
        self,
        *,
        name: str,
        mode: CredentialMode,
        team_id: int,
        value: str | None = None,
        folder_id: int | None = None,
        read_access: ReadAccess | None = None,
        shared_team_slugs: Sequence[str] | None = None,
        description: str | None = None,
        metadata: dict[str, Any] | None = None,
        allowed_hosts: Sequence[str] | None = None,
        live_credential_id: int | None = None,
        expires_at: datetime | str | None = None,
        expiry_notifications_enabled: bool | None = None,
        credential_notification_recipient_user_ids: Sequence[int] | None = None,
        include_references: bool | None = None,
        aws_authentication_type: AwsAuthenticationType | None = None,
        aws_access_key: str | None = None,
        aws_secret_key: str | None = None,
        aws_assumed_role_arn: str | None = None,
        aws_assumed_role_source_identity: str | None = None,
        use_static_external_id: bool | None = None,
        http_request_options: dict[str, Any] | str | None = None,
        http_request_location_of_token: str | None = None,
        http_request_secret: str | None = None,
        http_request_ttl: int | None = None,
        credential_requests: Sequence[dict[str, Any]] | None = None,
        jwt_algorithm: str | None = None,
        jwt_payload: dict[str, Any] | None = None,
        jwt_auto_generate_time_claims: bool | None = None,
        jwt_private_key: str | None = None,
        mtls_client_certificate: str | None = None,
        mtls_client_private_key: str | None = None,
        mtls_root_certificate: str | None = None,
        oauth_url: str | None = None,
        oauth_token_url: str | None = None,
        oauth_client_id: str | None = None,
        oauth_client_secret: str | None = None,
        oauth_scope: str | None = None,
        oauth_grant_type: OAuthGrantType | None = None,
        oauthPkceCodeChallengeMethod: PkceCodeChallengeMethod | None = None,
        oauth_authorization_code: str | None = None,
        oauth_redirect_uri: str | None = None,
        oauth_code_verifier: str | None = None,
    ) -> Response:
        """Create a credential. ``POST /api/v1/user_credentials``

        ``name``, ``mode`` and ``team_id`` are always needed, and ``mode`` decides which of the
        mode-specific parameters apply. Secrets are sent to Tines and never returned.

        Args:
            name: The name of the credential.
            mode: ``TEXT``, ``JWT``, ``OAUTH``, ``AWS``, ``MTLS``, ``HTTP_REQUEST_AGENT`` or
                ``MULTI_REQUEST``.
            team_id: The ID of the team the credential belongs to.
            value: The value of a ``TEXT`` credential.
            folder_id: The ID of the folder to put it in.
            read_access: ``TEAM``, ``GLOBAL`` or ``SPECIFIC_TEAMS`` (premium). OAuth takes ``TEAM``
                and ``GLOBAL`` only.
            shared_team_slugs: The slugs of the teams that can use it. Needed for
                ``SPECIFIC_TEAMS``.
            description: A description of the credential.
            metadata: Key-value metadata, referenced through the ``INFO`` path.
            allowed_hosts: Domains where it can be used, with wildcards. It then works in HTTP
                requests only.
            live_credential_id: For a test credential, the ID of the live credential.
            expires_at: When it expires: a ``datetime`` or an ISO 8601 string.
            expiry_notifications_enabled: Whether to send expiry notifications.
            credential_notification_recipient_user_ids: The IDs of the users who get notifications.
            include_references: ``True`` adds ``references``, the stories and actions that use it.
            aws_authentication_type: AWS: ``KEY``, ``ROLE`` or ``INSTANCE_PROFILE``.
            aws_access_key: AWS: the access key.
            aws_secret_key: AWS: the secret key.
            aws_assumed_role_arn: AWS: the ARN of the role to assume. Needed for role-based access.
            aws_assumed_role_source_identity: AWS: a source identity of 2 to 64 characters.
            use_static_external_id: AWS: whether to use the team-scoped static external ID.
            http_request_options: HTTP request: the options of the HTTP Request action that fetches
                the value, as a JSON object.
            http_request_location_of_token: HTTP request and multi request: where the token is in
                the response.
            http_request_secret: HTTP request: a secret for the request, referenced as ``secret``.
            http_request_ttl: HTTP request and multi request: how long, in seconds, the value is
                kept.
            credential_requests: Multi request: two objects, each with ``options`` and
                ``http_request_secret``, that run in order.
            jwt_algorithm: JWT: the signing algorithm, such as ``RS256``.
            jwt_payload: JWT: the payload, as an object.
            jwt_auto_generate_time_claims: JWT: whether Tines generates ``iat`` and ``exp``.
            jwt_private_key: JWT: the private key.
            mtls_client_certificate: MTLS: the client certificate.
            mtls_client_private_key: MTLS: the private key of the client certificate.
            mtls_root_certificate: MTLS: the root certificate of the CA.
            oauth_url: OAuth: the authorization URL. Needed for ``authorization_code`` unless
                ``oauth_authorization_code`` is sent.
            oauth_token_url: OAuth: the token URL.
            oauth_client_id: OAuth: the client ID.
            oauth_client_secret: OAuth: the client secret.
            oauth_scope: OAuth: the scopes.
            oauth_grant_type: OAuth: ``client_credentials`` or ``authorization_code``.
            oauthPkceCodeChallengeMethod: OAuth: ``S256`` or ``plain``, not with
                ``oauth_authorization_code``. Written in camel case, as Tines does.
            oauth_authorization_code: OAuth: a code from your own app. Needs ``oauth_redirect_uri``
                and the grant type ``authorization_code``.
            oauth_redirect_uri: OAuth: needed with, and only with, ``oauth_authorization_code``.
            oauth_code_verifier: OAuth: 43 to 128 characters. Only with
                ``oauth_authorization_code``.

        Returns:
            A ``Response`` with a 201 status whose ``data`` is the credential, with a
            ``redirect_url`` for an OAuth credential that still has to be authorized.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/user_credentials",
            params=omit_none(values={"include_references": include_references}),
            json=omit_none(
                values={
                    "name": name,
                    "mode": mode,
                    "team_id": team_id,
                    "value": value,
                    "folder_id": folder_id,
                    "read_access": read_access,
                    "shared_team_slugs": to_list(values=shared_team_slugs),
                    "description": description,
                    "metadata": metadata,
                    "allowed_hosts": to_list(values=allowed_hosts),
                    "live_credential_id": live_credential_id,
                    "expires_at": to_iso(value=expires_at),
                    "expiry_notifications_enabled": expiry_notifications_enabled,
                    "credential_notification_recipient_user_ids": to_list(
                        values=credential_notification_recipient_user_ids
                    ),
                    "aws_authentication_type": aws_authentication_type,
                    "aws_access_key": aws_access_key,
                    "aws_secret_key": aws_secret_key,
                    "aws_assumed_role_arn": aws_assumed_role_arn,
                    "aws_assumed_role_source_identity": aws_assumed_role_source_identity,
                    "use_static_external_id": use_static_external_id,
                    "http_request_options": http_request_options,
                    "http_request_location_of_token": http_request_location_of_token,
                    "http_request_secret": http_request_secret,
                    "http_request_ttl": http_request_ttl,
                    "credential_requests": to_list(values=credential_requests),
                    "jwt_algorithm": jwt_algorithm,
                    "jwt_payload": jwt_payload,
                    "jwt_auto_generate_time_claims": jwt_auto_generate_time_claims,
                    "jwt_private_key": jwt_private_key,
                    "mtls_client_certificate": mtls_client_certificate,
                    "mtls_client_private_key": mtls_client_private_key,
                    "mtls_root_certificate": mtls_root_certificate,
                    "oauth_url": oauth_url,
                    "oauth_token_url": oauth_token_url,
                    "oauth_client_id": oauth_client_id,
                    "oauth_client_secret": oauth_client_secret,
                    "oauth_scope": oauth_scope,
                    "oauth_grant_type": oauth_grant_type,
                    "oauthPkceCodeChallengeMethod": oauthPkceCodeChallengeMethod,
                    "oauth_authorization_code": oauth_authorization_code,
                    "oauth_redirect_uri": oauth_redirect_uri,
                    "oauth_code_verifier": oauth_code_verifier,
                }
            ),
        )

    def update(
        self,
        *,
        credential_id: int,
        mode: CredentialMode,
        name: str | None = None,
        value: str | None = None,
        folder_id: int | None = None,
        read_access: ReadAccess | None = None,
        shared_team_slugs: Sequence[str] | None = None,
        description: str | None = None,
        metadata: dict[str, Any] | None = None,
        allowed_hosts: Sequence[str] | None = None,
        test_credential_enabled: bool | None = None,
        is_test: bool | None = None,
        expires_at: datetime | str | None = None,
        expiry_notifications_enabled: bool | None = None,
        credential_notification_recipient_user_ids: Sequence[int] | None = None,
        include_references: bool | None = None,
        aws_authentication_type: AwsAuthenticationType | None = None,
        aws_access_key: str | None = None,
        aws_secret_key: str | None = None,
        aws_assumed_role_arn: str | None = None,
        aws_assumed_role_source_identity: str | None = None,
        use_static_external_id: bool | None = None,
        http_request_options: dict[str, Any] | str | None = None,
        http_request_location_of_token: str | None = None,
        http_request_secret: str | None = None,
        http_request_ttl: int | None = None,
        credential_requests: Sequence[dict[str, Any]] | None = None,
        jwt_algorithm: str | None = None,
        jwt_payload: dict[str, Any] | None = None,
        jwt_auto_generate_time_claims: bool | None = None,
        jwt_private_key: str | None = None,
        mtls_client_certificate: str | None = None,
        mtls_client_private_key: str | None = None,
        mtls_root_certificate: str | None = None,
        oauth_url: str | None = None,
        oauth_token_url: str | None = None,
        oauth_client_id: str | None = None,
        oauth_client_secret: str | None = None,
        oauth_scope: str | None = None,
        oauth_grant_type: OAuthGrantType | None = None,
        oauthPkceCodeChallengeMethod: PkceCodeChallengeMethod | None = None,
        oauth_authorization_code: str | None = None,
        oauth_redirect_uri: str | None = None,
        oauth_code_verifier: str | None = None,
    ) -> Response:
        """Update a credential. ``PATCH /api/v1/user_credentials/{credential_id}``

        ``credential_id`` and ``mode`` are always needed. A parameter left as ``None`` is not sent,
        so a field cannot be set to ``null``.

        Args:
            credential_id: The ID of the credential to update.
            mode: ``TEXT``, ``JWT``, ``OAUTH``, ``AWS``, ``MTLS``, ``HTTP_REQUEST_AGENT`` or
                ``MULTI_REQUEST``.
            name: The new name.
            value: The new value of a ``TEXT`` credential.
            folder_id: The ID of the folder to move it to.
            read_access: ``TEAM``, ``GLOBAL`` or ``SPECIFIC_TEAMS`` (premium).
            shared_team_slugs: The slugs of the teams that can use it. Needed for
                ``SPECIFIC_TEAMS``.
            description: The new description.
            metadata: Key-value metadata for HTTP requests.
            allowed_hosts: Domains where it can be used, with wildcards. It then works in HTTP
                requests only.
            test_credential_enabled: Whether the credential has a test credential.
            is_test: Whether to update the test credential. Needs ``test_credential_enabled``.
            expires_at: When it expires: a ``datetime`` or an ISO 8601 string.
            expiry_notifications_enabled: Whether to send expiry notifications.
            credential_notification_recipient_user_ids: The IDs of the users who get notifications.
            include_references: ``True`` adds ``references``, the stories and actions that use it.
            aws_authentication_type: AWS: ``KEY``, ``ROLE`` or ``INSTANCE_PROFILE``.
            aws_access_key: AWS: the access key.
            aws_secret_key: AWS: the secret key.
            aws_assumed_role_arn: AWS: the ARN of the role to assume. Needed for role-based access.
            aws_assumed_role_source_identity: AWS: a source identity of 2 to 64 characters. An empty
                string clears it.
            use_static_external_id: AWS: whether to use the team-scoped static external ID.
            http_request_options: HTTP request: the options of the HTTP Request action that fetches
                the value.
            http_request_location_of_token: HTTP request and multi request: where the token is in
                the response.
            http_request_secret: HTTP request: a secret for the request.
            http_request_ttl: HTTP request and multi request: how long, in seconds, the value is
                kept.
            credential_requests: Multi request: the requests, as for ``create``.
            jwt_algorithm: JWT: the signing algorithm.
            jwt_payload: JWT: the payload, as an object.
            jwt_auto_generate_time_claims: JWT: whether Tines generates ``iat`` and ``exp``.
            jwt_private_key: JWT: the private key.
            mtls_client_certificate: MTLS: the client certificate.
            mtls_client_private_key: MTLS: the private key of the client certificate.
            mtls_root_certificate: MTLS: the root certificate of the CA.
            oauth_url: OAuth: the authorization URL.
            oauth_token_url: OAuth: the token URL.
            oauth_client_id: OAuth: the client ID.
            oauth_client_secret: OAuth: the client secret.
            oauth_scope: OAuth: the scopes.
            oauth_grant_type: OAuth: ``client_credentials`` or ``authorization_code``.
            oauthPkceCodeChallengeMethod: OAuth: ``S256`` or ``plain``, not with
                ``oauth_authorization_code``. Written in camel case, as Tines does.
            oauth_authorization_code: OAuth: a code from your own app, to authorize the credential
                again. Needs ``oauth_redirect_uri`` and the grant type ``authorization_code``.
            oauth_redirect_uri: OAuth: needed with, and only with, ``oauth_authorization_code``.
            oauth_code_verifier: OAuth: 43 to 128 characters. Only with
                ``oauth_authorization_code``.

        Returns:
            A ``Response`` whose ``data`` is the updated credential, with a ``redirect_url`` when an
            OAuth credential has to be authorized again.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v1/user_credentials/{credential_id}",
            params=omit_none(values={"include_references": include_references}),
            json=omit_none(
                values={
                    "mode": mode,
                    "name": name,
                    "value": value,
                    "folder_id": folder_id,
                    "read_access": read_access,
                    "shared_team_slugs": to_list(values=shared_team_slugs),
                    "description": description,
                    "metadata": metadata,
                    "allowed_hosts": to_list(values=allowed_hosts),
                    "test_credential_enabled": test_credential_enabled,
                    "is_test": is_test,
                    "expires_at": to_iso(value=expires_at),
                    "expiry_notifications_enabled": expiry_notifications_enabled,
                    "credential_notification_recipient_user_ids": to_list(
                        values=credential_notification_recipient_user_ids
                    ),
                    "aws_authentication_type": aws_authentication_type,
                    "aws_access_key": aws_access_key,
                    "aws_secret_key": aws_secret_key,
                    "aws_assumed_role_arn": aws_assumed_role_arn,
                    "aws_assumed_role_source_identity": aws_assumed_role_source_identity,
                    "use_static_external_id": use_static_external_id,
                    "http_request_options": http_request_options,
                    "http_request_location_of_token": http_request_location_of_token,
                    "http_request_secret": http_request_secret,
                    "http_request_ttl": http_request_ttl,
                    "credential_requests": to_list(values=credential_requests),
                    "jwt_algorithm": jwt_algorithm,
                    "jwt_payload": jwt_payload,
                    "jwt_auto_generate_time_claims": jwt_auto_generate_time_claims,
                    "jwt_private_key": jwt_private_key,
                    "mtls_client_certificate": mtls_client_certificate,
                    "mtls_client_private_key": mtls_client_private_key,
                    "mtls_root_certificate": mtls_root_certificate,
                    "oauth_url": oauth_url,
                    "oauth_token_url": oauth_token_url,
                    "oauth_client_id": oauth_client_id,
                    "oauth_client_secret": oauth_client_secret,
                    "oauth_scope": oauth_scope,
                    "oauth_grant_type": oauth_grant_type,
                    "oauthPkceCodeChallengeMethod": oauthPkceCodeChallengeMethod,
                    "oauth_authorization_code": oauth_authorization_code,
                    "oauth_redirect_uri": oauth_redirect_uri,
                    "oauth_code_verifier": oauth_code_verifier,
                }
            ),
        )

    def delete(self, *, credential_id: int) -> Response:
        """Delete a credential. ``DELETE /api/v1/user_credentials/{credential_id}``

        Args:
            credential_id: The ID of the credential to delete.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(
            method="DELETE",
            path=f"/api/v1/user_credentials/{credential_id}",
        )
