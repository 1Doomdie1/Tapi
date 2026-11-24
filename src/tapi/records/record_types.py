from collections.abc import Sequence

from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_list
from tapi.records.types import (
    OnLimitReached,
    RecordTypeField,
    RecordTypeFieldChange,
    RecordTypeOrder,
    RetentionColumn,
    SortDirection,
)


class RecordTypes:
    """The record types, available as ``tines.records.record_types``.

    A record type defines the fields of its records and how long Tines keeps them. A record type,
    as returned in the ``data`` of the methods, has ``id``, ``name``, ``slug``, ``description``
    (or ``null``), ``editable``, ``ttl_days`` (or ``null`` when records are kept for ever),
    ``retention_column_name`` (``CREATED_AT`` or ``UPDATED_AT``), ``on_limit_reached`` (``REJECT``
    or ``EVICT_OLDEST``), ``custom_records_limit`` (or ``null``), ``effective_max_records``,
    ``has_custom_limit``, ``relationships`` (``team`` with its ``id``), ``created_at``,
    ``updated_at`` and ``fields``, ordered by ID. A field has ``id`` (which stays the same when it
    is renamed), ``name``, ``slug``, ``result_type``, ``fixed_values`` (the values of a
    ``TEXT_ENUM``), ``description`` (or ``null``) and ``config`` (``regex`` for a ``TEXT_REGEX``
    and ``disable_hyperlink`` for a ``URL``, and an empty object otherwise).

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        team_id: int | None = None,
        order: RecordTypeOrder | None = None,
        direction: SortDirection | None = None,
        limit: int | None = None,
        after: str | None = None,
    ) -> Response:
        """List record types. ``GET /api/v2/record_types``

        Args:
            team_id: Only the record types that this team can read. A team that does not exist or
                that the key cannot see is a 404.
            order: ``NAME``, ``CREATED_AT`` or ``UPDATED_AT``, in any case. Tines defaults to
                ``NAME``.
            direction: ``ASC`` or ``DESC``, in any case. Tines defaults to ``ASC``.
            limit: The number of record types in a page, from 1 to 500. Tines defaults to 20.
            after: The ``page.next_page_token`` of the previous page.

        Returns:
            A ``Response`` whose ``data`` is an object with ``data``, the record types of the
            page, and ``page``, which has ``next_page_token`` only when there is another page.
        """
        return self._transport.request(
            method="GET",
            path="/api/v2/record_types",
            params=omit_none(
                values={
                    "team_id": team_id,
                    "order": order,
                    "direction": direction,
                    "limit": limit,
                    "after": after,
                }
            ),
        )

    def get(self, *, record_type_id: int) -> Response:
        """Get a record type. ``GET /api/v2/record_types/{record_type_id}``

        Args:
            record_type_id: The ID of the record type.

        Returns:
            A ``Response`` whose ``data`` is an object with ``data``, the record type. The reply
            is a 404 for a record type that does not exist.
        """
        return self._transport.request(method="GET", path=f"/api/v2/record_types/{record_type_id}")

    def create(
        self,
        *,
        name: str,
        team_id: int,
        fields: Sequence[RecordTypeField],
        description: str | None = None,
        editable: bool | None = None,
        ttl_days: float | None = None,
        retention_column_name: RetentionColumn | None = None,
        on_limit_reached: OnLimitReached | None = None,
        custom_records_limit: int | None = None,
    ) -> Response:
        """Create a record type. ``POST /api/v2/record_types``

        Args:
            name: The name of the record type.
            team_id: The ID of the team that owns it.
            fields: The custom fields, at most 50, each with a ``name`` and a ``result_type``
                (``TEXT``, ``TEXT_ENUM``, ``TEXT_REGEX``, ``EMAIL``, ``URL``, ``IP_ADDRESS``,
                ``NUMBER``, ``BOOLEAN``, ``TIMESTAMP``, ``JSON`` or ``ARTIFACT``), and optionally
                a ``description`` and a ``config``. A ``TEXT_ENUM`` needs ``fixed_values``, at
                most 100, and no other type takes them. A ``TEXT_REGEX`` needs ``config`` with a
                ``regex``, which cannot be changed later. A ``URL`` takes ``config`` with
                ``disable_hyperlink`` to show its values as plain text. See
                ``tapi.records.RecordTypeField``.
            description: A description.
            editable: Whether the records of the type can be edited. Tines defaults to ``False``.
            ttl_days: How long Tines keeps a record, in days: one of 0.25, 0.5, 1, 2, 3, 7, 14,
                30, 60, 90, 180, 365, 548, 730, 1095, 1460, 1825, 2190, 2555, 2920, 3285 or 3650.
                Without it records are kept for ever.
            retention_column_name: The timestamp that ``ttl_days`` counts from: ``CREATED_AT``,
                the default, or ``UPDATED_AT``.
            on_limit_reached: What Tines does when the limit of records is reached: ``REJECT``,
                the default, or ``EVICT_OLDEST``.
            custom_records_limit: The most records the type can hold, a positive integer that is
                at most the limit of the tenant. Without it the limit of the tenant applies.

        Returns:
            A ``Response`` with a 201 status whose ``data`` is an object with ``data``, the
            record type. The reply is a 400 for a request that is not valid, a 404 for a team that
            does not exist, a 403 without permission to create record types in the team, and a
            422 when the record type cannot be created.
        """
        return self._transport.request(
            method="POST",
            path="/api/v2/record_types",
            json=omit_none(
                values={
                    "name": name,
                    "team_id": team_id,
                    "fields": to_list(values=fields),
                    "description": description,
                    "editable": editable,
                    "ttl_days": ttl_days,
                    "retention_column_name": retention_column_name,
                    "on_limit_reached": on_limit_reached,
                    "custom_records_limit": custom_records_limit,
                }
            ),
        )

    def update(
        self,
        *,
        record_type_id: int,
        name: str | None = None,
        description: str | None = None,
        editable: bool | None = None,
        ttl_days: float | None = None,
        retention_column_name: RetentionColumn | None = None,
        on_limit_reached: OnLimitReached | None = None,
        custom_records_limit: int | None = None,
        fields: Sequence[RecordTypeFieldChange] | None = None,
        field_ids_to_delete: Sequence[int] | None = None,
    ) -> Response:
        """Update a record type. ``PATCH /api/v2/record_types/{record_type_id}``

        What is left out stays as it is, and the request must change something, or it is a 400.
        Tines clears the description, turns retention off and drops the custom limit for a
        ``null``, which tapi cannot send.

        Args:
            record_type_id: The ID of the record type.
            name: The new name.
            description: The new description.
            editable: Whether the records of the type can be edited.
            ttl_days: How long Tines keeps a record, in days, one of the values listed for
                ``create``.
            retention_column_name: ``CREATED_AT`` or ``UPDATED_AT``.
            on_limit_reached: ``REJECT`` or ``EVICT_OLDEST``.
            custom_records_limit: The most records the type can hold.
            fields: The fields to add and to change. A field with an ``id`` is changed, and one
                without is added, with a ``name`` and a ``result_type``. The fields that are not
                listed stay. A field can appear once, and not in ``field_ids_to_delete``. A
                ``config`` replaces the old one. See ``tapi.records.RecordTypeFieldChange``.
            field_ids_to_delete: The IDs of the fields to delete. The built-in fields cannot be
                deleted.

        Returns:
            A ``Response`` whose ``data`` is an object with ``data``, the record type. The reply
            is a 404 for a record type that does not exist, a 400 for a request that changes
            nothing or is not valid, a 403 without permission and a 422 when it cannot be
            updated.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v2/record_types/{record_type_id}",
            json=omit_none(
                values={
                    "name": name,
                    "description": description,
                    "editable": editable,
                    "ttl_days": ttl_days,
                    "retention_column_name": retention_column_name,
                    "on_limit_reached": on_limit_reached,
                    "custom_records_limit": custom_records_limit,
                    "fields": to_list(values=fields),
                    "field_ids_to_delete": to_list(values=field_ids_to_delete),
                }
            ),
        )

    def delete(self, *, record_type_id: int) -> Response:
        """Delete a record type. ``DELETE /api/v2/record_types/{record_type_id}``

        This also deletes all the records of the type, their artifacts and the record views built
        on it, and it cannot be undone.

        Args:
            record_type_id: The ID of the record type.

        Returns:
            A ``Response`` with a 204 status and no data. The reply is a 404 for a record type
            that does not exist, and a 403 without permission to delete it.
        """
        return self._transport.request(
            method="DELETE", path=f"/api/v2/record_types/{record_type_id}"
        )
