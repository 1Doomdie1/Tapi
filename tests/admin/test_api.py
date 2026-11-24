from datetime import UTC, datetime

import pytest

from tests.support import Case, assert_covers, assert_sent, case_id

ACTION_INPUTS = [
    {"name": "input_text", "type": "TEXT", "required": True, "default_value": "Sample text"},
    {
        "name": "format",
        "type": "OPTION",
        "description": "Output format",
        "data": {"options": ["JSON", "CSV"], "multi_select_enabled": False},
    },
]
AGENT_OPTIONS = {"mode": "extract", "matchers": [{"path": "a", "regexp": "b", "to": "c"}]}

ROLE_CASES = [
    Case(target="admin.roles.list", arguments={}, route="GET /api/v1/admin/roles"),
    Case(
        target="admin.roles.list",
        arguments={"per_page": 50, "page": 2},
        route="GET /api/v1/admin/roles",
        params={"per_page": 50, "page": 2},
    ),
    Case(
        target="admin.roles.get",
        name="a role is found by its name too",
        arguments={"role_id": "TEAM_ADMIN"},
        route="GET /api/v1/admin/roles/TEAM_ADMIN",
    ),
    Case(
        target="admin.roles.create",
        arguments={"name": "MY_ROLE", "permissions": ["STORY_CREATE"]},
        route="POST /api/v1/admin/roles",
        body={"name": "MY_ROLE", "permissions": ["STORY_CREATE"]},
    ),
    Case(
        target="admin.roles.create",
        name="a tuple of permissions is sent as a list",
        arguments={
            "name": "MY_ROLE",
            "permissions": ("STORY_CREATE", "CASE_CREATE"),
            "description": "d",
        },
        route="POST /api/v1/admin/roles",
        body={
            "name": "MY_ROLE",
            "permissions": ["STORY_CREATE", "CASE_CREATE"],
            "description": "d",
        },
    ),
    Case(
        target="admin.roles.update",
        arguments={"role_id": "123"},
        route="PATCH /api/v1/admin/roles/123",
        body={},
    ),
    Case(
        target="admin.roles.update",
        arguments={"role_id": "123", "description": "New", "permissions": ["CASE_CREATE"]},
        route="PATCH /api/v1/admin/roles/123",
        body={"description": "New", "permissions": ["CASE_CREATE"]},
    ),
    Case(
        target="admin.roles.delete",
        arguments={"role_id": "123"},
        route="DELETE /api/v1/admin/roles/123",
    ),
]

TEMPLATE_CASES = [
    Case(target="admin.templates.list", arguments={}, route="GET /api/v1/admin/templates"),
    Case(
        target="admin.templates.list",
        arguments={"search": "Test", "folder_id": 42, "per_page": 50, "page": 2},
        route="GET /api/v1/admin/templates",
        params={"search": "Test", "folder_id": 42, "per_page": 50, "page": 2},
    ),
    Case(
        target="admin.templates.get",
        arguments={"template_id": 9},
        route="GET /api/v1/admin/templates/9",
    ),
    Case(
        target="admin.templates.create",
        arguments={
            "name": "Extract",
            "agent_type": "Agents::EventTransformationAgent",
            "agent_options": AGENT_OPTIONS,
            "product": "API",
            "description": "d",
            "vendor": "Vendor",
        },
        route="POST /api/v1/admin/templates",
        body={
            "name": "Extract",
            "agent_type": "Agents::EventTransformationAgent",
            "agent_options": AGENT_OPTIONS,
            "product": "API",
            "description": "d",
            "vendor": "Vendor",
        },
    ),
    Case(
        target="admin.templates.create",
        name="every argument, with the slugs and the inputs as lists",
        arguments={
            "name": "Extract",
            "agent_type": "Agents::EventTransformationAgent",
            "agent_options": AGENT_OPTIONS,
            "product": "API",
            "description": "d",
            "vendor": "Vendor",
            "team_id": 1,
            "folder_id": 42,
            "read_access": "SPECIFIC_TEAMS",
            "shared_team_slugs": ("one", "two"),
            "action_inputs": ACTION_INPUTS,
        },
        route="POST /api/v1/admin/templates",
        body={
            "name": "Extract",
            "agent_type": "Agents::EventTransformationAgent",
            "agent_options": AGENT_OPTIONS,
            "product": "API",
            "description": "d",
            "vendor": "Vendor",
            "team_id": 1,
            "folder_id": 42,
            "read_access": "SPECIFIC_TEAMS",
            "shared_team_slugs": ["one", "two"],
            "action_inputs": ACTION_INPUTS,
        },
    ),
    Case(
        target="admin.templates.update",
        name="the six required fields are always sent, because update is a full update",
        arguments={
            "template_id": 9,
            "name": "New",
            "description": "d",
            "agent_type": "Agents::EmailAgent",
            "agent_options": AGENT_OPTIONS,
            "vendor": "Vendor",
            "product": "API",
        },
        route="PATCH /api/v1/admin/templates/9",
        body={
            "name": "New",
            "description": "d",
            "agent_type": "Agents::EmailAgent",
            "agent_options": AGENT_OPTIONS,
            "vendor": "Vendor",
            "product": "API",
        },
    ),
    Case(
        target="admin.templates.update",
        arguments={
            "template_id": 9,
            "name": "New",
            "description": "d",
            "agent_type": "email",
            "agent_options": AGENT_OPTIONS,
            "vendor": "Vendor",
            "product": "API",
            "folder_id": 42,
            "read_access": "GLOBAL",
            "shared_team_slugs": ("one",),
            "action_inputs": ACTION_INPUTS,
        },
        route="PATCH /api/v1/admin/templates/9",
        body={
            "name": "New",
            "description": "d",
            "agent_type": "email",
            "agent_options": AGENT_OPTIONS,
            "vendor": "Vendor",
            "product": "API",
            "folder_id": 42,
            "read_access": "GLOBAL",
            "shared_team_slugs": ["one"],
            "action_inputs": ACTION_INPUTS,
        },
    ),
    Case(
        target="admin.templates.delete",
        arguments={"template_id": 9},
        route="DELETE /api/v1/admin/templates/9",
    ),
    Case(
        target="admin.templates.move",
        arguments={"template_id": 9, "team_id": 2},
        route="POST /api/v1/admin/templates/9/move",
        body={"team_id": 2},
    ),
    Case(
        target="admin.templates.move",
        arguments={"template_id": 9, "team_id": 2, "folder_id": 7},
        route="POST /api/v1/admin/templates/9/move",
        body={"team_id": 2, "folder_id": 7},
    ),
]

