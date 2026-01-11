from tapi.client import Client


class OwnersAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "stories"

    def create(
            self,
            story_id: int,
            user_id:  int
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{story_id}/owners",
            json = {
                "user_id": user_id
            }
        )

    def delete(
            self,
            story_id: int,
            user_id:  int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{story_id}/owners",
            json = {
                "user_id": user_id
            }
        )
