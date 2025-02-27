from tapi.utils.types import HTTPResponse
from typing           import Optional, Union, Dict, Any
from requests         import request, RequestException, Response


class Client:
    verify_ssl: bool = True

    def __init__(self, domain: str, apiKey: str) -> None:
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
        headers = {**kwargs.pop("headers", {}), "Authorization": f"Bearer {self.apiKey}"}

        try:
            response = request(method, url, headers=headers, verify=Client.verify_ssl, **kwargs)

            return {
                "body": self._parse_body(response),
                "headers": dict(response.headers),
                "status_code": response.status_code
            }

        except RequestException as e:
            return {
                "body": str(e),
                "headers": {},
                "status_code": 500
            }

    def _parse_body(
            self,
            response: Response
    ) -> Union[Dict[str, Any], str, bytes]:
        content_type = response.headers.get("Content-Type", "")

        if "application/json" in content_type:
            body = response.json()
        elif "application/pdf" in content_type:
            body = response.content
        else:
            body = response.text

        return body