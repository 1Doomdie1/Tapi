from tapi.client        import Client
from tapi.utils.helpers import is_ip_valid
from typing             import Optional, Union

class IpAccessControlAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "admin"

    def create(
            self,
            ip:          str,
            description: str
    ):
        if not is_ip_valid(ip):
            raise ValueError("Invalid IP address or CIDR range.")

        return self._http_request(
            "POST",
            f"{self.base_endpoint}/ip_access_control_rules",
            json = {
                "ip": ip,
                "description": description
            }
        )

    def get(
            self,
            id: Union[str, int]
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/ip_access_control_rules/{id}"
        )

    def update(
            self,
            id:          Union[str, int],
            ip:          str,
            description: str
    ):
        if not is_ip_valid(ip):
            raise ValueError("Invalid IP address or CIDR range.")

        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/ip_access_control_rules/{id}",
            json = {
                "ip": ip,
                "description": description
            }
        )

    def list(
            self,
            matching_ip: Optional[str] = None,
            per_page:    int           = 10,
            page:        int           = 1
    ):
        if matching_ip and not is_ip_valid(matching_ip):
            raise ValueError("Invalid IP address or CIDR range.")

        return self._http_request(
            "GET",
            f"{self.base_endpoint}/ip_access_control_rules",
            params = {key: value for key, value in locals().items() if value is not None and key != "self"}
        )

    def delete(
            self,
            id: Union[str, int]
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/ip_access_control_rules/{id}"
        )