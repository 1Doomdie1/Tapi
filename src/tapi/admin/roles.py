from collections.abc import Sequence

from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_list


class Roles:
    """The roles of the tenant, available as ``tines.admin.roles``.

    A role is a set of permissions that a user can have in a team. Tines has default roles, such as
    ``TEAM_ADMIN``, and a tenant can add custom roles. A role, as listed by ``list`` and returned
    by the other methods, has ``id`` (the name of a default role, and a number as a string for a
    custom one, although ``create`` returns that number as an integer), ``name``, ``type``
    (``default`` or ``custom``), ``description``, ``permissions`` (a list of permission names),
    ``created_at`` and ``updated_at`` (``null`` for a default role), and ``builder`` (whether the
    role grants permission to build and edit stories).

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List roles. ``GET /api/v1/admin/roles``

        Lists the default and the custom roles.

        The endpoint is paginated and one call returns one page. Read ``data["meta"]`` to decide
        whether to ask for the next page.

        Args:
            per_page: The number of results per page. Tines defaults to 20. It does not refuse a
                value that is not valid: ``0`` gives the default and a large value is not capped.
            page: The page to return, starting at 1. Tines defaults to 1, and ``0`` is accepted.

        Returns:
            A ``Response`` whose ``data`` is an object with ``admin/roles``, the roles of the
            page, and ``meta``, the pagination details: ``current_page``, ``previous_page`` and
            ``next_page`` (links), ``next_page_number``, ``per_page``, ``pages`` (the number of
            pages) and ``count``.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/admin/roles",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )

    def get(self, *, role_id: str) -> Response:
        """Get a role. ``GET /api/v1/admin/roles/{role_id}``

        Args:
            role_id: The ID or the name of the role, which can be a default role. A default role
                was found in lower case too.

        Returns:
            A ``Response`` whose ``data`` is the role. The reply is a 404 with ``Role not found``
            for a role that does not exist.
        """
        return self._transport.request(method="GET", path=f"/api/v1/admin/roles/{role_id}")

    def create(
        self,
        *,
        name: str,
        permissions: Sequence[str],
        description: str | None = None,
    ) -> Response:
        """Create a custom role. ``POST /api/v1/admin/roles``

        Args:
            name: The name of the role. It is unique among the custom roles.
            permissions: The names of the permissions to give the role, such as ``STORY_CREATE``.
                The Tines docs link a table of the permissions. A default role lists its own.
                The list cannot be empty, and Tines refuses a name that is not a permission.
            description: A description of the role.

        Returns:
            A ``Response`` whose ``data`` is the created role, with a 201 status. The reply is a
            422 for a name that another custom role has, a permission that does not exist
            (``NOT_A_PERMISSION is not a valid permission``) and an empty list.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/admin/roles",
            json=omit_none(
                values={
                    "name": name,
                    "permissions": to_list(values=permissions),
                    "description": description,
                }
            ),
        )

    def update(
        self,
        *,
        role_id: str,
        description: str | None = None,
        permissions: Sequence[str] | None = None,
    ) -> Response:
        """Change a custom role. ``PATCH /api/v1/admin/roles/{role_id}``

        The OpenAPI document lists the same operation under ``PUT`` and ``PATCH``, and tapi uses
        ``PATCH``. The name of a role cannot be changed, and a ``name`` in the body is ignored.

        Args:
            role_id: The ID or the name of the role.
            description: A new description.
            permissions: The names of the permissions, which replace the old ones. The list
                cannot be empty.

        Returns:
            A ``Response`` whose ``data`` is the updated role. A call that sends nothing is a 200
            and changes nothing. The reply is a 422 for an empty list of permissions, and a 404
            with ``Role not found`` for a role that does not exist.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v1/admin/roles/{role_id}",
            json=omit_none(
                values={"description": description, "permissions": to_list(values=permissions)}
            ),
        )

    def delete(self, *, role_id: str) -> Response:
        """Delete a custom role. ``DELETE /api/v1/admin/roles/{role_id}``

        Args:
            role_id: The ID or the name of the role.

        Returns:
            A ``Response`` with a 204 status and no data. The reply is a 404 with ``Role not
            found`` for a role that does not exist, which includes one that was deleted.
        """
        return self._transport.request(method="DELETE", path=f"/api/v1/admin/roles/{role_id}")
