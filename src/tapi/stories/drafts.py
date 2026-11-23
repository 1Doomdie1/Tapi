from tapi.core import Response, Transport
from tapi.core.params import omit_none


class Drafts:
    """The drafts of a story, available as ``tines.stories.drafts``.

    A draft, as returned by ``create`` and listed by ``list``, has the fields of a story, plus
    ``story_id`` and ``story_name`` (the story the draft belongs to). Its ``id`` is the draft ID,
    its ``mode`` is always ``TEST`` and its ``slug`` has a draft-specific suffix. When change
    control is enabled on a story, Tines creates a draft called ``test`` for it.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        story_id: int,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List the drafts of a story. ``GET /api/v1/stories/{story_id}/drafts``

        The endpoint is paginated and one call returns one page. The Tines docs show neither
        ``per_page`` nor ``page`` on this endpoint, and the OpenAPI document lists both.

        Args:
            story_id: The ID of the story.
            per_page: The number of results per page. Tines defaults to 20 and caps it at 500.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``drafts``, the drafts of the page,
            and ``meta``, the pagination details. The reply is a 422 with the message
            ``Change control is not enabled`` when the story has no change control.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/stories/{story_id}/drafts",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )

    def create(self, *, story_id: int, name: str) -> Response:
        """Create a draft of a story. ``POST /api/v1/stories/{story_id}/drafts``

        Args:
            story_id: The ID of the story.
            name: The name of the draft.

        Returns:
            A ``Response`` whose ``data`` is the created draft. The status is 200, and the Tines
            docs do not state one. The reply is a 422 when the story already has a draft with that
            name.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/stories/{story_id}/drafts",
            json={"name": name},
        )

    def delete(self, *, story_id: int, draft_id: int) -> Response:
        """Delete a draft of a story. ``DELETE /api/v1/stories/{story_id}/drafts/{draft_id}``

        Args:
            story_id: The ID of the story.
            draft_id: The ID of the draft to delete.

        Returns:
            A ``Response`` with a 204 status and no data. The reply is a 404 when the story is not
            visible to your key or the draft does not belong to it.
        """
        return self._transport.request(
            method="DELETE",
            path=f"/api/v1/stories/{story_id}/drafts/{draft_id}",
        )
