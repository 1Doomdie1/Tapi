from typing           import List
from tapi.http.client import Client
from utils.types      import CaseActionType


class CaseActionsAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "/cases"

    def create(
            self,
            case_id: int,
            url: str,
            label: str,
            action_type: CaseActionType,
            action_text: str | None = None
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{case_id}/actions",
            json={key: value for key, value in locals().items() if value != None and key not in ("self", "case_id")}
        )

    def get(
            self,
            case_id: int,
            id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/actions/{id}"
        )

    def update(
            self,
            case_id: int,
            id: int,
            url: str | None = None,
            label: str | None = None,
            action_type: CaseActionType | None = None,
            action_text: str | None = None
    ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{case_id}/actions/{id}",
            json={key: value for key, value in locals().items() if
                  value is not None and key not in ("self", "case_id", "id")}
        )

    def list(
            self,
            case_id: int,
            per_page: int = 10,
            page: int = 1,
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/actions",
            json={key: value for key, value in locals().items() if value is not None and key not in ("self", "case_id")}
        )

    def delete(
            self,
            case_id: int,
            id: int = 10
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{case_id}/actions/{id}"
        )

    def batch_delete(
            self,
            case_id: int,
            actions: List[dict[str, str]]
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{case_id}/actions/batch",
            json={"actions": actions}
        )