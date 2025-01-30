from tapi.utils.types import HTTPResponse
from requests         import request, RequestException

class Client:
    verify_ssl: bool = True

    def __init__(self, domain: str, apiKey) -> None:
        self.domain = domain
        self.apiKey = apiKey

    def _http_request(
            self, 
            method:      str,
            endpoint:    str,
            api_version: str = "v1",
            **kwargs
        ) -> HTTPResponse:
        url = f"https://{self.domain}.tines.com/api/{api_version}/{endpoint}"
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.apiKey}"

        try:
            response = request(method, url, headers=headers, verify=Client.verify_ssl, **kwargs)

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
