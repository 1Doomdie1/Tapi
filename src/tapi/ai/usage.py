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

        Covers tokens, credits and cost in US dollars. Administrators see the whole tenant, other
        users their teams. Use ``relative_date`` or ``start_date`` and ``end_date``, not both. The
        default is the last 30 days.

        Args:
            relative_date: ``today``, ``yesterday``, or a count and a unit, such as ``7 days`` or
                ``1 year``.
            start_date: The start of a custom window: a ``datetime`` or an ISO 8601 string. Needs
                ``end_date``.
            end_date: The end of the window, after ``start_date`` and at most one year later.
            team_id: Only usage of this team.
            model_id: Only usage of this model.
            provider_id: Only usage of this AI provider.
            feature: ``workbench``, ``workbench_storyboard``, ``ai_agents``, ``workbench_cases``,
                ``workbench_apps`` or ``other``.
            story_id: Only runtime usage of AI actions and agents in this story.
            user_id: Only usage started by this user.
            action_id: Only runtime usage of this AI action or agent.
            group_by: ``model``, ``provider``, ``team``, ``feature``, ``story``, ``user``,
                ``action`` or ``day``.

        Returns:
            A ``Response`` whose ``data`` has ``range``, ``totals`` and, with ``group_by``,
            ``groups``. ``totals`` and each group hold the token counts, ``credits_used``,
            ``usage_count`` and ``billed_cost``.
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
