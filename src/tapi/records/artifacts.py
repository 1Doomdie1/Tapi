from tapi.core import Response, Transport


class Artifacts:
    """The artifacts of a record, available as ``tines.records.artifacts``.

    An artifact is the stored content of a large text field of a record.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def get(self, *, record_id: int, artifact_id: int) -> Response:
        """Get an artifact. ``GET /api/v1/records/{record_id}/artifacts/{artifact_id}``

        Args:
            record_id: The ID of the record.
            artifact_id: The ID of the artifact.

        Returns:
            A ``Response`` whose ``data`` is an object with ``id``, ``value`` (the text),
            ``record_field`` (an object with the ``id`` and the ``name`` of the field),
            ``created_at`` and ``updated_at``.
        """
        return self._transport.request(
            method="GET", path=f"/api/v1/records/{record_id}/artifacts/{artifact_id}"
        )
