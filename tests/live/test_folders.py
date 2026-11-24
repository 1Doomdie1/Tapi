from functools import partial

import pytest

from tests.live.helpers import all_items, check, throwaway, wait_until_gone

pytestmark = pytest.mark.writes


def test_folders_nest_move_rename_and_delete(live, team_id, cleanup):
    def make(*, kind, **arguments):
        created = check(
            reply=live.folders.create(
                name=throwaway(kind=kind), content_type="STORY", team_id=team_id, **arguments
            ),
            status=201,
        )
        cleanup.add(
            description=f"folder {created['id']}",
            action=lambda: live.folders.delete(folder_id=created["id"]),
        )
        return created

    parent = make(kind="folder")
    child = make(kind="folder-child", parent_folder_id=parent["id"])
    other = make(kind="folder-other")

    assert parent["content_type"] == "STORY"
    assert child["parent_folder_id"] == parent["id"]
    assert check(reply=live.folders.get(folder_id=parent["id"]), status=200)["id"] == parent["id"]
    listed = all_items(
        method=live.folders.list,
        key="folders",
        arguments={"team_id": team_id, "content_type": "STORY"},
    )
    assert {parent["id"], child["id"], other["id"]} <= {folder["id"] for folder in listed}

    renamed = check(
        reply=live.folders.update(folder_id=parent["id"], name=f"{parent['name']}-renamed"),
        status=200,
    )
    assert renamed["name"] == f"{parent['name']}-renamed"

    moved = check(
        reply=live.folders.update(
            folder_id=child["id"], name=child["name"], parent_folder_id=other["id"]
        ),
        status=200,
    )
    assert moved["parent_folder_id"] == other["id"]

    for folder in (child, parent, other):
        check(reply=live.folders.delete(folder_id=folder["id"]), status=204)
        assert wait_until_gone(read=partial(live.folders.get, folder_id=folder["id"])) == 404
