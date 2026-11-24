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

IP_CASES = [
    Case(
        target="admin.ip_access_control_rules.list",
        arguments={},
        route="GET /api/v1/admin/ip_access_control_rules",
    ),
    Case(
        target="admin.ip_access_control_rules.list",
        arguments={"matching_ip": "192.168.1.1", "per_page": 50, "page": 2},
        route="GET /api/v1/admin/ip_access_control_rules",
        params={"matching_ip": "192.168.1.1", "per_page": 50, "page": 2},
    ),
    Case(
        target="admin.ip_access_control_rules.get",
        arguments={"rule_id": 1},
        route="GET /api/v1/admin/ip_access_control_rules/1",
    ),
    Case(
        target="admin.ip_access_control_rules.create",
        arguments={"ip": "192.168.1.1"},
        route="POST /api/v1/admin/ip_access_control_rules",
        body={"ip": "192.168.1.1"},
    ),
    Case(
        target="admin.ip_access_control_rules.create",
        arguments={"ip": "10.0.0.0/8", "description": "Office"},
        route="POST /api/v1/admin/ip_access_control_rules",
        body={"ip": "10.0.0.0/8", "description": "Office"},
    ),
    Case(
        target="admin.ip_access_control_rules.update",
        arguments={"rule_id": 1},
        route="PATCH /api/v1/admin/ip_access_control_rules/1",
        body={},
    ),
    Case(
        target="admin.ip_access_control_rules.update",
        arguments={"rule_id": 1, "ip": "10.0.0.0/16", "description": "Changed"},
        route="PATCH /api/v1/admin/ip_access_control_rules/1",
        body={"ip": "10.0.0.0/16", "description": "Changed"},
    ),
    Case(
        target="admin.ip_access_control_rules.delete",
        arguments={"rule_id": 1},
        route="DELETE /api/v1/admin/ip_access_control_rules/1",
    ),
]

EGRESS_CASES = [
    Case(
        target="admin.action_egress_control_rules.list",
        arguments={},
        route="GET /api/v1/admin/action_egress_control_rules",
    ),
    Case(
        target="admin.action_egress_control_rules.list",
        arguments={"per_page": 50, "page": 2},
        route="GET /api/v1/admin/action_egress_control_rules",
        params={"per_page": 50, "page": 2},
    ),
    Case(
        target="admin.action_egress_control_rules.get",
        arguments={"rule_id": 1},
        route="GET /api/v1/admin/action_egress_control_rules/1",
    ),
    Case(
        target="admin.action_egress_control_rules.create",
        arguments={"description": "Example", "allowed_action_types": ["http-request"]},
        route="POST /api/v1/admin/action_egress_control_rules",
        body={"description": "Example", "allowed_action_types": ["http-request"]},
    ),
    Case(
        target="admin.action_egress_control_rules.create",
        name="a tuple of types is sent as a list, with an ip and an fqdn",
        arguments={
            "description": "Example",
            "allowed_action_types": ("http-request", "send-email"),
            "ip": "192.168.1.1",
            "fqdn": "sub.example.com",
        },
        route="POST /api/v1/admin/action_egress_control_rules",
        body={
            "description": "Example",
            "allowed_action_types": ["http-request", "send-email"],
            "ip": "192.168.1.1",
            "fqdn": "sub.example.com",
        },
    ),
    Case(
        target="admin.action_egress_control_rules.update",
        arguments={"rule_id": 1, "description": "Example", "allowed_action_types": ["send-email"]},
        route="PATCH /api/v1/admin/action_egress_control_rules/1",
        body={"description": "Example", "allowed_action_types": ["send-email"]},
    ),
    Case(
        target="admin.action_egress_control_rules.update",
        arguments={
            "rule_id": 1,
            "description": "Changed",
            "allowed_action_types": ["http-request"],
            "ip": "10.0.0.1",
            "fqdn": "example.com",
        },
        route="PATCH /api/v1/admin/action_egress_control_rules/1",
        body={
            "description": "Changed",
            "allowed_action_types": ["http-request"],
            "ip": "10.0.0.1",
            "fqdn": "example.com",
        },
    ),
    Case(
        target="admin.action_egress_control_rules.delete",
        arguments={"rule_id": 1},
        route="DELETE /api/v1/admin/action_egress_control_rules/1",
    ),
]

