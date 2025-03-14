from tapi.client import Client
from typing      import Union, Literal, List, Dict, Optional


class CaseBlocksAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "cases"
        self.elements      = CaseBlockElementsAPI(domain, apiKey)

    def create(
            self,
            case_id:    int,
            title:      str,
            block_type: Union[Literal["note", "file"]],
            elements:   List[Dict[str, str]],
            position:   int                        = 0,
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{case_id}/blocks",
            "v2",
            json = {key: value for key, value in locals().items() if
                    value is not None and key not in ("self", "case_id")}
        )

    def get(
            self,
            case_id:  int,
            block_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/blocks/{block_id}",
            "v2",
        )

    def update(
            self,
            case_id:  int,
            block_id: int,
            title:    Optional[str] = None,
            position: Optional[str] = None
    ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{case_id}/blocks/{block_id}",
            "v2",
            json = {key: value for key, value in locals().items() if
                    value is not None and key not in ("self", "case_id", "block_id")}
        )

    def list(
            self,
            case_id:    int,
            block_type: Optional[Literal["note", "file"]] = None,
            per_page:   int = 10,
            page:       int = 1
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/blocks",
            "v2",
            params = {key: value for key, value in locals().items() if
                    value is not None and key not in ("self", "case_id")}
        )

    def delete(
            self,
            case_id:  int,
            block_id: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{case_id}/blocks/{block_id}",
            "v2"
        )


class CaseBlockElementsAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "cases"

    def get(
            self,
            case_id:    int,
            block_id:   int,
            element_id: int,
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/blocks/{block_id}/elements/{element_id}",
            "v2"
        )

    def update(
            self,
            case_id:    int,
            block_id:   int,
            element_id: int,
            content:    Optional[str]                                                   = None,
            color:      Optional[Literal[ "white", "gold", "magenta", "green", "blue"]] = None
    ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{case_id}/blocks/{block_id}/elements/{element_id}",
            "v2",
            json = {key: value for key, value in locals().items() if
                    value is not None and key not in ("self", "case_id", "block_id", "element_id")}
        )

