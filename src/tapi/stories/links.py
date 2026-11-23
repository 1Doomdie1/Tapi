from collections.abc import Sequence

from tapi.core import Response, Transport
from tapi.core.params import to_list
from tapi.stories.types import Link


class Links:
    """The links between the actions of stories, available as ``tines.stories.links``.

    A link connects a source action to a receiver action: the receiver gets the events that the
    source emits. Tines only documents deleting links here. Links are created with the
    ``source_ids``, ``links_to_sources``, ``receiver_ids`` and ``links_to_receivers`` of
    ``tines.stories.actions.create`` and ``tines.stories.actions.update``, and a link has no ID of
    its own: it is the pair of the ``source_id`` and the ``receiver_id``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def delete(self, *, links: Sequence[Link]) -> Response:
        """Delete links. ``DELETE /api/v1/links``

        Deletes one or more links between actions in a single request. Tines checks all the links
        before it deletes any, so a request that is refused deletes nothing. A link goes from the
        source to the receiver: the other direction is a different link. The type of a link does
        not matter.

        Args:
            links: The links to delete, each a dict with the ``source_id`` and the
                ``receiver_id`` of the actions it connects. All the links must belong to the same
                story.

        Returns:
            A ``Response`` with a 204 status and no data. The sources and the receivers of the two
            actions change at once. The reply is a 400 when ``links`` is not a list of objects
            (``Links must be an array of objects with source_id and receiver_id``), when an object
            has no ``source_id`` or no ``receiver_id`` (``Each link must have source_id and
            receiver_id``), and when the links belong to different stories (``All links must
            belong to the same story``). It is a 404 when a link does not exist or is not visible
            to your key, with a message that names the first pair it did not find, such as ``Link
            not found between 1 and 2``. An empty list is a 500.
        """
        return self._transport.request(
            method="DELETE",
            path="/api/v1/links",
            json={"links": to_list(values=links)},
        )
