from utils.types import HTTPResponse
from requests    import request, RequestException

class Client:
    def __init__(self, domain: str, apiKey) -> None:
        self.base_url = f"https://{domain}.tines.com/api/v1" 
        self.apiKey   = apiKey

    def _http_request(
            self, 
            method:   str, 
            endpoint: str, 
            **kwargs
        ) -> HTTPResponse:
        url = f"{self.base_url}/{endpoint}"
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.apiKey}"

        try:
            response = request(method, url, headers=headers, **kwargs)

            return {
                "body": response.json() if "application/json" in response.headers.get("Content-Type", "") else response.text,
                "headers": dict(response.headers),
                "status_code": response.status_code
            }

        except RequestException as e:
            return {
                "body": str(e),
                "headers": {},
                "status_code": 500
            }
