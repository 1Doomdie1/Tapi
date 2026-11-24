from tapi.admin.action_egress_control_rules import ActionEgressControlRules
from tapi.admin.custom_certificate_authority import CustomCertificateAuthority
from tapi.admin.ip_access_control_rules import IpAccessControlRules
from tapi.admin.jobs import Jobs
from tapi.admin.license import License
from tapi.admin.roles import Roles
from tapi.admin.smtp import Smtp
from tapi.admin.sync_destinations import SyncDestinations
from tapi.admin.templates import Templates
from tapi.admin.tunnels import Tunnels
from tapi.admin.users import Users
from tapi.core import Transport


class Admin:
    """Administration of the tenant, available as ``tines.admin``.

    The module has no methods of its own: each area of the administration is an attribute. The
    Tines docs and the OpenAPI document do not say that a tenant owner key is needed for every
    route, but they do say it for the health of a tunnel, and a key without access to a route gets
    a 404. The license and SMTP routes are for self-hosted tenants, and the jobs routes for
    dedicated tenants.

    Args:
        transport: The transport used to send requests.

    Attributes:
        action_egress_control_rules: The rules for the outbound traffic of actions. See
            ``tapi.admin.ActionEgressControlRules``.
        custom_certificate_authority: The certificate authority of the IMAP and HTTP Request
            actions. See ``tapi.admin.CustomCertificateAuthority``.
        ip_access_control_rules: The rules for who may access the tenant. See
            ``tapi.admin.IpAccessControlRules``.
        jobs: The background jobs of a dedicated tenant. See ``tapi.admin.Jobs``.
        license: The license of a self-hosted tenant. See ``tapi.admin.License``.
        roles: The roles of the tenant. See ``tapi.admin.Roles``.
        smtp: The SMTP configuration of a self-hosted tenant. See ``tapi.admin.Smtp``.
        sync_destinations: The story sync destinations. See ``tapi.admin.SyncDestinations``.
        templates: The private templates. See ``tapi.admin.Templates``.
        tunnels: The tunnels. See ``tapi.admin.Tunnels``.
        users: The users of the tenant. See ``tapi.admin.Users``.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport
        self.action_egress_control_rules = ActionEgressControlRules(transport=transport)
        self.custom_certificate_authority = CustomCertificateAuthority(transport=transport)
        self.ip_access_control_rules = IpAccessControlRules(transport=transport)
        self.jobs = Jobs(transport=transport)
        self.license = License(transport=transport)
        self.roles = Roles(transport=transport)
        self.smtp = Smtp(transport=transport)
        self.sync_destinations = SyncDestinations(transport=transport)
        self.templates = Templates(transport=transport)
        self.tunnels = Tunnels(transport=transport)
        self.users = Users(transport=transport)
