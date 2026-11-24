import time
import uuid
from collections.abc import Callable, Mapping
from typing import Any

from tapi import Response

PREFIX = "tapi-live-check"
DOMAIN_VARIABLE = "TINES_TEST_TENANT_DOMAIN"
KEY_VARIABLE = "TINES_TEST_API_KEY"
TEAM_VARIABLE = "TINES_TEST_TEAM_ID"
CONFIRM_VARIABLE = "TINES_TEST_CONFIRM_WRITES"

TEAM = "the team of the run"

COLLECTIONS = (
    ("tags.list", "tags", {}),
    ("folders.list", "folders", {}),
    ("resources.list", "global_resources", {}),
    ("credentials.list", "user_credentials", {}),
    ("teams.list", "teams", {"scope": "all"}),
    ("stories.list", "stories", {}),
    ("cases.list", "cases", {}),
    ("cases.fields.list", "case_inputs", {}),
    ("cases.statuses.list", "case_sub_statuses", {"team_id": TEAM}),
    ("cases.templates.list", "case_templates", {"team_id": TEAM}),
    ("cases.webhooks.list", "webhooks", {}),
    ("dashboards.list", "dashboards", {}),
    ("skills.list", "skills", {}),
    ("admin.roles.list", "admin/roles", {}),
    ("admin.templates.list", "admin/templates", {}),
    ("admin.users.list", "admin/users", {}),
)


def check(*, reply: Response, status: int) -> Any:
    assert reply.status_code == status, (
        f"expected {status}, got {reply.status_code}: {reply.data!r}"
    )
    return reply.data


def throwaway(*, kind: str) -> str:
    return f"{PREFIX}-{kind}-{uuid.uuid4().hex[:8]}"


def all_items(
    *,
    method: Callable[..., Response],
    key: str,
    arguments: Mapping[str, Any] | None = None,
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    page: int | None = 1
    while page is not None:
        data = check(reply=method(**(arguments or {}), per_page=100, page=page), status=200)
        items += data[key]
        page = data["meta"]["next_page_number"]
    return items


def all_cursor_items(
    *,
    method: Callable[..., Response],
    key: str = "data",
    arguments: Mapping[str, Any] | None = None,
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    token: str | None = None
    while True:
        extra = {"after": token} if token else {}
        data = check(reply=method(**(arguments or {}), limit=100, **extra), status=200)
        items += data[key]
        token = data["page"].get("next_page_token")
        if not token:
            return items


def wait_until_gone(*, read: Callable[[], Response], timeout: float = 30.0) -> int:
    deadline = time.monotonic() + timeout
    while True:
        status = read().status_code
        if status == 404 or time.monotonic() >= deadline:
            return status
        time.sleep(1)


def wait_for(*, condition: Callable[[], bool], timeout: float = 30.0) -> bool:
    deadline = time.monotonic() + timeout
    while True:
        if condition():
            return True
        if time.monotonic() >= deadline:
            return False
        time.sleep(1)


class Cleanup:
    def __init__(self) -> None:
        self._actions: list[tuple[str, Callable[[], Response]]] = []

    def add(self, *, description: str, action: Callable[[], Response]) -> None:
        self._actions.append((description, action))

    def run(self) -> list[str]:
        failures = []
        for description, action in reversed(self._actions):
            try:
                reply = action()
            except Exception as error:
                failures.append(f"{description}: {type(error).__name__}")
                continue
            if reply.status_code not in (200, 204, 404):
                failures.append(f"{description}: status {reply.status_code}")
        return failures
