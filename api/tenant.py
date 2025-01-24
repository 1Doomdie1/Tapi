from .client import Client


class TenantAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)

    def info(self) -> dict:
        return self._http_request("GET", "/info").json()