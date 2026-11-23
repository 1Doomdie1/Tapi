import time
from datetime import UTC, datetime
from functools import partial

import pytest

from tests.live.helpers import all_items, check, throwaway, wait_until_gone

pytestmark = pytest.mark.writes

NOTE = [{"id": "note-1", "name": "Note", "content": "Edited"}]


def exported(*, name, notes=()):
    return {
        "schema_version": 1,
        "export_type": "dashboard",
        "exported_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "dashboard": {
            "name": name,
            "notes": list(notes),
            "case_lists": [],
            "record_charts": [],
            "layout": [],
        },
    }


def letters(*, live, team_id, base, **arguments):
    listed = all_items(
        method=live.dashboards.list, key="dashboards", arguments={"team_id": team_id, **arguments}
    )
    return "".join(item["name"][-1] for item in listed if item["name"].startswith(base))


def test_dashboards_are_imported_listed_ordered_exported_replaced_and_deleted(
    live, team_id, cleanup
):
    dashboards = live.dashboards
    base = throwaway(kind="dashboard")
    ids = {}

    def import_new(*, letter, **arguments):
        reply = dashboards.import_(
            team_id=team_id, data=exported(name=f"{base}-{letter}"), **arguments
        )
        created = check(reply=reply, status=201)
        ids[letter] = created["id"]
        cleanup.add(
            description=f"dashboard {created['id']}",
            action=partial(dashboards.delete, dashboard_id=created["id"]),
        )
        return created

    for letter in "bca":
        created = import_new(letter=letter)
        time.sleep(1.1)

    assert set(created) == {"id", "name", "team", "created_at", "updated_at"}
    assert created["team"]["id"] == team_id
    assert letters(live=live, team_id=team_id, base=base) == "abc"

    replaced = check(
        reply=dashboards.import_(
            team_id=team_id,
            data=exported(name=f"{base}-b", notes=NOTE),
            mode="replace",
            new_name=f"{base}-b",
        ),
        status=201,
    )
    assert replaced["id"] == ids["b"]

    orders = {
        "NAME": "abc",
        "CREATED_ASC": "bca",
        "CREATED_DESC": "acb",
        "RECENTLY_EDITED": "bac",
        "LEAST_RECENTLY_EDITED": "cab",
        "RECENTLY_CREATED": "abc",
        "RECENTLY_UPDATED": "abc",
    }
    for order, expected in orders.items():
        found = letters(live=live, team_id=team_id, base=base, order=order)
        assert found == expected, order

    export = check(reply=dashboards.export(dashboard_id=ids["b"]), status=200)
    assert export["schema_version"] == 1
    assert export["export_type"] == "dashboard"
    assert export["dashboard"]["name"] == f"{base}-b"
    notes = export["dashboard"]["notes"]
    assert [(note["name"], note["content"]) for note in notes] == [("Note", "Edited")]
    assert notes[0]["id"] != NOTE[0]["id"]
    copy = check(
        reply=dashboards.import_(team_id=team_id, data=export, new_name=f"{base}-copy"),
        status=201,
    )
    ids["copy"] = copy["id"]
    cleanup.add(
        description=f"dashboard {copy['id']}",
        action=partial(dashboards.delete, dashboard_id=copy["id"]),
    )
    assert copy["id"] != ids["b"]

    refused = {
        "the name is used": dashboards.import_(team_id=team_id, data=exported(name=f"{base}-b")),
        "there is nothing to replace": dashboards.import_(
            team_id=team_id,
            data=exported(name=f"{base}-x"),
            mode="replace",
            new_name=f"{base}-nothing",
        ),
        "data is empty": dashboards.import_(team_id=team_id, data={}),
        "the schema version is not 1": dashboards.import_(
            team_id=team_id, data={**exported(name=f"{base}-y"), "schema_version": 2}
        ),
    }
    assert {reason: reply.status_code for reason, reply in refused.items()} == dict.fromkeys(
        refused, 400
    )
    assert refused["the name is used"].data == [
        f"dashboard with name {base}-b already exists for team"
    ]
    assert (
        dashboards.import_(
            team_id=team_id, data=exported(name=f"{base}-z"), mode="bogus"
        ).status_code
        == 422
    )
    assert dashboards.import_(team_id=999999999, data=exported(name=f"{base}-w")).status_code == 404

    for letter in ("a", "copy"):
        check(reply=dashboards.delete(dashboard_id=ids[letter]), status=204)
        read = partial(dashboards.export, dashboard_id=ids[letter])
        assert wait_until_gone(read=read) == 404
    assert dashboards.delete(dashboard_id=ids["a"]).status_code == 404
    assert dashboards.delete(dashboard_id=999999999).status_code == 404
