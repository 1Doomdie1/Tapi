from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any

from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_iso, to_list, to_object_or_list
from tapi.stories.types import (
    ActionFilterType,
    ActionLogLevel,
    ActionPosition,
    ActionType,
    ReceiverLink,
    SourceLink,
    StoryMode,
)


class Actions:
    """The actions of stories, available as ``tines.stories.actions``.

    An action, as returned by ``get``, ``create``, ``update``, ``clear_memory``,
    ``delete_events`` and ``delete_logs`` and listed by ``list``, has ``id``, ``guid``, ``slug``,
    ``type`` (such as ``Agents::HTTPRequestAgent``), ``name``, ``description`` (``null`` if there is
    none), ``user_id`` (the owner), ``options`` (the options block, which depends on the type),
    ``position`` (an object with ``x`` and ``y``), ``story_id``, ``story_mode`` (``LIVE`` or
    ``TEST``), ``group_id`` and ``nested_group_id`` (``null`` outside groups), ``team_id``,
    ``disabled``, ``schedule`` (a list of objects with a ``cron`` and a ``timezone``, or ``null``),
    ``sources`` and ``receivers`` (the IDs of the actions it receives events from and emits events
    to), ``links_to_sources`` and ``links_to_receivers`` (the same links as objects with a
    ``source_id`` or ``receiver_id`` and a ``link_type``), ``monitor_failures``,
    ``monitor_all_events``, ``monitor_no_events_emitted`` (seconds, or ``null``), ``created_at``,
    ``updated_at``, ``last_check_at``, ``last_receive_at``, ``last_event_at``,
    ``last_error_log_at`` (ISO 8601 timestamps, or ``null``), ``blended_events_count``,
    ``logs_count``, ``time_saved_unit``, ``time_saved_value``, ``page``,
    ``action_memory_contents`` and, for Receive Email and Webhook actions,
    ``story_run_save_setting``. Tines still calls actions agents in some names: the Condition
    action is ``Agents::TriggerAgent``, and ``list`` returns its actions under ``agents``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        story_id: int | None = None,
        story_mode: StoryMode | None = None,
        team_id: int | None = None,
        group_id: int | None = None,
        action_type: ActionFilterType | None = None,
        draft_id: int | None = None,
        include_live_activity: bool | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List actions. ``GET /api/v1/actions``

        The endpoint is paginated and one call returns one page.

        Args:
            story_id: Only actions of this story.
            story_mode: Only actions of the story in this mode: ``LIVE`` or ``TEST``. Use it with
                ``story_id``.
            team_id: Only actions of this team.
            group_id: Only actions of this group.
            action_type: Only actions of this type: ``Agents::CaseAgent``, ``Agents::EmailAgent``,
                ``Agents::EventTransformationAgent``, ``Agents::FormAgent``,
                ``Agents::GroupAgent``, ``Agents::HTTPRequestAgent``, ``Agents::IMAPAgent``,
                ``Agents::LLMAgent``, ``Agents::RecordAgent``, ``Agents::RunScriptAgent``,
                ``Agents::SendToStoryAgent``, ``Agents::TriggerAgent`` or
                ``Agents::WebhookAgent``.
            draft_id: Only actions of this draft.
            include_live_activity: Add ``pending_action_runs_count`` to each action. Tines
                defaults to ``False``.
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``agents``, the actions of the page,
            and ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/actions",
            params=omit_none(
                values={
                    "story_id": story_id,
                    "story_mode": story_mode,
                    "team_id": team_id,
                    "group_id": group_id,
                    "action_type": action_type,
                    "draft_id": draft_id,
                    "include_live_activity": include_live_activity,
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )

    def get(self, *, action_id: int, include_live_activity: bool | None = None) -> Response:
        """Get an action. ``GET /api/v1/actions/{action_id}``

        Args:
            action_id: The ID of the action to retrieve.
            include_live_activity: Add ``pending_action_runs_count`` to the action. Tines defaults
                to ``False``.

        Returns:
            A ``Response`` whose ``data`` is the action.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/actions/{action_id}",
            params=omit_none(values={"include_live_activity": include_live_activity}),
        )

    def create(
        self,
        *,
        type: ActionType,
        name: str,
        options: Mapping[str, Any] | None = None,
        position: ActionPosition | None = None,
        story_id: int | None = None,
        group_id: int | None = None,
        description: str | None = None,
        disabled: bool | None = None,
        source_ids: Sequence[int] | None = None,
        links_to_sources: Sequence[SourceLink] | None = None,
        receiver_ids: Sequence[int] | None = None,
        links_to_receivers: Sequence[ReceiverLink] | None = None,
        schedule: Mapping[str, Any] | Sequence[Mapping[str, Any]] | None = None,
        monitor_failures: bool | None = None,
        monitor_all_events: bool | None = None,
        monitor_no_events_emitted: int | None = None,
        draft_id: int | None = None,
    ) -> Response:
        """Create an action. ``POST /api/v1/actions``

        A story or a group must be given, or Tines answers with a 404. If change control is enabled
        on the story and no ``draft_id`` is given, Tines adds the action to a draft called ``test``.

        Args:
            type: The type of the action: ``Agents::EmailAgent``,
                ``Agents::EventTransformationAgent``, ``Agents::HTTPRequestAgent``,
                ``Agents::IMAPAgent``, ``Agents::LLMAgent``, ``Agents::TriggerAgent`` (the
                Condition action), ``Agents::WebhookAgent``, ``Agents::SendToStoryAgent``,
                ``Agents::GroupAgent`` or ``Agents::RunScriptAgent``.
            name: The name of the action.
            options: The options block of the action. Its keys depend on the type, and neither the
                Tines docs nor the OpenAPI document describe them. Tines fills in defaults when it
                is left out: an Event Transformation action then gets the ``message_only`` mode.
            position: The coordinates of the action on the story diagram, ``{"x": 100, "y": 200}``.
                Tines moved them by 5 on the tested tenant, and picks a position when it is left
                out.
            story_id: The ID of the story the action is added to.
            group_id: The ID of the group the action is added to.
            description: A description of the action.
            disabled: Whether the action is disabled. Tines defaults to ``False``.
            source_ids: The IDs of the actions that this action receives events from. Not with
                ``links_to_sources``. An ID that does not exist is ignored.
            links_to_sources: Links from source actions, each a dict with ``source_id`` and
                optionally ``type``: ``DEFAULT`` (the default), ``NO_MATCH`` or ``FAILURE``. Not
                with ``source_ids``. ``NO_MATCH`` needs a Condition action as the source, or
                Tines answers with a 422.
            receiver_ids: The IDs of the actions that this action emits events to. Not with
                ``links_to_receivers``.
            links_to_receivers: Links to receiver actions, each a dict with ``receiver_id`` and
                optionally ``type``: ``DEFAULT`` (the default), ``NO_MATCH`` or ``FAILURE``. Not
                with ``receiver_ids``. ``NO_MATCH`` needs this action to be a Condition action.
            schedule: The cron schedule of the action: an object with ``cron`` and ``timezone``,
                or a list of such objects. Tines accepts both and replies with a list.
            monitor_failures: Whether Tines sends a notification when the action fails.
            monitor_all_events: Whether all events are monitored.
            monitor_no_events_emitted: Seconds without an event after which Tines sends a
                notification.
            draft_id: The ID of the draft the action is added to.

        Returns:
            A ``Response`` whose ``data`` is the created action, with a 201 status. The reply is a
            400 when the links are mixed with ``source_ids`` or ``receiver_ids``, or have a type
            that does not exist, a 404 with ``Story or Group ID must be provided`` when neither
            is given, and a 422 for a ``type`` that does not exist (``Expected value to not be
            null``) and for a ``NO_MATCH`` link to or from an action that is not a Condition
            action.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/actions",
            json=omit_none(
                values={
                    "type": type,
                    "name": name,
                    "options": options,
                    "position": position,
                    "story_id": story_id,
                    "group_id": group_id,
                    "description": description,
                    "disabled": disabled,
                    "source_ids": to_list(values=source_ids),
                    "links_to_sources": to_list(values=links_to_sources),
                    "receiver_ids": to_list(values=receiver_ids),
                    "links_to_receivers": to_list(values=links_to_receivers),
                    "schedule": to_object_or_list(value=schedule),
                    "monitor_failures": monitor_failures,
                    "monitor_all_events": monitor_all_events,
                    "monitor_no_events_emitted": monitor_no_events_emitted,
                    "draft_id": draft_id,
                }
            ),
        )

    def update(
        self,
        *,
        action_id: int,
        name: str | None = None,
        description: str | None = None,
        options: Mapping[str, Any] | None = None,
        position: ActionPosition | None = None,
        source_ids: Sequence[int] | None = None,
        links_to_sources: Sequence[SourceLink] | None = None,
        receiver_ids: Sequence[int] | None = None,
        links_to_receivers: Sequence[ReceiverLink] | None = None,
        schedule: Mapping[str, Any] | Sequence[Mapping[str, Any]] | None = None,
        disabled: bool | None = None,
        monitor_failures: bool | None = None,
        monitor_all_events: bool | None = None,
        monitor_no_events_emitted: int | None = None,
        num_runs_to_save: int | None = None,
    ) -> Response:
        """Update an action. ``PATCH /api/v1/actions/{action_id}``

        A field left as ``None`` is not sent, and the action keeps its value. The type, the story
        and the group of an action cannot be changed. The Tines documentation shows this operation
        as ``PUT``. The OpenAPI document lists the same operation under ``PUT`` and ``PATCH``, and
        tapi uses ``PATCH``.

        Args:
            action_id: The ID of the action to update.
            name: The new name of the action.
            description: The new description of the action.
            options: The new options block of the action.
            position: The new coordinates of the action on the story diagram.
            source_ids: The IDs of the actions that this action receives events from. Not with
                ``links_to_sources``. This adds links and removes none: delete links with
                ``tines.stories.links.delete``.
            links_to_sources: Links from source actions, each a dict with ``source_id`` and
                optionally ``type``: ``DEFAULT``, ``NO_MATCH`` or ``FAILURE``. Not with
                ``source_ids``. This adds links and removes none.
            receiver_ids: The IDs of the actions that this action emits events to. Not with
                ``links_to_receivers``. This adds links and removes none.
            links_to_receivers: Links to receiver actions, each a dict with ``receiver_id`` and
                optionally ``type``: ``DEFAULT``, ``NO_MATCH`` or ``FAILURE``. Not with
                ``receiver_ids``. This adds links and removes none.
            schedule: The cron schedule of the action: an object with ``cron`` and ``timezone``,
                or a list of such objects. Tines accepts both and replies with a list.
            disabled: Whether the action is disabled.
            monitor_failures: Whether Tines sends a notification when the action fails. Send it
                together with ``monitor_all_events``.
            monitor_all_events: Whether all events are monitored. Send it together with
                ``monitor_failures``.
            monitor_no_events_emitted: Seconds without an event after which Tines sends a
                notification. Send it together with ``monitor_failures`` and
                ``monitor_all_events``.
            num_runs_to_save: The number of story runs to save for the action. Only for Receive
                Email and Webhook actions.

        Returns:
            A ``Response`` whose ``data`` is the updated action. The reply is a 400 when the links
            are invalid, or ``num_runs_to_save`` is used with an unsupported type (``This action
            type is not supported for saving runs``), and a 422 when ``monitor_failures`` or
            ``monitor_all_events`` is sent without the other, with ``Expected value to not be
            null`` for the one that is missing.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v1/actions/{action_id}",
            json=omit_none(
                values={
                    "name": name,
                    "description": description,
                    "options": options,
                    "position": position,
                    "source_ids": to_list(values=source_ids),
                    "links_to_sources": to_list(values=links_to_sources),
                    "receiver_ids": to_list(values=receiver_ids),
                    "links_to_receivers": to_list(values=links_to_receivers),
                    "schedule": to_object_or_list(value=schedule),
                    "disabled": disabled,
                    "monitor_failures": monitor_failures,
                    "monitor_all_events": monitor_all_events,
                    "monitor_no_events_emitted": monitor_no_events_emitted,
                    "num_runs_to_save": num_runs_to_save,
                }
            ),
        )

    def delete(self, *, action_id: int) -> Response:
        """Delete an action. ``DELETE /api/v1/actions/{action_id}``

        Args:
            action_id: The ID of the action to delete.

        Returns:
            A ``Response`` with a 204 status and no data. The links to the action disappear from
            the other actions, and a ``get`` answers 404 at once.
        """
        return self._transport.request(method="DELETE", path=f"/api/v1/actions/{action_id}")

    def list_events(
        self,
        *,
        action_id: int,
        since_id: int | None = None,
        until_id: int | None = None,
        since: datetime | str | None = None,
        until: datetime | str | None = None,
        show_reemitted_events_only: bool | None = None,
        exclude_previous_event_payloads: bool | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List the events of an action. ``GET /api/v1/actions/{action_id}/events``

        The endpoint is paginated and one call returns one page.

        Args:
            action_id: The ID of the action.
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
            and ``meta``, the pagination details. An event has ``id``, ``agent_id`` (the action),
            ``team_id``, ``payload``, ``created_at``, ``updated_at`` (always equal to
            ``created_at``), ``story_run_guid``, ``previous_events_ids`` and ``re_emitted``. The
            reply is a 400 when ``since`` or ``until`` is not a time, and a 422 when the payloads
            of the page add up to more than 200 MB, in which case a lower ``per_page`` helps.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/actions/{action_id}/events",
            params=omit_none(
                values={
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

    def list_logs(
        self,
        *,
        action_id: int,
        levels: Sequence[ActionLogLevel] | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List the logs of an action. ``GET /api/v1/actions/{action_id}/logs``

        The endpoint is paginated and one call returns one page.

        Args:
            action_id: The ID of the action.
            levels: Only logs of these severity levels: ``2`` for a warning, ``3`` for info and
                ``4`` for an error. Sent as ``level[]``, once per level.
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``action_logs``, the logs of the page,
            and ``meta``, the pagination details. A log has ``id``, ``level``, ``message``,
            ``created_at`` and ``inbound_event`` (the inbound event of the run, or ``null``).
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/actions/{action_id}/logs",
            params=omit_none(
                values={
                    "level[]": to_list(values=levels),
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )

    def delete_events(self, *, action_id: int, async_deletion: bool | None = None) -> Response:
        """Delete the events of an action. ``DELETE /api/v1/actions/{action_id}/remove_events``

        Deletes all the events that the action emitted.

        Args:
            action_id: The ID of the action.
            async_deletion: Whether to delete in a background job and not before the reply.

        Returns:
            A ``Response`` whose ``data`` is the action. The reply is a 400 when
            ``async_deletion`` is neither ``true`` nor ``false``, with the message ``Invalid value
            for async_deletion. Must be true or false.``
        """
        return self._transport.request(
            method="DELETE",
            path=f"/api/v1/actions/{action_id}/remove_events",
            params=omit_none(values={"async_deletion": async_deletion}),
        )

    def delete_logs(self, *, action_id: int) -> Response:
        """Delete the logs of an action. ``DELETE /api/v1/actions/{action_id}/remove_logs``

        Deletes all the logs that the action emitted.

        Args:
            action_id: The ID of the action.

        Returns:
            A ``Response`` whose ``data`` is the action.
        """
        return self._transport.request(
            method="DELETE",
            path=f"/api/v1/actions/{action_id}/remove_logs",
        )

    def clear_memory(self, *, action_id: int) -> Response:
        """Clear the memory of an action. ``DELETE /api/v1/actions/{action_id}/clear_memory``

        Clears all the values that the action keeps in its memory, shown on its status tab. It
        applies to Event Transformation actions in the ``deduplicate`` or ``implode`` mode.

        Args:
            action_id: The ID of the action.

        Returns:
            A ``Response`` whose ``data`` is the action. Any other type was accepted too, with
            nothing to clear. An action that does not exist is a 422 and not a 404, with a message
            such as ``No object found for `actionId: "..."```.
        """
        return self._transport.request(
            method="DELETE",
            path=f"/api/v1/actions/{action_id}/clear_memory",
        )
