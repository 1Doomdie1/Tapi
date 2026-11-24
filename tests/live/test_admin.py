import time
from functools import partial

import pytest

from tests.live.helpers import all_items, check, throwaway, wait_until_gone

pytestmark = pytest.mark.writes

OPTIONS = {"mode": "message_only", "message": "Hello"}
USER_DELETE_WAIT = 120.0


def remove_team(*, live, team_id, timeout=300.0):
    stories = live.stories.list(team_id=team_id, per_page=100)
    if stories.status_code != 200:
        return stories
    for story in stories.data["stories"]:
        live.stories.delete(story_id=story["id"])
    deadline = time.monotonic() + timeout
    while True:
        reply = live.teams.delete(team_id=team_id)
        if reply.status_code != 422 or time.monotonic() >= deadline:
            return reply
        time.sleep(15)


def test_a_custom_role_is_created_read_listed_changed_and_deleted(live, cleanup):
    roles = live.admin.roles
    name = throwaway(kind="role")

    created = check(
        reply=roles.create(name=name, permissions=["CASE_READ"], description="Throwaway."),
        status=201,
    )
    cleanup.add(description=f"role {name}", action=partial(roles.delete, role_id=name))

    assert created["type"] == "custom"
    assert created["permissions"] == ["CASE_READ"]
    assert created["builder"] is False
    assert created["created_at"] is not None
    by_name = check(reply=roles.get(role_id=name), status=200)
    by_id = check(reply=roles.get(role_id=created["id"]), status=200)
    assert by_name == by_id
    assert by_name["id"] == str(created["id"])
    listed = all_items(method=roles.list, key="admin/roles")
    assert name in {role["name"] for role in listed}
    assert {"default", "custom"} <= {role["type"] for role in listed}

    time.sleep(1.1)
    changed = check(reply=roles.update(role_id=name, description="Changed."), status=200)
    assert changed["description"] == "Changed."
    assert changed["permissions"] == ["CASE_READ"]
    assert changed["updated_at"] != created["updated_at"]
    replaced = check(
        reply=roles.update(role_id=created["id"], permissions=["CASE_READ", "CASE_CREATE"]),
        status=200,
    )
    assert replaced["permissions"] == ["CASE_READ", "CASE_CREATE"]
    assert roles.update(role_id=name).status_code == 200

    refused = {
        "a name that is taken": roles.create(name=name, permissions=["CASE_READ"]),
        "a permission that does not exist": roles.create(
            name=f"{name}-bogus", permissions=["NOT_A_PERMISSION"]
        ),
        "no permissions": roles.create(name=f"{name}-empty", permissions=[]),
        "empty permissions on update": roles.update(role_id=name, permissions=[]),
    }
    assert {reason: reply.status_code for reason, reply in refused.items()} == dict.fromkeys(
        refused, 422
    )
    assert refused["a permission that does not exist"].data == [
        "NOT_A_PERMISSION is not a valid permission"
    ]
    assert roles.update(role_id="no-such-role", description="x").status_code == 404

    check(reply=roles.delete(role_id=name), status=204)
    assert roles.get(role_id=name).status_code == 404
    assert roles.delete(role_id=name).status_code == 404


def test_a_template_is_created_read_listed_changed_moved_and_deleted(live, team_id, cleanup):
    templates = live.admin.templates
    name = throwaway(kind="template")
    base = {
        "name": name,
        "agent_type": "Agents::EventTransformationAgent",
        "agent_options": OPTIONS,
        "product": "Live check",
        "description": "Throwaway.",
        "vendor": "Vendor",
    }

    def create(**arguments):
        created = check(reply=templates.create(**{**base, **arguments}), status=200)
        cleanup.add(
            description=f"template {created['id']}",
            action=partial(templates.delete, template_id=created["id"]),
        )
        return created

    created = create(team_id=team_id)
    teamless = create(name=f"{name}-teamless")
    with_inputs = create(
        name=f"{name}-inputs",
        team_id=team_id,
        action_inputs=[
            {"name": "input_text", "type": "TEXT", "required": True, "default_value": "Sample"},
            {"name": "format", "type": "OPTION", "data": {"options": ["A", "B"]}},
        ],
    )

    assert created["read_access"] == "TEAM"
    assert (created["team_id"], created["folder_id"], created["action_inputs"]) == (
        team_id,
        None,
        [],
    )
    assert (teamless["read_access"], teamless["team_id"]) == ("GLOBAL", None)
    assert [item["name"] for item in with_inputs["action_inputs"]] == ["input_text", "format"]
    assert check(reply=templates.get(template_id=created["id"]), status=200) == created
    found = all_items(method=templates.list, key="admin/templates", arguments={"search": name})
    assert {item["id"] for item in found} == {created["id"], teamless["id"], with_inputs["id"]}

    refused = {
        "an agent_type that is not valid": templates.create(
            **{**base, "name": f"{name}-bad", "agent_type": "Agents::Nope"}
        ),
        "a CREDENTIAL with a description": templates.create(
            **{
                **base,
                "name": f"{name}-cred",
                "action_inputs": [
                    {"name": "c", "type": "CREDENTIAL", "required": True, "description": "no"}
                ],
            }
        ),
    }
    assert {reason: reply.status_code for reason, reply in refused.items()} == dict.fromkeys(
        refused, 422
    )
    assert "eventTransformation" in str(refused["an agent_type that is not valid"].data)
    assert (
        templates.create(**{**base, "name": f"{name}-t", "team_id": 999999999}).status_code == 404
    )

    time.sleep(1.1)
    full = {key: base[key] for key in ("name", "description", "agent_type", "vendor", "product")}
    full["agent_options"] = OPTIONS
    changed = check(
        reply=templates.update(
            template_id=with_inputs["id"],
            **{**full, "name": with_inputs["name"], "description": "Changed."},
        ),
        status=200,
    )
    assert changed["description"] == "Changed."
    assert [item["name"] for item in changed["action_inputs"]] == ["input_text", "format"]
    replaced = check(
        reply=templates.update(
            template_id=with_inputs["id"],
            **{**full, "name": with_inputs["name"]},
            action_inputs=[{"name": "only", "type": "TEXT"}],
        ),
        status=200,
    )
    assert [item["name"] for item in replaced["action_inputs"]] == ["only"]
    cleared = check(
        reply=templates.update(
            template_id=with_inputs["id"], **{**full, "name": with_inputs["name"]}, action_inputs=[]
        ),
        status=200,
    )
    assert cleared["action_inputs"] == []
    other_type = templates.update(
        template_id=created["id"], **{**full, "agent_type": "Agents::EmailAgent"}
    )
    assert other_type.status_code == 422
    assert other_type.data == {"message": "Action type cannot be changed"}
    unknown = templates.update(template_id=999999999, **full)
    assert unknown.status_code == 422

    teams = check(reply=live.teams.list(scope="all", per_page=100), status=200)["teams"]
    other_team = next((team["id"] for team in teams if team["id"] != team_id), None)
    if other_team is not None:
        moved = check(
            reply=templates.move(template_id=created["id"], team_id=other_team), status=200
        )
        assert moved["team_id"] == other_team
        back = check(reply=templates.move(template_id=created["id"], team_id=team_id), status=200)
        assert back["team_id"] == team_id
    assert templates.move(template_id=created["id"], team_id=999999999).status_code == 404
    assert templates.move(template_id=999999999, team_id=team_id).status_code == 404

    for template_id in (created["id"], teamless["id"], with_inputs["id"]):
        check(reply=templates.delete(template_id=template_id), status=204)
        assert templates.get(template_id=template_id).status_code == 404
    assert templates.delete(template_id=created["id"]).status_code == 404


