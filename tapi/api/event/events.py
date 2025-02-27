from tapi.client import Client
from typing      import Optional


class EventsAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "events"

    def get(
            self,
            event_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{event_id}"
        )

    def list(
            self,
            since_id:       Optional[int]  = None,
            until_id:       Optional[int]  = None,
            since:          Optional[str]  = None,
            until:          Optional[str]  = None,
            team_id:        Optional[int]  = None,
            story_id:       Optional[int]  = None,
            include_groups: Optional[bool] = None,
            per_page:       int            = 10,
            page:           int            = 1,
    ):
        return self._http_request(
            "GET",
            self.base_endpoint,
            params = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def re_emit(
            self,
            event_id: int
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{event_id}/reemit"
        )
