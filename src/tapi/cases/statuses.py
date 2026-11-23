from tapi.cases.types import CaseStatus
from tapi.core import Response, Transport
from tapi.core.params import omit_none


class Statuses:
    """The case statuses of a team, available as ``tines.cases.statuses``.

    A case is open or closed, and a case status (a sub-status) refines that. A status, as returned
    by ``get``, ``create`` and ``update`` and listed by ``list``, has ``id``, ``name``, ``slug``,
    ``description``, ``parent_status`` (``OPEN`` or ``CLOSED``), ``default``, ``team``,
    ``created_at`` and ``updated_at``. Every team starts with four statuses that have ``default``
    set: ``to_do`` and ``in_progress`` under ``OPEN``, and ``done`` and ``canceled`` under
    ``CLOSED``. A case is given a status with the ``sub_status_id`` of ``tines.cases.create`` and
    ``update``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        team_id: int,
        parent_status: CaseStatus | None = None,
        search: str | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List the case statuses of a team. ``GET /api/v1/case_sub_statuses``

        The endpoint is paginated and one call returns one page.

        Args:
            team_id: The ID of the team.
            parent_status: Only statuses under this one: ``OPEN`` or ``CLOSED``.
            search: Only statuses whose name contains this text, in any case.
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_sub_statuses``, the statuses of
            the page, and ``meta``, the pagination details. The reply is a 400 with ``team_id is
            required`` when ``team_id`` is missing.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/case_sub_statuses",
            params=omit_none(
                values={
                    "team_id": team_id,
                    "parent_status": parent_status,
                    "search": search,
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )

    def get(self, *, status_id: int) -> Response:
        """Get a case status. ``GET /api/v1/case_sub_statuses/{status_id}``

        Args:
            status_id: The ID of the status.

        Returns:
            A ``Response`` whose ``data`` is the status. The reply is a 404 with ``Case sub status
            not found`` for a status that does not exist.
        """
        return self._transport.request(method="GET", path=f"/api/v1/case_sub_statuses/{status_id}")

    def create(
        self,
        *,
        team_id: int,
        name: str,
        parent_status: CaseStatus | None = None,
        description: str | None = None,
    ) -> Response:
        """Create a case status. ``POST /api/v1/case_sub_statuses``

        Args:
            team_id: The ID of the team that gets the status.
            name: The name of the status.
            parent_status: The status that this one is under: ``OPEN`` or ``CLOSED``, which Tines
                also takes in lower case. Tines defaults to ``OPEN``.
            description: A description of the status.

        Returns:
            A ``Response`` whose ``data`` is the created status, with a 201 status. The reply is a
            422 for a ``parent_status`` that is not valid and for a ``name`` that the team already
            has (``A status named "..." already exists in this team.``), and a 404 for a team that
            does not exist.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/case_sub_statuses",
            json=omit_none(
                values={
                    "team_id": team_id,
                    "name": name,
                    "parent_status": parent_status,
                    "description": description,
                }
            ),
        )

    def update(
        self,
        *,
        status_id: int,
        name: str | None = None,
        description: str | None = None,
    ) -> Response:
        """Change a case status. ``PATCH /api/v1/case_sub_statuses/{status_id}``

        The Tines documentation shows this operation as ``PUT``. The OpenAPI document lists the
        same operation under ``PUT`` and ``PATCH``, and tapi uses ``PATCH``.

        Args:
            status_id: The ID of the status.
            name: A new name. The slug changes with it.
            description: A new description.

        Returns:
            A ``Response`` whose ``data`` is the updated status. The reply is a 404 with
            ``TeamCaseSubStatus not found`` for a status that does not exist.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v1/case_sub_statuses/{status_id}",
            json=omit_none(values={"name": name, "description": description}),
        )

    def delete(self, *, status_id: int, fallback_status_id: int) -> Response:
        """Delete a case status. ``DELETE /api/v1/case_sub_statuses/{status_id}``

        Args:
            status_id: The ID of the status.
            fallback_status_id: The ID of the status that the cases with the deleted one move to.
                It must be under the same parent status as the deleted one. Tines accepts the
                deleted status itself.

        Returns:
            A ``Response`` with a 204 status and no data. The reply is a 400 with
            ``fallback_status_id is required`` when ``fallback_status_id`` is missing, a 404 for a
            status that does not exist or a fallback that does not, and a 422 with ``Fallback
            status must be of the same parent status`` for a fallback under the other parent.
        """
        return self._transport.request(
            method="DELETE",
            path=f"/api/v1/case_sub_statuses/{status_id}",
            params={"fallback_status_id": fallback_status_id},
        )
