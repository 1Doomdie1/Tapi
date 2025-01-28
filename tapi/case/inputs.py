from typing           import List
from tapi.http.client import Client
from utils.types      import CaseInputType, CaseValidationType


class CaseInputsAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "/cases_inputs"

    def create(
            self,
            name:               str,
            input_type:         CaseInputType,
            team_id:            int,
            validation_type:    CaseValidationType   | None                  = None,
            validation_options: dict[str, List[str]] | dict[str, str] | None = None
    ):
        # I have to actually build the data object here I can't just parse it by using the same trick.
        return self._http_request(
            "POST",
            self.base_endpoint,
            json = {key: value for key, value in locals().items() if value != None and key not in ("self", "case_id")}
        )
