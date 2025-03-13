from tapi.client        import Client
from tapi.utils.helpers import is_ip_valid
from typing             import List, Optional, Literal, Union


class ActionEgressControlRulesAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "admin"

    def create(
            self,
            ip:                   Optional[str]                               = None,
            fqdn:                 Optional[str]                               = None,
            description:          str                                         = "",
            allowed_action_types: List[Literal["http-request", "send-email"]] = None
    ):
        if ip and fqdn:
            raise ValueError("Only IP or FQDN is allowed, not both.")

        if not ip and not fqdn:
            raise ValueError("Either IP or FQDN must be provided.")

        if ip and not is_ip_valid(ip):
            raise ValueError("Invalid IP address or CIDR range.")

        return self._http_request(
            "POST",
            f"{self.base_endpoint}/action_egress_control_rules",
            json = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def get(
            self,
            id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/action_egress_control_rules/{id}"
        )

    def update(
            self,
            id:                   Union[str, int],
            ip:                   Optional[str]                               = None,
            fqdn:                 Optional[str]                               = None,
            description:          Optional[str]                               = None,
            allowed_action_types: List[Literal["http-request", "send-email"]] = None
    ):
        if ip and fqdn:
            raise ValueError("Only IP or FQDN is allowed, not both.")

        if not ip and not fqdn:
            raise ValueError("Either IP or FQDN must be provided.")

        if ip and not is_ip_valid(ip):
            raise ValueError("Invalid IP address or CIDR range.")

        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/ip_access_control_rules/{id}",
            json = {key: value for key, value in locals().items()
                    if value is not None and key not in ("self", "id")}
        )

    def list(
            self,
            per_page: int = 10,
            page:     int = 1,
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/action_egress_control_rules",
            params = {
                "per_page": per_page,
                "page":     page
            }
        )

    def delete(
            self,
            id: Union[str, int]
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/action_egress_control_rules/{id}"
        )