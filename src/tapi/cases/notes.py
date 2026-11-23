from tapi.cases.types import NoteColor
from tapi.core import Response, Transport
from tapi.core.params import omit_none


class Notes:
    """The notes of a case, available as ``tines.cases.notes``.

    A note, as returned by ``get``, ``create``, ``update`` and ``append_content`` and listed by
    ``list``, has ``id``, ``case_id``, ``title``, ``content`` (Markdown, ``null`` if none),
    ``color``, ``sensitive`` (excluded from exports), ``hidden``, ``author`` (a user),
    ``created_at`` and ``updated_at``. The replies do not show a position.

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
        resolve_mentions: bool | None = None,
    ) -> Response:
        """List the notes of a case. ``GET /api/v2/cases/{case_id}/notes``

        The endpoint is paginated and one call returns one page.

        Args:
            case_id: The ID of the case.
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.
            resolve_mentions: When true, user mentions in the content are replaced by display
                names. Tines defaults to false.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id``, ``notes``, the notes of
            the page, and ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v2/cases/{case_id}/notes",
            params=omit_none(
                values={
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
        note_id: int,
        resolve_mentions: bool | None = None,
    ) -> Response:
        """Get a note. ``GET /api/v2/cases/{case_id}/notes/{note_id}``

        Args:
            case_id: The ID of the case.
            note_id: The ID of the note.
            resolve_mentions: When true, user mentions in the content are replaced by display
                names. Tines defaults to false.

        Returns:
            A ``Response`` whose ``data`` is the note, with ``case_id`` added.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v2/cases/{case_id}/notes/{note_id}",
            params=omit_none(values={"resolve_mentions": resolve_mentions}),
        )

    def create(
        self,
        *,
        case_id: int,
        title: str,
        content: str | None = None,
        color: NoteColor | None = None,
        position: int | None = None,
        sensitive: bool | None = None,
        hidden: bool | None = None,
        author_email: str | None = None,
    ) -> Response:
        """Add a note to a case. ``POST /api/v2/cases/{case_id}/notes``

        Args:
            case_id: The ID of the case.
            title: The title of the note. The server refuses a note without one, as the Tines
                docs say and the OpenAPI document does not. An empty title was accepted.
            content: The content of the note, as Markdown.
            color: The color, in lower case: ``white`` (the default), ``gold``, ``magenta``,
                ``green``, ``blue``, ``red``, ``mint`` or ``indigo``.
            position: The zero-based position of the note in the case. The server accepted it,
                and the reply does not show it.
            sensitive: Whether to leave the note out of exports. Tines defaults to false.
            hidden: Whether the note is hidden. Tines defaults to false.
            author_email: The email address of the author of the note. An address that is not a
                user was accepted.

        Returns:
            A ``Response`` whose ``data`` is the created note, with a 201 status. The reply is a
            422 naming the field when ``title`` is missing or ``color`` is not one of the
            values.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v2/cases/{case_id}/notes",
            json=omit_none(
                values={
                    "title": title,
                    "content": content,
                    "color": color,
                    "position": position,
                    "sensitive": sensitive,
                    "hidden": hidden,
                    "author_email": author_email,
                }
            ),
        )

    def update(
        self,
        *,
        case_id: int,
        note_id: int,
        title: str | None = None,
        content: str | None = None,
        color: NoteColor | None = None,
        position: int | None = None,
        sensitive: bool | None = None,
        hidden: bool | None = None,
        author_email: str | None = None,
    ) -> Response:
        """Change a note. ``PATCH /api/v2/cases/{case_id}/notes/{note_id}``

        The Tines documentation shows this operation as ``PUT``. The OpenAPI document lists the
        same operation under ``PUT`` and ``PATCH``, and tapi uses ``PATCH``.

        Args:
            case_id: The ID of the case.
            note_id: The ID of the note.
            title: A new title.
            content: New content, as Markdown. To add to it, use ``append_content``.
            color: A new color: ``white``, ``gold``, ``magenta``, ``green``, ``blue``, ``red``,
                ``mint`` or ``indigo``.
            position: A new zero-based position in the case. Only the Tines docs list it.
            sensitive: Whether to leave the note out of exports.
            hidden: Whether the note is hidden.
            author_email: The email address of the author of the note. Only the Tines docs list
                it.

        Returns:
            A ``Response`` whose ``data`` is the updated note. A call that sends nothing is a
            200, and a note that does not exist is a 404 with ``Note not found``.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v2/cases/{case_id}/notes/{note_id}",
            json=omit_none(
                values={
                    "title": title,
                    "content": content,
                    "color": color,
                    "position": position,
                    "sensitive": sensitive,
                    "hidden": hidden,
                    "author_email": author_email,
                }
            ),
        )

    def delete(self, *, case_id: int, note_id: int) -> Response:
        """Delete a note. ``DELETE /api/v2/cases/{case_id}/notes/{note_id}``

        Args:
            case_id: The ID of the case.
            note_id: The ID of the note.

        Returns:
            A ``Response`` with a 204 status and no data. Deleting it again is a 404 with
            ``TeamCaseNote not found``.
        """
        return self._transport.request(
            method="DELETE", path=f"/api/v2/cases/{case_id}/notes/{note_id}"
        )

    def append_content(
        self,
        *,
        case_id: int,
        note_id: int,
        content: str,
        author_email: str | None = None,
    ) -> Response:
        """Add text to a note. ``POST /api/v2/cases/{case_id}/notes/{note_id}/content``

        Args:
            case_id: The ID of the case.
            note_id: The ID of the note.
            content: The text to add, as Markdown.
            author_email: The email address of the author of the note.

        Returns:
            A ``Response`` whose ``data`` is the updated note.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v2/cases/{case_id}/notes/{note_id}/content",
            json=omit_none(values={"content": content, "author_email": author_email}),
        )
