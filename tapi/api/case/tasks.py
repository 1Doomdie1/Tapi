from tapi.client import Client
from typing      import List, Optional


class CaseTasksAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "cases"
    
    def create(
            self,
            case_id:         int,
            description:     str,
            assignee_emails: Optional[List[str]] = None
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{case_id}/tasks",
            "v2",
            json = {key: value for key, value in locals().items() if
                    value is not None and key not in ("self", "case_id")}
        )

    def get(
            self,
            case_id: int,
            task_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/tasks/{task_id}",
            "v2"
        )
    
    def update(
            self,
            case_id:         int,
            task_id:         int,
            description:     Optional[str]       = None,
            completed:       Optional[bool]      = None,
            assignee_emails: Optional[List[str]] = None
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/tasks/{task_id}",
            "v2",
            json = {key: value for key, value in locals().items() if
                    value is not None and key not in ("self", "case_id", "task_id")}
        )

    def list(
            self,
            case_id:  int,
            per_page: int = 10,
            page:     int = 1
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/tasks",
            "v2",
            params = {"per_page": per_page, "page": page}
        )

    def delete(
            self,
            case_id: int,
            task_id: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{case_id}/tasks/{task_id}",
            "v2"
        )
