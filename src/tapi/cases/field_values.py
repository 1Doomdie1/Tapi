from tapi.core import Response, Transport
from tapi.core.params import omit_none


class FieldValues:
    """The field values of a case, available as ``tines.cases.field_values``.

    A field is a custom value that a team defines for its cases, such as a severity or an owner.
    These methods read and set the value that one case holds for one field. A field value, as
    returned by ``get``, ``create`` and ``update`` and listed by ``list``, is an object with
    ``id`` (the ID of the field value, which is the ``field_id`` of the other methods), ``value``
    and ``case_input``, the field itself, with ``id``, ``key``, ``name``, ``validation_type`` and
    ``validation_options``.

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
        """List the field values of a case. ``GET /api/v2/cases/{case_id}/fields``

        The endpoint is paginated and one call returns one page.

        Args:
            case_id: The ID of the case.
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id``, ``fields``, the field
            values of the page, and ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v2/cases/{case_id}/fields",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )

    def get(self, *, case_id: int, field_id: int) -> Response:
        """Get a field value. ``GET /api/v2/cases/{case_id}/fields/{field_id}``

        Args:
            case_id: The ID of the case.
            field_id: The ID of the field value.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id`` and ``field``. The reply
            is a 404 with ``Field not found`` for a field value that does not exist.
        """
        return self._transport.request(
            method="GET", path=f"/api/v2/cases/{case_id}/fields/{field_id}"
        )

    def create(self, *, case_id: int, input_id: int, value: str) -> Response:
        """Set a field value on a case. ``POST /api/v2/cases/{case_id}/fields``

        Args:
            case_id: The ID of the case.
            input_id: The ID of the field, as defined for the team.
            value: The value, as a string. A field that allows several values takes them as one
                string separated by ``|``.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id`` and ``field``, with a 201
            status in the OpenAPI document. The reply is a 404 with ``TeamCaseInput not found``
            for a field that does not exist.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v2/cases/{case_id}/fields",
            json={"input_id": input_id, "value": value},
        )

    def update(self, *, case_id: int, field_id: int, value: str) -> Response:
        """Change a field value. ``PATCH /api/v2/cases/{case_id}/fields/{field_id}``

        The Tines documentation shows this operation as ``PUT``. The OpenAPI document lists the
        same operation under ``PUT`` and ``PATCH``, and tapi uses ``PATCH``.

        Args:
            case_id: The ID of the case.
            field_id: The ID of the field value.
            value: The new value, as a string. A field that allows several values takes them as
                one string separated by ``|``.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id`` and ``field``.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v2/cases/{case_id}/fields/{field_id}",
            json={"value": value},
        )

    def delete(self, *, case_id: int, field_id: int) -> Response:
        """Delete a field value. ``DELETE /api/v2/cases/{case_id}/fields/{field_id}``

        Args:
            case_id: The ID of the case.
            field_id: The ID of the field value.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(
            method="DELETE", path=f"/api/v2/cases/{case_id}/fields/{field_id}"
        )
