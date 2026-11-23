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

        Tines records an audit log whenever a user changes data in your tenant. Each entry holds
        the operation that was run, its inputs and outputs, and the user who triggered it. Tines
        documents audit logs as available to tenant admins, and names ``AUDIT_LOG_READ`` as a
        tenant permission that can be granted to a service API key. A key without access to the
        endpoint receives a 404.

        The endpoint is paginated and one call returns one page. Read ``data["meta"]`` to decide
        whether to ask for the next page.

        Args:
            before: Only logs created before this time, as a ``datetime`` or an ISO 8601 string. A
                datetime without a timezone is treated as UTC.
            after: Only logs created after this time, in the same formats.
            user_ids: Only logs from these users. Sent as ``user_id[]``, once per user.
            operation_names: Only logs for these operations, such as ``StoryItemsCreation`` or
                ``StoryItemsMovement``. Sent as ``operation_name[]``, once per name.
            team_ids: Only logs from these teams. Sent as ``team_id[]``, once per team.
            per_page: The number of results per page. Tines defaults to 20 and allows at most 500.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with:

            - ``audit_logs``: the entries of the page. Each has ``id``, ``operation_name``,
              ``created_at``, ``updated_at``, ``inputs`` and ``outputs`` (objects, or ``null``),
              ``request_ip``, ``request_user_agent``, ``tenant_id``, ``user_id``, ``user_email``,
              ``user_name``, ``impersonated_by``, ``source`` (where the operation came from, such
              as ``UI``, ``API`` or ``Workbench``), ``story_id``, ``team_id`` and ``team_name``.
            - ``meta``: ``current_page``, ``previous_page`` and ``next_page`` (links),
              ``next_page_number``, ``per_page``, ``pages`` (the number of pages) and ``count``.
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
