from tapi.http.client import Client
from .logs            import ActionLogsAPI
from .events          import ActionEventsAPI
from typing           import List, Dict, Any
from tapi.utils.types import ActionType, StoryMode


class ActionsAPI(Client):

    def __init__(self, domain: str,apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "/actions"
        self.logs   = ActionLogsAPI(domain, apiKey)
        self.events = ActionEventsAPI(domain, apiKey)

    def create(
            self,
            type:                      ActionType                 | str,
            name:                      str,
            options:                   Dict[str, Any],
            position:                  Dict[str, int],
            story_id:                  int                        | None = None,
            group_id:                  int                        | None = None,
            description:               str                        | None = None,
            disabled:                  bool                              = False,
            source_ids:                List[int]                  | None = None,
            links_to_sources:          List[Dict[str, str | int]] | None = None,
            receiver_ids:              List[int]                  | None = None,
            links_to_receivers:        List[Dict[str, str | int]] | None = None,
            schedule:                  List[Dict[str, str]]       | None = None,
            monitor_failures:          bool                              = True,
            monitor_all_events:        bool                              = False,
            monitor_no_events_emitted: int                        | None = None
    ):
        return self._http_request(
            "POST",
            self.base_endpoint,
            json = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def get(
            self,
            action_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{action_id}"
        )

    def update(
            self,
            action_id:                 int,
            name:                      str                        | None = None,
            description:               str                        | None = None,
            options:                   Dict[str, Any]             | None = None,
            position:                  Dict[str, int]             | None = None,
            source_ids:                List[int]                  | None = None,
            links_to_sources:          List[Dict[str, int | str]] | None = None,
            receiver_ids:              List[str]                  | None = None,
            links_to_receivers:        List[Dict[str, int | str]] | None = None,
            schedule:                  Dict[str, Any]             | None = None,
            disabled:                  bool                       | None = None,
            monitor_failures:          bool                       | None = None,
            monitor_all_events:        bool                       | None = None,
            monitor_no_events_emitted: int                        | None = None
    ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{action_id}",
            json = {key: value for key, value in locals().items()
                    if value is not None and key not in ("self", action_id)}
        )

    def list(
            self,
            story_id:   int       | None = None,
            story_mode: StoryMode | None = None,
            team_id:    int       | None = None,
            group_id:   int       | None = None,
            per_page:   int              = 10,
            page:       int              = 1
    ):
        return self._http_request(
            "GET",
            self.base_endpoint,
            params = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def delete(
            self,
            action_id: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{action_id}"
        )

    def clear_memory(
            self,
            action_id: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{action_id}/clear_memory"
        )
