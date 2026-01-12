from tapi.client import Client
from typing      import Optional


class RecipientsAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "stories"

    def create(
            self,
            story_id:  int,
            address:   int,
            draft_id:  Optional[int] = None
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{story_id}/recipients",
            json = {
                "address": address,
                "draft_id": draft_id
            }
        )

    def delete(
            self,
            story_id:  int,
            address:   int,
            draft_id:  Optional[int] = None
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{story_id}/recipients",
            json = {
                "address": address,
                "draft_id": draft_id
            }
        )
