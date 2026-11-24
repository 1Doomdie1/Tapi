from datetime import datetime

from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_iso
from tapi.stories.types import StoryMode


class Runs:
    """Story runs, available as ``tines.stories.runs``.

    A story run, as returned by ``get_summary`` and listed by ``list``, has ``guid``,
    ``story_id``, ``team_id`` (the team that owns the story now, which can differ from the team at
    the time of the run), ``start_time`` and ``end_time`` (ISO 8601 timestamps, ``end_time`` is
    ``null`` while the run is going), ``duration`` (seconds), ``action_count``, ``event_count``,
    ``story_mode`` (``LIVE`` or ``TEST``), and ``draft_id`` and ``draft_name`` (the selected
    draft, in ``TEST`` mode).

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        story_id: int,
        story_mode: StoryMode | None = None,
        draft_id: int | None = None,
        since: datetime | str | None = None,
        until: datetime | str | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List the runs of a story. ``GET /api/v1/stories/{story_id}/runs``

        Args:
            story_id: The ID of the story.
            story_mode: The mode of the story: ``TEST`` or ``LIVE``.
            draft_id: Only runs of this draft.
            since: Only runs that started after this time. A ``datetime``, or an ISO 8601 string. A
                ``datetime`` without a timezone is treated as UTC.
            until: Only runs that started until this time. A ``datetime``, or an ISO 8601 string. A
                ``datetime`` without a timezone is treated as UTC.
            per_page: The number of results per page.
            page: The page to return, starting at 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``story_runs``, the runs of the page,
            and ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/stories/{story_id}/runs",
            params=omit_none(
                values={
                    "story_mode": story_mode,
                    "draft_id": draft_id,
                    "since": to_iso(value=since),
                    "until": to_iso(value=until),
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )

    def list_events(
        self,
        *,
        story_id: int,
        story_run_guid: str,
        story_mode: StoryMode | None = None,
        draft_id: int | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List the events of a run. ``GET /api/v1/stories/{story_id}/runs/{story_run_guid}``

        Args:
            story_id: The ID of the story.
            story_run_guid: The guid of the story run.
            story_mode: The mode of the story: ``TEST`` or ``LIVE``.
            draft_id: Only events of this draft.
            per_page: The number of results per page.
            page: The page to return, starting at 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``story_run_events``, a list of objects
            with ``id``, ``action_id`` (the action that emitted the event), ``created_at`` and
            ``is_reemitted``, and ``meta``, the pagination details. A guid that does not exist is
            answered with a 200 and not with a 404.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/stories/{story_id}/runs/{story_run_guid}",
            params=omit_none(
                values={
                    "story_mode": story_mode,
                    "draft_id": draft_id,
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )

    def get_summary(
        self,
        *,
        story_id: int,
        story_run_guid: str,
        story_mode: StoryMode | None = None,
        draft_id: int | None = None,
    ) -> Response:
        """Get a run. ``GET /api/v1/stories/{story_id}/runs/{story_run_guid}/summary``

        Args:
            story_id: The ID of the story.
            story_run_guid: The guid of the story run.
            story_mode: The mode of the story: ``TEST`` or ``LIVE``.
            draft_id: The draft the run belongs to.

        Returns:
            A ``Response`` whose ``data`` is an object with ``story_run``, the run. The reply is a
            404 with the message ``Story run not found`` when no run has that guid.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/stories/{story_id}/runs/{story_run_guid}/summary",
            params=omit_none(values={"story_mode": story_mode, "draft_id": draft_id}),
        )
