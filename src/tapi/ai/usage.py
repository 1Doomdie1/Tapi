from datetime import datetime
from typing import Literal

from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_iso

Feature = Literal[
    "workbench",
    "workbench_storyboard",
    "ai_agents",
    "workbench_cases",
    "workbench_apps",
    "other",
]

GroupBy = Literal["model", "provider", "team", "feature", "story", "user", "action", "day"]


class Usage:
    """Aggregated AI usage, available as ``tines.ai.usage``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def get(
        self,
        *,
        relative_date: str | None = None,
        start_date: datetime | str | None = None,
        end_date: datetime | str | None = None,
        team_id: int | None = None,
        model_id: str | None = None,
        provider_id: int | None = None,
        feature: Feature | None = None,
        story_id: int | None = None,
        user_id: int | None = None,
        action_id: int | None = None,
        group_by: GroupBy | None = None,
    ) -> Response:
        """Get aggregated AI usage for the tenant. ``GET /api/v1/ai_usage``

        The usage covers tokens, credits and cost in US dollars. Administrators see the usage of the
        whole tenant. Other users see the usage of the teams they belong to, plus usage that is not
        attributed to any team. When a filter names a team, story, user or action that a non
        administrator may not see, the reply holds zeroed usage and is not an error.

        Choose the time window with ``relative_date`` or with ``start_date`` and ``end_date``, not
        both. Without any of them the last 30 days are used.

        Args:
            relative_date: A window relative to now: ``today``, ``yesterday``, or a count followed
                by ``day``, ``week``, ``month`` or ``year``, singular or plural, such as
                ``7 days`` or ``1 year``. Cannot be combined with ``start_date`` and ``end_date``.
                Defaults to ``30 days`` when no dates are given.
            start_date: The start of a custom window, as a ``datetime`` or an ISO 8601 string. A
                datetime without a timezone is treated as UTC. Must be paired with ``end_date``.
            end_date: The end of a custom window, in the same formats. Must be paired with
                ``start_date``, must be after it, and the window cannot be longer than one year.
            team_id: Only usage attributed to this team.
            model_id: Only usage attributed to this model.
            provider_id: Only usage attributed to this AI provider.
            feature: Only usage attributed to this feature: ``workbench``,
                ``workbench_storyboard``, ``ai_agents``, ``workbench_cases``, ``workbench_apps``
                or ``other``.
            story_id: Only runtime usage from AI actions and AI agents in this story.
            user_id: Only usage initiated by this user.
            action_id: Only runtime usage from this AI action or AI agent. An AI action that an
                agent uses as a tool reports its usage under its own ID.
            group_by: Split the usage by one of ``model``, ``provider``, ``team``, ``feature``,
                ``story``, ``user``, ``action`` or ``day``. When omitted, only the totals are
                returned.

        Returns:
            A ``Response`` whose ``data`` is an object with:

            - ``range``: the resolved time window, with ``start`` and ``end``.
            - ``totals``: the usage of the whole window.
            - ``group_by`` and ``groups``: only when ``group_by`` was given. ``groups`` has one
              entry per value of the grouping.

            ``totals`` and every group hold ``input_tokens``, ``cached_read_input_tokens``,
            ``cached_write_input_tokens``, ``output_tokens``, ``credits_used``, ``usage_count``
            and ``billed_cost`` (an object with ``currency`` and ``amount``, a string with two
            decimals). Each group also holds the keys of its grouping: ``model_id``;
            ``provider_id`` and ``provider_name``; ``team_id`` and ``team_name``; ``story_id`` and
            ``story_name``; ``user_id``, ``user_email``, ``user_name`` and
            ``is_service_account``; ``action_id``, ``action_name`` and ``story_id``; ``feature``;
            or ``day``. An identifier is ``null`` for usage that does not belong to anything of
            that kind, or that you cannot see.

            An invalid request is answered with a 400 whose ``data`` is a list of messages. That
            happens when ``relative_date`` is combined with ``start_date`` or ``end_date``, when
            only one of those two is given, when a date cannot be parsed or ``relative_date`` is
            unknown, when ``end_date`` is not after ``start_date`` or the window is longer than a
            year, when ``feature`` is invalid, or when AI usage is unavailable on the tenant.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/ai_usage",
            params=omit_none(
                values={
                    "relative_date": relative_date,
                    "start_date": to_iso(value=start_date),
                    "end_date": to_iso(value=end_date),
                    "team_id": team_id,
                    "model_id": model_id,
                    "provider_id": provider_id,
                    "feature": feature,
                    "story_id": story_id,
                    "user_id": user_id,
                    "action_id": action_id,
                    "group_by": group_by,
                }
            ),
        )
