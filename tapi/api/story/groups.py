from tapi.client import Client


class GroupsAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "groups"

    def list_run_events(
            self,
            group_id:       int,
            group_run_guid: str,
            per_page:       int = 10,
            page:           int = 1
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{group_id}/runs/{group_run_guid}",
            params = {
                "page": page,
                "per_page": per_page
            }
        )

    def list_runs(
            self,
            group_id: int,
            per_page: int = 10,
            page:     int = 1
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{group_id}/runs",
            params={
                "page": page,
                "per_page": per_page
            }
        )
