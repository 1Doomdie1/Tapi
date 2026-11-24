import os
from collections.abc import Iterator
from pathlib import Path

import pytest

from tapi import Tines
from tests.live.helpers import (
    COLLECTIONS,
    CONFIRM_VARIABLE,
    DOMAIN_VARIABLE,
    KEY_VARIABLE,
    PREFIX,
    TEAM,
    TEAM_VARIABLE,
    Cleanup,
    all_items,
)
from tests.support import resolve

LIVE_DIRECTORY = Path(__file__).parent


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        if LIVE_DIRECTORY in item.path.parents:
            item.add_marker(pytest.mark.live)


@pytest.fixture(autouse=True)
def _writes_need_confirmation(request: pytest.FixtureRequest) -> None:
    if request.node.get_closest_marker("writes") is None:
        return
    domain = os.environ.get(DOMAIN_VARIABLE, "")
    if not domain or os.environ.get(CONFIRM_VARIABLE) != domain:
        pytest.skip(f"set {CONFIRM_VARIABLE} to the test tenant's domain to allow writes")


@pytest.fixture(scope="session")
def live() -> Iterator[Tines]:
    domain = os.environ.get(DOMAIN_VARIABLE)
    key = os.environ.get(KEY_VARIABLE)
    if not domain or not key:
        pytest.skip(f"set {DOMAIN_VARIABLE} and {KEY_VARIABLE} to run the live tests")
    with Tines(tenant_domain=domain, api_key=key, timeout=120) as client:
        yield client


@pytest.fixture(scope="session")
def team_id(live: Tines) -> int:
    configured = os.environ.get(TEAM_VARIABLE)
    if configured:
        return int(configured)
    reply = live.teams.list(scope="standard")
    teams = reply.data["teams"] if reply.status_code == 200 else []
    if not teams:
        pytest.skip("the test tenant has no standard team")
    return int(teams[0]["id"])


@pytest.fixture(scope="session")
def no_leftovers(live: Tines, team_id: int) -> None:
    found = []
    for target, key, arguments in COLLECTIONS:
        method = resolve(tines=live, target=target)
        filled = {name: team_id if value == TEAM else value for name, value in arguments.items()}
        for item in all_items(method=method, key=key, arguments=filled):
            label = str(item.get("name") or item.get("email") or "")
            if label.startswith(PREFIX):
                found.append(f"{target.split('.')[0]} {item.get('id', item.get('case_id'))}")
    if found:
        pytest.exit(
            f"throwaway objects of an earlier run are still on the test tenant: {', '.join(found)}."
            " Delete them and run again.",
            returncode=2,
        )


@pytest.fixture
def cleanup(live: Tines, no_leftovers: None) -> Iterator[Cleanup]:
    registry = Cleanup()
    yield registry
    failures = registry.run()
    assert not failures, f"throwaway objects were not cleaned up: {failures}"
