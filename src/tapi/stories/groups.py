from tapi.core import Response, Transport
from tapi.core.params import omit_none


class Groups:
    """The runs of the groups of a story, available as ``tines.stories.groups``.

    A group run, as listed by ``list_runs``, has the fields of a story run, plus ``group_id``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list_runs(
        self,
        *,
        group_id: int,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List the runs of a group. ``GET /api/v1/groups/{group_id}/runs``

        The endpoint is paginated and one call returns one page.

        Args:
            group_id: The ID of the group.
            per_page: The number of results per page. Tines defaults to 20 and caps it at 500.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``group_runs``, the runs of the page,
            and ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/groups/{group_id}/runs",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )

    def list_run_events(
        self,
        *,
        group_id: int,
        group_run_guid: str,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List the events of a group run. ``GET /api/v1/groups/{group_id}/runs/{group_run_guid}``

        The endpoint is paginated and one call returns one page.

        Args:
            group_id: The ID of the group.
            group_run_guid: The guid of the group run.
            per_page: The number of results per page. Tines defaults to 20 and caps it at 500.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``group_run_events``, a list of objects
            with ``id``, ``action_id`` (the action that emitted the event), ``created_at`` and
            ``is_reemitted``, and ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/groups/{group_id}/runs/{group_run_guid}",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )
