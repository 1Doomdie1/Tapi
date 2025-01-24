from requests import Response, request


class Client:
    def __init__(self, domain: str, apiKey) -> None:
        self.base_url = f"https://{domain}.tines.com/api/v1" 
        self.apiKey = apiKey

    def _http_request(self, 
        method: str, 
        endpoint: str, 
        **kwargs
        ) -> Response:

        headers = {
            "Authorization": f"Bearer {self.apiKey}",
            **kwargs.get("headers", {})
        }

        return request(method, f"{self.base_url}{endpoint}", headers=headers, **kwargs)