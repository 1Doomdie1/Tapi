from tapi.api.http.client import Client
from tapi.utils.types     import CaseActionType
from typing               import List, Optional, Dict, Any


class CaseActionsAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "cases"

    def create(
            self,
            case_id:     int,
            url:         str,
            label:       str,
            action_type: CaseActionType,
            action_text: Optional[str] = None
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{case_id}/actions",
            "v2",
            json={key: value for key, value in locals().items() if
                  value is not None and key not in ("self", "case_id")}
        )

    def get(
            self,
            case_id: int,
            id:      int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/actions/{id}",
            "v2"
        )

    def update(
            self,
            case_id:     int,
            id:          int,
            url:         Optional[str]            = None,
            label:       Optional[str]            = None,
            action_type: Optional[CaseActionType] = None,
            action_text: Optional[str]            = None
    ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{case_id}/actions/{id}",
            "v2",
            json={key: value for key, value in locals().items() if
                  value is not None and key not in ("self", "case_id", "id")}
        )

    def list(
            self,
            case_id:  int,
            per_page: Optional[ int] = 10,
            page:     Optional[ int] = 1,
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/actions",
            "v2",
            json={key: value for key, value in locals().items() if
                  value is not None and key not in ("self", "case_id")}
        )

    def delete(
            self,
            case_id: int,
            id:      Optional[int] = 10
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{case_id}/actions/{id}",
            "v2"
        )

    def batch_update(
            self,
            case_id: int,
            actions: List[Dict[str, Any]]
    ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{case_id}/actions/batch",
            "v2",
            json={"actions": actions}
        )