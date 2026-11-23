from tapi.core import Response, Transport


class Owners:
    """The owners of a story, available as ``tines.stories.owners``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def add(self, *, story_id: int, user_id: int) -> Response:
        """Add an owner to a story. ``POST /api/v1/stories/{story_id}/owners``

        Args:
            story_id: The ID of the story.
            user_id: The ID of the user to add. The user must be a member of the team the story
                belongs to.

        Returns:
            A ``Response`` whose ``data`` is the story, with the new owner in ``owners``. The
            reply is a 404 with the message ``User not found`` when no user has that ID.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/stories/{story_id}/owners",
            json={"user_id": user_id},
        )

    def remove(self, *, story_id: int, user_id: int) -> Response:
        """Remove an owner from a story. ``DELETE /api/v1/stories/{story_id}/owners``

        Args:
            story_id: The ID of the story.
            user_id: The ID of the user to remove. The user must be an owner of the story.

        Returns:
            A ``Response`` with a 204 status and no data. The reply is a 404 with the message
            ``User not found`` when no user has that ID.
        """
        return self._transport.request(
            method="DELETE",
            path=f"/api/v1/stories/{story_id}/owners",
            json={"user_id": user_id},
        )
