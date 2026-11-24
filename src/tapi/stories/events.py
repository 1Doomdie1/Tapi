from datetime import datetime
from typing import Literal

from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_iso


class Events:
    """The events of the tenant, available as ``tines.stories.events``.

    An event, as returned by ``get`` and listed by ``list``, has ``id``, ``agent_id`` (the ID of
    the action that emitted it), ``team_id`` (the team that owns the action now, which can differ
    from the team at the time), ``payload`` (an object), ``created_at`` and ``updated_at`` (ISO
    8601 timestamps; ``updated_at`` is always equal to ``created_at``), ``story_run_guid``,
    ``previous_events_ids`` (the IDs of the events of the upstream action in the same story run)
    and ``re_emitted``. The Tines docs samples also show a ``user_id``, which the replies did not
    have.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        team_id: int | None = None,
        story_id: int | None = None,
        story_mode: Literal["test"] | None = None,
        include_groups: bool | None = None,
        since_id: int | None = None,
        until_id: int | None = None,
        since: datetime | str | None = None,
        until: datetime | str | None = None,
        show_reemitted_events_only: bool | None = None,
        exclude_previous_event_payloads: bool | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List events. ``GET /api/v1/events``

        The endpoint is paginated and one call returns one page, the newest events first. A tenant
        can hold a very large number of events, so narrow the list: with ``since`` and ``until``
        or with a small ``per_page``. ``include_groups`` with ``story_id`` timed out on the tested
        tenant. To list the events of one action, use ``tines.stories.actions.list_events``.

        Args:
            team_id: Only events of this team. When it is given with ``story_id``, Tines ignores
                ``story_id``.
            story_id: Only events of this story.
            story_mode: ``test`` to list the events of the default test story. Only with
                ``story_id``.
            include_groups: Whether to include the events of groups in the story. Only with
                ``story_id``. Tines defaults to ``False``.
            since_id: Only events after this event ID.
            until_id: Only events until and including this event ID.
            since: Only events created after this time. A ``datetime``, or an ISO 8601 string. A
                ``datetime`` without a timezone is treated as UTC.
            until: Only events created until this time. A ``datetime``, or an ISO 8601 string. A
                ``datetime`` without a timezone is treated as UTC.
            show_reemitted_events_only: Only events that were re-emitted. Tines defaults to
                ``False``.
            exclude_previous_event_payloads: Keep only the output of the action in the payload of
                each event, without the payloads that came from upstream events of the story run.
                Tines defaults to ``False``.
            per_page: The number of results per page. Tines defaults to 20 and caps it at 500.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``events``, the events of the page,
            and ``meta``, the pagination details. The reply is a 400 when ``since`` or ``until``
            is not a time, a 422 when the payloads of the page add up to more than 200 MB, in
            which case a lower ``per_page`` helps, and a 504 with the message ``Listing events
            timed out; narrow since/until, reduce per_page, or filter by agent_id.`` when the
            list takes too long. A ``team_id`` that does not exist is a 404.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/events",
            params=omit_none(
                values={
                    "team_id": team_id,
                    "story_id": story_id,
                    "story_mode": story_mode,
                    "include_groups": include_groups,
                    "since_id": since_id,
                    "until_id": until_id,
                    "since": to_iso(value=since),
                    "until": to_iso(value=until),
                    "show_reemitted_events_only": show_reemitted_events_only,
                    "exclude_previous_event_payloads": exclude_previous_event_payloads,
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )

    def get(
        self,
        *,
        event_id: int,
        exclude_previous_event_payloads: bool | None = None,
    ) -> Response:
        """Get an event. ``GET /api/v1/events/{event_id}``

        Args:
            event_id: The ID of the event to retrieve.
            exclude_previous_event_payloads: Keep only the output of the action in the payload,
                without the payloads that came from upstream events of the story run. Tines
                defaults to ``False``.

        Returns:
            A ``Response`` whose ``data`` is the event. The reply is a 404 with the message
            ``Event not found`` when no event with that ID is visible to your key.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/events/{event_id}",
            params=omit_none(
                values={"exclude_previous_event_payloads": exclude_previous_event_payloads}
            ),
        )

    def reemit(self, *, event_id: int) -> Response:
        """Re-emit an event. ``POST /api/v1/events/{event_id}/reemit``

        The actions that receive the events of the action that emitted this one get it again.
        Neither the Tines docs nor the OpenAPI document say more.

        Args:
            event_id: The ID of the event to re-emit.

        Returns:
            A ``Response`` with a 204 status and no data. The reply is a 404 with the message
            ``Event not found`` when no event with that ID is visible to your key.
        """
        return self._transport.request(method="POST", path=f"/api/v1/events/{event_id}/reemit")
