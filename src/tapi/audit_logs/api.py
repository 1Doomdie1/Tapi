from collections.abc import Sequence
from datetime import datetime

from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_iso, to_list


class AuditLogs:
    """Audit logs, available as ``tines.audit_logs``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        before: datetime | str | None = None,
        after: datetime | str | None = None,
        user_ids: Sequence[int] | None = None,
        operation_names: Sequence[str] | None = None,
        team_ids: Sequence[int] | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List audit logs. ``GET /api/v1/audit_logs``

        For tenant admins, or a service key with ``AUDIT_LOG_READ``. A key without access gets a
        404.

        Args:
            before: Only logs created before this time: a ``datetime`` or an ISO 8601 string.
            after: Only logs created after this time.
            user_ids: Only logs from these users.
            operation_names: Only logs of these operations, such as ``StoryItemsCreation``.
            team_ids: Only logs from these teams.
            per_page: The number of results per page, at most 500.
            page: The page to return, from 1.

        Returns:
            A ``Response`` whose ``data`` has ``audit_logs`` and ``meta``, the pagination details.
            An entry has ``id``, ``operation_name``, ``inputs``, ``outputs``, ``user_id``,
            ``team_id``, ``source`` and timestamps.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/audit_logs",
            params=omit_none(
                values={
                    "before": to_iso(value=before),
                    "after": to_iso(value=after),
                    "user_id[]": to_list(values=user_ids),
                    "operation_name[]": to_list(values=operation_names),
                    "team_id[]": to_list(values=team_ids),
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )
