import pytest

from tests.live.helpers import all_items, check, throwaway, wait_until_gone

pytestmark = pytest.mark.writes


def make(*, live, cleanup, team_id, kind, **arguments):
    created = check(
        reply=live.resources.create(name=throwaway(kind=kind), team_id=team_id, **arguments),
        status=201,
    )
    cleanup.add(
        description=f"resource {created['id']}",
        action=lambda: live.resources.delete(resource_id=created["id"]),
    )
    return created


def typed_value(*, live, resource_id):
    reply = live.resources.get(resource_id=resource_id, typed_value=True)
    return check(reply=reply, status=200)["value"]


def test_a_text_resource_is_created_read_listed_updated_and_deleted(live, team_id, cleanup):
    created = make(
        live=live, cleanup=cleanup, team_id=team_id, kind="resource", value="placeholder"
    )
    resource_id = created["id"]

    assert created["value"] == "placeholder"
    assert check(reply=live.resources.get(resource_id=resource_id), status=200)["id"] == resource_id
    listed = all_items(method=live.resources.list, key="global_resources")
    assert resource_id in [resource["id"] for resource in listed]

    updated = check(
        reply=live.resources.update(
            resource_id=resource_id, value="changed", description="Updated by a live check."
        ),
        status=200,
    )
    assert updated["value"] == "changed"
    assert updated["description"] == "Updated by a live check."
    assert updated["name"] == created["name"]

    check(reply=live.resources.delete(resource_id=resource_id), status=204)
    assert wait_until_gone(read=lambda: live.resources.get(resource_id=resource_id)) == 404


def test_an_array_resource_is_appended_replaced_and_trimmed(live, team_id, cleanup):
    created = make(
        live=live,
        cleanup=cleanup,
        team_id=team_id,
        kind="array",
        value=["a", "b", "c"],
        typed_value=True,
    )
    resource_id = created["id"]
    assert typed_value(live=live, resource_id=resource_id) == ["a", "b", "c"]

    check(reply=live.resources.append(resource_id=resource_id, value="d"), status=200)
    assert typed_value(live=live, resource_id=resource_id) == ["a", "b", "c", "d"]

    check(reply=live.resources.replace(resource_id=resource_id, index=0, value="A"), status=200)
    assert typed_value(live=live, resource_id=resource_id) == ["A", "b", "c", "d"]

    check(reply=live.resources.remove(resource_id=resource_id, index=0), status=200)
    assert typed_value(live=live, resource_id=resource_id) == ["b", "c", "d"]


def test_an_object_resource_is_replaced_and_trimmed_by_key(live, team_id, cleanup):
    created = make(
        live=live,
        cleanup=cleanup,
        team_id=team_id,
        kind="object",
        value={"count": 5, "owner": "run-1"},
        typed_value=True,
    )
    resource_id = created["id"]

    check(
        reply=live.resources.replace(resource_id=resource_id, key="count", value=6, if_value=5),
        status=200,
    )
    assert typed_value(live=live, resource_id=resource_id) == {"count": 6, "owner": "run-1"}

    refused = live.resources.replace(resource_id=resource_id, key="count", value=7, if_value=5)
    assert refused.status_code == 422
    assert typed_value(live=live, resource_id=resource_id) == {"count": 6, "owner": "run-1"}

    check(reply=live.resources.remove(resource_id=resource_id, key="owner"), status=200)
    assert typed_value(live=live, resource_id=resource_id) == {"count": 6}
