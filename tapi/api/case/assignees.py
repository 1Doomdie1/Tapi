from tapi.client import Client


class CaseAssigneesAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "cases"

    def list(
            self,
            case_id:  int,
            per_page: int = 10,
            page:     int = 1,
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/assignees",
            "v2",
            json = {key: value for key, value in locals().items() if
                    value is not None and key not in ("self", "case_id")}
        )