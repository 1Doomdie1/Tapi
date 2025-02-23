from tapi.api.http.client import Client
from .case                import CaseAPI
from .team                import TeamsAPI
from .event               import EventsAPI
from .story               import StoriesAPI
from .audit_log           import AuditLogsAPI
from .credential          import CredentialsAPI


class TenantAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.cases       = CaseAPI(domain, apiKey)
        self.teams       = TeamsAPI(domain, apiKey)
        self.events      = EventsAPI(domain, apiKey)
        self.stories     = StoriesAPI(domain, apiKey)
        self.audit_logs  = AuditLogsAPI(domain, apiKey)
        self.credentials = CredentialsAPI(domain, apiKey)

    def info(self) -> dict:
        return self._http_request("GET", "info")
