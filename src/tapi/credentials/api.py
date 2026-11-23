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
CredentialFilter = Literal["ALL", "UNUSED_IN_ACTIONS", "UNRESTRICTED", "RESTRICTED"]
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

        The endpoint is paginated and one call returns one page.

        Args:
            team_id: Only credentials of this team.
            folder_id: Only credentials in this folder.
            filter: Only credentials matching ``UNUSED_IN_ACTIONS``, ``UNRESTRICTED`` or
                ``RESTRICTED``. Tines does not document what each value matches. The server also
                accepts ``ALL``, which neither the Tines docs nor its OpenAPI document list.
            include_references: When true, each credential has ``references``: the stories and
                actions that use it, limited to 100 visible actions per credential.
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``user_credentials``, the credentials
            of the page, and ``meta``, the pagination details.
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

        ``name``, ``mode`` and ``team_id`` are always needed. ``mode`` decides which of the
        mode-specific parameters below apply, and Tines documents each of them under its mode.
        Secrets such as ``value``, ``aws_secret_key`` and ``jwt_private_key`` are only ever sent
        to Tines and are not part of the reply.

        Args:
            name: The name of the credential.
            mode: The type of credential: ``TEXT``, ``JWT``, ``OAUTH``, ``AWS``, ``MTLS``,
                ``HTTP_REQUEST_AGENT`` or ``MULTI_REQUEST``.
            team_id: The ID of the team the credential belongs to.
            value: The value of a ``TEXT`` credential.
            folder_id: The ID of the folder to put the credential in.
            read_access: Where the credential can be used: ``TEAM`` (the default), ``GLOBAL`` or
                ``SPECIFIC_TEAMS``, which is a premium feature. OAuth credentials accept only
                ``TEAM`` and ``GLOBAL``.
            shared_team_slugs: The slugs of the teams that can use the credential. Needed to set
                ``read_access`` to ``SPECIFIC_TEAMS``.
            description: A description of the credential. Tines defaults to an empty string.
            metadata: Key/value metadata that can be referenced through the ``INFO`` path.
            allowed_hosts: Domains where the credential can be used. The credential can only be
                used in HTTP requests, and domain matching supports wildcards.
            live_credential_id: For a test credential used in the TEST mode of change control, the
                ID of the live credential that it corresponds to.
            expires_at: When the credential expires, as a ``datetime`` or an ISO 8601 string. A
                datetime without a timezone is treated as UTC.
            expiry_notifications_enabled: Whether to send expiry notifications. Tines defaults to
                false.
            credential_notification_recipient_user_ids: The IDs of the users who receive
                credential notifications, such as expiry notifications.
            include_references: When true, the credential has ``references``: the stories and
                actions that use it, limited to 500 visible actions.
            aws_authentication_type: AWS credentials only: ``KEY``, ``ROLE`` or
                ``INSTANCE_PROFILE``.
            aws_access_key: AWS credentials only: the access key from your AWS security
                credentials.
            aws_secret_key: AWS credentials only: the secret from your AWS security credentials.
            aws_assumed_role_arn: AWS credentials only: the ARN of the role to assume, such as
                ``arn:aws:iam::123456789012:role/write-access-role``. Required for role-based
                access.
            aws_assumed_role_source_identity: AWS credentials only: a source identity of 2 to 64
                characters, made of letters, numbers, underscores and ``+=,.@-``. The IAM policies
                it needs are described in the Tines documentation.
            use_static_external_id: AWS credentials only: whether to use the team-scoped static
                external ID.
            http_request_options: HTTP request credentials only: the options of the HTTP Request
                action that fetches the credential, as a JSON object. Tines' create page says a
                JSON object and its update page says a JSON string, and tapi sends what it is
                given.
            http_request_location_of_token: HTTP request and multi request credentials only: where
                the token is in the response.
            http_request_secret: HTTP request credentials only: a secret to save for the request.
                The request options can reference it as ``secret``.
            http_request_ttl: HTTP request and multi request credentials only: how long, in
                seconds, the fetched value is kept.
            credential_requests: Multi request credentials only: the HTTP requests that fetch the
                credential value. Two objects, each with an ``options`` key (the options of an HTTP
                Request action) and an ``http_request_secret`` key. They run in the given order.
            jwt_algorithm: JWT credentials only: the algorithm that signs the JWT, such as
                ``RS256``.
            jwt_payload: JWT credentials only: the payload of the JWT, as an object.
            jwt_auto_generate_time_claims: JWT credentials only: whether Tines generates the
                ``iat`` and ``exp`` claims.
            jwt_private_key: JWT credentials only: the private key that signs the JWT.
            mtls_client_certificate: MTLS credentials only: the certificate that the CA issued for
                this client.
            mtls_client_private_key: MTLS credentials only: the private key of the client
                certificate.
            mtls_root_certificate: MTLS credentials only: the root certificate of the CA that is
                responsible for the signatures.
            oauth_url: OAuth credentials only: your app's OAuth authorization URL. Required when
                ``oauth_grant_type`` is ``authorization_code``, unless you send
                ``oauth_authorization_code``.
            oauth_token_url: OAuth credentials only: your app's OAuth token URL.
            oauth_client_id: OAuth credentials only: your app's client ID.
            oauth_client_secret: OAuth credentials only: your app's client secret.
            oauth_scope: OAuth credentials only: one or more scope values for the parts of the
                user's account you want to access.
            oauth_grant_type: OAuth credentials only: ``client_credentials`` or
                ``authorization_code``.
            oauthPkceCodeChallengeMethod: OAuth credentials only: ``S256`` or ``plain``. It cannot
                be used with ``oauth_authorization_code``; send ``oauth_code_verifier`` instead.
                The Tines documentation spells this name in camel case, and tapi sends it as
                written.
            oauth_authorization_code: OAuth credentials only: an authorization code that your own
                OAuth app got from the provider. Tines exchanges it for tokens instead of
                returning a ``redirect_url``. It needs ``oauth_redirect_uri``, and
                ``oauth_grant_type`` must be ``authorization_code``.
            oauth_redirect_uri: OAuth credentials only: required with, and only accepted with,
                ``oauth_authorization_code``.
            oauth_code_verifier: OAuth credentials only: 43 to 128 characters from letters,
                numbers and ``-._~``. Only accepted with ``oauth_authorization_code``.

        Returns:
            A ``Response`` whose ``data`` is the credential, with a 201 status. For an OAuth
            credential that still has to be authorized, ``data`` also has a ``redirect_url``. If
            the exchange of ``oauth_authorization_code`` fails, Tines does not create the
            credential and answers with a 422.
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

        ``credential_id`` and ``mode`` are always needed. Only the other parameters you give are
        sent. A parameter left as ``None`` is not sent, so tapi cannot set a field to ``null``,
        and cannot move a credential to the root folder, which Tines does with an empty value.

        The Tines documentation shows this operation as ``PUT``. The OpenAPI document lists the
        same operation under ``PUT`` and ``PATCH``, and tapi uses ``PATCH``.

        Args:
            credential_id: The ID of the credential to update.
            mode: The type of credential: ``TEXT``, ``JWT``, ``OAUTH``, ``AWS``, ``MTLS``,
                ``HTTP_REQUEST_AGENT`` or ``MULTI_REQUEST``. The OpenAPI document requires it.
            name: The new name of the credential.
            value: The new value of a ``TEXT`` credential.
            folder_id: The ID of the folder to move the credential to.
            read_access: Where the credential can be used: ``TEAM``, ``GLOBAL`` or
                ``SPECIFIC_TEAMS``, which is a premium feature.
            shared_team_slugs: The slugs of the teams that can use the credential. Needed to set
                ``read_access`` to ``SPECIFIC_TEAMS``.
            description: The new description of the credential.
            metadata: Key/value metadata for use in HTTP requests alongside the credential value.
            allowed_hosts: Domains where the credential can be used. The credential can only be
                used in HTTP requests, and domain matching supports wildcards.
            test_credential_enabled: Whether the credential is enabled for using a test
                credential.
            is_test: Whether the test credential is the one to update. It requires
                ``test_credential_enabled`` to be true and a test credential to exist.
            expires_at: When the credential expires, as a ``datetime`` or an ISO 8601 string. A
                datetime without a timezone is treated as UTC.
            expiry_notifications_enabled: Whether to send expiry notifications.
            credential_notification_recipient_user_ids: The IDs of the users who receive
                credential notifications, such as expiry notifications.
            include_references: When true, the credential has ``references``: the stories and
                actions that use it, limited to 500 visible actions.
            aws_authentication_type: AWS credentials only: ``KEY``, ``ROLE`` or
                ``INSTANCE_PROFILE``.
            aws_access_key: AWS credentials only: the access key from your AWS security
                credentials.
            aws_secret_key: AWS credentials only: the secret from your AWS security credentials.
            aws_assumed_role_arn: AWS credentials only: the ARN of the role to assume. Required
                for role-based access.
            aws_assumed_role_source_identity: AWS credentials only: a source identity of 2 to 64
                characters. Leaving it out keeps the current value, and an empty string clears it.
            use_static_external_id: AWS credentials only: whether to use the team-scoped static
                external ID.
            http_request_options: HTTP request credentials only: the options of the HTTP Request
                action that fetches the credential. Tines' update page says a JSON string and its
                create page says a JSON object, and tapi sends what it is given.
            http_request_location_of_token: HTTP request and multi request credentials only: where
                the token is in the response.
            http_request_secret: HTTP request credentials only: a secret to save for the request.
            http_request_ttl: HTTP request and multi request credentials only: how long, in
                seconds, the fetched value is kept. Tines documents that not sending it during an
                update sets it to ``null``.
            credential_requests: Multi request credentials only: the HTTP requests that fetch the
                credential value, as described for ``create``.
            jwt_algorithm: JWT credentials only: the algorithm that signs the JWT.
            jwt_payload: JWT credentials only: the payload of the JWT, as an object.
            jwt_auto_generate_time_claims: JWT credentials only: whether Tines generates the
                ``iat`` and ``exp`` claims.
            jwt_private_key: JWT credentials only: the private key that signs the JWT.
            mtls_client_certificate: MTLS credentials only: the certificate that the CA issued for
                this client.
            mtls_client_private_key: MTLS credentials only: the private key of the client
                certificate.
            mtls_root_certificate: MTLS credentials only: the root certificate of the CA that is
                responsible for the signatures.
            oauth_url: OAuth credentials only: your app's OAuth authorization URL.
            oauth_token_url: OAuth credentials only: your app's OAuth token URL.
            oauth_client_id: OAuth credentials only: your app's client ID.
            oauth_client_secret: OAuth credentials only: your app's client secret.
            oauth_scope: OAuth credentials only: one or more scope values for the parts of the
                user's account you want to access.
            oauth_grant_type: OAuth credentials only: ``client_credentials`` or
                ``authorization_code``.
            oauthPkceCodeChallengeMethod: OAuth credentials only: ``S256`` or ``plain``. It cannot
                be used with ``oauth_authorization_code``. The Tines documentation spells this
                name in camel case, and tapi sends it as written.
            oauth_authorization_code: OAuth credentials only: an authorization code from your own
                OAuth app, used to authorize the credential again. It needs
                ``oauth_redirect_uri``, and ``oauth_grant_type`` must be ``authorization_code``.
            oauth_redirect_uri: OAuth credentials only: required with, and only accepted with,
                ``oauth_authorization_code``.
            oauth_code_verifier: OAuth credentials only: 43 to 128 characters from letters,
                numbers and ``-._~``. Only accepted with ``oauth_authorization_code``.

        Returns:
            A ``Response`` whose ``data`` is the updated credential. When a change to an OAuth
            credential requires authorizing it again, ``data`` also has a ``redirect_url``.
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
