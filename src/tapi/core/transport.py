from collections.abc import Mapping
from typing import Any

import httpx

from tapi.core.auth import ApiKeyAuth
from tapi.core.exceptions import TinesConnectionError
from tapi.core.response import Response, decode_body


class Transport:
    """Sends HTTP requests to one Tines tenant and wraps every reply in a ``Response``.

    The transport does not retry, follow redirects or treat any status code as an error.

    Args:
        base_url: The tenant root URL, for example ``https://acme.tines.com``.
        api_key: The Tines API key.
        timeout: Seconds to wait for the connection and for each part of the reply.

    The attribute of the transport is:

    - ``base_url``: The tenant root URL it sends requests to.
    """

    def __init__(self, *, base_url: str, api_key: str, timeout: float = 30.0) -> None:
        self.base_url = base_url
        self._client = httpx.Client(
            base_url=base_url,
            auth=ApiKeyAuth(api_key=api_key),
            timeout=timeout,
        )

    def request(
        self,
        *,
        method: str,
        path: str,
        params: Mapping[str, Any] | None = None,
        json: Any = None,
        headers: Mapping[str, str] | None = None,
    ) -> Response:
        """Send one request.

        Args:
            method: The HTTP method, such as ``GET`` or ``POST``.
            path: The path on the tenant, such as ``/api/v1/tags``.
            params: Query string parameters. Values must not be ``None``.
            json: A value to send as the JSON request body.
            headers: Extra request headers, such as ``Idempotency-Key``.

        Returns:
            The reply, whatever its status code.

        Raises:
            TinesConnectionError: If no reply was received because the connection was refused,
                failed or timed out.
        """
        try:
            reply = self._client.request(
                method=method, url=path, params=params, json=json, headers=headers
            )
        except httpx.TransportError as error:
            raise TinesConnectionError(f"Could not reach {self.base_url}: {error}") from error
        return Response(
            status_code=reply.status_code,
            data=decode_body(
                content=reply.content,
                content_type=reply.headers.get("content-type"),
            ),
            headers=dict(reply.headers.items()),
        )

    def close(self) -> None:
        """Close the underlying connections."""
        self._client.close()
