from tapi.http.client import Client
from utils.types      import CaseActivityType


class CaseActivitiesAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "/cases"

    def get(
            self,
            case_id: int,
            activity_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/activities/{activity_id}"
        )

    def list(
            self,
            case_id: int,
            activity_type: CaseActivityType | None = None,
            per_page: int = 10,
            page: int = 1
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/activities",
            json={key: value for key, value in locals().items() if value != None and key not in ("self", "case_id")}
        )