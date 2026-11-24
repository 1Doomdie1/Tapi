from types import TracebackType
from typing import Self

from tapi.admin import Admin
from tapi.ai import AI
from tapi.apps import Apps
from tapi.audit_logs import AuditLogs
from tapi.cases import Cases
from tapi.change_requests import ChangeRequests
from tapi.core.config import resolve_api_key, resolve_base_url
from tapi.core.transport import Transport
from tapi.credentials import Credentials
from tapi.dashboards import Dashboards
from tapi.folders import Folders
from tapi.info import Info
from tapi.records import Records
from tapi.reporting import Reporting
from tapi.resources import Resources
from tapi.skills import Skills
from tapi.stories import Stories
from tapi.tags import Tags
from tapi.teams import Teams
from tapi.workbench import Workbench


class Tines:
    """Entry point to the Tines API for one tenant.

    The client holds the connection and the credentials. Use it as a context manager, or call
    ``close`` when you are done, to release the connections.

    Args:
        tenant_domain: The domain of your Tines tenant, such as ``acme.tines.com``. Self-hosted
            tenants and tenants with a custom domain use their own domain. A scheme is accepted
            and any path is ignored. Defaults to the ``TINES_TENANT_DOMAIN`` environment variable.
        api_key: A Tines API key: personal, service, team or tenant owner. Defaults to the
            ``TINES_API_KEY`` environment variable.
        timeout: Seconds to wait for the connection and for each part of a reply. A request that
            takes longer raises ``TinesConnectionError``.

    Attributes:
        admin: Administration of the tenant. See ``tapi.admin.Admin``.
        ai: AI providers and AI usage. See ``tapi.ai.AI``.
        apps: Apps. See ``tapi.apps.Apps``.
        audit_logs: Audit logs. See ``tapi.audit_logs.AuditLogs``.
        cases: Cases, with their activities and assignees. See ``tapi.cases.Cases``.
        change_requests: Change requests of stories. See ``tapi.change_requests.ChangeRequests``.
        credentials: Credentials. See ``tapi.credentials.Credentials``.
        dashboards: Dashboards. See ``tapi.dashboards.Dashboards``.
        folders: Folders. See ``tapi.folders.Folders``.
        info: Information about your tenant. See ``tapi.info.Info``.
        records: Records, their types and their views. See ``tapi.records.Records``.
        reporting: Reports about your tenant. See ``tapi.reporting.Reporting``.
        resources: Resources. See ``tapi.resources.Resources``.
        skills: Skills of AI agents. See ``tapi.skills.Skills``.
        stories: Stories, their actions, drafts, runs, versions and change requests. See
            ``tapi.stories.Stories``.
        tags: Tags. See ``tapi.tags.Tags``.
        teams: Teams and their members. See ``tapi.teams.Teams``.
        workbench: Workbench conversations. See ``tapi.workbench.Workbench``.

    Raises:
        TinesConfigurationError: If the tenant domain or the API key is missing or invalid.
    """

    def __init__(
        self,
        *,
        tenant_domain: str | None = None,
        api_key: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        self._transport = Transport(
            base_url=resolve_base_url(tenant_domain=tenant_domain),
            api_key=resolve_api_key(api_key=api_key),
            timeout=timeout,
        )
        self.admin = Admin(transport=self._transport)
        self.ai = AI(transport=self._transport)
        self.apps = Apps(transport=self._transport)
        self.audit_logs = AuditLogs(transport=self._transport)
        self.cases = Cases(transport=self._transport)
        self.change_requests = ChangeRequests(transport=self._transport)
        self.credentials = Credentials(transport=self._transport)
        self.dashboards = Dashboards(transport=self._transport)
        self.folders = Folders(transport=self._transport)
        self.info = Info(transport=self._transport)
        self.records = Records(transport=self._transport)
        self.reporting = Reporting(transport=self._transport)
        self.resources = Resources(transport=self._transport)
        self.skills = Skills(transport=self._transport)
        self.stories = Stories(transport=self._transport)
        self.tags = Tags(transport=self._transport)
        self.teams = Teams(transport=self._transport)
        self.workbench = Workbench(transport=self._transport)

    def close(self) -> None:
        """Close the underlying connections."""
        self._transport.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"Tines(base_url={self._transport.base_url!r})"
