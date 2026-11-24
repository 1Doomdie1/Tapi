from collections.abc import Mapping
from typing import Any

from tapi.core import Response, Transport
from tapi.core.params import omit_none
from tapi.records.types import RecordViewImportMode, RecordViewOrder


class RecordViews:
    """The record views, available as ``tines.records.record_views``.

    A record view is a saved view of a record type, with its filters, charts and table layout. A
    view, as listed by ``list``, has ``id``, ``name``, ``team`` and ``record_type`` (each an object
    with ``id`` and ``name``), ``created_at``, ``updated_at``, ``report_view`` (``record_table``,
    ``split_view`` or ``chart``), ``url`` and ``record_report_group_id``. These routes answer
    errors as a list of messages, not as the object of the other record routes.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        team_id: int | None = None,
        record_type_id: int | None = None,
        order: RecordViewOrder | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List record views. ``GET /api/v1/record_views``

        The endpoint is paginated and one call returns one page. Read ``data["meta"]`` to decide
        whether to ask for the next page.

        Args:
            team_id: Only the views of this team.
            record_type_id: Only the views of this record type.
            order: ``NAME``, ``RECENTLY_CREATED`` or ``RECENTLY_UPDATED``. Tines defaults to
                ``NAME``, also for a value that is not valid.
            per_page: The number of results per page. Tines defaults to 20 and caps it at 500.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``record_views``, the views of the
            page, and ``meta``, the pagination details: ``current_page``, ``previous_page`` and
            ``next_page`` (links), ``next_page_number``, ``per_page``, ``pages`` (the number of
            pages) and ``count``.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/record_views",
            params=omit_none(
                values={
                    "team_id": team_id,
                    "record_type_id": record_type_id,
                    "order": order,
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )

    def delete(self, *, record_view_id: int) -> Response:
        """Delete a record view. ``DELETE /api/v1/record_views/{record_view_id}``

        Args:
            record_view_id: The ID of the record view.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(
            method="DELETE", path=f"/api/v1/record_views/{record_view_id}"
        )

    def export(self, *, record_view_id: int) -> Response:
        """Export a record view. ``GET /api/v1/record_views/{record_view_id}/export``

        Pass the whole reply as ``data`` to ``import_`` to recreate the view in another team or
        tenant.

        Args:
            record_view_id: The ID of the record view.

        Returns:
            A ``Response`` whose ``data`` is an object with ``schema_version``, ``export_type``
            (``record_view``), ``exported_at`` and ``record_view``, which has ``name``,
            ``report_view``, ``elements`` (each with an ``id`` and the settings of a chart or a
            table) and ``layout`` (each entry has an ``i`` that is the ``id`` of its element).
        """
        return self._transport.request(
            method="GET", path=f"/api/v1/record_views/{record_view_id}/export"
        )

    def import_(
        self,
        *,
        team_id: int,
        data: Mapping[str, Any],
        mode: RecordViewImportMode | None = None,
        name: str | None = None,
    ) -> Response:
        """Import a record view. ``POST /api/v1/record_views/import``

        The record types and the story slugs that the view refers to must exist in the team, as
        Tines finds them by name and does not create them.

        Args:
            team_id: The ID of the team to add the view to.
            data: The view in the form that ``export`` returns, with ``schema_version``. Keep
                the ``id`` of each element and the ``i`` of each layout entry.
            mode: ``new`` to create a view, the default, or ``replace`` to replace the view of
                the team that has the same name.
            name: The name of the view. Tines defaults to the name in ``data``. With ``replace``
                it picks the view to replace.

        Returns:
            A ``Response`` with a 201 status whose ``data`` is an object with ``id``, ``name``,
            ``team`` (with ``id`` and ``name``), ``created_at`` and ``updated_at``. The reply is a
            400 when ``data`` is not a JSON object, cannot be read or holds a team that is not
            valid.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/record_views/import",
            json=omit_none(
                values={
                    "team_id": team_id,
                    "data": dict(data),
                    "mode": mode,
                    "name": name,
                }
            ),
        )
