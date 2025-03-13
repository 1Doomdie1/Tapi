from tapi.client import Client
from typing      import Literal


class JobsAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint      = "admin"

    def list(
            self,
            job_type: Literal["dead", "in_progress", "queued", "retry"],
            per_page: int = 10,
            page:     int = 1
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{job_type}_jobs",
            params = {
                "per_page": per_page,
                "page": page
            }
        )

    def delete(
            self,
            job_type: Literal["dead", "queued", "retry"]
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/delete_all_{job_type}_jobs"
        )

    def delete_by_action(
            self,
            action_id: int,
            job_type: Literal["dead", "queued", "retry"]
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/actions/{action_id}/delete_all_{job_type}_jobs"
        )