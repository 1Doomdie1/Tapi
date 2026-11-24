import pytest

from tests.support import Case, assert_covers, assert_sent, case_id, wire

COMMON = {
    "value": "secret",
    "folder_id": 4,
    "read_access": "GLOBAL",
    "shared_team_slugs": ("a", "b"),
    "description": "a description",
    "metadata": {"account_domain": "https://example.com"},
    "allowed_hosts": ("*.example.com",),
    "expires_at": "2026-12-01T00:00:00Z",
    "expiry_notifications_enabled": True,
    "credential_notification_recipient_user_ids": (1, 2),
}
BY_MODE = {
    "aws_authentication_type": "ROLE",
    "aws_access_key": "access-key",
    "aws_secret_key": "secret-key",
    "aws_assumed_role_arn": "arn:aws:iam::123456789012:role/r",
    "aws_assumed_role_source_identity": "me",
    "use_static_external_id": True,
    "http_request_options": {"url": "https://example.com"},
    "http_request_location_of_token": "access_token",
    "http_request_secret": "request-secret",
    "http_request_ttl": 3600,
    "credential_requests": [{"options": {}, "http_request_secret": "a"}],
    "jwt_algorithm": "RS256",
    "jwt_payload": {"iss": "me"},
    "jwt_auto_generate_time_claims": True,
    "jwt_private_key": "pem",
    "mtls_client_certificate": "certificate",
    "mtls_client_private_key": "private-key",
    "mtls_root_certificate": "root",
    "oauth_url": "https://auth.example.com",
    "oauth_token_url": "https://token.example.com",
    "oauth_client_id": "client-id",
    "oauth_client_secret": "client-secret",
    "oauth_scope": "read write",
    "oauth_grant_type": "authorization_code",
    "oauthPkceCodeChallengeMethod": "S256",
    "oauth_authorization_code": "code",
    "oauth_redirect_uri": "https://callback.example.com",
    "oauth_code_verifier": "v" * 43,
}
LIST = {
    "team_id": 3,
    "folder_id": 4,
    "filter": "UNUSED_IN_ACTIONS",
    "include_references": True,
    "per_page": 100,
    "page": 2,
}
CREATE = {
    "name": "Slack token",
    "mode": "TEXT",
    "team_id": 1,
    **COMMON,
    "live_credential_id": 5,
    **BY_MODE,
    "include_references": True,
}
UPDATE = {
    "credential_id": 21,
    "mode": "TEXT",
    "name": "renamed",
    **COMMON,
    "test_credential_enabled": True,
    "is_test": False,
    **BY_MODE,
    "include_references": True,
}
PATH = "/api/v1/user_credentials"

CASES = [
    Case(target="credentials.list", arguments={}, route=f"GET {PATH}"),
    Case(target="credentials.list", arguments=LIST, route=f"GET {PATH}", params=LIST),
    Case(target="credentials.get", arguments={"credential_id": 21}, route=f"GET {PATH}/21"),
    Case(
        target="credentials.get",
        name="false is sent, not left out",
        arguments={"credential_id": 21, "include_references": False},
        route=f"GET {PATH}/21",
        params={"include_references": False},
    ),
    Case(
        target="credentials.create",
        arguments={"name": "Slack token", "mode": "TEXT", "team_id": 1},
        route=f"POST {PATH}",
        body={"name": "Slack token", "mode": "TEXT", "team_id": 1},
    ),
    Case(
        target="credentials.create",
        name="include_references goes in the query, the rest in the body",
        arguments=CREATE,
        route=f"POST {PATH}",
        params={"include_references": True},
        body=wire(arguments=CREATE, drop=["include_references"]),
    ),
    Case(
        target="credentials.update",
        arguments={"credential_id": 21, "mode": "TEXT"},
        route=f"PATCH {PATH}/21",
        body={"mode": "TEXT"},
    ),
    Case(
        target="credentials.update",
        name="include_references goes in the query, the rest in the body",
        arguments=UPDATE,
        route=f"PATCH {PATH}/21",
        params={"include_references": True},
        body=wire(arguments=UPDATE, drop=["credential_id", "include_references"]),
    ),
    Case(target="credentials.delete", arguments={"credential_id": 21}, route=f"DELETE {PATH}/21"),
]


@pytest.mark.parametrize("case", CASES, ids=case_id)
def test_request(tines, router, case):
    assert_sent(tines=tines, router=router, case=case)


def test_every_method_and_argument_has_a_case(tines):
    assert_covers(tines=tines, area="credentials", cases=CASES)
