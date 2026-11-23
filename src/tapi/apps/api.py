from collections.abc import Sequence
from typing import NotRequired, TypedDict

from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_list


class AppFile(TypedDict):
    """A file of an app: its ``path`` and, optionally, its ``contents``."""

    path: str
    contents: NotRequired[str]


class Apps:
    """Apps, available as ``tines.apps``.

    An app, as returned by ``get``, ``create`` and ``publish`` and listed by ``list``, has ``id``,
    ``guid``, ``name``, ``description``, ``emoji``, ``created_at``, ``updated_at``, ``team`` (an
    object with the ``id`` and ``name`` of the team the app belongs to) and ``published_version``
    (an object with the ``id`` of the published version, or ``null`` if the app has not been
    published).

    Apps are not available on every Tines plan. Where they are not, or where they are switched
    off, every endpoint answers with a 404 and the message ``Not found``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(self, *, per_page: int | None = None, page: int | None = None) -> Response:
        """List the apps visible to you. ``GET /api/v1/apps``

        The endpoint is paginated and one call returns one page.

        Args:
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``apps``, the apps of the page, and
            ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/apps",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )

    def get(self, *, app_id: int) -> Response:
        """Get an app. ``GET /api/v1/apps/{app_id}``

        Args:
            app_id: The ID of the app to retrieve.

        Returns:
            A ``Response`` whose ``data`` is the app. The reply is a 404 with the message
            ``App not found`` when no app with that ID is visible to your key.
        """
        return self._transport.request(method="GET", path=f"/api/v1/apps/{app_id}")

    def create(
        self,
        *,
        team_id: int,
        name: str | None = None,
        description: str | None = None,
    ) -> Response:
        """Create an app. ``POST /api/v1/apps``

        Args:
            team_id: The ID of the team the app belongs to. It must not be a personal team.
            name: The name of the app.
            description: A description of the app.

        Returns:
            A ``Response`` whose ``data`` is the created app, with a 201 status. The reply is a 422
            with the message ``Validation failed: Cannot create app in a personal team`` when
            ``team_id`` is a personal team.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/apps",
            json=omit_none(values={"team_id": team_id, "name": name, "description": description}),
        )

    def delete(self, *, app_id: int) -> Response:
        """Delete an app and all of its versions. ``DELETE /api/v1/apps/{app_id}``

        Args:
            app_id: The ID of the app to delete.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(method="DELETE", path=f"/api/v1/apps/{app_id}")

    def export(self, *, app_id: int, version_id: int | None = None) -> Response:
        """Export an app. ``GET /api/v1/apps/{app_id}/export``

        Args:
            app_id: The ID of the app to export.
            version_id: The ID of the app version to export. Tines defaults to the current draft.

        Returns:
            A ``Response`` whose ``data`` is an object with the ``name`` of the app, its
            ``description`` (``null`` if there is none) and its ``files``: a list of objects with a
            ``path`` and ``contents``, in the format that ``replace_files`` takes. The reply is a
            404 when no app is visible or the version does not belong to the app, and a 413 when
            the files are too large to export.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/apps/{app_id}/export",
            params=omit_none(values={"version_id": version_id}),
        )

    def replace_files(self, *, app_id: int, files: Sequence[AppFile]) -> Response:
        """Replace all draft files of an app. ``PUT /api/v1/apps/{app_id}/files``

        This does not build the app. To build it, open the app in the Tines UI or use ``publish``.

        Args:
            app_id: The ID of the app whose draft files are replaced.
            files: The complete set of draft files. Each is a dict with ``path`` (the file path)
                and optionally ``contents`` (the file contents, an empty string by default). One
                file must have the path ``App.tsx``. Existing files that are left out are
                deleted.

        Returns:
            A ``Response`` whose ``data`` is an object with ``files``, the complete set of draft
            files of the app, each with a ``path`` and ``contents``. The reply is a 422 with the
            message ``Missing required entry file App.tsx`` when no file has that path, and
            nothing is replaced.
        """
        return self._transport.request(
            method="PUT",
            path=f"/api/v1/apps/{app_id}/files",
            json={"files": to_list(values=files)},
        )

    def publish(
        self,
        *,
        app_id: int,
        name: str | None = None,
        description: str | None = None,
    ) -> Response:
        """Publish an app. ``POST /api/v1/apps/{app_id}/publish``

        Builds the current draft and publishes it as a new version. If the draft has not changed
        since the latest version, that version is published instead.

        Args:
            app_id: The ID of the app to publish.
            name: A name for the published version.
            description: A description of the published version.

        Returns:
            A ``Response`` whose ``data`` is the published app, with ``published_version`` set. It
            does not echo ``name`` or ``description``. Tines documents a 422 with the build error
            when the build fails, but a syntax error in ``App.tsx`` was answered with a 500 and
            nothing was published.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/apps/{app_id}/publish",
            json=omit_none(values={"name": name, "description": description}),
        )
