from tapi.cases.types import FieldType, FieldValidation, FieldValidationOptions
from tapi.core import Response, Transport
from tapi.core.params import omit_none


class Fields:
    """The case fields of a team, available as ``tines.cases.fields``.

    A field is a custom value that cases of a team can hold, such as a severity or an owner. This
    is the definition of the field. To read and set the value that one case holds for a field, use
    ``tines.cases.field_values``. A field, as returned by ``get``, ``create`` and ``update`` and
    listed by ``list``, has ``id``, ``name``, ``key`` (a slug), ``input_type``, ``sensitive``,
    ``validation_type`` (``none`` for a new field), ``validation_options`` (an empty object for a
    new field), ``team``, ``team_case_input_group`` (``null`` outside a group), ``created_at`` and
    ``updated_at``. ``create`` returns the field inside an object with one key,
    ``team_case_input``, and ``get`` and ``update`` return it as it is.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        team_id: int | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List the case fields. ``GET /api/v1/case_inputs``

        The endpoint is paginated and one call returns one page.

        Args:
            team_id: Only fields of this team.
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_inputs``, the fields of the
            page, and ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/case_inputs",
            params=omit_none(values={"team_id": team_id, "per_page": per_page, "page": page}),
        )

    def get(self, *, field_id: int) -> Response:
        """Get a case field. ``GET /api/v1/case_inputs/{field_id}``

        Args:
            field_id: The ID of the field.

        Returns:
            A ``Response`` whose ``data`` is the field. The Tines docs show it inside an object
            with ``case_input``, which the server does not do. The reply is a 404 with
            ``TeamCaseInput not found`` for a field that does not exist.
        """
        return self._transport.request(method="GET", path=f"/api/v1/case_inputs/{field_id}")

    def create(
        self,
        *,
        name: str,
        input_type: FieldType,
        team_id: int,
        sensitive: bool | None = None,
        validation_type: FieldValidation | None = None,
        validation_options: FieldValidationOptions | None = None,
        group_name: str | None = None,
    ) -> Response:
        """Create a case field. ``POST /api/v1/case_inputs``

        Args:
            name: The name of the field. It is unique within the team.
            input_type: The type of the values: ``string``, ``number``, ``boolean``, ``timestamp``,
                ``email``, ``url`` or ``ip_address``.
            team_id: The ID of the team that gets the field.
            sensitive: Whether the sensitive field permission is needed to read or write it.
            validation_type: ``options`` or ``regex``, for a ``string`` field.
            validation_options: What to check a value against. For ``options``, an object with the
                allowed values: ``{"options": ["low", "high"]}``. For ``regex``, an object with the
                pattern: ``{"regex": "^T-[0-9]+$"}``.
            group_name: The name of the group to put the field in.

        Returns:
            A ``Response`` whose ``data`` is an object with ``team_case_input``, the created field,
            with a 201 status.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/case_inputs",
            json=omit_none(
                values={
                    "name": name,
                    "input_type": input_type,
                    "team_id": team_id,
                    "sensitive": sensitive,
                    "validation_type": validation_type,
                    "validation_options": validation_options,
                    "group_name": group_name,
                }
            ),
        )

    def update(
        self,
        *,
        field_id: int,
        name: str | None = None,
        sensitive: bool | None = None,
        validation_type: FieldValidation | None = None,
        validation_options: FieldValidationOptions | None = None,
        group_name: str | None = None,
    ) -> Response:
        """Change a case field. ``PATCH /api/v2/case_inputs/{field_id}``

        Args:
            field_id: The ID of the field.
            name: A new name.
            sensitive: Whether the sensitive field permission is needed to read or write it.
            validation_type: ``none``, ``options`` or ``regex``. Going back to ``none`` leaves the
                old ``validation_options`` in the field.
            validation_options: What to check a value against, in the shapes that ``create``
                describes.
            group_name: The name of the group to put the field in.

        Returns:
            A ``Response`` whose ``data`` is the updated field, as it is.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v2/case_inputs/{field_id}",
            json=omit_none(
                values={
                    "name": name,
                    "sensitive": sensitive,
                    "validation_type": validation_type,
                    "validation_options": validation_options,
                    "group_name": group_name,
                }
            ),
        )

    def delete(self, *, field_id: int) -> Response:
        """Delete a case field. ``DELETE /api/v2/case_inputs/{field_id}``

        Args:
            field_id: The ID of the field.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(method="DELETE", path=f"/api/v2/case_inputs/{field_id}")

    def list_values(
        self,
        *,
        field_id: int,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List the values of a field across cases. ``GET /api/v1/case_inputs/{field_id}/fields``

        The endpoint is paginated and one call returns one page.

        Args:
            field_id: The ID of the field.
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``fields``, the values of the page,
            each with ``id``, ``value``, ``case`` (an object with an ``id``) and ``case_input``,
            and ``meta``, the pagination details. The reply is a 404 with ``CaseInput not found``
            for a field that does not exist.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/case_inputs/{field_id}/fields",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )
