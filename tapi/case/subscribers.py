from typing           import List
from tapi.http.client import Client
from typing           import Optional


class CaseSubscribersAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "cases"

    def create(
            self,
            case_id:    int,
            user_email: str
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{case_id}/subscribers",
            "v2",
            json = {"user_email": user_email}
        )

    def list(
            self,
            case_id:  int,
            per_page: Optional[int] = 10,
            page:     Optional[int] = 1
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/subscribers",
            "v2",
            params = {"per_page": per_page, "page": page}
        )

    def delete(
            self,
            case_id:       int,
            subscriber_id: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{case_id}/subscribers/{subscriber_id}",
            "v2"
        )

    def batch_create(
            self,
            case_id:     int,
            user_emails: List[str]
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{case_id}/subscribers/batch",
            "v2",
            json = {"user_emails": user_emails}
        )
