from tapi.client import Client
from typing      import Optional, Dict, List, Union, Any, Literal


class ResourcesAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "global_resources"

    def create(
            self,
            name:              str,
            value:             Union[str, Dict[str, Any], List[Union[int, str, Dict[str, Any]]]],
            team_id:           int                                         = None,
            folder_id:         Optional[int]                               = None,
            read_access:       Literal["TEAM", "GLOBAL", "SPECIFIC_TEAMS"] = "TEAM",
            shared_team_slugs: Optional[List[str]]                         = None,
            description:       Optional[str]                               = None,
            live_resource_id:  Optional[int]                               = None,

    ):
        return self._http_request(
            "POST",
            self.base_endpoint,
            json = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def get(
            self,
            resource_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{resource_id}"
        )

    def update(
            self,
            resource_id:           int,
            value:                 Union[str, Dict[str, Any], List[Dict[str, Any]]],
            name:                  Optional[str]                                         = None,
            folder_id:             Optional[int]                                         = None,
            read_access:           Optional[Literal["TEAM", "GLOBAL", "SPECIFIC_TEAMS"]] = None,
            shared_team_slugs:     Optional[List[str]]                                   = None,
            description:           Optional[str]                                         = None,
            test_resource_enabled: Optional[bool]                                        = None,
            is_test:               Optional[bool]                                        = None
    ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{resource_id}",
            json = {key: value for key, value in locals().items()
                    if value is not None and key not in ("self", "resource_id")}
        )

    def list(
            self,
            team_id:   Optional[int] = None,
            folder_id: Optional[int] = None,
            per_page:  int           = 10,
            page:      int           = 1,
    ):
        return self._http_request(
            "GET",
            self.base_endpoint,
            params = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def remove_element(
            self,
            resource_id: int,
            key:         Optional[str]  = None,
            index:       Optional[int]  = None,
            is_test:     Optional[bool] = None
    ):
        if not key and not index:
            raise ValueError("Please specify either 'key' or 'index'.")
        elif key and index:
            raise ValueError("Please specify only one of 'key' or 'index', not both.")

        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{resource_id}/remove",
            json = {key: value for key, value in locals().items()
                    if value is not None and key not in ("self", "resource_id")}
        )

    def delete(
            self,
            resource_id: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{resource_id}"
        )

    def append_element(
            self,
            resource_id: int,
            value:       Union[str, List],
            is_test:     Optional[bool] = None
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{resource_id}/append",
            json = {key: value for key, value in locals().items()
                  if value is not None and key not in ("self", "resource_id")}
        )

    def replace_element(
            self,
            resource_id: int,
            value:       str,
            key:         Optional[str]  = None,
            index:       Optional[str]  = None,
            is_test:     Optional[bool] = None
    ):
        if not key and not index:
            raise ValueError("Please specify either 'key' or 'index'.")
        elif key and index:
            raise ValueError("Please specify only one of 'key' or 'index', not both.")

        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{resource_id}/append",
            json = {key: value for key, value in locals().items()
                  if value is not None and key not in ("self", "resource_id")}
        )
























