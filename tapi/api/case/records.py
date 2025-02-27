from tapi.client import Client


class CaseRecordsAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "cases"

    def create(
            self,
            case_id:   int,
            record_id: int
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{case_id}/records",
            "v2",
            json = {"record_id": record_id}
        )

    def get(
            self,
            case_id:   int,
            record_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/records/{record_id}",
            "v2"
        )

    def list(
            self,
            case_id:  int,
            per_page: int = 10,
            page:     int = 1
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/records",
            "v2",
            params = {"per_page": per_page, "page": page}
        )

    def delete(
            self,
            case_id:   int,
            record_id: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{case_id}/records/{record_id}",
            "v2"
        )
