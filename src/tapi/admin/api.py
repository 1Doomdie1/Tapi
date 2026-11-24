from tapi.admin.roles import Roles
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
        roles: The roles of the tenant. See ``tapi.admin.Roles``.
        templates: The private templates. See ``tapi.admin.Templates``.
        tunnels: The tunnels. See ``tapi.admin.Tunnels``.
        users: The users of the tenant. See ``tapi.admin.Users``.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport
        self.roles = Roles(transport=transport)
        self.templates = Templates(transport=transport)
        self.tunnels = Tunnels(transport=transport)
        self.users = Users(transport=transport)
