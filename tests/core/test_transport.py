import json

import httpx
import pytest

from tapi.core import Response, TinesConnectionError, TinesError


def test_request_authenticates_and_returns_status_data_and_lower_cased_headers(
    transport, router, api_key
):
    route = router.get("/api/v1/tags").mock(
        return_value=httpx.Response(200, json={"tags": []}, headers={"X-Request-Id": "abc"})
    )

    response = transport.request(method="GET", path="/api/v1/tags")

    assert route.calls.last.request.headers["x-user-token"] == api_key
    assert isinstance(response, Response)
    assert response.status_code == 200
    assert response.data == {"tags": []}
    assert response.headers["x-request-id"] == "abc"


def test_query_parameters_and_json_body_are_sent(transport, router):
    route = router.post("/api/v1/tags").mock(return_value=httpx.Response(201, json={"id": 1}))

    transport.request(
        method="POST", path="/api/v1/tags", params={"team_id": 3}, json={"name": "phishing"}
    )

    request = route.calls.last.request
    assert request.url.params["team_id"] == "3"
    assert json.loads(request.content) == {"name": "phishing"}


def test_extra_headers_are_sent_beside_the_api_key(transport, router, api_key):
    route = router.post("/api/v2/records").mock(return_value=httpx.Response(201, json={}))

    transport.request(method="POST", path="/api/v2/records", headers={"Idempotency-Key": "once"})

    request = route.calls.last.request
    assert request.headers["idempotency-key"] == "once"
    assert request.headers["x-user-token"] == api_key


@pytest.mark.parametrize(
    ("status", "kwargs"),
    [
        pytest.param(404, {"json": ["Tag not found"]}, id="404 json"),
        pytest.param(500, {"json": {"errors": [{"message": "boom"}]}}, id="500 json"),
        pytest.param(
            429,
            {"text": "Too many requests", "headers": {"Retry-After": "30"}},
            id="429 text with Retry-After",
        ),
    ],
)
def test_non_2xx_replies_are_returned_not_raised_nor_retried(transport, router, status, kwargs):
    route = router.get("/api/v1/tags/9").mock(return_value=httpx.Response(status, **kwargs))

    response = transport.request(method="GET", path="/api/v1/tags/9")

    assert response.status_code == status
    assert response.data == (kwargs.get("json") or kwargs["text"])
    assert route.call_count == 1
    if "headers" in kwargs:
        assert response.headers["retry-after"] == "30"


def test_redirects_are_returned_not_followed(transport, router):
    route = router.get("/api/v1/tags").mock(
        return_value=httpx.Response(302, headers={"Location": "https://elsewhere.example/tags"})
    )

    response = transport.request(method="GET", path="/api/v1/tags")

    assert response.status_code == 302
    assert response.headers["location"] == "https://elsewhere.example/tags"
    assert route.call_count == 1


def test_empty_body_gives_none(transport, router):
    router.delete("/api/v1/tags/9").mock(return_value=httpx.Response(204))

    assert transport.request(method="DELETE", path="/api/v1/tags/9").data is None


@pytest.mark.parametrize(
    "error",
    [
        pytest.param(httpx.ConnectError("refused"), id="refused"),
        pytest.param(httpx.ReadTimeout("slow"), id="timeout"),
    ],
)
def test_connection_failures_raise_tines_connection_error(transport, router, error):
    router.get("/api/v1/tags").mock(side_effect=error)

    with pytest.raises(TinesConnectionError) as raised:
        transport.request(method="GET", path="/api/v1/tags")

    assert raised.value.__cause__ is error
    assert isinstance(raised.value, TinesError)
    assert "acme.tines.com" in str(raised.value)
