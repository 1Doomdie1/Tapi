from collections.abc import Sequence

from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_list


class Subscribers:
    """The users subscribed to a case, available as ``tines.cases.subscribers``.

    A subscriber, as listed by ``list``, has an ``id``, a ``user_id``, ``first_name``,
    ``last_name``, ``email`` and ``avatar_url``. The Tines docs show the user fields inside a
    ``user`` object, which ``create`` and ``batch_create`` return. A new case already has one
    subscriber.

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
        """List the subscribers of a case. ``GET /api/v2/cases/{case_id}/subscribers``

        The endpoint is paginated and one call returns one page.

        Args:
            case_id: The ID of the case.
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id``, ``subscribers``, the
            subscribers of the page, and ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v2/cases/{case_id}/subscribers",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )

    def create(self, *, case_id: int, user_email: str) -> Response:
        """Subscribe a user to a case. ``POST /api/v2/cases/{case_id}/subscribers``

        Args:
            case_id: The ID of the case.
            user_email: The email address of the user to subscribe.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id``, ``id`` and ``user``,
            with a 201 status in the OpenAPI document. The reply is a 404 with ``User not
            found`` for an address that is not a user.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v2/cases/{case_id}/subscribers",
            json={"user_email": user_email},
        )

    def batch_create(self, *, case_id: int, user_emails: Sequence[str]) -> Response:
        """Subscribe several users. ``POST /api/v2/cases/{case_id}/subscribers/batch``

        Args:
            case_id: The ID of the case.
            user_emails: The email addresses of the users to subscribe, at most 50.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id`` and ``subscribers``, with
            a 201 status in the OpenAPI document, also for an empty list. The reply is a 404
            with ``Users not found`` when an address is not a user, and a 400 when
            ``user_emails`` is not a list of strings.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v2/cases/{case_id}/subscribers/batch",
            json={"user_emails": to_list(values=user_emails)},
        )

    def delete(self, *, case_id: int, subscriber_id: int) -> Response:
        """Unsubscribe a user. ``DELETE /api/v2/cases/{case_id}/subscribers/{subscriber_id}``

        Args:
            case_id: The ID of the case.
            subscriber_id: The ID of the subscriber. The Tines docs do not say whether it is the
                ``id`` or the ``user_id`` of the listing. On a new case the server answered
                ``User not found`` for the ``id`` and ``Subscriber not found`` for the
                ``user_id`` of the subscriber that the case has from the start.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(
            method="DELETE", path=f"/api/v2/cases/{case_id}/subscribers/{subscriber_id}"
        )
