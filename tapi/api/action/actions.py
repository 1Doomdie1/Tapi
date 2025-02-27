from tapi.client      import Client
from .logs            import ActionLogsAPI
from .events          import ActionEventsAPI
from tapi.utils.types import AgentType, StoryMode
from typing           import List, Dict, Any, Optional, Union


class ActionsAPI(Client):

    def __init__(self, domain: str,apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "actions"
        self.logs   = ActionLogsAPI(domain, apiKey)
        self.events = ActionEventsAPI(domain, apiKey)

    def create(
            self,
            type:                      Union[AgentType, str],
            name:                      str,
            options:                   Dict[str, Any],
            position:                  Dict[str, int],
            story_id:                  Optional[int]                              = None,
            group_id:                  Optional[int]                              = None,
            description:               Optional[str]                              = None,
            disabled:                  Optional[bool]                             = False,
            source_ids:                Optional[List[int]]                        = None,
            links_to_sources:          Optional[List[Dict[str, Union[str, int]]]] = None,
            receiver_ids:              Optional[List[int]]                        = None,
            links_to_receivers:        Optional[List[Dict[str, Union[str, int]]]] = None,
            schedule:                  Optional[List[Dict[str, str]]]             = None,
            monitor_failures:          Optional[bool]                             = True,
            monitor_all_events:        Optional[bool]                             = False,
            monitor_no_events_emitted: Optional[int]                              = None
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
            name:                      Optional[str]                              = None,
            description:               Optional[str]                              = None,
            options:                   Optional[Dict[str, Any]]                   = None,
            position:                  Optional[Dict[str, int]]                   = None,
            source_ids:                Optional[List[int]]                        = None,
            links_to_sources:          Optional[List[Dict[str, Union[int, str]]]] = None,
            receiver_ids:              Optional[List[str]]                        = None,
            links_to_receivers:        Optional[List[Dict[str, Union[int, str]]]] = None,
            schedule:                  Optional[Dict[str, Any]]                   = None,
            disabled:                  Optional[bool]                             = None,
            monitor_failures:          Optional[bool]                             = None,
            monitor_all_events:        Optional[bool]                             = None,
            monitor_no_events_emitted: Optional[int]                              = None
    ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{action_id}",
            json = {key: value for key, value in locals().items()
                    if value is not None and key not in ("self", "action_id")}
        )

    def list(
            self,
            story_id:   Optional[int]       = None,
            story_mode: Optional[StoryMode] = None,
            team_id:    Optional[int]       = None,
            group_id:   Optional[int]       = None,
            per_page:   int                 = 10,
            page:       int                 = 1
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
