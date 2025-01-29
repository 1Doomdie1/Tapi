from tapi.http.client import Client
from utils.types      import ReactionType


class CaseCommentsAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "/cases"

    def create(
            self,
            case_id:      int,
            value:        str,
            author_email: str | None = None
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{case_id}/comments",
            "v2",
            json = {"value": value, "author_email": author_email}
        )

    def get(
            self,
            case_id:    int,
            comment_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/comments/{comment_id}",
            "v2"
        )

    def update(
            self,
            case_id:    int,
            comment_id: int,
            value:      str
    ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{case_id}/comments/{comment_id}",
            "v2",
            json = {"value": value}
        )

    def list(
            self,
            case_id:  int,
            per_page: int = 10,
            page:     int = 1
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/comments",
            "v2",
            json = {"per_page": per_page, "page": page}
        )

    def delete(
            self,
            case_id: int,
            comment_id: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{case_id}/comments/{comment_id}",
            "v2"
        )

class CaseCommentsReactionsAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "/cases"

    def add(
            self,
            case_id:    int,
            comment_id: int,
            value:      ReactionType
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{case_id}/comments/{comment_id}/add_reaction",
            "v2",
            json = {"value": value}
        )

    def remove(
            self,
            case_id:    int,
            comment_id: int,
            value:      ReactionType
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{case_id}/comments/{comment_id}/remove_reaction",
            "v2",
            json={"value": value}
        )
