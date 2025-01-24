from utils.types import *
from typing      import List
from .client     import Client


class StoriesAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "/stories"
        self.runs = RunsAPI(domain, apiKey)
        self.versions = Versions(domain, apiKey)
        self.change_request = ChangeRequestAPI(domain, apiKey)

    def create(
            self,
            team_id:         int,
            name:            str           | None = None,
            description:     str           | None = "Created With Tines CLI",
            keep_events_for: KeepEventsFor | None = KeepEventsFor.ONE_DAY,
            folder_id:       int           | None = None,
            tags:            List[str]     | None = None,
            disabled:        bool                 = False,
            priority:        bool                 = False
        ):
        return self._http_request(
            "POST",
            self.base_endpoint,
            json = {key: value for key, value in locals().items() if value != None and key not in ("self")}
        )

    def get(
            self,
            story_id:   int,
            story_mode: StoryMode = StoryMode.ALL
        ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{story_id}",
            json = {"story_mode": story_mode}
        )

    def update(
            self,
            story_id:                                      int,
            name:                                          str                     | None = None,
            description:                                   str                     | None = None,
            add_tag_names:                                 List[str]               | None = None,
            remove_tag_names:                              List[str]               | None = None,
            keep_events_for:                               KeepEventsFor           | None = None,
            disabled:                                      bool                    | None = None,
            locked:                                        bool                    | None = None,
            priority:                                      bool                    | None = None,
            send_to_story_access_source:                   SendToStoryAccessSource | None = None,
            send_to_story_access:                          SendToStoryAccess       | None = None,
            send_to_story_skill_use_requires_confirmation: bool                    | None = None,
            entry_agent_id:                                int                     | None = None,
            exit_agent_ids:                                int                     | None = None,
            team_id:                                       int                     | None = None,
            folder_id:                                     int                     | None = None,
            change_control_enabled:                        bool                    | None = None,
        ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{story_id}",
            json = {key: value for key, value in locals().items() if value != None and key not in ("self", "story_id")}
        )

    def list(
            self,
            team_id:   int                | None = None,
            folder_id: int                | None = None,
            per_page:  int                       = 10,
            page:      int                       = 1,
            tags:      List[str]          | None = None,
            filter:    Filter             | None = None,
            order:     StoriesReturnOrder | None = None,
        ):
        return self._http_request(
            "GET",
            self.base_endpoint,
            json = {key: value for key, value in locals().items() if value != None and key != "self"}
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
            randomize_urls: bool = True
        ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{story_id}/export",
            json = {"randomize_urls": randomize_urls}
        )

    def import_(
            self,
            new_name:  str,
            data:      dict,
            team_id:   int,
            fodler_id: str | None = None,
            mode:      Mode       = Mode.NEW
        ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/import",
            json = {key: value for key, value in locals().items() if value != None and key != "self"}
        )

class ChangeRequestAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "/stories"

    def create(
            self,
            story_id:    int,
            title:       str | None = None,
            description: str | None = None
        ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{story_id}/change_request",
            json = {key: value for key, value in locals().items() if value != None and key not in ("self", "story_id")}
        )

    def approve(
            self,
            story_id:          int,
            change_request_id: int
        ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{story_id}/change_request/approve",
            json = {"change_request_id": change_request_id}
        )
    
    def cancel(
            self,
            story_id:          int,
            change_request_id: int
        ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{story_id}/change_request/cancel",
            json = {"change_request_id": change_request_id}
        )
    
    def promote(
            self,
            story_id:          int,
            change_request_id: int
        ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{story_id}/change_request/promote",
            json = {"change_request_id": change_request_id}
        )
    
    def view(
            self,
            story_id: int
        ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{story_id}/change_request/view"
        )
    

class RunsAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "/stories"
    
    def events(
            self,
            story_id:       int,
            story_run_guid: str,
            story_mode:     StoryMode | None = None,
            per_page:       int              = 10,
            page:           int              = 1,
        ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{story_id}/runs/{story_run_guid}",
            json = {key: value for key, value in locals().items() if value != None and key not in  ("self", "story_id", "story_run_guid")}
        )
    
    def list(
            self,
            story_id:       int,
            story_mode:     StoryMode | None = None,
            per_page:       int              = 10,
            page:           int              = 1,
        ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{story_id}/runs",
            json = {key: value for key, value in locals().items() if value != None and key not in  ("self", "story_id")}
        )

class Versions(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "/stories"
    
    def create(
            self,
            story_id: int,
            name:     str | None = None,
        ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{story_id}/versions",
            json = {key: value for key, value in locals().items() if value != None and key not in ("self", "story_id")}
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
            json = {"name": name}
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
            json = {key: value for key, value in locals().items() if value != None and key not in ("self", "story_id")}
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
    
    