SYNC_REQUIRED = {
    "destination_tenant_url": "https://destination.example.com",
    "destination_team_id": 42,
    "team_id": 7,
    "story_ids": [9981, 9982],
}

SYNC_CASES = [
    Case(
        target="admin.sync_destinations.list",
        arguments={},
        route="GET /api/v1/admin/sync_destinations",
    ),
    Case(
        target="admin.sync_destinations.list",
        arguments={"per_page": 50, "page": 2},
        route="GET /api/v1/admin/sync_destinations",
        params={"per_page": 50, "page": 2},
    ),
    Case(
        target="admin.sync_destinations.get",
        arguments={"sync_destination_id": 24},
        route="GET /api/v1/admin/sync_destinations/24",
    ),
    Case(
        target="admin.sync_destinations.create",
        arguments=SYNC_REQUIRED,
        route="POST /api/v1/admin/sync_destinations",
        body=SYNC_REQUIRED,
    ),
    Case(
        target="admin.sync_destinations.create",
        name="false is sent, and a tuple of stories is sent as a list",
        arguments={
            **SYNC_REQUIRED,
            "story_ids": (9981, 9982),
            "destination_tenant_api_key": "key",
            "manual_sync_only": False,
            "sync_mode": "draft_editable",
        },
        route="POST /api/v1/admin/sync_destinations",
        body={
            **SYNC_REQUIRED,
            "destination_tenant_api_key": "key",
            "manual_sync_only": False,
            "sync_mode": "draft_editable",
        },
    ),
    Case(
        target="admin.sync_destinations.update",
        arguments={"sync_destination_id": 24},
        route="PATCH /api/v1/admin/sync_destinations/24",
        body={},
    ),
    Case(
        target="admin.sync_destinations.update",
        name="an empty list of stories is sent, to remove the subscriptions",
        arguments={
            "sync_destination_id": 24,
            "destination_tenant_api_key": "new-key",
            "story_ids": [],
            "manual_sync_only": True,
        },
        route="PATCH /api/v1/admin/sync_destinations/24",
        body={"destination_tenant_api_key": "new-key", "story_ids": [], "manual_sync_only": True},
    ),
    Case(
        target="admin.sync_destinations.delete",
        name="no body is sent when keep_stories is left out",
        arguments={"sync_destination_id": 24},
        route="DELETE /api/v1/admin/sync_destinations/24",
    ),
    Case(
        target="admin.sync_destinations.delete",
        name="false is sent in the body, not left out",
        arguments={"sync_destination_id": 24, "keep_stories": False},
        route="DELETE /api/v1/admin/sync_destinations/24",
        body={"keep_stories": False},
    ),
    Case(
        target="admin.sync_destinations.manual_sync",
        arguments={"sync_destination_id": 24},
        route="POST /api/v1/admin/sync_destinations/24/manual_sync",
    ),
    Case(
        target="admin.sync_destinations.sync_story",
        arguments={"sync_destination_id": 24, "story_id": 12},
        route="POST /api/v1/admin/sync_destinations/24/story/12/sync",
    ),
]

LICENSE_CASES = [
    Case(target="admin.license.get", arguments={}, route="GET /api/v1/admin/license"),
    Case(
        target="admin.license.create",
        arguments={"license": "TINES-company-ENV::DATA"},
        route="POST /api/v1/admin/license",
        body={"license": "TINES-company-ENV::DATA"},
    ),
    Case(
        target="admin.license.update",
        arguments={"license": "TINES-company-ENV::DATA"},
        route="PATCH /api/v1/admin/license",
        body={"license": "TINES-company-ENV::DATA"},
    ),
]

SMTP_REQUIRED = {
    "address": "smtp.example.com",
    "port": 587,
    "encryption_mode": "starttls_auto",
    "verify_ssl_certificate": True,
}

