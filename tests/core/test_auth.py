import httpx

from tapi.core.auth import ApiKeyAuth


def authenticate(*, auth):
    request = httpx.Request("GET", "https://acme.tines.com/api/v1/tags")
    next(auth.auth_flow(request))
    return request


def test_api_key_is_sent_in_the_x_user_token_header():
    request = authenticate(auth=ApiKeyAuth(api_key="secret"))

    assert request.headers["X-User-Token"] == "secret"
    assert "Authorization" not in request.headers


def test_repr_does_not_reveal_the_api_key():
    assert "secret" not in repr(ApiKeyAuth(api_key="secret"))
