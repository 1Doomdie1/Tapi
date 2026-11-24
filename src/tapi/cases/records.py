from tapi.core import Response, Transport
from tapi.core.params import omit_none


class Records:
    """The records attached to a case, available as ``tines.cases.records``.

    A record, as returned by ``get`` and ``create`` and listed by ``list``, has ``id``,
    ``record_type``, ``results``, ``created_at`` and ``linked_at``.

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
        """List the records of a case. ``GET /api/v2/cases/{case_id}/records``

        The endpoint is paginated and one call returns one page.

        Args:
            case_id: The ID of the case.
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id``, ``records``, the
            records of the page, and ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v2/cases/{case_id}/records",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )

    def get(self, *, case_id: int, record_id: int) -> Response:
        """Get a record of a case. ``GET /api/v2/cases/{case_id}/records/{record_id}``

        Args:
            case_id: The ID of the case.
            record_id: The ID of the record.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id`` and ``record``.
        """
        return self._transport.request(
            method="GET", path=f"/api/v2/cases/{case_id}/records/{record_id}"
        )

    def create(self, *, case_id: int, record_id: int) -> Response:
        """Attach a record to a case. ``POST /api/v2/cases/{case_id}/records``

        Args:
            case_id: The ID of the case.
            record_id: The ID of the record to attach. This is the property of the Tines docs. The
                OpenAPI document calls it ``record_result_set_id``, which the server did not read.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id`` and ``record``, with a
            201 status in the OpenAPI document. The reply is a 404 with ``RecordResultSet not
            found`` for a record that does not exist.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v2/cases/{case_id}/records",
            json={"record_id": record_id},
        )

    def delete(self, *, case_id: int, record_id: int) -> Response:
        """Remove a record from a case. ``DELETE /api/v2/cases/{case_id}/records/{record_id}``

        Args:
            case_id: The ID of the case.
            record_id: The ID of the record to remove.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(
            method="DELETE", path=f"/api/v2/cases/{case_id}/records/{record_id}"
        )
