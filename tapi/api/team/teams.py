from tapi.client import Client
from .members    import MembersAPI


class TeamsAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "teams"
        self.members       = MembersAPI(domain, apiKey)

    def create(
            self,
            name: str
        ):
        return self._http_request(
            "POST",
            self.base_endpoint,
            json = {"name": name}
        )

    def get(
            self,
            team_id: int
        ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{team_id}"
        )

    def update(
            self,
            team_id: int,
            name:    str
        ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{team_id}",
            json = {"name": name}
        )

    def list(
            self,
            include_personal_teams: bool = False,
            per_page:               int  = 10,
            page:                   int  = 1,
        ):
        return self._http_request(
            "GET",
            self.base_endpoint,
            json = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def delete(
            self,
            team_id: int
        ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{team_id}",
        )
