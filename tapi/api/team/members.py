from tapi.utils.types import Role
from tapi.client      import Client
from typing           import Optional

class MembersAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "teams"

    def list(
            self,
            team_id:  int,
            per_page: Optional[int] = 10,
            page:     Optional[int] = 1,
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{team_id}/members",
            json = {key: value for key, value in locals().items() if value is not None and key not in ("self", "team_id")}
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
            email:   Optional[str]  = None,
            user_id: Optional[int]  = None,
            role:    Optional[Role] = Role.VIEWER
    ):
        if email and user_id:
            raise ValueError("Invalid input: Provide either 'email' or 'user_id', not both.")

        if not email and not user_id:
            raise ValueError("Invalid input: You must provide at least one of 'email' or 'user_id'.")

        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{team_id}/invite_member",
            json={key: value for key, value in locals().items() if value is not None and key not in ("self", "team_id")}
        )

    def resend_invite(
            self,
            team_id: int,
            user_id: Optional[int] = None,
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{team_id}/resend_invitation",
            json = {"user_id": user_id}
        )
