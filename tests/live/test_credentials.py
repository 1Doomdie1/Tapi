from datetime import UTC, datetime, timedelta

import pytest

from tests.live.helpers import all_items, check, throwaway, wait_until_gone

pytestmark = pytest.mark.writes

SECRET = "tapi-throwaway-placeholder"
NEW_SECRET = "tapi-throwaway-placeholder-2"


def test_a_credential_is_created_read_listed_updated_and_deleted(live, team_id, cleanup):
    name = throwaway(kind="credential")
    created = check(
        reply=live.credentials.create(
            name=name,
            mode="TEXT",
            team_id=team_id,
            value=SECRET,
            description="Throwaway credential from a live check.",
        ),
        status=201,
    )
    credential_id = created["id"]
    cleanup.add(
        description=f"credential {credential_id}",
        action=lambda: live.credentials.delete(credential_id=credential_id),
    )

    assert created["name"] == name
    assert created["mode"] == "TEXT"
    assert created["team_id"] == team_id
    assert SECRET not in str(created)
    fetched = check(reply=live.credentials.get(credential_id=credential_id), status=200)
    assert fetched["id"] == credential_id
    assert SECRET not in str(fetched)
    listed = all_items(method=live.credentials.list, key="user_credentials")
    assert credential_id in [credential["id"] for credential in listed]

    described = check(
        reply=live.credentials.update(
            credential_id=credential_id, mode="TEXT", description="Updated by a live check."
        ),
        status=200,
    )
    assert described["description"] == "Updated by a live check."
    assert described["name"] == name

    expires = datetime.now(UTC) + timedelta(days=30)
    changed = check(
        reply=live.credentials.update(
            credential_id=credential_id,
            mode="TEXT",
            name=f"{name}-renamed",
            value=NEW_SECRET,
            allowed_hosts=["example.com"],
            expires_at=expires,
            expiry_notifications_enabled=False,
        ),
        status=200,
    )
    assert changed["name"] == f"{name}-renamed"
    assert changed["allowed_hosts"] == ["example.com"]
    assert changed["expires_at"] is not None
    assert changed["expiry_notifications_enabled"] is False
    assert NEW_SECRET not in str(changed)

    check(reply=live.credentials.delete(credential_id=credential_id), status=204)
    assert wait_until_gone(read=lambda: live.credentials.get(credential_id=credential_id)) == 404
