from tapi.http.client import Client
from typing           import Optional
from tapi.utils.types import CaseActivityType


class CaseActivitiesAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "cases"

    def get(
            self,
            case_id:     int,
            activity_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/activities/{activity_id}",
            "v2"
        )

    def list(
            self,
            case_id:       int,
            activity_type: Optional[CaseActivityType] = None,
            per_page:      Optional[int]             = 10,
            page:          Optional[int]             = 1
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/activities",
            "v2",
            params = {"activity_type": activity_type},
            json   = {"per_page": per_page, "page": page}
        )