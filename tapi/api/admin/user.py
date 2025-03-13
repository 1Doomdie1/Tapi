from tapi.client import Client
from datetime    import datetime
from typing      import Optional, List, Literal, Union


class UsersAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "admin"

    def create(
            self,
            email:              str,
            first_name:         Optional[str]                                                                     = None,
            last_name:          Optional[str]                                                                     = None,
            admin:              bool                                                                              = False,
            tenant_permissions: Optional[List[Literal["AUDIT_LOG_READ", "FEATURE_FLAG_MANAGE", "TUNNEL_MANAGE"]]] = None,
            is_active:          bool                                                                              = True
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/users",
            json = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def get(
            self,
            user_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/users/{user_id}"
        )

    def sign_in_activity(
            self,
            user_id:  int,
            before:   Optional[Union[datetime, str]] = None,
            after:    Optional[Union[datetime, str]] = None,
            per_page: int                            = 10,
            page:     int                            = 1
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/users/{user_id}/signin_activities",
            params = {key: value for key, value in locals().items()
                      if value is not None and key not in ("self", "user_id")}
        )

    def update(
            self,
            user_id:            int,
            email:              Optional[str]                                                                     = None,
            first_name:         Optional[str]                                                                     = None,
            last_name:          Optional[str]                                                                     = None,
            admin:              Optional[bool]                                                                    = None,
            tenant_permissions: Optional[List[Literal["AUDIT_LOG_READ", "FEATURE_FLAG_MANAGE", "TUNNEL_MANAGE"]]] = None,
            is_active:          Optional[bool]                                                                    = None
    ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/users/{user_id}",
            json = {key: value for key, value in locals().items()
                    if value is not None and key not in ("self", "user_id")}
        )

    def list(
            self,
            per_page: int                               = 10,
            page:     int                               = 1,
            filter:   Optional[Literal["TENANT_OWNER"]] = None
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/users",
            params = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def delete(
            self,
            user_id: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/users/{user_id}"
        )

    def resend_invitation(
            self,
            user_id: int
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/users/{user_id}/resend_invitation"
        )

    def expire_session(
            self,
            user_id: int
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/users/{user_id}/expire_session"
        )