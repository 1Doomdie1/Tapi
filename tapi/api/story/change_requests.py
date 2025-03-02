from tapi.client import Client
from typing      import Optional


class ChangeRequestAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "stories"

    def create(
            self,
            story_id:    int,
            title:       Optional[str] = None,
            description: Optional[str] = None
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{story_id}/change_request",
            json={key: value for key, value in locals().items() if
                  value is not None and key not in ("self", "story_id")}
        )

    def approve(
            self,
            story_id:          int,
            change_request_id: int
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{story_id}/change_request/approve",
            json={"change_request_id": change_request_id}
        )

    def cancel(
            self,
            story_id:          int,
            change_request_id: int
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{story_id}/change_request/cancel",
            json={"change_request_id": change_request_id}
        )

    def promote(
            self,
            story_id:          int,
            change_request_id: int
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{story_id}/change_request/promote",
            json={"change_request_id": change_request_id}
        )

    def view(
            self,
            story_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{story_id}/change_request/view"
        )

