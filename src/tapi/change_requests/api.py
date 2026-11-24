from collections.abc import Sequence

from tapi.change_requests.types import ChangeRequestStatus
from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_list


class ChangeRequests:
    """Change requests across stories, available as ``tines.change_requests``.

    A change request asks to promote the changes of a draft to the live story. These methods read
    change requests of any story that the API key can access. Creating, approving, cancelling,
    rejecting and promoting one are operations on a story, and they are in
    ``tines.stories.change_control``.

    A change request, as returned by ``get`` and listed by ``list``, has ``id``, ``name``,
    ``description``, ``status`` (one of ``PENDING``, ``APPROVED``, ``REJECTED``, ``PUSHED`` and
    ``IN_PROGRESS``, which is what its author cancelling it leaves), ``story_id``, ``story_name``,
    ``team_id``, ``draft_id``, ``draft_name``, ``user_id``, ``participants`` (user IDs),
    ``created_at`` and ``updated_at``. ``draft_id`` and ``draft_name`` are ``null`` once the draft
    is gone.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        team_ids: Sequence[int] | None = None,
        statuses: Sequence[ChangeRequestStatus] | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List change requests. ``GET /api/v1/change_requests``

        Lists change requests across the stories that the API key can access, newest first. Only the
        latest change request of each draft is returned.

        Args:
            team_ids: Only change requests of stories in these teams.
            statuses: Only change requests with one of these statuses: ``PENDING``, ``APPROVED``,
                ``REJECTED``, ``PUSHED`` or ``IN_PROGRESS``. Tines returns every status except
                ``PUSHED`` when this is left out.
            per_page: The number of results per page.
            page: The page to return, starting at 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``change_requests``, the change requests
            of the page, and ``meta``, the pagination details. The items do not hold
            ``live_story_export`` and ``draft_export``, which ``get`` returns.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/change_requests",
            params=omit_none(
                values={
                    "team_id[]": to_list(values=team_ids),
                    "status[]": to_list(values=statuses),
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )

    def get(self, *, change_request_id: int) -> Response:
        """Get a change request. ``GET /api/v1/change_requests/{change_request_id}``

        Returns a change request in any status, with the export of the live story and the export
        of the draft.

        Args:
            change_request_id: The ID of the change request.

        Returns:
            A ``Response`` whose ``data`` is the change request, with the fields that ``list``
            returns and also ``live_story_export`` and ``draft_export``, each a string that holds
            the JSON export of a story. ``draft_export`` is ``null`` once the draft is gone. The
            reply is a 404 with ``StoryChangeRequest not found`` when no change request with that
            ID is visible to the API key.
        """
        return self._transport.request(
            method="GET", path=f"/api/v1/change_requests/{change_request_id}"
        )
