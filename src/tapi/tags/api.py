from tapi.core import Response, Transport
from tapi.core.params import omit_none


class Tags:
    """Tags, available as ``tines.tags``.

    A tag, as returned by ``get``, ``create`` and ``update`` and listed by ``list``, has ``id``,
    ``name``, ``color`` (a ``#RRGGBB`` hex value), ``teams`` (a list of objects with the ``id`` and
    ``name`` of each team the tag belongs to), ``created_at`` and ``updated_at`` (ISO 8601
    timestamps). A tag created after February 2025 belongs to a single team.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        team_id: int | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List tags. ``GET /api/v1/tags``

        The endpoint is paginated and one call returns one page.

        Args:
            team_id: Only tags of this team.
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``tags``, the tags of the page that
            your key has access to, and ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/tags",
            params=omit_none(values={"team_id": team_id, "per_page": per_page, "page": page}),
        )

    def get(self, *, tag_id: int) -> Response:
        """Get a tag. ``GET /api/v1/tags/{tag_id}``

        Args:
            tag_id: The ID of the tag to retrieve.

        Returns:
            A ``Response`` whose ``data`` is the tag.
        """
        return self._transport.request(method="GET", path=f"/api/v1/tags/{tag_id}")

    def create(self, *, name: str, team_id: int, color: str) -> Response:
        """Create a tag. ``POST /api/v1/tags``

        Args:
            name: The name of the tag. It must be unused.
            team_id: The ID of the team the tag belongs to.
            color: The color of the tag: one of ``purple``, ``blue``, ``gold``, ``green``,
                ``magenta``, ``red``, ``orange`` or ``mint``, or a ``#RRGGBB`` hex value. Tines
                returns the color as a hex value. Neither the Tines docs nor its OpenAPI document
                say that it is required, but Tines refuses a tag without one.

        Returns:
            A ``Response`` whose ``data`` is the created tag, with a 201 status. The reply is a 422
            with a message when the name is already used or the color is not valid.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/tags",
            json=omit_none(values={"name": name, "team_id": team_id, "color": color}),
        )

    def update(
        self,
        *,
        tag_id: int,
        name: str | None = None,
        color: str | None = None,
    ) -> Response:
        """Update a tag. ``PATCH /api/v1/tags/{tag_id}``

        The team of a tag cannot be changed. Without ``name`` and ``color`` nothing changes and the
        reply is the tag. The Tines documentation shows this operation as ``PUT``. The OpenAPI
        document lists the same operation under ``PUT`` and ``PATCH``, and tapi uses ``PATCH``.

        Args:
            tag_id: The ID of the tag to update.
            name: The new name of the tag.
            color: The new color of the tag: one of ``purple``, ``blue``, ``gold``, ``green``,
                ``magenta``, ``red``, ``orange`` or ``mint``, or a ``#RRGGBB`` hex value. A color
                that is neither, or an empty one, is answered with a 422.

        Returns:
            A ``Response`` whose ``data`` is the updated tag.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v1/tags/{tag_id}",
            json=omit_none(values={"name": name, "color": color}),
        )

    def delete(self, *, tag_id: int, team_id: int | None = None) -> Response:
        """Delete a tag. ``DELETE /api/v1/tags/{tag_id}``

        Args:
            tag_id: The ID of the tag to delete.
            team_id: Remove the tag from this team only. Without it the tag is deleted entirely.
                An unknown team is answered with a 404 and the tag is kept. Tines reads this
                parameter from the query and from a JSON body, and tapi sends it in the query.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(
            method="DELETE",
            path=f"/api/v1/tags/{tag_id}",
            params=omit_none(values={"team_id": team_id}),
        )
