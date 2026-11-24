from typing import Literal

from tapi.core import Response, Transport
from tapi.core.params import omit_none

FolderContentType = Literal["CREDENTIAL", "RESOURCE", "STORY"]
FolderFilterContentType = FolderContentType


class Folders:
    """Folders, available as ``tines.folders``.

    A folder, as returned by ``get``, ``create`` and ``update`` and listed by ``list``, has ``id``,
    ``name``, ``team_id``, ``content_type`` (``CREDENTIAL``, ``RESOURCE`` or ``STORY``, and also
    ``REPORT``, ``CASE`` or ``TEMPLATE``), ``size`` (the number of items in the folder, not
    counting subfolders) and ``parent_folder_id`` (``null`` for a folder at the root level).

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        team_id: int | None = None,
        content_type: FolderFilterContentType | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List folders. ``GET /api/v1/folders``

        The endpoint is paginated and one call returns one page.

        Args:
            team_id: Only folders of this team.
            content_type: Only folders that hold this type of content: ``CREDENTIAL``,
                ``RESOURCE`` or ``STORY``.
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``folders``, the folders of the page,
            and ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/folders",
            params=omit_none(
                values={
                    "team_id": team_id,
                    "content_type": content_type,
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )

    def get(self, *, folder_id: int) -> Response:
        """Get a folder. ``GET /api/v1/folders/{folder_id}``

        Args:
            folder_id: The ID of the folder to retrieve.

        Returns:
            A ``Response`` whose ``data`` is the folder.
        """
        return self._transport.request(method="GET", path=f"/api/v1/folders/{folder_id}")

    def create(
        self,
        *,
        name: str,
        content_type: FolderContentType,
        team_id: int,
        parent_folder_id: int | None = None,
    ) -> Response:
        """Create a folder. ``POST /api/v1/folders``

        Args:
            name: The name of the folder.
            content_type: The type of content the folder holds: ``CREDENTIAL``, ``RESOURCE`` or
                ``STORY``.
            team_id: The ID of the team the folder is created in.
            parent_folder_id: The ID of the folder to create it in. Tines defaults to ``null``,
                the root level.

        Returns:
            A ``Response`` whose ``data`` is the created folder, with a 201 status.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/folders",
            json=omit_none(
                values={
                    "name": name,
                    "content_type": content_type,
                    "team_id": team_id,
                    "parent_folder_id": parent_folder_id,
                }
            ),
        )

    def update(
        self,
        *,
        folder_id: int,
        name: str,
        parent_folder_id: int | None = None,
    ) -> Response:
        """Rename or move a folder. ``PATCH /api/v1/folders/{folder_id}``

        Tines moves a folder to the root level when ``parent_folder_id`` is sent as ``null`` or as
        an empty string. A parameter left as ``None`` is not sent, so tapi cannot do that yet. The
        content type and the team of a folder cannot be changed.

        Args:
            folder_id: The ID of the folder to update.
            name: The name of the folder.
            parent_folder_id: The ID of the folder to move it into.

        Returns:
            A ``Response`` whose ``data`` is the updated folder.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v1/folders/{folder_id}",
            json=omit_none(values={"name": name, "parent_folder_id": parent_folder_id}),
        )

    def delete(self, *, folder_id: int) -> Response:
        """Delete a folder. ``DELETE /api/v1/folders/{folder_id}``

        A folder with contents, such as a subfolder, cannot be deleted: Tines answers with a 422
        and a message asking you to remove the contents first.

        Args:
            folder_id: The ID of the folder to delete.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(method="DELETE", path=f"/api/v1/folders/{folder_id}")
