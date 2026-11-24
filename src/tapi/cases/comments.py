from tapi.cases.types import Reaction
from tapi.core import Response, Transport
from tapi.core.params import omit_none


class Comments:
    """The comments on a case, available as ``tines.cases.comments``.

    A comment, as returned by ``get``, ``create``, ``update`` and ``add_reaction`` and listed by
    ``list``, is an activity of the case: ``id``, ``activity_type`` (``COMMENTED``), ``value``
    (the Markdown text), ``created_at``, ``user`` (an object with ``user_id``, ``first_name``,
    ``last_name``, ``email``, ``avatar_url`` and ``is_service_account``) and ``reactions`` (a
    list of objects with an ``emoji`` such as ``:+1:`` and its ``reactants``, each with a
    ``user_id``, a ``user_name`` and ``reacted_at``).

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
        """List the comments of a case. ``GET /api/v2/cases/{case_id}/comments``

        The endpoint is paginated and one call returns one page.

        Args:
            case_id: The ID of the case.
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id``, ``comments``, the
            comments of the page, and ``meta``, the pagination details. The reply repeats the ID
            as ``caseId``.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v2/cases/{case_id}/comments",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )

    def get(self, *, case_id: int, comment_id: int) -> Response:
        """Get a comment. ``GET /api/v2/cases/{case_id}/comments/{comment_id}``

        Args:
            case_id: The ID of the case.
            comment_id: The ID of the comment.

        Returns:
            A ``Response`` whose ``data`` is the comment, with ``case_id`` added.
        """
        return self._transport.request(
            method="GET", path=f"/api/v2/cases/{case_id}/comments/{comment_id}"
        )

    def create(
        self,
        *,
        case_id: int,
        value: str,
        author_email: str | None = None,
    ) -> Response:
        """Add a comment to a case. ``POST /api/v2/cases/{case_id}/comments``

        Args:
            case_id: The ID of the case.
            value: The text of the comment, as Markdown. User mentions are written
                ``<@user-2435>``.
            author_email: The email address of the user who comments. An address that is not a
                user was ignored.

        Returns:
            A ``Response`` whose ``data`` is the created comment, with a 201 status. The reply is
            a 422 when ``value`` is missing. An empty ``value`` was accepted.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v2/cases/{case_id}/comments",
            json=omit_none(values={"value": value, "author_email": author_email}),
        )

    def update(self, *, case_id: int, comment_id: int, value: str) -> Response:
        """Change a comment. ``PATCH /api/v2/cases/{case_id}/comments/{comment_id}``

        Args:
            case_id: The ID of the case.
            comment_id: The ID of the comment.
            value: The new text of the comment, as Markdown.

        Returns:
            A ``Response`` whose ``data`` is the updated comment. The reply is a 422 with ``Comment
            cannot be blank`` for an empty ``value``, and a 404 with ``Comment not found`` for a
            comment that does not exist.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v2/cases/{case_id}/comments/{comment_id}",
            json={"value": value},
        )

    def delete(self, *, case_id: int, comment_id: int) -> Response:
        """Delete a comment. ``DELETE /api/v2/cases/{case_id}/comments/{comment_id}``

        The Tines docs say that only the author of the comment or an admin can delete it.

        Args:
            case_id: The ID of the case.
            comment_id: The ID of the comment.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(
            method="DELETE", path=f"/api/v2/cases/{case_id}/comments/{comment_id}"
        )

    def add_reaction(self, *, case_id: int, comment_id: int, value: Reaction) -> Response:
        """React to a comment. ``POST /api/v2/cases/{case_id}/comments/{comment_id}/reactions``

        Args:
            case_id: The ID of the case.
            comment_id: The ID of the comment.
            value: The reaction: ``+1``, ``-1``, ``eyes``, ``heart`` or ``white_check_mark``.

        Returns:
            A ``Response`` whose ``data`` is the comment with its ``reactions``, with a 201
            status. Reacting twice with the same value was a 201 too. The reply is a 422 that
            lists the supported values for any other.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v2/cases/{case_id}/comments/{comment_id}/reactions",
            json={"value": value},
        )

    def remove_reaction(self, *, case_id: int, comment_id: int, value: Reaction) -> Response:
        """Remove a reaction. ``DELETE /api/v2/cases/{case_id}/comments/{comment_id}/reactions``

        Args:
            case_id: The ID of the case.
            comment_id: The ID of the comment.
            value: The reaction to remove: ``+1``, ``-1``, ``eyes``, ``heart`` or
                ``white_check_mark``.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(
            method="DELETE",
            path=f"/api/v2/cases/{case_id}/comments/{comment_id}/reactions",
            json={"value": value},
        )
