from collections.abc import Sequence
from typing import Any

from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_iso, to_list
from tapi.records.artifacts import Artifacts
from tapi.records.fields import Fields
from tapi.records.record_types import RecordTypes
from tapi.records.record_views import RecordViews
from tapi.records.types import (
    FieldValue,
    RecordAggregation,
    RecordFilterNode,
    RecordGroupBy,
    RecordInclude,
    RecordOrderBy,
    RecordSearchInclude,
    RecordSort,
    RecordTimeRange,
)


def _joined(*, values: Sequence[str] | None) -> str | None:
    items = to_list(values=values)
    return ",".join(items) if items else None


def _time_range_body(*, windows: Sequence[RecordTimeRange] | None) -> list[dict[str, Any]] | None:
    items = to_list(values=windows)
    if items is None:
        return None
    body: list[dict[str, Any]] = []
    for window in items:
        entry: dict[str, Any] = dict(window)
        if "range_start" in window:
            entry["range_start"] = to_iso(value=window["range_start"])
        if "range_end" in window:
            entry["range_end"] = to_iso(value=window["range_end"])
        body.append(entry)
    return body


class Records:
    """Records, available as ``tines.records``.

    A record is one row of a record type. The lists page with a cursor: ``limit`` and ``after``,
    the ``page.next_page_token`` of the previous reply.

    Args:
        transport: The transport used to send requests.

    The sub-areas are attributes of the module:

    - ``artifacts``: The artifacts of a record.
    - ``fields``: The large fields of a record.
    - ``record_types``: The record types.
    - ``record_views``: The record views.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport
        self.artifacts = Artifacts(transport=transport)
        self.fields = Fields(transport=transport)
        self.record_types = RecordTypes(transport=transport)
        self.record_views = RecordViews(transport=transport)

    def create(
        self,
        *,
        record_type_id: int | None = None,
        record_type_name: str | None = None,
        field_values: Sequence[FieldValue] | None = None,
        parent_id: int | None = None,
        test_mode: bool | None = None,
        idempotency_key: str | None = None,
    ) -> Response:
        """Create a record. ``POST /api/v2/records``

        Args:
            record_type_id: The ID of the record type. Send this or ``record_type_name``. When both
                are sent, the ID wins.
            record_type_name: The name or the slug of the record type. A name that matches more than
                one type is a 400.
            field_values: The values of the fields, each an object with ``value`` and either
                ``field_id`` or ``field_name``, never both. See ``tapi.records.FieldValue``. A field
                can appear once. A ``value`` of ``None`` clears the field. Scalar fields take a
                string, a number, a boolean or an ISO 8601 string for a timestamp, JSON fields take
                an object or an array, and artifact fields take a text.
            parent_id: The ID of the parent record. Leave it out for a top-level record.
            test_mode: ``True`` to create a test record, which needs change control.
            idempotency_key: A key of at most 255 characters that makes the create safe to retry,
                sent in the ``Idempotency-Key`` header. The same key with the same body replays the
                first reply. The same key with another body is a 422, a retry while the first
                request is running is a 409 and a replay after the record was deleted is a 410. Keys
                expire after 24 hours.

        Returns:
            A ``Response`` with a 201 status whose ``data`` is an object with ``data``, the record,
            and ``field_ids``.
        """
        return self._transport.request(
            method="POST",
            path="/api/v2/records",
            json=omit_none(
                values={
                    "record_type_id": record_type_id,
                    "record_type_name": record_type_name,
                    "field_values": to_list(values=field_values),
                    "parent_id": parent_id,
                    "test_mode": test_mode,
                }
            ),
            headers={"Idempotency-Key": idempotency_key} if idempotency_key is not None else None,
        )

    def get(
        self,
        *,
        record_id: int,
        record_type_id: int | None = None,
        include: Sequence[RecordInclude] | None = None,
        expand: Sequence[str] | None = None,
        fields: Sequence[str] | None = None,
        timezone: str | None = None,
    ) -> Response:
        """Get a record. ``GET /api/v2/records/{record_id}``

        Args:
            record_id: The ID of the record.
            record_type_id: Only a record of this type: a record of another type is a 404.
            include: What to embed, any of ``record_type``, ``parent_record``, ``child_records``,
                ``child_record_ids`` and ``cases``. They are sent as one comma-separated value.
                ``record_type``, ``child_records`` and ``cases`` add bodies under ``included``,
                ``child_record_ids`` adds the IDs of every direct child under ``relationships``, and
                ``parent_record`` changes nothing, because the reference is always there. The
                to-many embeds hold at most 20 items and say when they were cut short.
            expand: The JSON and artifact fields to inline, such as ``fields.payload``, or
                ``fields.*`` for all of them. They are sent as one comma-separated value.
            fields: The slugs of the fields to return, instead of all of them. They are sent as one
                comma-separated ``fields[record]``.
            timezone: An IANA timezone name for the timestamps.

        Returns:
            A ``Response`` whose ``data`` is an object with ``data``, the record, ``field_ids`` and,
            with ``include``, ``included``.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v2/records/{record_id}",
            params=omit_none(
                values={
                    "record_type_id": record_type_id,
                    "include": _joined(values=include),
                    "expand": _joined(values=expand),
                    "fields[record]": _joined(values=fields),
                    "timezone": timezone,
                }
            ),
        )

    def update(
        self,
        *,
        record_id: int,
        field_values: Sequence[FieldValue] | None = None,
        parent_id: int | None = None,
        test_mode: bool | None = None,
    ) -> Response:
        """Update a record. ``PATCH /api/v2/records/{record_id}``

        The fields that are left out keep their value.

        Args:
            record_id: The ID of the record.
            field_values: The values to set, each an object with ``value`` and either ``field_id``
                or ``field_name``. See ``tapi.records.FieldValue``. A ``value`` of ``None`` clears
                the field. An empty list is accepted only with ``parent_id``.
            parent_id: The ID of the new parent record.
            test_mode: A guard: ``True`` requires a test record and ``False`` a live record, and a
                record of the other mode is a 422. Leave it out to update either.

        Returns:
            A ``Response`` whose ``data`` is an object with ``data``, the updated record, and
            ``field_ids``.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v2/records/{record_id}",
            json=omit_none(
                values={
                    "field_values": to_list(values=field_values),
                    "parent_id": parent_id,
                    "test_mode": test_mode,
                }
            ),
        )

    def delete(self, *, record_id: int, test_mode: bool | None = None) -> Response:
        """Delete a record. ``DELETE /api/v2/records/{record_id}``

        Args:
            record_id: The ID of the record.
            test_mode: A guard: ``True`` requires a test record and ``False`` a live record, and
                a record of the other mode is a 422. Leave it out to delete either.

        Returns:
            A ``Response`` with a 204 status and no data. The reply is a 404 for a record that
            does not exist, and a 403 without permission to delete it.
        """
        return self._transport.request(
            method="DELETE",
            path=f"/api/v2/records/{record_id}",
            params=omit_none(values={"test_mode": test_mode}),
        )

    def search(
        self,
        *,
        record_type_id: int | None = None,
        record_type_name: str | None = None,
        filter: RecordFilterNode | None = None,
        sort: Sequence[RecordSort] | None = None,
        fields: Sequence[str] | None = None,
        include: Sequence[RecordSearchInclude] | None = None,
        ids: Sequence[int] | None = None,
        time_range: Sequence[RecordTimeRange] | None = None,
        timezone: str | None = None,
        limit: int | None = None,
        after: str | None = None,
        include_total: bool | None = None,
        test_mode: bool | None = None,
    ) -> Response:
        """Search records. ``POST /api/v2/records/search``

        Reads records, although it is a ``POST``.

        Args:
            record_type_id: The ID of the record type. Send this or ``record_type_name``.
            record_type_name: The name or the slug of the record type.
            filter: A condition ``{"field_name": ..., "operator": ..., "value": ...}`` or a group
                ``{"op": "AND", "nodes": [...]}``, up to 4 levels and 50 nodes. See
                ``tapi.records.RecordFilterNode``.
            sort: Keys in priority order, each with ``field_id`` or ``field_name`` and a
                ``direction`` (``ASC`` or ``DESC``). Without it the newest records come first.
            fields: The slugs of the fields to return.
            include: ``record_type``, to add the type under ``included``.
            ids: At most 500 record IDs. Not with ``after``.
            time_range: At most two windows, one for each ``field`` (``created_at`` or
                ``updated_at``), each with a ``rolling_date_range`` or a ``range_start`` and
                ``range_end``. See ``tapi.records.RecordTimeRange``.
            timezone: An IANA timezone name for the presets and the timestamps.
            limit: The number of records in a page, from 1 to 500.
            after: The ``page.next_page_token`` of the previous page.
            include_total: ``True`` adds ``page.total``.
            test_mode: ``True`` searches test records, which needs change control.

        Returns:
            A ``Response`` whose ``data`` has ``data`` (the records), ``field_ids``, ``page`` and
            ``applied``, and ``included`` with ``include``.
        """
        return self._transport.request(
            method="POST",
            path="/api/v2/records/search",
            json=omit_none(
                values={
                    "record_type_id": record_type_id,
                    "record_type_name": record_type_name,
                    "filter": filter,
                    "sort": to_list(values=sort),
                    "fields": {"record": to_list(values=fields)} if fields else None,
                    "include": to_list(values=include),
                    "ids": to_list(values=ids),
                    "time_range": _time_range_body(windows=time_range),
                    "timezone": timezone,
                    "limit": limit,
                    "after": after,
                    "include_total": include_total,
                    "test_mode": test_mode,
                }
            ),
        )

    def aggregate(
        self,
        *,
        aggregations: Sequence[RecordAggregation],
        record_type_id: int | None = None,
        record_type_name: str | None = None,
        group_by: Sequence[RecordGroupBy] | None = None,
        filter: RecordFilterNode | None = None,
        time_range: Sequence[RecordTimeRange] | None = None,
        order_by: Sequence[RecordOrderBy] | None = None,
        parent_ids: Sequence[int] | None = None,
        timezone: str | None = None,
        limit: int | None = None,
    ) -> Response:
        """Aggregate records. ``POST /api/v2/records/aggregate``

        Reads records, although it is a ``POST``. It does not page.

        Args:
            aggregations: One to five values, each with an ``fn`` (``COUNT``, ``SUM``, ``AVG``,
                ``MIN``, ``MAX``, ``MEDIAN``, ``P90``, ``P95`` or ``P99``), a ``field_id`` or
                ``field_name`` (not for ``COUNT``) and an ``alias``. See
                ``tapi.records.RecordAggregation``.
            record_type_id: The ID of the record type. Send this or ``record_type_name``.
            record_type_name: The name or the slug of the record type.
            group_by: Up to two fields, each with ``field_id`` or ``field_name`` and, for a
                timestamp, a ``date_trunc`` (``hour``, ``day``, ``week``, ``month`` or ``year``).
                See ``tapi.records.RecordGroupBy``.
            filter: A condition or a group, as for ``search``.
            time_range: At most two windows, as for ``search``.
            order_by: At most one key, a group-by field or an ``alias``, with a ``direction``. See
                ``tapi.records.RecordOrderBy``.
            parent_ids: At most 100 record IDs: only their direct children are counted.
            timezone: An IANA timezone name for the buckets and the time ranges.
            limit: The number of rows, from 1 to 500. Without it Tines returns up to 1000.

        Returns:
            A ``Response`` whose ``data`` has ``rows`` and ``meta`` (``row_count``, ``truncated``
            and ``columns``).
        """
        return self._transport.request(
            method="POST",
            path="/api/v2/records/aggregate",
            json=omit_none(
                values={
                    "aggregations": to_list(values=aggregations),
                    "record_type_id": record_type_id,
                    "record_type_name": record_type_name,
                    "group_by": to_list(values=group_by),
                    "filter": filter,
                    "time_range": _time_range_body(windows=time_range),
                    "order_by": to_list(values=order_by),
                    "parent_ids": to_list(values=parent_ids),
                    "timezone": timezone,
                    "limit": limit,
                }
            ),
        )

    def list_cases(
        self,
        *,
        record_id: int,
        timezone: str | None = None,
        limit: int | None = None,
        after: str | None = None,
    ) -> Response:
        """List the cases of a record. ``GET /api/v2/records/{record_id}/cases``

        The cases come oldest first, by case ID.

        Args:
            record_id: The ID of the record.
            timezone: An IANA timezone name for the timestamps.
            limit: The number of cases in a page, from 1 to 500.
            after: The ``page.next_page_token`` of the previous page.

        Returns:
            A ``Response`` whose ``data`` is an object with ``data``, the cases, each with ``id``
            (the case number), ``name``, ``status``, ``priority``, ``linked_at``, ``created_at`` and
            ``updated_at``, and ``page``.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v2/records/{record_id}/cases",
            params=omit_none(values={"timezone": timezone, "limit": limit, "after": after}),
        )

    def link_case(self, *, record_id: int, case_id: int) -> Response:
        """Link a case to a record. ``POST /api/v2/records/{record_id}/cases``

        Linking a case that is linked already is not an error.

        Args:
            record_id: The ID of the record.
            case_id: The number of the case, a positive integer.

        Returns:
            A ``Response`` with a 204 status and no data. The reply is a 404 for a record or a
            case that does not exist, and a 422 when the case cannot be linked, for example
            without permission to manage records.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v2/records/{record_id}/cases",
            json={"case_id": case_id},
        )

    def unlink_case(self, *, record_id: int, case_id: int) -> Response:
        """Unlink a case from a record. ``DELETE /api/v2/records/{record_id}/cases/{case_id}``

        Neither the record nor the case is deleted. Unlinking a case that is not linked is not an
        error.

        Args:
            record_id: The ID of the record.
            case_id: The number of the case.

        Returns:
            A ``Response`` with a 204 status and no data. The reply is a 404 for a record or a
            case that does not exist.
        """
        return self._transport.request(
            method="DELETE", path=f"/api/v2/records/{record_id}/cases/{case_id}"
        )

    def list_child_record_ids(
        self, *, record_id: int, limit: int | None = None, after: str | None = None
    ) -> Response:
        """List the child record IDs. ``GET /api/v2/records/{record_id}/child_record_ids``

        The IDs of every direct child come newest first, also of children that the caller cannot
        read.

        Args:
            record_id: The ID of the parent record.
            limit: The number of IDs in a page, from 1 to 500. Tines defaults to 20.
            after: The ``page.next_page_token`` of the previous page.

        Returns:
            A ``Response`` whose ``data`` is an object with ``data``, a list of integers, and
            ``page``. The reply is a 404 for a record that does not exist.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v2/records/{record_id}/child_record_ids",
            params=omit_none(values={"limit": limit, "after": after}),
        )

    def list_child_records(
        self,
        *,
        record_id: int,
        timezone: str | None = None,
        limit: int | None = None,
        after: str | None = None,
    ) -> Response:
        """List the child records. ``GET /api/v2/records/{record_id}/child_records``

        The children come newest first. Children in a record type that the caller cannot access
        are left out: ``list_child_record_ids`` lists all of them.

        Args:
            record_id: The ID of the parent record.
            timezone: An IANA timezone name for the timestamps. Tines defaults to ``UTC``.
            limit: The number of records in a page, from 1 to 500. Tines defaults to 20.
            after: The ``page.next_page_token`` of the previous page.

        Returns:
            A ``Response`` whose ``data`` is an object with ``data``, the child records, and
            ``page``. The reply is a 404 for a record that does not exist.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v2/records/{record_id}/child_records",
            params=omit_none(values={"timezone": timezone, "limit": limit, "after": after}),
        )
