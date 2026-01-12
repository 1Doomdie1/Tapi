from tapi.client      import Client
from typing           import Union, List


class StorySyncDestinationsAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "admin"
    
    def create(
        self,
        destination_tenant_url:     str,
        destination_tenant_api_key: str,
        destination_team_id:        Union[str, int],
        team_id:                    int,
        story_ids:                  List[int],
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/sync_destinations",
            json = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def list(
        self,
        per_page: int = 10,
        page:     int = 1,
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/sync_destinations",
            params = {
                "per_page": per_page,
                "page": page
            }
        )
    
    def delete(
        self,
        id_: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/sync_destinations/{id_}"
        )

    def manual_sync(
        self,
        id_: int
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/sync_destinations/{id_}/manual_sync"
        )
