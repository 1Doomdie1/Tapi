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

        Returns the flow usage of the tenant against its licensed flow limit, broken down by team.
        Tines recalculates the counts when a story changes, not on each request. Only tenant owners
        can call it, and only tenants on the flows pricing model can use it.

        The teams are paginated and one call returns one page.

        Args:
            per_page: The number of teams per page. Tines defaults to 20 and caps it at 500.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with:

            - ``flows``: the usage of the whole tenant, with ``used`` (flows in use), ``limit``
              (the licensed limit), ``allocated`` (flows given to specific teams) and
              ``unallocated`` (flows that teams without an allocation share).
            - ``teams``: the teams of the page. Each has ``id``, ``name``, ``flows_used``,
              ``flows_allocated`` and ``flows_available``. The last two are ``null`` for a team
              that has no allocation and draws from the unallocated flows.
            - ``meta``: ``current_page``, ``previous_page`` and ``next_page`` (links),
              ``next_page_number``, ``per_page``, ``pages`` (the number of pages) and ``count``.

            The reply is a 400 when the tenant is not on the flows pricing model, and a 400 for a
            ``per_page`` or ``page`` that is not a positive integer.
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

        Returns the time that Tines saved, as dated records, grouped by an hour, a day, a week or
        a month.

        The endpoint is paginated and one call returns one page. Read ``data["meta"]`` to decide
        whether to ask for the next page.

        Args:
            start_date: Only records after this time, as a ``datetime`` or an ISO 8601 string. A
                datetime without a timezone is treated as UTC. The reply holds no records when it
                is left out, so pass it to get any.
            end_date: Only records before this time, in the same formats. Tines defaults to the
                current time, and it must be later than ``start_date``.
            date_unit: How to group the records: ``hour``, ``day``, ``week`` or ``month``, in
                lower case. Tines defaults to ``day``. A value in upper case is not refused, and
                the reply holds no records.
            fill_gaps: Whether to fill the groups that have no data with a value of 0. Tines
                defaults to ``True``. ``False`` is sent, and then only the groups that have data
                are returned.
            team_id: Only records of this team.
            story_id: Only records of this story.
            action_id: Only records of this action.
            per_page: The number of results per page. Tines defaults to 20 and caps it at 500.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``time_saved``, the records of the
            page, and ``meta``, the pagination details: ``current_page``, ``previous_page`` and
            ``next_page`` (links), ``next_page_number``, ``per_page``, ``pages`` (the number of
            pages) and ``count``. Each record has ``date``, a UTC timestamp rounded down to the
            ``date_unit`` (written ``2026-11-23T00:00:00Z``, and ``2026-11-23T21:00:00+00:00``
            for hours), and ``value``, the time saved in seconds as a number. The reply is a 400
            for a ``date_unit`` that is not valid, an ``end_date`` that is not later than the
            start, and a ``per_page`` or ``page`` that is not a positive integer, a 422 for a date
            that cannot be read, and a 404 (``Team not found``, ``Story not found`` or ``Action
            not found``) for a ``team_id``, ``story_id`` or ``action_id`` that does not exist or
            that the key cannot see.
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
