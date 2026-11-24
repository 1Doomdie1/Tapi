from collections.abc import Generator

import httpx


class ApiKeyAuth(httpx.Auth):
    """Sends the Tines API key in the ``X-User-Token`` header of every request.

    Args:
        api_key: The Tines API key.
    """

    header_name = "X-User-Token"

    def __init__(self, *, api_key: str) -> None:
        self._api_key = api_key

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        request.headers[self.header_name] = self._api_key
        yield request

    def __repr__(self) -> str:
        return "ApiKeyAuth(api_key='***')"
