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

        Args:
            team_id: Only dashboards of this team.
            order: How to order the results: ``NAME`` (the default), ``RECENTLY_EDITED`` (the latest
                edit first), ``LEAST_RECENTLY_EDITED``, ``CREATED_DESC`` (the newest first) or
                ``CREATED_ASC``.
            per_page: The number of results per page.
            page: The page to return, starting at 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``dashboards``, the dashboards of the
            page, and ``meta``, the pagination details.
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

        Creates a dashboard from what ``export`` returned, or replaces an existing one. The names of
        the dashboards of a team are unique.

        Args:
            team_id: The ID of the team that gets the dashboard.
            data: The dashboard in exported form: what ``export`` returned. Tines needs a
                ``schema_version`` of 1 and a ``dashboard`` object with a ``name``.
            mode: ``new`` to create a dashboard or ``replace`` to replace an existing one by name. A
                replaced dashboard keeps its ID and its creation time.
            new_name: The name of the dashboard. In ``replace`` mode, it selects which existing
                dashboard to replace.

        Returns:
            A ``Response`` whose ``data`` is the dashboard, with a 201 status.
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
