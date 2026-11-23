from typing import Literal

from tapi.core import Response, Transport
from tapi.core.params import omit_none
from tapi.teams.members import Members

TeamScope = Literal["all", "standard", "personal_only"]


class Teams:
    """Teams, available as ``tines.teams``.

    A team, as returned by ``get``, ``create`` and ``update`` and listed by ``list``, has ``id``,
    ``name`` and ``groups``: a list of objects with the ``id`` and ``name`` of each group of the
    team, empty if it has none.

    Args:
        transport: The transport used to send requests.

    Attributes:
        members: The members of a team. See ``tapi.teams.Members``.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport
        self.members = Members(transport=transport)

    def list(
        self,
        *,
        scope: TeamScope | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List teams. ``GET /api/v1/teams``

        The endpoint is paginated and one call returns one page. Tines also accepts the deprecated
        ``include_personal_teams`` and ``include_drafts`` parameters, which ``scope`` replaces and
        tapi does not offer.

        Args:
            scope: Which teams to list: ``standard`` for shared teams, ``personal_only`` for
                personal teams or ``all`` for both. Tines defaults to ``standard``.
            per_page: The number of results per page. Tines defaults to 20 and caps it at 500.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``teams``, the teams of the page, and
            ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/teams",
            params=omit_none(values={"scope": scope, "per_page": per_page, "page": page}),
        )

    def get(self, *, team_id: int) -> Response:
        """Get a team. ``GET /api/v1/teams/{team_id}``

        Args:
            team_id: The ID of the team to retrieve.

        Returns:
            A ``Response`` whose ``data`` is the team. The reply is a 404 with the message
            ``Team not found`` when no team with that ID is visible to your key.
        """
        return self._transport.request(method="GET", path=f"/api/v1/teams/{team_id}")

    def create(self, *, name: str) -> Response:
        """Create a team. ``POST /api/v1/teams``

        Args:
            name: The name of the team.

        Returns:
            A ``Response`` whose ``data`` is the created team, with a 201 status.
        """
        return self._transport.request(method="POST", path="/api/v1/teams", json={"name": name})

    def update(self, *, team_id: int, name: str) -> Response:
        """Rename a team. ``PATCH /api/v1/teams/{team_id}``

        The Tines documentation shows this operation as ``PUT``. The OpenAPI document lists the
        same operation under ``PUT`` and ``PATCH``, and tapi uses ``PATCH``.

        Args:
            team_id: The ID of the team to update.
            name: The new name of the team. Tines answers an update without it with a 500 and
                changes nothing, so it is required.

        Returns:
            A ``Response`` whose ``data`` is the updated team.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v1/teams/{team_id}",
            json={"name": name},
        )

    def delete(self, *, team_id: int) -> Response:
        """Delete a team. ``DELETE /api/v1/teams/{team_id}``

        Args:
            team_id: The ID of the team to delete.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(method="DELETE", path=f"/api/v1/teams/{team_id}")

    def destroy_static_external_id(self, *, team_id: int) -> Response:
        """Destroy a static external ID. ``POST /api/v1/teams/{team_id}/destroy_static_external_id``

        Destroys the static external ID of a team.

        Args:
            team_id: The ID of the team whose static external ID is destroyed.

        Returns:
            A ``Response`` with a 200 status. The Tines docs say the body is the ID of the
            destroyed static external ID, and show a bare number. The reply is a 422 with the
            message ``Team static external ID not found`` when the team has none.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/teams/{team_id}/destroy_static_external_id",
        )
