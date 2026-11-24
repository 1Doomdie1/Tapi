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

    Use it as a context manager, or call ``close`` when you are done.

    Args:
        tenant_domain: The domain of your tenant, such as ``acme.tines.com``. Defaults to the
            ``TINES_TENANT_DOMAIN`` environment variable.
        api_key: A Tines API key. Defaults to the ``TINES_API_KEY`` environment variable.
        timeout: Seconds to wait for the connection and for each part of a reply.

    Raises:
        TinesConfigurationError: If the tenant domain or the API key is missing or invalid.

    The modules are attributes of the client:

    - ``admin``: Administration of the tenant.
    - ``ai``: AI providers and AI usage.
    - ``apps``: Apps.
    - ``audit_logs``: Audit logs.
    - ``cases``: Cases.
    - ``change_requests``: Change requests of stories.
    - ``credentials``: Credentials.
    - ``dashboards``: Dashboards.
    - ``folders``: Folders.
    - ``info``: Information about your tenant.
    - ``records``: Records, their types and their views.
    - ``reporting``: Reports about your tenant.
    - ``resources``: Resources.
    - ``skills``: Skills of AI agents.
    - ``stories``: Stories and their sub-areas.
    - ``tags``: Tags.
    - ``teams``: Teams and their members.
    - ``workbench``: Workbench conversations.
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
