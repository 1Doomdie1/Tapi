from tapi.admin.action_egress_control_rules import ActionEgressControlRules
from tapi.admin.ip_access_control_rules import IpAccessControlRules
from tapi.admin.roles import Roles
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
    a 404.

    Args:
        transport: The transport used to send requests.

    Attributes:
        action_egress_control_rules: The rules for the outbound traffic of actions. See
            ``tapi.admin.ActionEgressControlRules``.
        ip_access_control_rules: The rules for who may access the tenant. See
            ``tapi.admin.IpAccessControlRules``.
        roles: The roles of the tenant. See ``tapi.admin.Roles``.
        sync_destinations: The story sync destinations. See ``tapi.admin.SyncDestinations``.
        templates: The private templates. See ``tapi.admin.Templates``.
        tunnels: The tunnels. See ``tapi.admin.Tunnels``.
        users: The users of the tenant. See ``tapi.admin.Users``.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport
        self.action_egress_control_rules = ActionEgressControlRules(transport=transport)
        self.ip_access_control_rules = IpAccessControlRules(transport=transport)
        self.roles = Roles(transport=transport)
        self.sync_destinations = SyncDestinations(transport=transport)
        self.templates = Templates(transport=transport)
        self.tunnels = Tunnels(transport=transport)
        self.users = Users(transport=transport)
