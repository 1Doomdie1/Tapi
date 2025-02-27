from tapi.client import Client
from typing      import List, Optional


class LinkedCasesAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "cases"

    def create(
            self,
            case_id: int,
            id:      int
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{case_id}/linked_cases",
            "v2",
            json = {"id": id}
        )

    def list(
            self,
            case_id:  int,
            per_page: int = 10,
            page:     int = 1
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/linked_cases",
            "v2",
            params = {"per_page": per_page, "page": page}
        )

    def delete(
            self,
            case_id:        int,
            linked_case_id: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{case_id}/linked_cases/{linked_case_id}",
            "v2"
        )

    def batch_delete(
            self,
            case_id: int,
            ids:     List[int]
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{case_id}/linked_cases/batch",
            "v2",
            json = {"ids": ids}
        )

