from collections.abc import Mapping
from typing import Any

from tapi.core import Response, Transport
from tapi.core.params import omit_none
from tapi.dashboards.types import DashboardOrder, ImportMode


class Dashboards:
    """Dashboards, available as ``tines.dashboards``.

    A dashboard belongs to a team and shows charts and lists of its records and cases. A dashboard,
    as listed by ``list`` and returned by ``import_``, has ``id``, ``name``, ``team`` (an object
    with the ``id`` and ``name`` of the team), ``created_at`` and ``updated_at``. Tines has no
    endpoint to create or change a dashboard other than ``import_``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        team_id: int | None = None,
        order: DashboardOrder | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List dashboards. ``GET /api/v1/dashboards``

        Lists the dashboards that the API key has access to.

        The endpoint is paginated and one call returns one page. Read ``data["meta"]`` to decide
        whether to ask for the next page.

        Args:
            team_id: Only dashboards of this team.
            order: How to order the results: ``NAME`` (the default), ``RECENTLY_EDITED`` (the
                latest edit first), ``LEAST_RECENTLY_EDITED``, ``CREATED_DESC`` (the newest
                first) or ``CREATED_ASC``. The Tines docs give ``RECENTLY_CREATED`` and
                ``RECENTLY_UPDATED`` instead, which Tines does not know: like any value that is not
                valid, they are not refused and the results are ordered by ``NAME``.
            per_page: The number of results per page. Tines defaults to 20 and caps it at 500.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``dashboards``, the dashboards of the
            page, and ``meta``, the pagination details: ``current_page``, ``previous_page`` and
            ``next_page`` (links), ``next_page_number``, ``per_page``, ``pages`` (the number of
            pages) and ``count``. The reply is a 404 with ``Team not found`` for a ``team_id``
            that does not exist, and a 400 for a ``per_page`` or ``page`` that is not a positive
            integer.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/dashboards",
            params=omit_none(
                values={
                    "team_id": team_id,
                    "order": order,
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )

    def delete(self, *, dashboard_id: int) -> Response:
        """Delete a dashboard. ``DELETE /api/v1/dashboards/{dashboard_id}``

        Args:
            dashboard_id: The ID of the dashboard.

        Returns:
            A ``Response`` with a 204 status and no data. The reply is a 404 with ``Dashboard not
            found`` for a dashboard that does not exist, which includes one that was deleted.
        """
        return self._transport.request(method="DELETE", path=f"/api/v1/dashboards/{dashboard_id}")

    def export(self, *, dashboard_id: int) -> Response:
        """Export a dashboard. ``GET /api/v1/dashboards/{dashboard_id}/export``

        The reply can be passed to ``import_`` to recreate the dashboard in another team or
        tenant.

        Args:
            dashboard_id: The ID of the dashboard.

        Returns:
            A ``Response`` whose ``data`` is an object with ``schema_version`` (1),
            ``export_type`` (``dashboard``), ``exported_at`` and ``dashboard``. The ``dashboard``
            object has the ``name``, the ``notes``, ``case_lists`` and ``record_charts`` it shows,
            and its ``layout``. The reply is a 404 with ``Dashboard not found`` for a dashboard
            that does not exist.
        """
        return self._transport.request(
            method="GET", path=f"/api/v1/dashboards/{dashboard_id}/export"
        )

    def import_(
        self,
        *,
        team_id: int,
        data: Mapping[str, Any],
        mode: ImportMode | None = None,
        new_name: str | None = None,
    ) -> Response:
        """Import a dashboard. ``POST /api/v1/dashboards/import``

        Creates a dashboard from what ``export`` returned, or replaces an existing one. The names
        of the dashboards of a team are unique.

        Args:
            team_id: The ID of the team that gets the dashboard.
            data: The dashboard in exported form: what ``export`` returned. Tines needs a
                ``schema_version`` of 1 and a ``dashboard`` object with a ``name``.
            mode: ``new`` to create a dashboard or ``replace`` to replace an existing one by name.
                Tines defaults to ``new``. A replaced dashboard keeps its ID and its creation
                time.
            new_name: The name of the dashboard. Tines defaults to the name in ``data``. In
                ``replace`` mode, it selects which existing dashboard to replace.

        Returns:
            A ``Response`` whose ``data`` is the dashboard, with a 201 status. The reply is a 400
            when ``data`` is not a JSON object (``data must be a JSON object``), has no
            ``schema_version`` or an unsupported one, or has no ``dashboard.name``, when ``new``
            finds a dashboard of that name in the team (``dashboard with name ... already exists
            for team``), and when ``replace`` finds none (``dashboard with name ... not found``).
            It is a 422 for a ``mode`` that is not valid, and a 404 with ``Team not found`` for a
            ``team_id`` that does not exist.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/dashboards/import",
            json=omit_none(
                values={
                    "team_id": team_id,
                    "data": data,
                    "mode": mode,
                    "new_name": new_name,
                }
            ),
        )
