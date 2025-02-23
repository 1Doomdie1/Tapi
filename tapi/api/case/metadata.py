from tapi.client import Client
from typing      import List, Dict


class CaseMetadataAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "cases"

    def create(
            self,
            case_id:  int,
            metadata: Dict[str, str]
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{case_id}/metadata",
            "v2",
            json = {"metadata": metadata}
        )

    def get(
            self,
            case_id: int,
            key:     str
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/metadata/{key}",
            "v2"
        )

    def update(
            self,
            case_id:  int,
            metadata: Dict[str, str]
    ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{case_id}/metadata",
            "v2",
            json = {"metadata": metadata}
        )

    def list(
            self,
            case_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/metadata",
            "v2"
        )

    def delete(
            self,
            case_id:       int,
            metadata_keys: List[str]
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{case_id}/metadata",
            "v2",
            json = {"metadata": metadata_keys}
        )
