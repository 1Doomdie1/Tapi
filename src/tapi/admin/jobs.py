from tapi.core import Response, Transport
from tapi.core.params import omit_none


class Jobs:
    """The background jobs of a dedicated tenant, available as ``tines.admin.jobs``.

    The Tines docs say that every route is relevant for dedicated tenants only. The routes are in
    the Tines docs and not in the OpenAPI document, and the docs do not say which key they need,
    which status codes they answer with, or what the type of an action ID is. A tenant that is not
    dedicated answers the lists with a 403 and an object whose ``error`` is ``Endpoint not
    available on this tenant``. A job, as listed, has
    ``id``, ``type`` (such as ``AgentReceiveJob`` or ``CredentialRefreshJob``), ``agent`` (an
    object with the ``id`` and ``name`` of the action for an ``AgentReceiveJob``, and the ID of the
    action for a ``CredentialRefreshJob``) and ``events`` (an event ID). The dead and the retry
    jobs also have ``retry_count``, ``last_retry`` (a timestamp) and ``error_class``, and the
    in-progress jobs have ``started_at`` (a timestamp).

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list_dead(self, *, per_page: int | None = None, page: int | None = None) -> Response:
        """List dead jobs. ``GET /api/v1/admin/dead_jobs``

        The endpoint is paginated and one call returns one page. Read ``data["meta"]`` to decide
        whether to ask for the next page.

        Args:
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is, in the docs, an object with ``admin/dead_jobs``, the
            jobs of the page, and ``meta``, the pagination details: ``current_page``,
            ``previous_page`` and ``next_page`` (links), ``next_page_number``, ``per_page``,
            ``pages`` (the number of pages) and ``count``.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/admin/dead_jobs",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )

    def list_in_progress(self, *, per_page: int | None = None, page: int | None = None) -> Response:
        """List in-progress jobs. ``GET /api/v1/admin/in_progress_jobs``

        The endpoint is paginated and one call returns one page. Read ``data["meta"]`` to decide
        whether to ask for the next page.

        Args:
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is, in the docs, an object with
            ``admin/in_progress_jobs``, the jobs of the page, and ``meta``, the pagination
            details, as for ``list_dead``.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/admin/in_progress_jobs",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )

    def list_queued(self, *, per_page: int | None = None, page: int | None = None) -> Response:
        """List queued jobs. ``GET /api/v1/admin/queued_jobs``

        A snapshot of the job queue at the moment of the request. The endpoint is paginated and
        one call returns one page. Read ``data["meta"]`` to decide whether to ask for the next
        page.

        Args:
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is, in the docs, an object with ``admin/queued_jobs``,
            the jobs of the page, and ``meta``, the pagination details, as for ``list_dead``.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/admin/queued_jobs",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )

    def list_retry(self, *, per_page: int | None = None, page: int | None = None) -> Response:
        """List retry jobs. ``GET /api/v1/admin/retry_jobs``

        The endpoint is paginated and one call returns one page. Read ``data["meta"]`` to decide
        whether to ask for the next page.

        Args:
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is, in the docs, an object with ``admin/retry_jobs``,
            the jobs of the page, and ``meta``, the pagination details, as for ``list_dead``.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/admin/retry_jobs",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )

    def delete_all_dead(self) -> Response:
        """Delete all dead jobs. ``DELETE /api/v1/admin/delete_all_dead_jobs``

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(method="DELETE", path="/api/v1/admin/delete_all_dead_jobs")

    def delete_all_queued(self) -> Response:
        """Delete all queued jobs. ``DELETE /api/v1/admin/delete_all_queued_jobs``

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(method="DELETE", path="/api/v1/admin/delete_all_queued_jobs")

    def delete_all_retry(self) -> Response:
        """Delete all retry jobs. ``DELETE /api/v1/admin/delete_all_retry_jobs``

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(method="DELETE", path="/api/v1/admin/delete_all_retry_jobs")

    def delete_dead_by_action(self, *, action_id: int) -> Response:
        """Delete dead. ``DELETE /api/v1/admin/actions/{action_id}/delete_all_dead_jobs``

        Deletes all the dead jobs of one action.

        Args:
            action_id: The ID of the action.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(
            method="DELETE", path=f"/api/v1/admin/actions/{action_id}/delete_all_dead_jobs"
        )

    def delete_queued_by_action(self, *, action_id: int) -> Response:
        """Delete queued. ``DELETE /api/v1/admin/actions/{action_id}/delete_all_queued_jobs``

        Deletes all the queued jobs of one action.

        Args:
            action_id: The ID of the action.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(
            method="DELETE", path=f"/api/v1/admin/actions/{action_id}/delete_all_queued_jobs"
        )

    def delete_retry_by_action(self, *, action_id: int) -> Response:
        """Delete retry. ``DELETE /api/v1/admin/actions/{action_id}/delete_all_retry_jobs``

        Deletes all the retry jobs of one action.

        Args:
            action_id: The ID of the action.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(
            method="DELETE", path=f"/api/v1/admin/actions/{action_id}/delete_all_retry_jobs"
        )
