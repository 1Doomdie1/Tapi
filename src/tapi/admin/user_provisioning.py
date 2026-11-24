from tapi.admin.types import UserGroupMapping
from tapi.core import Response, Transport


class UserProvisioning:
    """The user provisioning, available as ``tines.admin.user_provisioning``.

    The route is in the OpenAPI document and has no page in the Tines docs. It replaces the
    deprecated ``/api/v1/admin/scim_user_group_mapping`` routes, which tapi does not offer. There is
    no operation to read the mapping.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def update_mapping(self, *, user_group_mapping: UserGroupMapping) -> Response:
        """Update the mapping. ``POST /api/v1/admin/user_provisioning/mapping``

        Maps the groups of an identity provider to Tines teams, roles and tenant permissions. It
        replaces the whole mapping: adding to it is not supported, so send every entry you want to
        keep.

        Args:
            user_group_mapping: The new mapping, with ``mappings`` (objects with ``group_name``,
                ``team_name`` and ``role_name``), ``tenant_permissions`` (objects with
                ``group_name`` and ``permission``) and ``tenant_owners_groups`` (the names of the
                groups whose members become tenant owners). Every key is snake_case.

        Returns:
            A ``Response`` whose ``data`` is an object with ``user_group_mapping``, the updated
            mapping. The OpenAPI document lists a 400 for a key that is not snake_case, and a 422
            for the older ``sso_group`` key, which is ``group_name`` now.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/admin/user_provisioning/mapping",
            json={"user_group_mapping": user_group_mapping},
        )
