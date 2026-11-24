import pytest

from tests.support import Case, assert_covers, assert_sent, case_id

CASES = [
    Case(target="teams.list", arguments={}, route="GET /api/v1/teams"),
    Case(
        target="teams.list",
        arguments={"scope": "all", "per_page": 100, "page": 2},
        route="GET /api/v1/teams",
        params={"scope": "all", "per_page": 100, "page": 2},
    ),
    Case(target="teams.get", arguments={"team_id": 4}, route="GET /api/v1/teams/4"),
    Case(
        target="teams.create",
        arguments={"name": "Security team"},
        route="POST /api/v1/teams",
        body={"name": "Security team"},
    ),
    Case(
        target="teams.update",
        arguments={"team_id": 4, "name": "Renamed"},
        route="PATCH /api/v1/teams/4",
        body={"name": "Renamed"},
    ),
    Case(target="teams.delete", arguments={"team_id": 4}, route="DELETE /api/v1/teams/4"),
    Case(
        target="teams.destroy_static_external_id",
        arguments={"team_id": 4},
        route="POST /api/v1/teams/4/destroy_static_external_id",
    ),
    Case(
        target="teams.members.list", arguments={"team_id": 4}, route="GET /api/v1/teams/4/members"
    ),
    Case(
        target="teams.members.list",
        arguments={"team_id": 4, "per_page": 100, "page": 2},
        route="GET /api/v1/teams/4/members",
        params={"per_page": 100, "page": 2},
    ),
    Case(
        target="teams.members.invite",
        name="required arguments send an empty JSON body",
        arguments={"team_id": 4},
        route="POST /api/v1/teams/4/invite_member",
        body={},
    ),
    Case(
        target="teams.members.invite",
        arguments={"team_id": 4, "email": "user@example.com", "user_id": 2, "role": "VIEWER"},
        route="POST /api/v1/teams/4/invite_member",
        body={"email": "user@example.com", "user_id": 2, "role": "VIEWER"},
    ),
    Case(
        target="teams.members.resend_invitation",
        arguments={"team_id": 4, "user_id": 2},
        route="POST /api/v1/teams/4/resend_invitation",
        body={"user_id": 2},
    ),
    Case(
        target="teams.members.remove",
        arguments={"team_id": 4, "user_id": 2},
        route="POST /api/v1/teams/4/remove_member",
        body={"user_id": 2},
    ),
]


@pytest.mark.parametrize("case", CASES, ids=case_id)
def test_request(tines, router, case):
    assert_sent(tines=tines, router=router, case=case)


def test_every_method_and_argument_has_a_case(tines):
    assert_covers(tines=tines, area="teams", cases=CASES)
