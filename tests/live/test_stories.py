from functools import partial

import pytest

from tests.live.helpers import all_items, check, throwaway, wait_until_gone

pytestmark = pytest.mark.writes

ACTION_TYPE = "Agents::EventTransformationAgent"
ACTION_OPTIONS = {"mode": "message_only", "message": "hello from a live check"}


@pytest.fixture
def story(live, team_id, cleanup):
    created = check(
        reply=live.stories.create(
            team_id=team_id,
            name=throwaway(kind="story"),
            description="Throwaway story from a live check.",
        ),
        status=201,
    )
    cleanup.add(
        description=f"story {created['id']}",
        action=lambda: live.stories.delete(story_id=created["id"]),
    )
    return created


def test_a_story_is_created_read_updated_disabled_exported_and_deleted(live, story):
    story_id = story["id"]

    assert check(reply=live.stories.get(story_id=story_id), status=200) == story
    updated = check(
        reply=live.stories.update(story_id=story_id, description="Changed by a live check."),
        status=200,
    )
    assert updated["description"] == "Changed by a live check."
    assert updated["name"] == story["name"]

    disabled = check(reply=live.stories.disable(story_id=story_id, disabled=True), status=200)
    assert disabled == {"disabled": True}
    assert check(reply=live.stories.get(story_id=story_id), status=200)["disabled"] is True
    check(reply=live.stories.disable(story_id=story_id, disabled=False), status=200)

    exported = check(reply=live.stories.export(story_id=story_id), status=200)
    assert exported["name"] == story["name"]

    listed = all_items(
        method=live.stories.list, key="stories", arguments={"team_id": story["team_id"]}
    )
    assert story_id in [item["id"] for item in listed]

    check(reply=live.stories.delete(story_id=story_id), status=204)
    assert wait_until_gone(read=lambda: live.stories.get(story_id=story_id)) == 404


def test_a_note_is_created_read_listed_updated_and_deleted(live, story):
    story_id = story["id"]
    created = check(
        reply=live.stories.notes.create(
            story_id=story_id, content="# Header\n - item 1", position={"x": 100, "y": 200}
        ),
        status=201,
    )
    note_id = created["id"]

    assert created["story_id"] == story_id
    assert created["content"] == "# Header\n - item 1"
    assert created["position"] == {"x": 100, "y": 200}
    assert check(reply=live.stories.notes.get(note_id=note_id), status=200) == created
    listed = all_items(
        method=live.stories.notes.list, key="annotations", arguments={"story_id": story_id}
    )
    assert note_id in [note["id"] for note in listed]

    updated = check(reply=live.stories.notes.update(note_id=note_id, content="Changed"), status=200)
    assert updated["content"] == "Changed"
    assert updated["position"] == {"x": 100, "y": 200}

    check(reply=live.stories.notes.delete(note_id=note_id), status=204)
    assert wait_until_gone(read=lambda: live.stories.notes.get(note_id=note_id)) == 404


def test_a_note_without_a_story_or_a_group_is_not_found(live):
    reply = live.stories.notes.create(content="Nowhere to go")

    assert reply.status_code == 404


def test_actions_are_linked_and_the_link_is_deleted(live, story):
    story_id = story["id"]
    first = check(
        reply=live.stories.actions.create(
            type=ACTION_TYPE,
            name=throwaway(kind="action"),
            story_id=story_id,
            options=ACTION_OPTIONS,
        ),
        status=201,
    )
    second = check(
        reply=live.stories.actions.create(
            type=ACTION_TYPE,
            name=throwaway(kind="action"),
            story_id=story_id,
            options=ACTION_OPTIONS,
            source_ids=[first["id"]],
        ),
        status=201,
    )

    assert (
        first["id"]
        in check(reply=live.stories.actions.get(action_id=second["id"]), status=200)["sources"]
    )
    assert (
        second["id"]
        in check(reply=live.stories.actions.get(action_id=first["id"]), status=200)["receivers"]
    )

    check(
        reply=live.stories.links.delete(
            links=[{"source_id": first["id"], "receiver_id": second["id"]}]
        ),
        status=204,
    )

    assert (
        check(reply=live.stories.actions.get(action_id=second["id"]), status=200)["sources"] == []
    )
    again = live.stories.links.delete(
        links=[{"source_id": first["id"], "receiver_id": second["id"]}]
    )
    assert again.status_code == 404

    listed = all_items(
        method=live.stories.actions.list, key="agents", arguments={"story_id": story_id}
    )
    assert {first["id"], second["id"]} <= {action["id"] for action in listed}
    for action in (second, first):
        check(reply=live.stories.actions.delete(action_id=action["id"]), status=204)
        read = partial(live.stories.actions.get, action_id=action["id"])
        assert wait_until_gone(read=read) == 404


def test_a_version_is_created_read_renamed_listed_and_deleted(live, story):
    story_id = story["id"]
    created = check(reply=live.stories.versions.create(story_id=story_id), status=200)
    version_id = created["story_version"]["id"]

    fetched = check(
        reply=live.stories.versions.get(story_id=story_id, version_id=version_id), status=200
    )
    assert fetched["story_version"]["id"] == version_id
    renamed = check(
        reply=live.stories.versions.update(
            story_id=story_id, version_id=version_id, name="Named by a live check"
        ),
        status=200,
    )
    assert renamed["story_version"]["name"] == "Named by a live check"
    listed = check(reply=live.stories.versions.list(story_id=story_id), status=200)
    assert version_id in [version["id"] for version in listed["story_versions"]]

    deleted = check(
        reply=live.stories.versions.delete(story_id=story_id, version_id=version_id), status=200
    )
    assert deleted["destroyed_id"] == version_id
    gone = live.stories.versions.get(story_id=story_id, version_id=version_id)
    assert gone.status_code == 404
