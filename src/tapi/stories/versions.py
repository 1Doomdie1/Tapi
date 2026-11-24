from tapi.core import Response, Transport
from tapi.core.params import omit_none


class Versions:
    """The versions of a story, available as ``tines.stories.versions``.

    A version, as returned by ``create``, ``get`` and ``update`` and listed by ``list``, has
    ``id``, ``name`` (``null`` if it has none), ``description`` and ``timestamp`` (when the version
    was created, an ISO 8601 timestamp). ``get`` also returns ``export_file``, the story in
    exported form. The Tines docs show the version itself as the reply of ``create``, ``get`` and
    ``update``, and the server wraps it in an object with a ``story_version`` key.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        story_id: int,
        draft_id: int | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List the versions of a story. ``GET /api/v1/stories/{story_id}/versions``

        The endpoint is paginated and one call returns one page.

        Args:
            story_id: The ID of the story.
            draft_id: Only versions of this draft.
            per_page: The number of results per page. Tines defaults to 20 and caps it at 500.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``story_versions``, the versions of the
            page, and ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/stories/{story_id}/versions",
            params=omit_none(values={"draft_id": draft_id, "per_page": per_page, "page": page}),
        )

    def create(
        self,
        *,
        story_id: int,
        name: str | None = None,
        draft_id: int | None = None,
    ) -> Response:
        """Create a version of a story. ``POST /api/v1/stories/{story_id}/versions``

        Args:
            story_id: The ID of the story.
            name: The name of the version.
            draft_id: The ID of the draft to create the version for.

        Returns:
            A ``Response`` whose ``data`` is an object with ``story_version``, the created
            version. The status is 200, although the OpenAPI document says 201.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/stories/{story_id}/versions",
            json=omit_none(values={"name": name, "draft_id": draft_id}),
        )

    def get(self, *, story_id: int, version_id: int) -> Response:
        """Get a version of a story. ``GET /api/v1/stories/{story_id}/versions/{version_id}``

        Args:
            story_id: The ID of the story.
            version_id: The ID of the version to retrieve.

        Returns:
            A ``Response`` whose ``data`` is an object with ``story_version``, the version with
            its ``export_file``. The reply is a 404 with the message ``StoryVersion not found``
            when the story has no such version.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/stories/{story_id}/versions/{version_id}",
        )

    def update(self, *, story_id: int, version_id: int, name: str) -> Response:
        """Rename a version. ``POST /api/v1/stories/{story_id}/versions/{version_id}``

        Tines documents this operation as ``POST``, and no other method is listed.

        Args:
            story_id: The ID of the story.
            version_id: The ID of the version to rename.
            name: The new name of the version.

        Returns:
            A ``Response`` whose ``data`` is an object with ``story_version``, the updated
            version.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/stories/{story_id}/versions/{version_id}",
            json={"name": name},
        )

    def delete(self, *, story_id: int, version_id: int) -> Response:
        """Delete a version. ``DELETE /api/v1/stories/{story_id}/versions/{version_id}``

        Args:
            story_id: The ID of the story.
            version_id: The ID of the version to delete.

        Returns:
            A ``Response`` with a 200 status whose ``data`` is an object with ``destroyed_id``, the
            ID of the deleted version.
        """
        return self._transport.request(
            method="DELETE",
            path=f"/api/v1/stories/{story_id}/versions/{version_id}",
        )
