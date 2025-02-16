from tapi.http.client import Client
from typing import Optional, Dict

from tapi.utils.types import StoryMode


class NotesAPI(Client):

    def __init__(self, domain: str,apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "notes"

    def create(
            self,
            content:  str,
            story_id: Optional[int]            = None,
            group_id: Optional[int]            = None,
            position: Optional[Dict[str, int]] = None,
            draft_id: Optional[int]            = None
    ):
        if not (story_id or group_id):
            raise ValueError("Story ID or Group ID must be specified.")

        if story_id and group_id:
            raise ValueError("Story ID or Group ID must be specified but not both.")

        return self._http_request(
            "POST",
            self.base_endpoint,
            json = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def get(
            self,
            note_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{note_id}"
        )

    def update(
            self,
            note_id:  int,
            content:  Optional[str]            = None,
            position: Optional[Dict[str, int]] = None
    ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{note_id}",
            json = {key: value for key, value in locals().items()
                    if value is not None and key not in ("self", "note_id")}
        )

    def list(
            self,
            story_id: Optional[int]       = None,
            mode:     Optional[StoryMode] = None,
            team_id:  Optional[int]       = None,
            group_id: Optional[int]       = None,
            draft_id: Optional[int]       = None,
            per_page: Optional[int]       = 10,
            page:     Optional[int]       = 1
    ):
        return self._http_request(
            "GET",
            self.base_endpoint,
            json = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def delete(
            self,
            note_id: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{note_id}"
        )
