from tapi.client import Client
from typing      import Dict, Optional, Any, Literal


class RecordViewsAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "record_views"

    def list(
            self,
            team_id:        Optional[int]                                                     = None,
            record_type_id: Optional[int]                                                     = None,
            order:          Optional[Literal["NAME", "RECENTLY_CREATED", "RECENTLY_UPDATED"]] = "NAME",
            per_page:       Optional[int]                                                     = 10,
            page:           Optional[int]                                                     = 1
    ):
        return self._http_request(
            "GET",
            self.base_endpoint,
            params = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def delete(
            self,
            record_view_id: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{record_view_id}"
        )

    def export(
            self,
            record_view_id:  int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{record_view_id}/export"
        )

    def import_(
            self,
            team_id: int,
            data:    Dict[str, Any],
            mode:    Optional[Literal["new", "replace"]] = "new",
            name:    Optional[str]                       = None
    ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/import",
            json = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )
