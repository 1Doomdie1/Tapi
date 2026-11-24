from tapi.core import Response, Transport
from tapi.core.params import omit_none
from tapi.stories.types import NotePosition, StoryMode


class Notes:
    """The notes on the storyboard of a story, available as ``tines.stories.notes``.

    A note, as returned by ``get``, ``create`` and ``update`` and listed by ``list``, has ``id``,
    ``story_id``, ``story_mode`` (``LIVE`` or ``TEST``), ``group_id`` (``null`` outside groups),
    ``content`` (Markdown text), ``position`` (an object with the integers ``x`` and ``y``) and,
    for a story with change control, ``draft_id`` and ``draft_name``. Tines calls a note an
    annotation in some names: ``list`` returns the notes under ``annotations``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        story_id: int | None = None,
        mode: StoryMode | None = None,
        team_id: int | None = None,
        group_id: int | None = None,
        draft_id: int | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List notes. ``GET /api/v1/notes``

        Args:
            story_id: Only notes of this story.
            mode: Only notes of the story in this mode: ``LIVE`` or ``TEST``. Use it with
                ``story_id``.
            team_id: Only notes of this team.
            group_id: Only notes of this group.
            draft_id: Only notes of this draft.
            per_page: The number of results per page.
            page: The page to return, starting at 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``annotations``, the notes of the page,
            and ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/notes",
            params=omit_none(
                values={
                    "story_id": story_id,
                    "mode": mode,
                    "team_id": team_id,
                    "group_id": group_id,
                    "draft_id": draft_id,
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )

    def get(self, *, note_id: int) -> Response:
        """Get a note. ``GET /api/v1/notes/{note_id}``

        Args:
            note_id: The ID of the note to retrieve.

        Returns:
            A ``Response`` whose ``data`` is the note. The reply is a 404 with the message
            ``DiagramNote not found`` when no note with that ID is visible to your key.
        """
        return self._transport.request(method="GET", path=f"/api/v1/notes/{note_id}")

    def create(
        self,
        *,
        story_id: int | None = None,
        group_id: int | None = None,
        content: str,
        position: NotePosition | None = None,
        draft_id: int | None = None,
    ) -> Response:
        """Create a note. ``POST /api/v1/notes``

        A story or a group must be given. The Tines documentation says that if change control is
        enabled on the story and no ``draft_id`` is given, Tines adds the note to a draft called
        ``test``.

        Args:
            story_id: The ID of the story the note is added to.
            group_id: The ID of the group the note is added to.
            content: The content of the note, as Markdown, up to 8000 characters. It can be an empty
                string. Tines refuses a note without content.
            position: The coordinates of the note on the story diagram, ``{"x": 0, "y": 0}``. ``x``
                and ``y`` must both be given and must be integers. Without a position the note is
                placed at ``{"x": 0, "y": 0}``.
            draft_id: The ID of the draft the note is added to. It is refused for a story without
                change control.

        Returns:
            A ``Response`` whose ``data`` is the created note, with a 201 status.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/notes",
            json=omit_none(
                values={
                    "story_id": story_id,
                    "group_id": group_id,
                    "content": content,
                    "position": position,
                    "draft_id": draft_id,
                }
            ),
        )

    def update(
        self,
        *,
        note_id: int,
        content: str | None = None,
        position: NotePosition | None = None,
    ) -> Response:
        """Update a note. ``PATCH /api/v1/notes/{note_id}``

        Args:
            note_id: The ID of the note to update.
            content: The new content of the note, as Markdown, up to 8000 characters. An empty
                string is accepted.
            position: The new coordinates of the note on the story diagram. Give both ``x`` and
                ``y``: with only one of them the note was moved to ``{"x": 0, "y": 0}``. The
                position in the reply was not always the one sent, so read it from ``data``.

        Returns:
            A ``Response`` whose ``data`` is the updated note.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v1/notes/{note_id}",
            json=omit_none(values={"content": content, "position": position}),
        )

    def delete(self, *, note_id: int) -> Response:
        """Delete a note. ``DELETE /api/v1/notes/{note_id}``

        Args:
            note_id: The ID of the note to delete.

        Returns:
            A ``Response`` with a 204 status and no data. The note is gone at once. The reply is a
            404 with ``DiagramNote not found`` when there is no such note, including for a note
            that was already deleted.
        """
        return self._transport.request(method="DELETE", path=f"/api/v1/notes/{note_id}")
