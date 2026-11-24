from datetime import datetime

from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_iso
from tapi.reporting.types import DateUnit


class Reporting:
    """Reports about the tenant, available as ``tines.reporting``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def flow_usage(
        self,
        *,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """Get flow usage by team. ``GET /api/v1/reporting/flow_usage``

        For tenant owners on the flows pricing model. The counts change when a story changes.

        Args:
            per_page: The number of teams per page, at most 500.
            page: The page to return, from 1.

        Returns:
            A ``Response`` whose ``data`` has ``flows`` (``used``, ``limit``, ``allocated`` and
            ``unallocated``), ``teams`` (each with ``id``, ``name``, ``flows_used``,
            ``flows_allocated`` and ``flows_available``) and ``meta``.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/reporting/flow_usage",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )

    def time_saved(
        self,
        *,
        start_date: datetime | str | None = None,
        end_date: datetime | str | None = None,
        date_unit: DateUnit | None = None,
        fill_gaps: bool | None = None,
        team_id: int | None = None,
        story_id: int | None = None,
        action_id: int | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List time saved. ``GET /api/v1/reporting/time_saved``

        Returns the time that Tines saved, as dated records, grouped by an hour, a day, a week or a
        month.

        Args:
            start_date: Only records after this time, as a ``datetime`` or an ISO 8601 string. A
                datetime without a timezone is treated as UTC. The reply holds no records when it is
                left out, so pass it to get any.
            end_date: Only records before this time, in the same formats.
            date_unit: How to group the records: ``hour``, ``day``, ``week`` or ``month``, in lower
                case. A value in upper case is not refused, and the reply holds no records.
            fill_gaps: Whether to fill the groups that have no data with a value of 0. ``False`` is
                sent, and then only the groups that have data are returned.
            team_id: Only records of this team.
            story_id: Only records of this story.
            action_id: Only records of this action.
            per_page: The number of results per page.
            page: The page to return, starting at 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``time_saved``, the records of the page,
            and ``meta``, the pagination details. Each record has ``date``, a UTC timestamp rounded
            down to the ``date_unit`` (written ``2026-11-23T00:00:00Z``, and
            ``2026-11-23T21:00:00+00:00`` for hours), and ``value``, the time saved in seconds as a
            number.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/reporting/time_saved",
            params=omit_none(
                values={
                    "start_date": to_iso(value=start_date),
                    "end_date": to_iso(value=end_date),
                    "date_unit": date_unit,
                    "fill_gaps": fill_gaps,
                    "team_id": team_id,
                    "story_id": story_id,
                    "action_id": action_id,
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )
