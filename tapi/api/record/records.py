from tapi.client      import Client
from .types           import RecordTypesAPI
from .artifacts       import RecordArtifactsAPI
from tapi.utils.types import RecordFieldValue, RecordFilter
from typing           import Optional, Dict, List, Union, Any, Literal


class RecordsAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "records"
        self.types         = RecordTypesAPI(domain, apiKey)
        self.artifacts     = RecordArtifactsAPI(domain, apiKey)

    def create(
            self,
            record_type_id: int,
            field_values:   List[Union[RecordFieldValue, Dict[str, Any]]],
            case_ids:       Optional[List[Union[str, int]]]        = None,
            test_mode:      bool                                   = False
    ):
        return self._http_request(
            "POST",
            self.base_endpoint,
            json = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def get(
            self,
            record_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{record_id}"
        )

    def list(
            self,
            record_type_id:   Optional[int]                                              = None,
            record_field_ids: Optional[int]                                              = None,
            range_start:      Optional[Union[str, int]]                                  = None,
            range_end:        Optional[Union[str, int]]                                  = None,
            story_ids:        Optional[List[Union[str, int]]]                            = None,
            order_direction:  Literal["ASC", "DESC"]                                     = "DESC",
            order_field_id:   Optional[int]                                              = None,
            filters:          Optional[List[Union[RecordFilter, Union[Dict[str, str]]]]] = None,
            test_mode:        Optional[bool]                                             = None,
            per_page:         int                                                        = 10,
            page:             int                                                        = 1
    ):
        if not record_type_id and not record_field_ids:
            raise ValueError("Please specify either 'record_type_id' or 'record_field_ids'.")
        elif record_type_id and record_field_ids:
            raise ValueError("Please specify only one of 'record_type_id' or 'record_field_ids', not both.")

        return self._http_request(
            "GET",
            self.base_endpoint,
            params = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def update(
            self,
            record_id: int,
            add_child_records:    Optional[List[Union[str, int]]]               = None,
            remove_child_records: Optional[List[Union[str, int]]]               = None,
            add_team_case_ids:    Optional[List[Union[str, int]]]               = None,
            remove_team_case_ids: Optional[List[Union[str, int]]]               = None,
            field_values:         List[Union[RecordFieldValue, Dict[str, Any]]] = None
    ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{record_id}",
            json = {key: value for key, value in locals().items()
                    if value is not None and key not in ("self", "record_id")}
        )

    def delete(
            self,
            record_id: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{record_id}"
        )
