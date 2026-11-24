from collections.abc import Mapping, Sequence
from typing import Any

from tapi.admin.types import ActionInput, AgentType, ReadAccess
from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_list


class Templates:
    """The private templates of the tenant, available as ``tines.admin.templates``.

    A template is an action that can be reused in stories. A template, as listed by ``list`` and
    returned by the other methods, has ``id``, ``name``, ``description``, ``agent_type``,
    ``agent_options``, ``vendor``, ``product``, ``team_id``, ``folder_id`` (``null`` when it is not
    in a folder), ``read_access``, ``shared_team_slugs`` and ``action_inputs``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        search: str | None = None,
        folder_id: int | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List templates. ``GET /api/v1/admin/templates``

        Lists the private templates.

        Args:
            search: Only templates that match this text in the name, the description, the vendor,
                the product or the action options.
            folder_id: Only templates in this folder.
            per_page: The number of results per page.
            page: The page to return, starting at 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``admin/templates``, the templates of
            the page, and ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/admin/templates",
            params=omit_none(
                values={
                    "search": search,
                    "folder_id": folder_id,
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )

    def get(self, *, template_id: int) -> Response:
        """Get a template. ``GET /api/v1/admin/templates/{template_id}``

        Args:
            template_id: The ID of the template.

        Returns:
            A ``Response`` whose ``data`` is the template. The reply is a 404 with ``Template not
            found`` for a template that does not exist.
        """
        return self._transport.request(method="GET", path=f"/api/v1/admin/templates/{template_id}")

    def create(
        self,
        *,
        name: str,
        agent_type: AgentType,
        agent_options: Mapping[str, Any],
        product: str,
        description: str,
        vendor: str,
        team_id: int | None = None,
        folder_id: int | None = None,
        read_access: ReadAccess | None = None,
        shared_team_slugs: Sequence[str] | None = None,
        action_inputs: Sequence[ActionInput] | None = None,
    ) -> Response:
        """Create a template. ``POST /api/v1/admin/templates``

        Args:
            name: The name of the template. Tines does not require it to be unique.
            agent_type: The type of action to create.
            agent_options: The options of the action, as an object.
            product: The name of the product.
            description: A description of the template. Tines refuses a template without one,
                although the OpenAPI document does not list it as required.
            vendor: The name of the vendor. Required in the same way.
            team_id: The ID of the team that the template belongs to.
            folder_id: The ID of a template folder of the same team to put the template in.
            read_access: Where the template can be used: ``TEAM``, ``GLOBAL`` or ``SPECIFIC_TEAMS``,
                which is a premium feature that Tines ignored without an error where it was not
                available.
            shared_team_slugs: The slugs of the teams where the template can be used. Needed for
                ``SPECIFIC_TEAMS``.
            action_inputs: The input parameters of the template. See ``tapi.admin.ActionInput``.

        Returns:
            A ``Response`` whose ``data`` is the created template, with a 200 status.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/admin/templates",
            json=omit_none(
                values={
                    "name": name,
                    "agent_type": agent_type,
                    "agent_options": agent_options,
                    "product": product,
                    "description": description,
                    "vendor": vendor,
                    "team_id": team_id,
                    "folder_id": folder_id,
                    "read_access": read_access,
                    "shared_team_slugs": to_list(values=shared_team_slugs),
                    "action_inputs": to_list(values=action_inputs),
                }
            ),
        )

    def update(
        self,
        *,
        template_id: int,
        name: str,
        description: str,
        agent_type: AgentType,
        agent_options: Mapping[str, Any],
        vendor: str,
        product: str,
        folder_id: int | None = None,
        read_access: ReadAccess | None = None,
        shared_team_slugs: Sequence[str] | None = None,
        action_inputs: Sequence[ActionInput] | None = None,
    ) -> Response:
        """Change a template. ``PATCH /api/v1/admin/templates/{template_id}``

        A full update: send the name, the description, the type, the options, the vendor and the
        product every time. To change the team, use ``move``.

        Args:
            template_id: The ID of the template.
            name: The name of the template.
            description: A description of the template.
            agent_type: The type of action. It cannot be changed. See ``create`` for the values.
            agent_options: The options of the action, as an object.
            vendor: The name of the vendor.
            product: The name of the product.
            folder_id: The ID of a template folder of the same team.
            read_access: ``TEAM``, ``GLOBAL`` or ``SPECIFIC_TEAMS``.
            shared_team_slugs: The slugs of the teams where it can be used. Needed for
                ``SPECIFIC_TEAMS``.
            action_inputs: The input parameters. They replace the old ones, and an empty list
                removes them.

        Returns:
            A ``Response`` whose ``data`` is the updated template.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v1/admin/templates/{template_id}",
            json=omit_none(
                values={
                    "name": name,
                    "description": description,
                    "agent_type": agent_type,
                    "agent_options": agent_options,
                    "vendor": vendor,
                    "product": product,
                    "folder_id": folder_id,
                    "read_access": read_access,
                    "shared_team_slugs": to_list(values=shared_team_slugs),
                    "action_inputs": to_list(values=action_inputs),
                }
            ),
        )

    def delete(self, *, template_id: int) -> Response:
        """Delete a template. ``DELETE /api/v1/admin/templates/{template_id}``

        Args:
            template_id: The ID of the template.

        Returns:
            A ``Response`` with a 204 status and no data. The reply is a 404 with ``Template not
            found`` for a template that does not exist.
        """
        return self._transport.request(
            method="DELETE", path=f"/api/v1/admin/templates/{template_id}"
        )

    def move(
        self,
        *,
        template_id: int,
        team_id: int,
        folder_id: int | None = None,
    ) -> Response:
        """Move a template to another team. ``POST /api/v1/admin/templates/{template_id}/move``

        The access settings of the template are reset to team-only visibility. Resources and
        credentials that the template uses may not exist in the target team.

        Args:
            template_id: The ID of the template.
            team_id: The ID of the team to move the template to.
            folder_id: The ID of a template folder of the target team to put the template in.

        Returns:
            A ``Response`` whose ``data`` is the updated template, with a 200 status. Moving to
            the team that it already has is accepted. The reply is a 404 with ``Template not
            found``, ``Team not found`` or ``Folder not found``.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/admin/templates/{template_id}/move",
            json=omit_none(values={"team_id": team_id, "folder_id": folder_id}),
        )
