import pytest

from tapi.core.config import resolve_api_key, resolve_base_url
from tapi.core.exceptions import TinesConfigurationError


@pytest.mark.parametrize(
    "value", ["acme.tines.com", "https://acme.tines.com/api/v1", "  acme.tines.com/  "]
)
def test_tenant_domain_becomes_a_root_url(value):
    assert resolve_base_url(tenant_domain=value) == "https://acme.tines.com"


def test_http_scheme_and_port_are_preserved():
    assert resolve_base_url(tenant_domain="http://localhost:3000") == "http://localhost:3000"


def test_an_argument_wins_over_the_environment_and_the_environment_is_the_fallback(monkeypatch):
    monkeypatch.setenv("TINES_TENANT_DOMAIN", "env.tines.com")
    monkeypatch.setenv("TINES_API_KEY", "from-env")

    assert resolve_base_url(tenant_domain=None) == "https://env.tines.com"
    assert resolve_base_url(tenant_domain="acme.tines.com") == "https://acme.tines.com"
    assert resolve_api_key(api_key=None) == "from-env"
    assert resolve_api_key(api_key="explicit") == "explicit"


def test_missing_values_are_rejected():
    with pytest.raises(TinesConfigurationError, match="TINES_TENANT_DOMAIN"):
        resolve_base_url(tenant_domain=None)
    with pytest.raises(TinesConfigurationError, match="TINES_API_KEY"):
        resolve_api_key(api_key=None)


@pytest.mark.parametrize("value", ["ftp://acme.tines.com", "https://", "   "])
def test_invalid_tenant_domain_is_rejected(value):
    with pytest.raises(TinesConfigurationError):
        resolve_base_url(tenant_domain=value)


def test_api_key_is_stripped():
    assert resolve_api_key(api_key="  secret \n") == "secret"
