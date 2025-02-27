from tapi.client import Client
from typing      import Optional, Literal


class FoldersAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "folders"

    def create(
            self,
            name:         str,
            content_type: Literal["CREDENTIAL", "RESOURCE", "STORY"],
            team_id:      int
    ):
        return self._http_request(
            "POST",
            self.base_endpoint,
            json = {
                "name": name,
                "content_type": content_type,
                "team_id": team_id
            }
        )

    def get(
            self,
            folder_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{folder_id}"
        )

    def update(
            self,
            folder_id: int,
            name:      str
    ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{folder_id}",
            json = {"name": name}
        )

    def list(
            self,
            team_id:      Optional[int]                              = None,
            content_type: Literal["CREDENTIAL", "RESOURCE", "STORY"] = "STORY",
            per_page:     int                                        = 10,
            page:         int                                        = 1
    ):
        return self._http_request(
            "GET",
            self.base_endpoint,
            params = {
                "team_id": team_id,
                "content_type": content_type,
                "per_page": per_page,
                "page": page
            }
        )

    def delete(
            self,
            folder_id: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{folder_id}"
        )