def test_a_user_is_created_read_changed_signed_out_and_deleted(live, cleanup):
    users = live.admin.users
    email = f"{throwaway(kind='user')}@example.invalid"
    personal = {"scope": "personal_only"}
    teams_before = {
        team["id"] for team in all_items(method=live.teams.list, key="teams", arguments=personal)
    }

    created = check(
        reply=users.create(
            email=email,
            first_name="Tapi",
            last_name="Check",
            admin=False,
            tenant_permissions=["AUDIT_LOG_READ"],
            is_active=True,
        ),
        status=201,
    )
    user_id = created["id"]
    cleanup.add(description=f"user {user_id}", action=partial(users.delete, user_id=user_id))
    new_teams = {
        team["id"] for team in all_items(method=live.teams.list, key="teams", arguments=personal)
    } - teams_before
    for new_team in new_teams:
        cleanup.add(
            description=f"personal team {new_team}",
            action=partial(remove_team, live=live, team_id=new_team),
        )

    assert len(new_teams) == 1
    assert (created["admin"], created["is_active"]) == (False, True)
    assert created["tenant_permissions"] == ["AUDIT_LOG_READ"]
    assert (created["scim_uid"], created["last_seen"]) == (None, None)
    by_email = check(reply=users.get(user_id=email), status=200)
    assert by_email["id"] == user_id
    teams = check(reply=users.get(user_id=user_id, include="team_memberships"), status=200)
    assert isinstance(teams["team_memberships"], list)
    assert check(reply=users.list(search=email), status=200)["admin/users"][0]["id"] == user_id

    again = check(reply=users.create(email=email.upper(), first_name="Other"), status=201)
    assert (again["id"], again["first_name"]) == (user_id, "Other")

    time.sleep(1.1)
    for arguments in (
        {"last_name": "Name"},
        {"tenant_permissions": []},
        {"is_active": False},
        {"admin": False},
        {},
    ):
        changed = check(reply=users.update(user_id=user_id, **arguments), status=200)
        for key, value in arguments.items():
            assert changed[key] == value
    assert changed["updated_at"] != created["updated_at"]
    owners = check(reply=users.list(filter="TENANT_OWNER", per_page=100), status=200)
    assert user_id not in {item["id"] for item in owners["admin/users"]}

    sign_ins = check(reply=users.list_signin_activities(user_id=user_id), status=200)
    assert sign_ins["admin/login_activities"] == []
    assert check(reply=users.resend_invitation(user_id=user_id), status=200) == {}
    signed_out = users.expire_session(user_id=user_id)
    assert (signed_out.status_code, signed_out.data) == (200, None)

    refused = {
        "an email that is not valid": users.create(email="not-an-email"),
        "an unknown user on update": users.update(user_id=999999999, first_name="x"),
        "an unknown user on resend": users.resend_invitation(user_id=999999999),
        "an unknown user on delete": users.delete(user_id=999999999),
    }
    assert [reply.status_code for reply in refused.values()] == [422, 404, 404, 404]
    assert users.expire_session(user_id=999999999).status_code == 422

    check(reply=users.delete(user_id=user_id), status=204)
    read = partial(users.get, user_id=user_id)
    assert wait_until_gone(read=read, timeout=USER_DELETE_WAIT) == 404
    assert users.delete(user_id=user_id).status_code == 404

    (personal_team,) = new_teams
    left = check(reply=live.teams.members.list(team_id=personal_team), status=200)
    assert left["members"] == []
    story_names = [
        story["name"]
        for story in check(reply=live.stories.list(team_id=personal_team), status=200)["stories"]
    ]
    assert story_names == ["Your first story"]
    assert live.teams.delete(team_id=personal_team).status_code == 422
    assert remove_team(live=live, team_id=personal_team).status_code == 204
    assert live.teams.get(team_id=personal_team).status_code == 404
