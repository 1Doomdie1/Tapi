from tapi.utils.types     import *
from tapi.api.http.client import Client
from .runs                import RunsAPI
from ..note               import NotesAPI
from ..action.actions     import ActionsAPI
from .versions            import VersionsAPI
from .change_requests     import ChangeRequestAPI
from typing               import List, Optional, Dict, Any


class StoriesAPI(Client):

    def __init__(
            self,
            domain: str,
            apiKey: str
    ):
        super().__init__(domain, apiKey)
        self.base_endpoint  = "stories"
        self.runs           = RunsAPI(domain, apiKey)
        self.notes          = NotesAPI(domain, apiKey)
        self.actions        = ActionsAPI(domain, apiKey)
        self.versions       = VersionsAPI(domain, apiKey)
        self.change_request = ChangeRequestAPI(domain, apiKey)

    def create(
            self,
            team_id:         int,
            name:            Optional[str]           = None,
            description:     Optional[str]           = None,
            keep_events_for: Optional[KeepEventsFor] = KeepEventsFor.ONE_DAY,
            folder_id:       Optional[int]           = None,
            tags:            Optional[List[str]]     = None,
            disabled:        Optional[bool]          = False,
            priority:        Optional[bool]          = False
        ):
        return self._http_request(
            "POST",
            self.base_endpoint,
            json = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def get(
            self,
            story_id:   int,
            story_mode: Optional[StoryMode] = StoryMode.ALL
        ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{story_id}",
            json = {"story_mode": story_mode}
        )

    def update(
            self,
            story_id:                                      int,
            name:                                          Optional[str]                     = None,
            description:                                   Optional[str]                     = None,
            add_tag_names:                                 Optional[List[str]]               = None,
            remove_tag_names:                              Optional[List[str]]               = None,
            keep_events_for:                               Optional[KeepEventsFor]           = None,
            disabled:                                      Optional[bool]                    = None,
            locked:                                        Optional[bool]                    = None,
            priority:                                      Optional[bool]                    = None,
            send_to_story_access_source:                   Optional[SendToStoryAccessSource] = None,
            send_to_story_access:                          Optional[SendToStoryAccess]       = None,
            send_to_story_skill_use_requires_confirmation: Optional[bool]                    = None,
            entry_agent_id:                                Optional[int]                     = None,
            exit_agent_ids:                                Optional[int]                     = None,
            team_id:                                       Optional[int]                     = None,
            folder_id:                                     Optional[int]                     = None,
            change_control_enabled:                        Optional[bool]                    = None,
        ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{story_id}",
            json = {key: value for key, value in locals().items() if value is not None and key not in ("self", "story_id")}
        )

    def list(
            self,
            team_id:   Optional[int]                = None,
            folder_id: Optional[int]                = None,
            per_page:  Optional[int]                = 10,
            page:      Optional[int]                = 1,
            tags:      Optional[List[str]]          = None,
            filter:    Optional[Filter]             = None,
            order:     Optional[StoriesReturnOrder] = None,
        ):
        return self._http_request(
            "GET",
            self.base_endpoint,
            json = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def delete(
            self,
            story_id: int
        ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{story_id}"
        )

    def batch_delete(
            self,
            story_ids: List[int]
        ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/batch",
            json = {"ids": story_ids}
        )

    def export(
            self,
            story_id:       int,
            randomize_urls: Optional[bool] = True
        ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{story_id}/export",
            json = {"randomize_urls": randomize_urls}
        )

    def import_(
            self,
            new_name:  str,
            data:      Dict[str, Any],
            team_id:   int,
            folder_id: Optional[str]  = None,
            mode:      Optional[Mode] = Mode.NEW
        ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/import",
            json = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )
