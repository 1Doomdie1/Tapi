import time
from functools import partial

import pytest

from tests.live.helpers import all_items, check, throwaway, wait_until_gone

pytestmark = pytest.mark.writes


def test_skills_are_created_read_listed_changed_renamed_and_deleted(live, team_id, cleanup):
    skills = live.skills
    name = throwaway(kind="skill")
    other = f"{name}-full"

    def create(*, skill_name, **arguments):
        reply = skills.create(
            team_id=team_id,
            name=skill_name,
            description="A throwaway skill.",
            body="# Throwaway\n\nText.",
            **arguments,
        )
        created = check(reply=reply, status=201)
        cleanup.add(
            description=f"skill {skill_name}",
            action=partial(skills.delete, skill_name=skill_name, team_id=team_id),
        )
        return created

    minimal = create(skill_name=name)
    full = create(
        skill_name=other,
        license="Apache-2.0",
        compatibility="Any",
        metadata={"source_repo": "runbooks", "k": "v"},
    )

    assert set(minimal) == {
        "name",
        "description",
        "body",
        "license",
        "compatibility",
        "metadata",
        "team_id",
        "created_at",
        "updated_at",
    }
    assert (minimal["license"], minimal["compatibility"], minimal["metadata"]) == (None, None, {})
    assert minimal["team_id"] == team_id
    assert full["metadata"] == {"source_repo": "runbooks", "k": "v"}
    assert check(reply=skills.get(skill_name=name, team_id=team_id), status=200) == minimal
    listed = all_items(method=skills.list, key="skills", arguments={"team_id": team_id})
    assert {name, other} <= {item["name"] for item in listed}
    found = check(reply=skills.list(search=name.upper()), status=200)["skills"]
    assert {item["name"] for item in found} == {name, other}
    only_full = check(reply=skills.list(search="-FULL"), status=200)["skills"]
    assert other in {item["name"] for item in only_full}
    assert name not in {item["name"] for item in only_full}

    time.sleep(1.1)
    changed = check(
        reply=skills.update(skill_name=name, team_id=team_id, description="Changed."), status=200
    )
    assert changed["description"] == "Changed."
    assert changed["body"] == minimal["body"]
    assert changed["created_at"] == minimal["created_at"]
    assert changed["updated_at"] != minimal["updated_at"]
    replaced = check(
        reply=skills.update(skill_name=other, team_id=team_id, metadata={"x": "y"}), status=200
    )
    assert (replaced["metadata"], replaced["license"]) == ({"x": "y"}, "Apache-2.0")
    cleared = check(reply=skills.update(skill_name=other, team_id=team_id, metadata={}), status=200)
    assert cleared["metadata"] == {}

    renamed = f"{name}-renamed"
    cleanup.add(
        description=f"skill {renamed}",
        action=partial(skills.delete, skill_name=renamed, team_id=team_id),
    )
    check(reply=skills.update(skill_name=name, team_id=team_id, name=renamed), status=200)
    assert skills.get(skill_name=name, team_id=team_id).status_code == 404
    assert (
        check(reply=skills.get(skill_name=renamed, team_id=team_id), status=200)["name"] == renamed
    )

    refused = {
        "a name that is taken": skills.create(
            team_id=team_id, name=other, description="d", body="b"
        ),
        "an upper-case name": skills.create(
            team_id=team_id, name=f"{name}-Upper", description="d", body="b"
        ),
        "a name of 65 characters": skills.create(
            team_id=team_id, name="a" * 65, description="d", body="b"
        ),
        "an empty description": skills.create(
            team_id=team_id, name=f"{name}-empty", description="", body="b"
        ),
        "an empty body": skills.create(
            team_id=team_id, name=f"{name}-empty", description="d", body=""
        ),
        "metadata that is not flat": skills.create(
            team_id=team_id,
            name=f"{name}-nested",
            description="d",
            body="b",
            metadata={"k": {"x": "y"}},
        ),
        "a rename onto another skill": skills.update(
            skill_name=renamed, team_id=team_id, name=other
        ),
    }
    assert {reason: reply.status_code for reason, reply in refused.items()} == dict.fromkeys(
        refused, 422
    )
    assert refused["a name that is taken"].data == [
        "Validation failed: Name has already been taken"
    ]
    unknown = {
        "update": skills.update(skill_name=f"{name}-nothing", team_id=team_id, description="x"),
        "get in another team": skills.get(skill_name=renamed, team_id=999999999),
        "delete": skills.delete(skill_name=f"{name}-nothing", team_id=team_id),
        "create in another team": skills.create(
            team_id=999999999, name=f"{name}-team", description="d", body="b"
        ),
    }
    assert {action: reply.status_code for action, reply in unknown.items()} == dict.fromkeys(
        unknown, 404
    )
    assert unknown["update"].data == ["Skill not found"]

    for skill_name in (renamed, other):
        check(reply=skills.delete(skill_name=skill_name, team_id=team_id), status=204)
        read = partial(skills.get, skill_name=skill_name, team_id=team_id)
        assert wait_until_gone(read=read) == 404
    assert skills.delete(skill_name=renamed, team_id=team_id).status_code == 404
