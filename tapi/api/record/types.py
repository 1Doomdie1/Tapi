from tapi.client import Client
from typing      import Dict, Optional, List, Union, Any


class RecordTypesAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "record_types"

    def create(
            self,
            name:     str,
            team_id:  int,
            fields:   List[Dict[str, Union[str, int, bool]]],
            editable: Optional[bool]                  = None,
            ttl_days: Optional[int]                   = None
    ):
        return self._http_request(
            "POST",
            self.base_endpoint,
            json = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def get(
            self,
            record_type_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{record_type_id}"
        )
    
    def update(
            self,
            record_type_id:      int,
            name:                Optional[str]            = None,
            editable:            Optional[bool]           = None,
            ttl_days:            Optional[int]            = None,
            fields:              Optional[Dict[str, Any]] = None,
            field_ids_to_delete: Optional[List[int]]      = None
    ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{record_type_id}",
            json = {key: value for key, value in locals().items() if value is not None and key not in ("self", "record_type_id")}
        )

    def list(
            self,
            team_id:  int,
            per_page: int = 10,
            page:     int = 1
    ):
        return self._http_request(
            "GET",
            self.base_endpoint,
            params = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def delete(
            self,
            record_type_id: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{record_type_id}"
        )
