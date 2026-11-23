import contextlib
import json
from email.message import Message
from typing import Any

from pydantic import BaseModel, ConfigDict

TEXT_MEDIA_TYPES = frozenset({"application/xml", "application/yaml", "application/x-yaml"})
TEXT_MEDIA_SUFFIXES = ("+xml", "+yaml")


class Response(BaseModel):
    """The result of one API call.

    Every HTTP status is returned as a ``Response``, including 4xx and 5xx. Inspect
    ``status_code`` to decide what to do with it.

    Printing a ``Response`` shows it as indented JSON.

    Attributes:
        status_code: The HTTP status code.
        data: The decoded body: parsed JSON for JSON content types, ``str`` for text content
            types, ``bytes`` for anything else and ``None`` when the body is empty.
        headers: The response headers, with lower-cased names.
    """

    model_config = ConfigDict(frozen=True)

    status_code: int
    data: Any
    headers: dict[str, str]

    def __str__(self) -> str:
        """Return the response as indented JSON, which is what ``print`` shows.

        Binary ``data`` cannot be written as JSON, so it is shown as its size, ``<7 bytes>``.
        """
        dumped = self.model_dump()
        if isinstance(dumped["data"], bytes):
            dumped["data"] = f"<{len(dumped['data'])} bytes>"
        return json.dumps(dumped, indent=2, ensure_ascii=False)


def decode_body(*, content: bytes, content_type: str | None) -> Any:
    """Decode a response body according to its content type.

    The body is decoded as JSON for JSON content types (``application/json`` and ``+json``
    types), and as text for ``text/*``, ``application/xml``, ``application/yaml`` and ``+xml`` or
    ``+yaml`` types. Text uses the charset from the content type, or UTF-8. Any other type is
    returned as the raw bytes. Without a content type the body is tried as JSON, then as UTF-8
    text. A body that does not match its declared type falls back to text and then to bytes.

    Args:
        content: The raw response body.
        content_type: The value of the ``Content-Type`` header, or ``None`` if it is missing.

    Returns:
        ``None`` for an empty body, otherwise parsed JSON, a ``str`` or the raw ``bytes``.
    """
    if not content:
        return None
    media_type, charset = _parse_content_type(content_type=content_type)
    if media_type is None or _is_json(media_type=media_type):
        with contextlib.suppress(ValueError):
            return json.loads(content)
    if media_type is None or _is_json(media_type=media_type) or _is_text(media_type=media_type):
        with contextlib.suppress(UnicodeDecodeError, LookupError):
            return content.decode(charset)
    return content


def _parse_content_type(*, content_type: str | None) -> tuple[str | None, str]:
    if not content_type:
        return None, "utf-8"
    message = Message()
    message["Content-Type"] = content_type
    return message.get_content_type(), message.get_content_charset("utf-8")


def _is_json(*, media_type: str) -> bool:
    return media_type == "application/json" or media_type.endswith("+json")


def _is_text(*, media_type: str) -> bool:
    return (
        media_type.startswith("text/")
        or media_type in TEXT_MEDIA_TYPES
        or media_type.endswith(TEXT_MEDIA_SUFFIXES)
    )
