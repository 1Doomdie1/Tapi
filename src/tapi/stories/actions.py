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

        Args:
            story_id: Only actions of this story.
            story_mode: Only actions of the story in this mode: ``LIVE`` or ``TEST``. Use it with
                ``story_id``.
            team_id: Only actions of this team.
            group_id: Only actions of this group.
            action_type: Only actions of this type: ``Agents::CaseAgent``, ``Agents::EmailAgent``,
                ``Agents::EventTransformationAgent``, ``Agents::FormAgent``, ``Agents::GroupAgent``,
                ``Agents::HTTPRequestAgent``, ``Agents::IMAPAgent``, ``Agents::LLMAgent``,
                ``Agents::RecordAgent``, ``Agents::RunScriptAgent``, ``Agents::SendToStoryAgent``,
                ``Agents::TriggerAgent`` or ``Agents::WebhookAgent``.
            draft_id: Only actions of this draft.
            include_live_activity: Add ``pending_action_runs_count`` to each action.
            per_page: The number of results per page.
            page: The page to return, starting at 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``agents``, the actions of the page, and
            ``meta``, the pagination details.
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

        A story or a group is needed. With change control and no ``draft_id``, the action goes to
        the ``test`` draft.

        Args:
            type: ``Agents::EmailAgent``, ``Agents::EventTransformationAgent``,
                ``Agents::HTTPRequestAgent``, ``Agents::IMAPAgent``, ``Agents::LLMAgent``,
                ``Agents::TriggerAgent`` (Condition), ``Agents::WebhookAgent``,
                ``Agents::SendToStoryAgent``, ``Agents::GroupAgent`` or ``Agents::RunScriptAgent``.
            name: The name of the action.
            options: The options block. Its keys depend on the type.
            position: The coordinates on the story diagram, ``{"x": 100, "y": 200}``.
            story_id: The ID of the story.
            group_id: The ID of the group.
            description: A description of the action.
            disabled: Whether the action is disabled.
            source_ids: The IDs of the actions that it receives events from. Not with
                ``links_to_sources``.
            links_to_sources: Links from source actions, dicts with ``source_id`` and optionally
                ``type`` (``DEFAULT``, ``NO_MATCH`` or ``FAILURE``). Not with ``source_ids``.
                ``NO_MATCH`` needs a Condition action as the source.
            receiver_ids: The IDs of the actions that it emits events to. Not with
                ``links_to_receivers``.
            links_to_receivers: Links to receiver actions, dicts with ``receiver_id`` and optionally
                ``type``. Not with ``receiver_ids``. ``NO_MATCH`` needs this to be a Condition
                action.
            schedule: The cron schedule: an object with ``cron`` and ``timezone``, or a list of
                them.
            monitor_failures: Whether Tines sends a notification when the action fails.
            monitor_all_events: Whether all events are monitored.
            monitor_no_events_emitted: Seconds without an event after which Tines sends a
                notification.
            draft_id: The ID of the draft.

        Returns:
            A ``Response`` with a 201 status whose ``data`` is the created action.
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

        The type, the story and the group cannot be changed. Links are only added: delete them with
        ``tines.stories.links.delete``.

        Args:
            action_id: The ID of the action.
            name: The new name.
            description: The new description.
            options: The new options block.
            position: The new coordinates on the story diagram.
            source_ids: The IDs of the actions that it receives events from. Not with
                ``links_to_sources``.
            links_to_sources: Links from source actions, as for ``create``. Not with ``source_ids``.
            receiver_ids: The IDs of the actions that it emits events to. Not with
                ``links_to_receivers``.
            links_to_receivers: Links to receiver actions, as for ``create``. Not with
                ``receiver_ids``.
            schedule: The cron schedule, as for ``create``.
            disabled: Whether the action is disabled.
            monitor_failures: Whether Tines sends a notification when the action fails. Send it with
                ``monitor_all_events``.
            monitor_all_events: Whether all events are monitored. Send it with ``monitor_failures``.
            monitor_no_events_emitted: Seconds without an event after which Tines sends a
                notification. Send it with the two others.
            num_runs_to_save: The number of story runs to save, for Receive Email and Webhook
                actions.

        Returns:
            A ``Response`` whose ``data`` is the updated action.
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

        Args:
            action_id: The ID of the action.
            since_id: Only events after this event ID.
            until_id: Only events until and including this event ID.
            since: Only events created after this time. A ``datetime``, or an ISO 8601 string. A
                ``datetime`` without a timezone is treated as UTC.
            until: Only events created until this time. A ``datetime``, or an ISO 8601 string. A
                ``datetime`` without a timezone is treated as UTC.
            show_reemitted_events_only: Only events that were re-emitted.
            exclude_previous_event_payloads: Keep only the output of the action in the payload of
                each event, without the payloads that came from upstream events of the story run.
            per_page: The number of results per page.
            page: The page to return, starting at 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``events``, the events of the page, and
            ``meta``, the pagination details. An event has ``id``, ``agent_id`` (the action),
            ``team_id``, ``payload``, ``created_at``, ``updated_at`` (always equal to
            ``created_at``), ``story_run_guid``, ``previous_events_ids`` and ``re_emitted``.
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

        Args:
            action_id: The ID of the action.
            levels: Only logs of these severity levels: ``2`` for a warning, ``3`` for info and
                ``4`` for an error.
            per_page: The number of results per page.
            page: The page to return, starting at 1.

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
