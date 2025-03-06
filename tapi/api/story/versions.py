from tapi.client import Client
from typing      import Optional


class VersionsAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "stories"

    def create(
            self,
            story_id: int,
            name:     Optional[str] = None
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{story_id}/versions",
            json={key: value for key, value in locals().items() if
                  value is not None and key not in ("self", "story_id")}
        )

    def get(
            self,
            story_id:   int,
            version_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{story_id}/versions/{version_id}"
        )

    def update(
            self,
            name:       str,
            story_id:   int,
            version_id: int
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{story_id}/versions/{version_id}",
            json={"name": name}
        )

    def list(
            self,
            story_id: int,
            per_page: int = 10,
            page:     int = 1,
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{story_id}/versions",
            json={key: value for key, value in locals().items() if
                  value is not None and key not in ("self", "story_id")}
        )

    def delete(
            self,
            story_id:   int,
            version_id: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{story_id}/versions/{version_id}"
        )
