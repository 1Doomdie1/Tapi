from tapi.client      import Client
from tapi.utils.types import AuditLogType
from typing           import Optional, List, Union


class AuditLogsAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "audit_logs"

    def list(
            self,
            before:         Optional[int]                            = None,
            after:          Optional[int]                            = None,
            user_id:        Optional[List[int]]                      = None,
            operation_name: Optional[List[Union[AuditLogType, str]]] = None,
            per_page:       int                                      = 10,
            page:           int                                      = 1
    ):
        return self._http_request(
            "GET",
            self.base_endpoint,
            params = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )