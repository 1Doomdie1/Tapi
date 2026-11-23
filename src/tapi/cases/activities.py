from collections.abc import Sequence

from tapi.cases.types import ActivityType
from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_list


class Activities:
    """The activity log of a case, available as ``tines.cases.activities``.

    An activity, as returned by ``get`` and listed by ``list``, has ``id``, ``activity_type``,
    ``value`` (for a comment, its text), ``file`` (for a file activity, an object with the
    ``filename`` and the ``url``), ``user`` (who did it), ``created_at`` and, for a comment,
    ``reactions``. Activities are written by Tines and cannot be created, changed or deleted
    through the API.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        case_id: int,
        activity_types: Sequence[ActivityType] | None = None,
        per_page: int | None = None,
        page: int | None = None,
        resolve_mentions: bool | None = None,
    ) -> Response:
        """List the activities of a case. ``GET /api/v2/cases/{case_id}/activities``

        The endpoint is paginated and one call returns one page.

        Args:
            case_id: The ID of the case.
            activity_types: Only activities of these types. Sent as ``activity_type[]``, once per
                type. See ``tapi.cases.types.ActivityType`` for the values.
            per_page: The number of results per page. Tines defaults to 20, and its docs give a
                maximum of 50, which the server did not enforce.
            page: The page to return, starting at 1. Tines defaults to 1.
            resolve_mentions: When true, user mentions in comments are replaced by display names.
                Tines defaults to false.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id``, ``activities``, the
            activities of the page, and ``meta``, the pagination details. The reply is a 422
            listing the valid values for an activity type that does not exist.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v2/cases/{case_id}/activities",
            params=omit_none(
                values={
                    "activity_type[]": to_list(values=activity_types),
                    "per_page": per_page,
                    "page": page,
                    "resolve_mentions": resolve_mentions,
                }
            ),
        )

    def get(
        self,
        *,
        case_id: int,
        activity_id: int,
        resolve_mentions: bool | None = None,
    ) -> Response:
        """Get an activity of a case. ``GET /api/v2/cases/{case_id}/activities/{activity_id}``

        Args:
            case_id: The ID of the case.
            activity_id: The ID of the activity.
            resolve_mentions: When true, user mentions in a comment are replaced by display
                names. Tines defaults to false.

        Returns:
            A ``Response`` whose ``data`` is the activity, with ``case_id`` added. The reply is a
            404 with ``TeamCaseAction not found`` for an activity that does not exist, and a 500
            for an activity of another case.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v2/cases/{case_id}/activities/{activity_id}",
            params=omit_none(values={"resolve_mentions": resolve_mentions}),
        )
