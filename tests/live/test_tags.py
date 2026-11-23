import pytest

from tests.live.helpers import all_items, check, throwaway, wait_until_gone

pytestmark = pytest.mark.writes

RED = "#FF8888"


def test_a_tag_is_created_read_listed_updated_and_deleted(live, team_id, cleanup):
    name = throwaway(kind="tag")
    created = check(reply=live.tags.create(name=name, team_id=team_id, color="red"), status=201)
    tag_id = created["id"]
    cleanup.add(description=f"tag {tag_id}", action=lambda: live.tags.delete(tag_id=tag_id))

    assert created["name"] == name
    assert created["color"] == RED
    assert check(reply=live.tags.get(tag_id=tag_id), status=200) == created
    listed = all_items(method=live.tags.list, key="tags", arguments={"team_id": team_id})
    assert tag_id in [tag["id"] for tag in listed]

    renamed = check(reply=live.tags.update(tag_id=tag_id, name=f"{name}-renamed"), status=200)
    assert renamed["name"] == f"{name}-renamed"
    assert renamed["color"] == RED

    recolored = check(reply=live.tags.update(tag_id=tag_id, color="#123ABC"), status=200)
    assert recolored["color"] == "#123ABC"

    check(reply=live.tags.delete(tag_id=tag_id), status=204)
    assert wait_until_gone(read=lambda: live.tags.get(tag_id=tag_id)) == 404
