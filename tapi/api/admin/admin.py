from tapi.client                  import Client
from .job                         import JobsAPI
from .template                    import TemplatesAPI
from .ip_access_control           import IpAccessControlAPI
from .scim                        import SCIMUserGroupMappingAPI
from .action_egress_control_rules import ActionEgressControlRulesAPI


class AdminAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint           = "admin"
        self.jobs                    = JobsAPI(domain, apiKey)
        self.templates               = TemplatesAPI(domain, apiKey)
        self.ip_access_control       = IpAccessControlAPI(domain, apiKey)
        self.scim_user_group_mapping = SCIMUserGroupMappingAPI(domain, apiKey)
        self.egress_rules            = ActionEgressControlRulesAPI(domain, apiKey)


    def set_custom_certificate_authority(
            self,
            name:        str,
            certificate: str

    ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/custom_certificate_authority",
            json = {
                "name":        name,
                "certificate": certificate
            }
        )

    def tunnel_health(
            self,
            tunnel_name: str
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/tunnel/{tunnel_name}/health"
        )
