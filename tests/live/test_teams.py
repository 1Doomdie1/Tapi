import pytest

from tests.live.helpers import all_items, check, throwaway, wait_until_gone

pytestmark = pytest.mark.writes

UNKNOWN_USER = 999999999


def test_a_team_is_created_read_listed_updated_and_deleted(live, cleanup):
    name = throwaway(kind="team")
    created = check(reply=live.teams.create(name=name), status=201)
    team_id = created["id"]
    cleanup.add(description=f"team {team_id}", action=lambda: live.teams.delete(team_id=team_id))

    assert created["name"] == name
    assert check(reply=live.teams.get(team_id=team_id), status=200) == created
    standard = all_items(method=live.teams.list, key="teams", arguments={"scope": "standard"})
    assert team_id in [team["id"] for team in standard]

    renamed = check(reply=live.teams.update(team_id=team_id, name=f"{name}-renamed"), status=200)
    assert renamed["name"] == f"{name}-renamed"
    assert check(reply=live.teams.get(team_id=team_id), status=200)["name"] == f"{name}-renamed"

    members = check(reply=live.teams.members.list(team_id=team_id), status=200)
    assert isinstance(members["members"], list)

    check(reply=live.teams.delete(team_id=team_id), status=204)
    assert wait_until_gone(read=lambda: live.teams.get(team_id=team_id)) == 404


def test_members_that_do_not_exist_are_not_found(live, cleanup):
    created = check(reply=live.teams.create(name=throwaway(kind="team")), status=201)
    team_id = created["id"]
    cleanup.add(description=f"team {team_id}", action=lambda: live.teams.delete(team_id=team_id))

    resent = live.teams.members.resend_invitation(team_id=team_id, user_id=UNKNOWN_USER)
    removed = live.teams.members.remove(team_id=team_id, user_id=UNKNOWN_USER)

    assert resent.status_code == 404
    assert removed.status_code == 404
