from typing      import Union
from tapi.client import Client


class CaseFieldsAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "cases"

    def create(
            self,
            case_id:  int,
            input_id: int,
            value:    Union[str, int]
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{case_id}/fields",
            "v2",
            params = {"input_id": input_id, "value": value}
        )

    def get(
            self,
            case_id:  int,
            field_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/fields/{field_id}",
            "v2"
        )

    def update(
            self,
            case_id:  int,
            field_id: int,
            value:    Union[str, int]
    ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{case_id}/fields/{field_id}",
            "v2",
            json={"value": value}
        )

    def list(
            self,
            case_id:  int,
            per_page: int = 10,
            page:     int = 1
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/fields",
            "v2",
            params = {"per_page": per_page, "page": page}
        )

    def delete(
            self,
            case_id:  int,
            field_id: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{case_id}/fields/{field_id}",
            "v2"
        )
