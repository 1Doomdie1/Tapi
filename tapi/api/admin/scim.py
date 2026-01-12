from tapi.client      import Client
from typing           import Union, Dict
from tapi.utils.types import SCIMUserGroupMapping


class SCIMUserGroupMappingAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint      = "admin"

    def get(self):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/scim_user_group_mapping"
        )

    def update(
            self,
            mappings: Union[SCIMUserGroupMapping, Dict[str, str]]
    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/scim_user_group_mapping",
            json = {
                "mappings": mappings
            }
        )