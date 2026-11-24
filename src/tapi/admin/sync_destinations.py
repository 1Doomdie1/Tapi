from collections.abc import Sequence

from tapi.admin.types import SyncMode
from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_list


class SyncDestinations:
    """The story sync destinations, available as ``tines.admin.sync_destinations``.

    A sync destination delivers stories of this tenant to a team of another tenant, or of the same
    tenant. The source stories must use change control, and draft syncing must be enabled for the
    source tenant. A destination, as listed by ``list`` and returned by the other methods, has
    ``id``, ``destination_tenant_url``, ``destination_team_id``, ``manual_sync_only``,
    ``sync_mode``, ``origin_team_id`` (the team of this tenant where it was created) and
    ``subscriptions``: one object for each story, with ``story`` (its ``id`` and ``name``),
    ``status`` (``synced``, ``failed`` or ``requires_sync``) and ``error_message`` (``null``
    unless the status is ``failed``). The Tines docs show a destination inside an object with
    ``sync_destination`` for ``get``, ``create`` and ``update``, and the OpenAPI document shows it
    as it is.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List sync destinations. ``GET /api/v1/admin/sync_destinations``

        The endpoint is paginated and one call returns one page. Read ``data["meta"]`` to decide
        whether to ask for the next page.

        Args:
            per_page: The number of results per page. Tines caps it at 500.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``sync_destinations``, the
            destinations of the page, and ``meta``, the pagination details: ``current_page``,
            ``previous_page`` and ``next_page`` (links), ``next_page_number``, ``per_page``,
            ``pages`` (the number of pages) and ``count``.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/admin/sync_destinations",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )

    def get(self, *, sync_destination_id: int) -> Response:
        """Get a sync destination. ``GET /api/v1/admin/sync_destinations/{sync_destination_id}``

        Args:
            sync_destination_id: The ID of the sync destination.

        Returns:
            A ``Response`` whose ``data`` is the destination. The reply is a 404 with ``Sync
            destination not found`` for a destination that does not exist.
        """
        return self._transport.request(
            method="GET", path=f"/api/v1/admin/sync_destinations/{sync_destination_id}"
        )

    def create(
        self,
        *,
        destination_tenant_url: str,
        destination_team_id: int,
        team_id: int,
        story_ids: Sequence[int],
        destination_tenant_api_key: str | None = None,
        manual_sync_only: bool | None = None,
        sync_mode: SyncMode | None = None,
    ) -> Response:
        """Create a sync destination. ``POST /api/v1/admin/sync_destinations``

        Creates a destination and subscribes it to the stories.

        Args:
            destination_tenant_url: The base URL of the destination tenant. For a sync to a team
                of this tenant, use the URL of this tenant.
            destination_team_id: The ID of the team on the destination tenant that owns the
                synced stories.
            team_id: The ID of the team on this tenant that creates the sync.
            story_ids: The IDs of the stories of this tenant to sync. They must use change
                control.
            destination_tenant_api_key: A Tines API key used to publish to the destination
                tenant, needed only for another tenant. It needs the ``STORY_CREATE`` and
                ``STORY_UPDATE`` permissions on the destination team.
            manual_sync_only: Whether the stories are synced only when ``manual_sync`` or
                ``sync_story`` is called.
            sync_mode: ``live_readonly`` to replace the live story on the destination with each
                delivery, which is the default, or ``draft_editable`` to create an editable
                draft with each delivery. It cannot be changed afterwards: delete the destination
                and create it again.

        Returns:
            A ``Response`` whose ``data`` is the created destination, with a 201 status.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/admin/sync_destinations",
            json=omit_none(
                values={
                    "destination_tenant_url": destination_tenant_url,
                    "destination_team_id": destination_team_id,
                    "team_id": team_id,
                    "story_ids": to_list(values=story_ids),
                    "destination_tenant_api_key": destination_tenant_api_key,
                    "manual_sync_only": manual_sync_only,
                    "sync_mode": sync_mode,
                }
            ),
        )

    def update(
        self,
        *,
        sync_destination_id: int,
        destination_tenant_api_key: str | None = None,
        story_ids: Sequence[int] | None = None,
        manual_sync_only: bool | None = None,
    ) -> Response:
        """Change a destination. ``PATCH /api/v1/admin/sync_destinations/{sync_destination_id}``

        The Tines documentation shows this operation as ``PUT``. The OpenAPI document lists the
        same operation under ``PUT`` and ``PATCH``, and tapi uses ``PATCH``. The teams, the URL
        of the destination tenant and the sync mode cannot be changed: delete the destination
        and create it again.

        Args:
            sync_destination_id: The ID of the sync destination.
            destination_tenant_api_key: A new API key, to rotate the old one. It is kept when
                left out.
            story_ids: The IDs of the stories to sync. An empty list removes all the
                subscriptions, and they are kept when left out.
            manual_sync_only: Whether the stories are synced only by hand. It is kept when left
                out.

        Returns:
            A ``Response`` whose ``data`` is the updated destination.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v1/admin/sync_destinations/{sync_destination_id}",
            json=omit_none(
                values={
                    "destination_tenant_api_key": destination_tenant_api_key,
                    "story_ids": to_list(values=story_ids),
                    "manual_sync_only": manual_sync_only,
                }
            ),
        )

    def delete(
        self,
        *,
        sync_destination_id: int,
        keep_stories: bool | None = None,
    ) -> Response:
        """Delete a destination. ``DELETE /api/v1/admin/sync_destinations/{sync_destination_id}``

        Removes the destination. By default Tines also deletes the synced stories on the
        destination tenant, which it does in the background.

        Args:
            sync_destination_id: The ID of the sync destination.
            keep_stories: ``True`` to keep the stories on the destination, detached from the
                source, instead of deleting them. The stories of a ``draft_editable`` destination
                are always kept. Tines defaults to ``False``. It is sent in the body.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(
            method="DELETE",
            path=f"/api/v1/admin/sync_destinations/{sync_destination_id}",
            json={"keep_stories": keep_stories} if keep_stories is not None else None,
        )

    def manual_sync(self, *, sync_destination_id: int) -> Response:
        """Sync all. ``POST /api/v1/admin/sync_destinations/{sync_destination_id}/manual_sync``

        Syncs a destination by hand. It queues the delivery of every subscribed story to the
        destination tenant. For a ``live_readonly`` destination each delivery replaces the live
        story there. For a ``draft_editable`` one each delivery creates a new draft.

        Args:
            sync_destination_id: The ID of the sync destination.

        Returns:
            A ``Response`` with a 200 status. ``data`` is an object with ``sync_initiated``.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/admin/sync_destinations/{sync_destination_id}/manual_sync",
        )

    def sync_story(self, *, sync_destination_id: int, story_id: int) -> Response:
        """``POST /api/v1/admin/sync_destinations/{sync_destination_id}/story/{story_id}/sync``

        Syncs one story by hand. It queues the delivery of one subscribed story. For a
        ``live_readonly`` destination, a story that is already ``synced`` is not sent again.

        Args:
            sync_destination_id: The ID of the sync destination.
            story_id: The ID of the story, as in ``subscriptions[].story.id``.

        Returns:
            A ``Response`` with a 200 status. ``data`` is an object with ``story_sync_initiated``.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/admin/sync_destinations/{sync_destination_id}/story/{story_id}/sync",
        )
