import httpx
import pytest

import tapi
from tapi import Tines, TinesConfigurationError, TinesConnectionError, TinesError
from tests.support import public_methods


def test_client_builds_the_tenant_url_and_hides_the_api_key():
    with Tines(tenant_domain="acme.tines.com", api_key="super-secret") as client:
        assert repr(client) == "Tines(base_url='https://acme.tines.com')"


def test_client_reads_its_configuration_from_the_environment(monkeypatch):
    monkeypatch.setenv("TINES_TENANT_DOMAIN", "env.tines.com")
    monkeypatch.setenv("TINES_API_KEY", "env-key")

    with Tines() as client:
        assert repr(client) == "Tines(base_url='https://env.tines.com')"


@pytest.mark.parametrize(
    "arguments", [{"api_key": "key"}, {"tenant_domain": "acme.tines.com"}], ids=["domain", "key"]
)
def test_client_requires_a_tenant_domain_and_an_api_key(arguments):
    with pytest.raises(TinesConfigurationError):
        Tines(**arguments)


def test_timeout_is_applied_to_the_http_client(api_key):
    with Tines(tenant_domain="acme.tines.com", api_key=api_key, timeout=7) as client:
        assert client._transport._client.timeout == httpx.Timeout(7)


def test_the_context_manager_closes_the_client(api_key):
    with Tines(tenant_domain="acme.tines.com", api_key=api_key) as client:
        assert not client._transport._client.is_closed

    assert client._transport._client.is_closed


def test_public_api_is_exported_from_the_package():
    assert set(tapi.__all__) == {
        "Response",
        "Tines",
        "TinesConfigurationError",
        "TinesConnectionError",
        "TinesError",
    }
    assert issubclass(TinesConfigurationError, TinesError)
    assert issubclass(TinesConnectionError, TinesError)


def test_every_area_shares_the_clients_transport(tines):
    areas = {method.__self__ for method in public_methods(tines=tines).values()}

    assert areas
    assert all(getattr(area, "_transport", tines._transport) is tines._transport for area in areas)


def test_a_call_through_the_client_authenticates_and_returns_the_reply(tines, router, api_key):
    route = router.get("/api/v1/info").mock(return_value=httpx.Response(200, json={"stack": {}}))

    response = tines.info.get()

    assert response.data == {"stack": {}}
    assert route.calls.last.request.headers["x-user-token"] == api_key


def test_a_connection_failure_is_raised_through_the_client(tines, router):
    router.get("/api/v1/info").mock(side_effect=httpx.ConnectError("refused"))

    with pytest.raises(TinesConnectionError):
        tines.info.get()
