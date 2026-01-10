from tapi.client      import Client
from typing           import List, Dict, Optional, Union
from tapi.utils.types import CaseInputType, CaseValidationType


class CaseInputsAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "case_inputs"
        self.fields        = CaseInputsFieldsAPI(domain, apiKey)

    def create(
            self,
            name:               str,
            input_type:         Union[CaseInputType, str],
            team_id:            int,
            validation_type:    Optional[Union[CaseValidationType, str]]              = None,
            validation_options: Optional[Union[Dict[str, List[str]], Dict[str, str]]] = None
    ):
        return self._http_request(
            "POST",
            self.base_endpoint,
            json = {key: value for key, value in locals().items() if
                    value is not None and key != "self"}
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
            team_id:  Optional[int] = None,
            per_page: int           = 10,
            page:     int           = 1,
    ):
        return self._http_request(
            "GET",
            self.base_endpoint,
            params = {"team_id": team_id},
            json   = {"per_page": per_page,"page": page}
        )

class CaseInputsFieldsAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "case_inputs"

    def list(
            self,
            case_input_id: int,
            per_page:      Optional[int] = None,
            page:          Optional[int] = None
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_input_id}/fields",
            json = {"per_page": per_page, "page": page}
        )
