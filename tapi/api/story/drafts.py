from tapi.client import Client


class DraftsAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "stories"

    def create(
            self,
            story_id: int,
            name:     str
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{story_id}/drafts",
            json = {
                "name": name
            }
        )

    def list(
            self,
            story_id: int,
            per_page: int = 10,
            page:     int = 1
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{story_id}/drafts",
            params = {
                "per_page": per_page,
                "page": page
            }
        )

    def delete(
            self,
            story_id: int,
            draft_id: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{story_id}/drafts/{draft_id}"
        )
