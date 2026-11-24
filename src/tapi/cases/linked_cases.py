from collections.abc import Sequence

from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_list


class LinkedCases:
    """The cases linked to a case, available as ``tines.cases.linked_cases``.

    A link is shown as a ``linked_case``, an object with the ``case_id`` and the ``name`` of the
    other case.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        case_id: int,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List the cases linked to a case. ``GET /api/v2/cases/{case_id}/linked_cases``

        The endpoint is paginated and one call returns one page.

        Args:
            case_id: The ID of the case.
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id``, ``name``,
            ``linked_cases``, the linked cases of the page, and ``meta``.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v2/cases/{case_id}/linked_cases",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )

    def create(self, *, case_id: int, id: int) -> Response:
        """Link a case to another. ``POST /api/v2/cases/{case_id}/linked_cases``

        The link shows on both cases.

        Args:
            case_id: The ID of the case that gets the link.
            id: The ID of the case to link to it. This is the property of the Tines docs.

        Returns:
            A ``Response`` whose ``data`` is an object with the ``case_id`` and ``name`` of the case
            and the ``linked_case``, with a 201 status.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v2/cases/{case_id}/linked_cases",
            json={"id": id},
        )

    def batch_create(self, *, case_id: int, ids: Sequence[int]) -> Response:
        """Link a case to several others. ``POST /api/v2/cases/{case_id}/linked_cases/batch``

        Args:
            case_id: The ID of the case that gets the links.
            ids: The IDs of the cases to link, at most 150 according to the Tines docs. This is
                the property of the Tines docs. The OpenAPI document calls it ``linked_case_ids``,
                which was a 500.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id``, ``name`` and the
            ``linked_cases``, with a 201 status, also for an empty list and for cases that are
            linked already. The reply is a 404 with ``Target cases not found`` for a case that
            does not exist and a 422 for the case itself.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v2/cases/{case_id}/linked_cases/batch",
            json={"ids": to_list(values=ids)},
        )

    def delete(self, *, case_id: int, linked_case_id: int) -> Response:
        """Unlink a case. ``DELETE /api/v2/cases/{case_id}/linked_cases/{linked_case_id}``

        Args:
            case_id: The ID of the case.
            linked_case_id: The ID of the linked case to remove.

        Returns:
            A ``Response`` with a 204 status and no data. The link goes from both cases, and a
            case that is not linked is a 204 too. A case that does not exist is a 404.
        """
        return self._transport.request(
            method="DELETE", path=f"/api/v2/cases/{case_id}/linked_cases/{linked_case_id}"
        )
