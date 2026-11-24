from tapi.core import Response, Transport
from tapi.core.params import omit_none


class Recipients:
    """The monitoring recipients of a story, available as ``tines.stories.recipients``.

    A recipient receives the monitoring communications of a story when monitoring is enabled.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def add(self, *, story_id: int, address: str, draft_id: int | None = None) -> Response:
        """Add a recipient to a story. ``POST /api/v1/stories/{story_id}/recipients``

        Args:
            story_id: The ID of the story.
            address: The email address or webhook URL that receives the monitoring
                communications.
            draft_id: The ID of the draft to update.

        Returns:
            A ``Response`` whose ``data`` is the story, with the new recipient in ``recipients``.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/stories/{story_id}/recipients",
            json=omit_none(values={"address": address, "draft_id": draft_id}),
        )

    def remove(self, *, story_id: int, address: str, draft_id: int | None = None) -> Response:
        """Remove a recipient from a story. ``DELETE /api/v1/stories/{story_id}/recipients``

        The recipient stops receiving the monitoring communications and leaves the recipients.

        Args:
            story_id: The ID of the story.
            address: The email address or webhook URL to remove.
            draft_id: The ID of the draft to update.

        Returns:
            A ``Response`` with no data. The status is 200, although the Tines docs say 204. The
            reply is a 404 with the message ``Recipient not found`` when the address is not a
            recipient of the story.
        """
        return self._transport.request(
            method="DELETE",
            path=f"/api/v1/stories/{story_id}/recipients",
            json=omit_none(values={"address": address, "draft_id": draft_id}),
        )
