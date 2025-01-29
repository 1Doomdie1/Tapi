from typing           import List
from tapi.http.client import Client
from utils.types      import CaseInputType, CaseValidationType


class CaseInputsAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "/case_inputs"
        self.inputs        = CaseInputsFieldsAPI(domain, apiKey)

    def create(
            self,
            name:               str,
            input_type:         CaseInputType,
            team_id:            int,
            validation_type:    CaseValidationType   | None                  = None,
            validation_options: dict[str, List[str]] | dict[str, str] | None = None
    ):
        return self._http_request(
            "POST",
            self.base_endpoint,
            json = {key: value for key, value in locals().items() if
                    value is not None and key not in ("self", "case_id")}
        )

    def get(
            self,
            case_input_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_input_id}"
        )

    def list(
            self,
            team_id:  int | None = None,
            per_page: int        = 10,
            page:     int        = 1,
    ):
        return self._http_request(
            "GET",
            self.base_endpoint,
            params = {"team_id": team_id},
            json   = {"per_page": per_page,"page": page}
        )

class CaseInputsFieldsAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "/case_inputs"

    def list(
            self,
            case_input_id: int,
            per_page:      int | None = None,
            page:          int | None = None
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_input_id}/fields",
            json = {"per_page": per_page, "page": page}
        )
