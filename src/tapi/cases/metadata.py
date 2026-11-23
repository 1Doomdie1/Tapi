from collections.abc import Mapping, Sequence

from tapi.core import Response, Transport
from tapi.core.params import to_list

MetadataValue = str | int | float | bool | None


class Metadata:
    """The metadata of a case, available as ``tines.cases.metadata``.

    Metadata is a set of key-value pairs that a case holds. A value is a string, a number, a
    boolean or ``null``: an object or a list as a value is a 422. ``list`` and ``get`` return an
    object with ``case_id`` and ``metadata``, an object of the pairs.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(self, *, case_id: int) -> Response:
        """List the metadata of a case. ``GET /api/v2/cases/{case_id}/metadata``

        The OpenAPI document shows a paginated list, and the server returns every pair in an
        object and ignores ``per_page`` and ``page``.

        Args:
            case_id: The ID of the case.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id`` and ``metadata``, an
            empty object for a case without metadata.
        """
        return self._transport.request(method="GET", path=f"/api/v2/cases/{case_id}/metadata")

    def get(self, *, case_id: int, key: str) -> Response:
        """Get one pair of metadata. ``GET /api/v2/cases/{case_id}/metadata/{key}``

        Args:
            case_id: The ID of the case.
            key: The key of the pair.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id`` and ``metadata``, which
            holds only the pair that was asked for. The reply is a 404 with ``Metadata key <key>
            does not exist`` for a key that is not there.
        """
        return self._transport.request(method="GET", path=f"/api/v2/cases/{case_id}/metadata/{key}")

    def create(self, *, case_id: int, metadata: Mapping[str, MetadataValue]) -> Response:
        """Add pairs of metadata. ``POST /api/v2/cases/{case_id}/metadata``

        This creates keys only. If one of the keys already has a value, the reply is a 409 with
        ``Metadata key <key> already exists`` and none of the pairs are set. To change a value,
        use ``update``.

        Args:
            case_id: The ID of the case.
            metadata: The key-value pairs to add. A value is a string, a number, a boolean or
                ``None``.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id`` and ``metadata``, with a
            201 status. The reply is a 400 with ``Invalid metadata`` when ``metadata`` is empty,
            and a 422 when a value is an object or a list.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v2/cases/{case_id}/metadata",
            json={"metadata": metadata},
        )

    def update(self, *, case_id: int, metadata: Mapping[str, MetadataValue]) -> Response:
        """Set pairs of metadata. ``PUT /api/v2/cases/{case_id}/metadata``

        This changes the keys that exist and creates the others. The operation is ``PUT`` only,
        and a ``PATCH`` is a 404, so tapi does not use ``PATCH`` here.

        Args:
            case_id: The ID of the case.
            metadata: The key-value pairs to set. A value is a string, a number, a boolean or
                ``None``.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id`` and ``metadata``, with
            every pair of the case. The reply is a 400 with ``Invalid metadata`` when
            ``metadata`` is empty.
        """
        return self._transport.request(
            method="PUT",
            path=f"/api/v2/cases/{case_id}/metadata",
            json={"metadata": metadata},
        )

    def delete(self, *, case_id: int, metadata: Sequence[str]) -> Response:
        """Delete pairs of metadata. ``DELETE /api/v2/cases/{case_id}/metadata``

        The keys are sent as a JSON body named ``metadata``, as the Tines docs show. The OpenAPI
        document calls the property ``keys`` and says that leaving it out deletes everything, and
        the server answered both with a 400.

        Args:
            case_id: The ID of the case.
            metadata: The keys to delete. An empty list deletes nothing.

        Returns:
            A ``Response`` with a 204 status and no data. The reply is a 404 with ``Metadata key
            <key> does not exist`` for a key that is not there.
        """
        return self._transport.request(
            method="DELETE",
            path=f"/api/v2/cases/{case_id}/metadata",
            json={"metadata": to_list(values=metadata)},
        )
