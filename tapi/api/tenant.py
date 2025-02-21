from tapi.api.http.client import Client
from tapi.api.case        import CaseAPI
from tapi.api.team        import TeamsAPI
from tapi.api.story       import StoriesAPI
from tapi.api.audit_log   import AuditLogsAPI
from tapi.api.credential  import CredentialsAPI

class TenantAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.cases       = CaseAPI(domain, apiKey)
        self.teams       = TeamsAPI(domain, apiKey)
        self.stories     = StoriesAPI(domain, apiKey)
        self.audit_logs  = AuditLogsAPI(domain, apiKey)
        self.credentials = CredentialsAPI(domain, apiKey)

    def info(self) -> dict:
        return self._http_request("GET", "info")
