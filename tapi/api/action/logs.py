from tapi.client      import Client
from typing           import Optional, Union
from tapi.utils.types import LogSeverityLevel


class ActionLogsAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "actions"

    def list(
            self,
            action_id: int,
            level:     Optional[Union[LogSeverityLevel, str]] = None,
            per_page:  int                                    = 10,
            page:      int                                    = 1
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{action_id}/logs",
            params = {key: value for key, value in locals().items()
                      if value is not None and key not in ("self", "action_id")}
        )

    def delete(
            self,
            action_id:      int,
            async_deletion: bool = True
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{action_id}/remove_logs",
            json={"async_deletion": async_deletion}
        )