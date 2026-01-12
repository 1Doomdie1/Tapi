from tapi.utils.types import *
from tapi.client      import Client
from .runs            import RunsAPI
from ..note           import NotesAPI
from .groups          import GroupsAPI
from .drafts          import DraftsAPI
from .owners          import OwnersAPI
from ..action.actions import ActionsAPI
from .versions        import VersionsAPI
from .recipients      import RecipientsAPI
from .change_requests import ChangeRequestAPI
from typing           import List, Optional, Dict, Any


class StoriesAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint  = "stories"
        self.runs           = RunsAPI(domain, apiKey)
        self.notes          = NotesAPI(domain, apiKey)
        self.groups         = GroupsAPI(domain, apiKey)
        self.drafts         = DraftsAPI(domain, apiKey)
        self.owners         = OwnersAPI(domain, apiKey)
        self.actions        = ActionsAPI(domain, apiKey)
        self.versions       = VersionsAPI(domain, apiKey)
        self.recipients     = RecipientsAPI(domain, apiKey)
        self.change_request = ChangeRequestAPI(domain, apiKey)

    def create(
            self,
            team_id:         int,
            name:            Optional[str]             = None,
            description:     Optional[str]             = None,
            keep_events_for: Union[KeepEventsFor, int] = KeepEventsFor.ONE_DAY,
            folder_id:       Optional[int]             = None,
            tags:            Optional[List[str]]       = None,
            disabled:        bool                      = False,
            priority:        bool                      = False
        ):
        return self._http_request(
            "POST",
            self.base_endpoint,
            json = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def get(
            self,
            story_id:              int,
            story_mode:            Union[StoryMode, str] = StoryMode.ALL,
            draft_id:              Optional[int]         = None,
            include_live_activity: Optional[bool]        = None
        ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{story_id}",
            params = {key: value for key, value in locals().items() if value is not None and key not in ("self", "story_id")}
        )

    def update(
            self,
            story_id:                                      int,
            name:                                          Optional[str]                                 = None,
            description:                                   Optional[str]                                 = None,
            add_tag_names:                                 Optional[List[str]]                           = None,
            remove_tag_names:                              Optional[List[str]]                           = None,
            keep_events_for:                               Optional[Union[KeepEventsFor, str]]           = None,
            disabled:                                      Optional[bool]                                = None,
            locked:                                        Optional[bool]                                = None,
            priority:                                      Optional[bool]                                = None,
            webhook_api_enabled:                           Optional[bool]                                = None,
            api_entry_action_id:                           Optional[int]                                 = None,
            api_exit_action_ids:                           Optional[List[int]]                           = None,
            send_to_story_access_source:                   Optional[Union[SendToStoryAccessSource, str]] = None,
            entry_action_id:                               Optional[int]                                 = None,
            exit_action_id:                                Optional[int]                                 = None,
            send_to_story_access:                          Optional[Union[SendToStoryAccess, str]]       = None,
            shared_team_slugs:                             Optional[List[str]]                           = None,
            send_to_story_skill_use_requires_confirmation: Optional[bool]                                = None,
            team_id:                                       Optional[int]                                 = None,
            folder_id:                                     Optional[int]                                 = None,
            change_control_enabled:                        Optional[bool]                                = None,
            draft_id:                                      Optional[int]                                 = None,
            monitor_failures:                              Optional[bool]                                = None
        ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{story_id}",
            json = {key: value for key, value in locals().items() if value is not None and key not in ("self", "story_id")}
        )

    def list(
            self,
            team_id:               Optional[int]                            = None,
            folder_id:             Optional[int]                            = None,
            per_page:              int                                      = 10,
            page:                  int                                      = 1,
            tags:                  Optional[List[str]]                      = None,
            search:                Optional[str]                            = None,
            filter:                Optional[Union[Filter, str]]             = None,
            order:                 Optional[Union[StoriesReturnOrder, str]] = None,
            include_live_activity: Optional[bool]                           = None
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
            randomize_urls: Optional[bool] = True,
            draft_id:       Optional[int]  = None,
        ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{story_id}/export",
            json = {
                "randomize_urls": randomize_urls,
                "draft_id": draft_id
            }
        )

    def import_(
            self,
            new_name:  str,
            data:      Dict[str, Any],
            team_id:   int,
            folder_id: Optional[int]    = None,
            mode:      Union[Mode, str] = Mode.NEW
        ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/import",
            json = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def disable(
            self,
            id:       int,
            disabled: bool
        ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{id}/disable",
            json = {"disabled": disabled}
        )
    
    def list_pending_actions(
            self,
            story_id:   int,
            search:     Optional[str]                     = None,
            story_mode: Optional[Literal["LIVE", "TEST"]] = "LIVE",
            per_page:   int                               = 10,
            page:       int                               = 1,
            draft_id:   Optional[int]                     = None
        ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{story_id}/pending_actions",
            json = {
                "search":   search,
                "draft_id": draft_id
            },
            params = {
                "page":       page,
                "per_page":   per_page,
                "story_mode": story_mode,
            }
        )
