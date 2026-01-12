from tapi.client import Client
from typing      import Optional


class WorkbenchAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "workbench"
    
    def get(
            self,
            guid: str
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{guid}"
        )
    
    def list(
            self,
            search:     Optional[str]  = None,
            favorited:  Optional[bool] = None,
            creator_id: Optional[str]  = None,
            per_page:   Optional[int]  = 10,
            page:       Optional[int]  = 1
    ):
        return self._http_request(
            "GET",
            self.base_endpoint,
            params = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )