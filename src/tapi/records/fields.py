from tapi.core import Response, Transport
from tapi.core.params import omit_none
from tapi.records.types import FieldFormat


class Fields:
    """The large fields of a record, available as ``tines.records.fields``.

    A field of the type ``JSON`` or ``ARTIFACT`` is returned by the record routes as a handle. This
    reads its content.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def get(
        self, *, record_id: int, field: int | str, format: FieldFormat | None = None
    ) -> Response:
        """Get a record field. ``GET /api/v2/records/{record_id}/fields/{field}``

        Args:
            record_id: The ID of the record.
            field: The ID, the name or the slug of the field.
            format: ``json`` to return JSON, re-encoded in a canonical form, or ``text``, ``txt`` or
                ``plain`` to return the stored text as it is.

        Returns:
            A ``Response`` whose ``data`` is the content of the field, without an envelope: the
            parsed JSON for ``json``, and a ``str`` for ``text``. A field with no stored value has
            ``None`` as ``data`` for a text, and ``null`` for JSON.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v2/records/{record_id}/fields/{field}",
            params=omit_none(values={"format": format}),
        )
