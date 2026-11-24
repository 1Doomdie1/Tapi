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

        Deletes one or more links between actions in a single request. A link goes from the source
        to the receiver: the other direction is a different link. The type of a link does not
        matter.

        Args:
            links: The links to delete, each a dict with the ``source_id`` and the ``receiver_id``
                of the actions it connects. All the links must belong to the same story.

        Returns:
            A ``Response`` with a 204 status and no data. The sources and the receivers of the two
            actions change at once.
        """
        return self._transport.request(
            method="DELETE",
            path="/api/v1/links",
            json={"links": to_list(values=links)},
        )