TUNNEL_CASES = [
    Case(
        target="admin.tunnels.health",
        name="the route has tunnel in the singular",
        arguments={"tunnel_name": "my-tunnel"},
        route="GET /api/v1/admin/tunnel/my-tunnel/health",
    ),
]

USER_CASES = [
    Case(target="admin.users.list", arguments={}, route="GET /api/v1/admin/users"),
    Case(
        target="admin.users.list",
        arguments={
            "filter": "ADMIN",
            "search": "alice",
            "include": "team_memberships",
            "per_page": 50,
            "page": 2,
        },
        route="GET /api/v1/admin/users",
        params={
            "filter": "ADMIN",
            "search": "alice",
            "include": "team_memberships",
            "per_page": 50,
            "page": 2,
        },
    ),
    Case(target="admin.users.get", arguments={"user_id": 5}, route="GET /api/v1/admin/users/5"),
    Case(
        target="admin.users.get",
        name="a user is found by an email address too",
        arguments={"user_id": "alice@example.com", "include": "team_memberships"},
        route="GET /api/v1/admin/users/alice@example.com",
        params={"include": "team_memberships"},
    ),
    Case(
        target="admin.users.create",
        arguments={"email": "alice@example.com"},
        route="POST /api/v1/admin/users",
        body={"email": "alice@example.com"},
    ),
    Case(
        target="admin.users.create",
        name="false is sent, and a tuple of permissions is sent as a list",
        arguments={
            "email": "alice@example.com",
            "first_name": "Alice",
            "last_name": "Smith",
            "admin": False,
            "tenant_permissions": ("AUDIT_LOG_READ",),
            "is_active": False,
            "team_id": 3,
        },
        route="POST /api/v1/admin/users",
        body={
            "email": "alice@example.com",
            "first_name": "Alice",
            "last_name": "Smith",
            "admin": False,
            "tenant_permissions": ["AUDIT_LOG_READ"],
            "is_active": False,
            "team_id": 3,
        },
    ),
    Case(
        target="admin.users.update",
        arguments={"user_id": 5},
        route="PATCH /api/v1/admin/users/5",
        body={},
    ),
    Case(
        target="admin.users.update",
        arguments={
            "user_id": 5,
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "Name",
            "admin": True,
            "tenant_permissions": [],
            "is_active": False,
        },
        route="PATCH /api/v1/admin/users/5",
        body={
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "Name",
            "admin": True,
            "tenant_permissions": [],
            "is_active": False,
        },
    ),
    Case(
        target="admin.users.delete", arguments={"user_id": 5}, route="DELETE /api/v1/admin/users/5"
    ),
    Case(
        target="admin.users.list_signin_activities",
        arguments={"user_id": 5},
        route="GET /api/v1/admin/users/5/signin_activities",
    ),
    Case(
        target="admin.users.list_signin_activities",
        name="a datetime and a string are sent as ISO 8601",
        arguments={
            "user_id": 5,
            "before": datetime(2026, 11, 22, tzinfo=UTC),
            "after": "2026-11-01T00:00:00Z",
            "per_page": 50,
            "page": 2,
        },
        route="GET /api/v1/admin/users/5/signin_activities",
        params={
            "before": "2026-11-22T00:00:00+00:00",
            "after": "2026-11-01T00:00:00Z",
            "per_page": 50,
            "page": 2,
        },
    ),
    Case(
        target="admin.users.resend_invitation",
        arguments={"user_id": 5},
        route="POST /api/v1/admin/users/5/resend_invitation",
    ),
    Case(
        target="admin.users.expire_session",
        arguments={"user_id": 5},
        route="POST /api/v1/admin/users/5/expire_session",
    ),
]

CASES = [*ROLE_CASES, *TEMPLATE_CASES, *TUNNEL_CASES, *USER_CASES]


@pytest.mark.parametrize("case", CASES, ids=case_id)
def test_request(tines, router, case):
    assert_sent(tines=tines, router=router, case=case)


def test_every_method_and_argument_has_a_case(tines):
    assert_covers(tines=tines, area="admin", cases=CASES)
