from utils.types import *
from .client     import Client

class TeamsAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "/teams"
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
            self.base_endpoint,
            json = {"team_id": team_id}
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
            json = {key: value for key, value in locals().items() if value != None and key != "self"}
        )
    
    def delete(
            self,
            team_id
        ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{team_id}",
        )


class MembersAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "/teams"

    def list(
            self,
            team_id:  int,
            per_page: int  = 10,
            page:     int  = 1,
        ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{team_id}/members",
            json = {key: value for key, value in locals().items() if value != None and key not in ("self", "team_id")}
        )
    
    def remove(
            self,
            team_id: int,
            user_id: int
        ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{team_id}/remove_member",
            json = {"user_id": user_id}
        )
    
    def invite(
            self,
            team_id: int,
            email:   str,
            user_id: int | None = None,
            role:    Role       = Role.VIEWER
        ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{team_id}/invite_member",
            json = {key: value for key, value in locals().items() if value != None and key not in ("self", "team_id")}
        )
    
    def resend_invite(
            self,
            team_id: int,
            user_id: int | None = None,
        ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{team_id}/resend_invitation",
            json = {"user_id": user_id}
        )
    
    
    
    