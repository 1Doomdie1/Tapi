from tapi.http.client import Client
from .case            import CaseAPI
from .team            import TeamsAPI
from .story           import StoriesAPI
from .audit_log       import AuditLogsAPI

class TenantAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.cases      = CaseAPI(domain, apiKey)
        self.teams      = TeamsAPI(domain, apiKey)
        self.stories    = StoriesAPI(domain, apiKey)
        self.audit_logs = AuditLogsAPI(domain, apiKey)

    def info(self) -> dict:
        return self._http_request("GET", "/info")