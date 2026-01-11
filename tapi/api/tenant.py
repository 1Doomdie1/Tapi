from tapi.client import Client
from requests    import request
from .case       import CasesAPI
from .team       import TeamsAPI
from .admin      import AdminAPI
from .event      import EventsAPI
from .story      import StoriesAPI
from .folder     import FoldersAPI
from .record     import RecordsAPI
from .report     import ReportingAPI
from .resource   import ResourcesAPI
from .audit_log  import AuditLogsAPI
from .workbench  import WorkbenchAPI
from .credential import CredentialsAPI
from typing      import Optional, Literal


class TenantAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "info"
        self.cases         = CasesAPI(domain, apiKey)
        self.teams         = TeamsAPI(domain, apiKey)
        self.admin         = AdminAPI(domain, apiKey)
        self.events        = EventsAPI(domain, apiKey)
        self.stories       = StoriesAPI(domain, apiKey)
        self.folders       = FoldersAPI(domain, apiKey)
        self.records       = RecordsAPI(domain, apiKey)
        self.resources     = ResourcesAPI(domain, apiKey)
        self.reporting     = ReportingAPI(domain, apiKey)
        self.workbench     = WorkbenchAPI(domain, apiKey)
        self.audit_logs    = AuditLogsAPI(domain, apiKey)
        self.credentials   = CredentialsAPI(domain, apiKey)

    def trigger_webhook(
            self,
            path:   str,
            secret: str,
            method: Literal["GET", "PUT", "POST", "PATCH", "DELETE"] = "GET",
            domain: Optional[str]                                    = None,
            **kwargs
    ):
        domain = domain or self.domain

        req = request(
            method = method,
            url    = f"https://{domain}.tines.com/webhook/{path}/{secret}",
            **kwargs
        )

        return req.json()

    def info(self):
        return self._http_request(
            "GET",
            self.base_endpoint
        )

    def web_statistics(self):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/web_stats"
        )

    def worker_statistics(self):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/worker_stats"
        )

