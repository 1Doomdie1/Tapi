from tapi.core import Response, Transport
from tapi.core.params import omit_none


class Assignees:
    """The assignees of a case, available as ``tines.cases.assignees``.

    To change the assignees of a case, use ``tines.cases.update`` with ``assignee_emails``,
    ``add_assignee_emails`` and ``remove_assignee_emails``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        case_id: int,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List the assignees of a case. ``GET /api/v2/cases/{case_id}/assignees``

        The endpoint is paginated and one call returns one page.

        Args:
            case_id: The ID of the case.
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id``, ``assignees``, the users
            of the page, and ``meta``, the pagination details. A user has ``user_id``,
            ``first_name``, ``last_name``, ``email``, ``avatar_url`` and ``is_service_account``.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v2/cases/{case_id}/assignees",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )
