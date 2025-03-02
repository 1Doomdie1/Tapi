from tapi.client      import Client
from tapi.utils.types import StoryMode
from typing           import Optional, Union


class RunsAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "stories"

    def events(
            self,
            story_id:       int,
            story_run_guid: str,
            story_mode:     Optional[Union[StoryMode, str]] = None,
            per_page:       int                             = 10,
            page:           int                             = 1,
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{story_id}/runs/{story_run_guid}",
            json={key: value for key, value in locals().items() if
                  value is not None and key not in ("self", "story_id", "story_run_guid")}
        )

    def list(
            self,
            story_id:   int,
            story_mode: Optional[Union[StoryMode, str]] = None,
            per_page:   int                             = 10,
            page:       int                             = 1,
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{story_id}/runs",
            json={key: value for key, value in locals().items() if
                  value is not None and key not in ("self", "story_id")}
        )
