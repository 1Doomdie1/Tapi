from tapi.client      import Client
from tapi.utils.types import AgentType
from typing           import Union, Dict, Any


class TemplatesAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "admin"

    def create(
            self,
            name:          str,
            description:   str,
            vendor:        str,
            product:       str,
            agent_type:    Union[AgentType, str],
            agent_options: Dict[str, Any]
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/templates",
            json = {
                "name":          name,
                "description":   description,
                "vendor":        vendor,
                "product":       product,
                "agent_type":    agent_type,
                "agent_options": agent_options
            }
        )

    def get(
            self,
            template_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/templates/{template_id}"
        )

    def update(
            self,
            template_id:   int,
            name:          str,
            description:   str,
            vendor:        str,
            product:       str,
            agent_type:    Union[AgentType, str],
            agent_options: Dict[str, Any]
    ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/templates/{template_id}",
            json = {
                "name": name,
                "description": description,
                "vendor": vendor,
                "product": product,
                "agent_type": agent_type,
                "agent_options": agent_options
            }
        )

    def list(
            self,
            per_page: int = 10,
            page:     int = 1
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/templates",
            params = {
                "per_page": per_page,
                "page": page
            }
        )

    def delete(
            self,
            template_id: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/templates/{template_id}"
        )