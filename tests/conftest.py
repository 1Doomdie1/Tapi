import contextlib
from collections.abc import Iterator

import pytest
import respx

from tapi import Tines
from tapi.core import Transport


@pytest.fixture(autouse=True)
def isolated_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TINES_TENANT_DOMAIN", raising=False)
    monkeypatch.delenv("TINES_API_KEY", raising=False)


@pytest.fixture
def api_key() -> str:
    return "test-api-key"


@pytest.fixture
def base_url() -> str:
    return "https://acme.tines.com"


@pytest.fixture
def router(base_url: str) -> Iterator[respx.MockRouter]:
    with respx.mock(base_url=base_url, assert_all_called=False) as mock:
        yield mock


@pytest.fixture
def transport(router: respx.MockRouter, base_url: str, api_key: str) -> Iterator[Transport]:
    with contextlib.closing(Transport(base_url=base_url, api_key=api_key)) as instance:
        yield instance


@pytest.fixture
def tines(router: respx.MockRouter, api_key: str) -> Iterator[Tines]:
    with Tines(tenant_domain="acme.tines.com", api_key=api_key) as client:
        yield client
