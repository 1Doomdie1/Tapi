from tapi.api.http.client import Client
from typing               import Literal, Optional, List, Dict, Any


class CredentialsAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "user_credentials"

    def create_aws(
            self,
            name:                    str,
            team_id:                 int,
            aws_authentication_type: Literal["KEY", "ROLE", "INSTANCE_PROFILE"],
            aws_access_key:          str,
            aws_secret_key:          str,
            aws_assumed_role_arn:    Optional[str]                               = None,
            folder_id:               Optional[int]                               = None,
            read_access:             Literal["TEAM", "GLOBAL", "SPECIFIC_TEAMS"] = "TEAM",
            shared_team_slugs:       Optional[List[str]]                         = None,
            description:             Optional[str]                               = None,
            metadata:                Optional[Dict[str, Any]]                    = None,
            allowed_hosts:           Optional[List[str]]                         = None,
            live_credential_id:      Optional[int]                               = None
    ):
        data = {key: value for key, value in locals().items() if value is not None and key != "self"}
        data.update({"mode": "AWS"})

        return self._http_request(
            "POST",
            self.base_endpoint,
            json = data
        )

    def create_http_request(
            self,
            name:                           str,
            team_id:                        int,
            http_request_options:           Dict[str, Any],
            http_request_location_of_token: str,
            http_request_secret:            Optional[str]                               = None,
            http_request_ttl:               Optional[int]                               = None,
            content_type:                   Optional[str]                               = None,
            folder_id:                      Optional[int]                               = None,
            read_access:                    Literal["TEAM", "GLOBAL", "SPECIFIC_TEAMS"] = "TEAM",
            shared_team_slugs:              Optional[List[str]]                         = None,
            description:                    Optional[str]                               = None,
            metadata:                       Optional[Dict[str, Any]]                    = None,
            allowed_hosts:                  Optional[List[str]]                         = None,
            live_credential_id:             Optional[int]                               = None
    ):
        data = {key: value for key, value in locals().items() if value is not None and key != "self"}
        data.update({"mode": "HTTP_REQUEST_AGENT"})

        return self._http_request(
            "POST",
            self.base_endpoint,
            json = data
        )

    def create_jwt(
            self,
            name:                          str,
            team_id:                       int,
            jwt_algorithm:                 str,
            jwt_payload:                   Dict[str, str],
            jwt_auto_generate_time_claims: bool,
            jwt_private_key:               str,
            folder_id:                     Optional[int]                               = None,
            read_access:                   Literal["TEAM", "GLOBAL", "SPECIFIC_TEAMS"] = "TEAM",
            shared_team_slugs:             Optional[List[str]]                         = None,
            description:                   Optional[str]                               = None,
            metadata:                      Optional[Dict[str, Any]]                    = None,
            allowed_hosts:                 Optional[List[str]]                         = None,
            live_credential_id:            Optional[int]                               = None
    ):
        data = {key: value for key, value in locals().items() if value is not None and key != "self"}
        data.update({"mode": "JWT"})

        return self._http_request(
            "POST",
            self.base_endpoint,
            json = data
        )


    def create_mtls(
            self,
            name:                    str,
            team_id:                 int,
            mtls_client_certificate: str,
            mtls_client_private_key: str,
            mtls_root_certificate:   str,
            folder_id:               Optional[int]                               = None,
            read_access:             Literal["TEAM", "GLOBAL", "SPECIFIC_TEAMS"] = "TEAM",
            shared_team_slugs:       Optional[List[str]]                         = None,
            description:             Optional[str]                               = None,
            metadata:                Optional[Dict[str, Any]]                    = None,
            allowed_hosts:           Optional[List[str]]                         = None,
            live_credential_id:      Optional[int]                               = None
    ):
        data = {key: value for key, value in locals().items() if value is not None and key != "self"}
        data.update({"mode": "MTLS"})

        return self._http_request(
            "POST",
            self.base_endpoint,
            json = data
        )

    def create_multi_request(
            self,
            name:                           str,
            team_id:                        int,
            http_request_location_of_token: str,
            credential_requests:            List[Dict[str, Any]],
            http_request_ttl:               Optional[int]                               = None,
            content_type:                   Optional[str]                               = None,
            folder_id:                      Optional[int]                               = None,
            read_access:                    Literal["TEAM", "GLOBAL", "SPECIFIC_TEAMS"] = "TEAM",
            shared_team_slugs:              Optional[List[str]]                         = None,
            description:                    Optional[str]                               = None,
            metadata:                       Optional[Dict[str, Any]]                    = None,
            allowed_hosts:                  Optional[List[str]]                         = None,
            live_credential_id:             Optional[int]                               = None
    ):
        data = {key: value for key, value in locals().items() if value is not None and key != "self"}
        data.update({"mode": "MULTI_REQUEST"})

        return self._http_request(
            "POST",
            self.base_endpoint,
            json = data
        )

    def create_oauth(
            self,
            name:                         str,
            team_id:                      int,
            oauth_url:                    str,
            oauth_token_url:              str,
            oauth_client_id:              str,
            oauth_client_secret:          str,
            oauth_scope:                  str,
            oauth_grant_type:             Literal["client_credentials", "authorization_code"],
            oauthPkceCodeChallengeMethod: Optional[Literal["S256", "plain"]]          = None,
            folder_id:                    Optional[int]                               = None,
            read_access:                  Literal["TEAM", "GLOBAL", "SPECIFIC_TEAMS"] = "TEAM",
            shared_team_slugs:            Optional[List[str]]                         = None,
            description:                  Optional[str]                               = None,
            metadata:                     Optional[Dict[str, Any]]                    = None,
            allowed_hosts:                Optional[List[str]]                         = None,
            live_credential_id:           Optional[int]                               = None
    ):
        data = {key: value for key, value in locals().items() if value is not None and key != "self"}
        data.update({"mode": "OAUTH"})

        return self._http_request(
            "POST",
            self.base_endpoint,
            json = data
        )

    def create_text(
            self,
            name:               str,
            team_id:            int,
            value:              str,
            folder_id:          Optional[int]                               = None,
            read_access:        Literal["TEAM", "GLOBAL", "SPECIFIC_TEAMS"] = "TEAM",
            shared_team_slugs:  Optional[List[str]]                         = None,
            description:        Optional[str]                               = None,
            metadata:           Optional[Dict[str, Any]]                    = None,
            allowed_hosts:      Optional[List[str]]                         = None,
            live_credential_id: Optional[int]                               = None
    ):
        data = {key: value for key, value in locals().items() if value is not None and key != "self"}
        data.update({"mode": "TEXT"})

        return self._http_request(
            "POST",
            self.base_endpoint,
            json = data
        )

    def update(
            self,
            mode:                    Literal["TEXT", "JWT", "OAUTH", "AWS", "MTLS", "HTTP_REQUEST_AGENT", "MULTI_REQUEST"],
            credential_id:           int,
            name:                    Optional[str]                               = None,
            folder_id:               Optional[int]                               = None,
            read_access:             Literal["TEAM", "GLOBAL", "SPECIFIC_TEAMS"] = None,
            shared_team_slugs:       Optional[List[str]]                         = None,
            description:             Optional[str]                               = None,
            metadata:                Optional[Dict[str, str]]                    = None,
            allowed_hosts:           Optional[List[str]]                         = None,
            test_credential_enabled: Optional[bool]                              = None,
            is_test:                 Optional[bool]                              = None,
            **options
    ):
        data = {key: value for key, value in locals().items() if value is not None and key not in ("self", "credential_id", "options")}
        data = {**data, **locals()["options"]}

        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{credential_id}",
            json = data
        )

    def get(
            self,
            credential_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{credential_id}"
        )

    def list(
            self,
            folder_id: Optional[int] = None,
            team_id:   Optional[int] = None,
            per_page:  int           = 10,
            page:      int           = 1
    ):
        return self._http_request(
            "GET",
            self.base_endpoint,
            params={key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def delete(
            self,
            credential_id: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{credential_id}"
        )

