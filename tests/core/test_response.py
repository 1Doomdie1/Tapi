import json

import pytest
from pydantic import ValidationError

from tapi.core.response import Response, decode_body


def test_response_has_exactly_three_fields_and_is_immutable():
    response = Response(status_code=200, data=None, headers={})

    assert set(Response.model_fields) == {"status_code", "data", "headers"}
    with pytest.raises(ValidationError):
        response.status_code = 404


def test_str_is_indented_json():
    response = Response(status_code=200, data={"a": 1}, headers={"x": "y"})

    assert (
        str(response)
        == """\
{
  "status_code": 200,
  "data": {
    "a": 1
  },
  "headers": {
    "x": "y"
  }
}"""
    )


def test_binary_data_is_shown_as_its_size_and_kept_as_bytes():
    response = Response(status_code=200, data=b"\x89PNG\r\n", headers={})

    assert json.loads(str(response))["data"] == "<6 bytes>"
    assert response.data == b"\x89PNG\r\n"


def test_non_ascii_text_stays_readable():
    assert "café" in str(Response(status_code=200, data="café", headers={}))


@pytest.mark.parametrize(
    ("content", "content_type", "expected"),
    [
        pytest.param(b"", "application/json", None, id="empty body"),
        pytest.param(b'{"id": 1}', "application/json", {"id": 1}, id="json"),
        pytest.param(b"[1, 2]", "application/json; charset=utf-8", [1, 2], id="json with charset"),
        pytest.param(b'{"a": 1}', "application/problem+json", {"a": 1}, id="+json type"),
        pytest.param(b"plain words", "text/plain", "plain words", id="text"),
        pytest.param(b"<svg/>", "image/svg+xml", "<svg/>", id="+xml type"),
        pytest.param(b"caf\xe9", "text/plain; charset=latin-1", "café", id="declared charset"),
        pytest.param(b"\x89PNG\r\n", "image/png", b"\x89PNG\r\n", id="image"),
        pytest.param(b"\x00\x01", "application/octet-stream", b"\x00\x01", id="binary"),
        pytest.param(b"not json", "application/json", "not json", id="invalid json is text"),
        pytest.param(b"\xff\xff", "application/json", b"\xff\xff", id="undecodable is bytes"),
        pytest.param(b'{"a": 1}', None, {"a": 1}, id="no content type, json"),
        pytest.param(b"plain", None, "plain", id="no content type, text"),
        pytest.param(b"\xff\xff\xff", None, b"\xff\xff\xff", id="no content type, binary"),
    ],
)
def test_decode_body(content, content_type, expected):
    assert decode_body(content=content, content_type=content_type) == expected