SMTP_CASES = [
    Case(target="admin.smtp.get", arguments={}, route="GET /api/v1/admin/smtp"),
    Case(
        target="admin.smtp.update",
        arguments=SMTP_REQUIRED,
        route="PATCH /api/v1/admin/smtp",
        body=SMTP_REQUIRED,
    ),
    Case(
        target="admin.smtp.update",
        name="false is sent, and every field is sent when it is given",
        arguments={
            **SMTP_REQUIRED,
            "verify_ssl_certificate": False,
            "domain": "example.com",
            "user_name": "smtp-user",
            "password": "smtp-password",
            "auth_type": "cram_md5",
            "ca_path": "/etc/ssl/certs",
            "ca_file": "/etc/ssl/ca.pem",
            "open_timeout": 10,
            "read_timeout": 20,
        },
        route="PATCH /api/v1/admin/smtp",
        body={
            **SMTP_REQUIRED,
            "verify_ssl_certificate": False,
            "domain": "example.com",
            "user_name": "smtp-user",
            "password": "smtp-password",
            "auth_type": "cram_md5",
            "ca_path": "/etc/ssl/certs",
            "ca_file": "/etc/ssl/ca.pem",
            "open_timeout": 10,
            "read_timeout": 20,
        },
    ),
    Case(target="admin.smtp.delete", arguments={}, route="DELETE /api/v1/admin/smtp"),
]

CERTIFICATE_CASES = [
    Case(
        target="admin.custom_certificate_authority.set",
        arguments={"certificate": "-----BEGIN CERTIFICATE-----"},
        route="PATCH /api/v1/admin/custom_certificate_authority",
        body={"certificate": "-----BEGIN CERTIFICATE-----"},
    ),
    Case(
        target="admin.custom_certificate_authority.set",
        arguments={"certificate": "-----BEGIN CERTIFICATE-----", "name": "internal"},
        route="PATCH /api/v1/admin/custom_certificate_authority",
        body={"certificate": "-----BEGIN CERTIFICATE-----", "name": "internal"},
    ),
]

USER_GROUP_MAPPING = {
    "mappings": [
        {"group_name": "Managers", "team_name": "Analytics", "role_name": "TEAM_ADMIN"},
        {"group_name": "Analysts", "team_name": "Analytics", "role_name": "EDITOR"},
    ],
    "tenant_permissions": [{"group_name": "Managers", "permission": "TENANT_ADMIN"}],
    "tenant_owners_groups": ["Managers"],
}

PROVISIONING_CASES = [
    Case(
        target="admin.user_provisioning.update_mapping",
        arguments={"user_group_mapping": USER_GROUP_MAPPING},
        route="POST /api/v1/admin/user_provisioning/mapping",
        body={"user_group_mapping": USER_GROUP_MAPPING},
    ),
]

JOB_LISTS = {
    "list_dead": "dead_jobs",
    "list_in_progress": "in_progress_jobs",
    "list_queued": "queued_jobs",
    "list_retry": "retry_jobs",
}

JOB_DELETES = {
    "delete_all_dead": "dead",
    "delete_all_queued": "queued",
    "delete_all_retry": "retry",
}

JOB_CASES = [
    *(
        Case(target=f"admin.jobs.{method}", arguments={}, route=f"GET /api/v1/admin/{path}")
        for method, path in JOB_LISTS.items()
    ),
    *(
        Case(
            target=f"admin.jobs.{method}",
            arguments={"per_page": 50, "page": 2},
            route=f"GET /api/v1/admin/{path}",
            params={"per_page": 50, "page": 2},
        )
        for method, path in JOB_LISTS.items()
    ),
    *(
        Case(
            target=f"admin.jobs.{method}",
            arguments={},
            route=f"DELETE /api/v1/admin/delete_all_{kind}_jobs",
        )
        for method, kind in JOB_DELETES.items()
    ),
    *(
        Case(
            target=f"admin.jobs.delete_{kind}_by_action",
            arguments={"action_id": 24},
            route=f"DELETE /api/v1/admin/actions/24/delete_all_{kind}_jobs",
        )
        for kind in JOB_DELETES.values()
    ),
]

CASES = [
    *ROLE_CASES,
    *TEMPLATE_CASES,
    *TUNNEL_CASES,
    *USER_CASES,
    *IP_CASES,
    *EGRESS_CASES,
    *SYNC_CASES,
    *LICENSE_CASES,
    *SMTP_CASES,
    *CERTIFICATE_CASES,
    *PROVISIONING_CASES,
    *JOB_CASES,
]


@pytest.mark.parametrize("case", CASES, ids=case_id)
def test_request(tines, router, case):
    assert_sent(tines=tines, router=router, case=case)


def test_every_method_and_argument_has_a_case(tines):
    assert_covers(tines=tines, area="admin", cases=CASES)
