from tapi.http.client import Client
from typing           import Optional


class ActionEventsAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "actions"

    def list(
            self,
            action_id: Optional[int] = None,
            since_id:  Optional[int] = None,
            until_id:  Optional[int] = None,
            per_page:  Optional[int] = 10,
            page:      Optional[int] = 11
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{action_id}/events",
            params = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def delete(
            self,
            action_id:      int,
            async_deletion: Optional[bool] = True
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{action_id}/remove_events",
            json = {"async_deletion": async_deletion}
        )
