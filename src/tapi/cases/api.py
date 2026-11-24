from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any

from tapi.cases.actions import Actions
from tapi.cases.activities import Activities
from tapi.cases.assignees import Assignees
from tapi.cases.blocks import Blocks
from tapi.cases.comments import Comments
from tapi.cases.field_values import FieldValues
from tapi.cases.fields import Fields
from tapi.cases.files import Files
from tapi.cases.linked_cases import LinkedCases
from tapi.cases.metadata import Metadata
from tapi.cases.notes import Notes
from tapi.cases.records import Records
from tapi.cases.statuses import Statuses
from tapi.cases.subscribers import Subscribers
from tapi.cases.tasks import Tasks
from tapi.cases.templates import Templates
from tapi.cases.types import (
    BulkFieldUpdate,
    CaseBlock,
    CaseFilters,
    CaseOrder,
    CasePriority,
    CaseStatus,
    CaseTask,
    ClosureCondition,
    SearchNode,
    SearchPage,
    SearchSort,
)
from tapi.cases.webhooks import Webhooks
from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_iso, to_list

DATE_FILTERS = frozenset(
    {
        "start_date",
        "end_date",
        "opened_at_start_date",
        "opened_at_end_date",
        "resolved_at_start_date",
        "resolved_at_end_date",
        "updated_at_start_date",
        "updated_at_end_date",
    }
)


def _filters_body(*, filters: Mapping[str, Any]) -> dict[str, Any]:
    body: dict[str, Any] = {}
    for key, value in filters.items():
        if key in DATE_FILTERS:
            body[key] = to_iso(value=value)
        elif isinstance(value, str | bytes | Mapping) or not isinstance(value, Sequence):
            body[key] = value
        else:
            body[key] = list(value)
    return body


class Cases:
    """Cases, available as ``tines.cases``.

    A case that does not exist, or that your key cannot see, is a 404 with ``TeamCase not
    found``.

    Args:
        transport: The transport used to send requests.

    The sub-areas are attributes of the module:

    - ``actions``: The actions of a case.
    - ``activities``: The activity log of a case.
    - ``assignees``: The assignees of a case.
    - ``blocks``: The blocks of a case and their elements.
    - ``comments``: The comments on a case and their reactions.
    - ``field_values``: The values of the fields of a case.
    - ``fields``: The case fields that a team defines.
    - ``files``: The files attached to a case.
    - ``linked_cases``: The cases linked to a case.
    - ``metadata``: The key-value metadata of a case.
    - ``notes``: The notes of a case.
    - ``records``: The records attached to a case.
    - ``statuses``: The case statuses of a team.
    - ``subscribers``: The users subscribed to a case.
    - ``tasks``: The tasks of a case.
    - ``templates``: The case templates of a team.
    - ``webhooks``: The case webhooks of a team.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport
        self.actions = Actions(transport=transport)
        self.activities = Activities(transport=transport)
        self.assignees = Assignees(transport=transport)
        self.blocks = Blocks(transport=transport)
        self.comments = Comments(transport=transport)
        self.field_values = FieldValues(transport=transport)
        self.fields = Fields(transport=transport)
        self.files = Files(transport=transport)
        self.linked_cases = LinkedCases(transport=transport)
        self.metadata = Metadata(transport=transport)
        self.notes = Notes(transport=transport)
        self.records = Records(transport=transport)
        self.statuses = Statuses(transport=transport)
        self.subscribers = Subscribers(transport=transport)
        self.tasks = Tasks(transport=transport)
        self.templates = Templates(transport=transport)
        self.webhooks = Webhooks(transport=transport)

    def list(
        self,
        *,
        team_id: int | None = None,
        filters: CaseFilters | None = None,
        order: CaseOrder | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List cases. ``GET /api/v2/cases``

        The endpoint is paginated and one call returns one page. Tines recommends ``search`` for
        new integrations.

        Args:
            team_id: Only cases of this team.
            filters: The filters to apply, an object with any of the keys of
                ``tapi.cases.CaseFilters``. They are sent as a JSON body, as the Tines docs show,
                and the server reads them in the query too. A single value is accepted in place
                of a list of one. Dates take a ``datetime`` or an ISO 8601 string. An unknown key
                is a 400 with ``Unsupported filter parameters``, and ``status`` takes one value,
                ``OPEN`` or ``CLOSED``, not a list.
            order: The order of the results: ``RECENTLY_EDITED``, ``LEAST_RECENTLY_EDITED``,
                ``PRIORITY_ASC``, ``PRIORITY_DESC``, ``OPENED_ASC``, ``OPENED_DESC``,
                ``CREATED_ASC`` or ``CREATED_DESC``. A value that is none of them was ignored.
            per_page: The number of results per page. Tines defaults to 20 and caps it at 500.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``cases``, the cases of the page, and
            ``meta``, the pagination details. The reply is a 404 with ``Team not found`` for a
            ``team_id`` that does not exist, and a 400 with the message when ``per_page`` is not a
            positive integer or a filter is not valid. A search that takes too long is a 408.
        """
        return self._transport.request(
            method="GET",
            path="/api/v2/cases",
            params=omit_none(
                values={"team_id": team_id, "order": order, "per_page": per_page, "page": page}
            ),
            json=None if filters is None else {"filters": _filters_body(filters=filters)},
        )

    def get(self, *, case_id: int, resolve_mentions: bool | None = None) -> Response:
        """Get a case. ``GET /api/v2/cases/{case_id}``

        Args:
            case_id: The ID of the case.
            resolve_mentions: When true, user mentions are replaced by display names. Tines
                defaults to false.

        Returns:
            A ``Response`` whose ``data`` is the case.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v2/cases/{case_id}",
            params=omit_none(values={"resolve_mentions": resolve_mentions}),
        )

    def create(
        self,
        *,
        team_id: int,
        name: str,
        template_id: int | str | None = None,
        description: str | None = None,
        priority: CasePriority | None = None,
        status: CaseStatus | None = None,
        sub_status_id: int | None = None,
        author_email: str | None = None,
        assignee_emails: Sequence[str] | None = None,
        tag_names: Sequence[str] | None = None,
        opened_at: datetime | str | None = None,
        resolved_at: datetime | str | None = None,
        metadata: Mapping[str, Any] | None = None,
        closure_conditions: Sequence[ClosureCondition] | None = None,
        field_values: Mapping[str, Any] | None = None,
        tasks: Sequence[CaseTask] | None = None,
        blocks: Sequence[CaseBlock] | None = None,
    ) -> Response:
        """Create a case. ``POST /api/v2/cases``

        Args:
            team_id: The ID of the team the case belongs to.
            name: The name of the case.
            template_id: The ID or the slug of a case template. The values of the template fill
                the parameters that are left out.
            description: The description, as Markdown. User mentions are written ``<@user-2435>``.
            priority: The priority: ``CRITICAL``, ``HIGH``, ``MEDIUM``, ``LOW`` or ``INFO``, in
                any case. A new case has the priority ``LOW`` if none is given.
            status: The status: ``OPEN`` or ``CLOSED``, in any case. A new case is ``OPEN`` if
                none is given.
            sub_status_id: The ID of a case status of the team. An ID that does not exist was
                ignored.
            author_email: The email address of the user creating the case.
            assignee_emails: The email addresses of the users to assign. An address that is not a
                user of the tenant was ignored.
            tag_names: The names of the tags to add.
            opened_at: When the case was opened: a ``datetime`` or an ISO 8601 string.
            resolved_at: When the case was resolved: a ``datetime`` or an ISO 8601 string.
            metadata: Key-value pairs to store on the case.
            closure_conditions: The conditions that must be true to close the case, each an
                object with a ``name`` and a ``formula``, such as ``=SIZE(team_case.assignees) >
                0``.
            field_values: The values of the case fields, keyed by the ID of the field. A field
                that allows several values takes them as one string separated by ``|``.
            tasks: Tasks to create with the case, each an object with a ``description`` and
                optionally ``assignee_ids`` and ``assignee_emails``.
            blocks: Blocks to create with the case, each an object with a ``title``, a
                ``block_type`` and its ``elements``. See ``tapi.cases.CaseBlock``.

        Returns:
            A ``Response`` whose ``data`` is the created case, with a 201 status. The reply is a
            422 naming the field when a value is not valid, such as a ``priority`` or ``status``
            that does not exist, an ``opened_at`` that is not a date or a closure condition
            without a ``formula``, and a 404 with ``Team not found`` for a ``team_id`` that does
            not exist.
        """
        return self._transport.request(
            method="POST",
            path="/api/v2/cases",
            json=omit_none(
                values={
                    "team_id": team_id,
                    "name": name,
                    "template_id": template_id,
                    "description": description,
                    "priority": priority,
                    "status": status,
                    "sub_status_id": sub_status_id,
                    "author_email": author_email,
                    "assignee_emails": to_list(values=assignee_emails),
                    "tag_names": to_list(values=tag_names),
                    "opened_at": to_iso(value=opened_at),
                    "resolved_at": to_iso(value=resolved_at),
                    "metadata": metadata,
                    "closure_conditions": to_list(values=closure_conditions),
                    "field_values": field_values,
                    "tasks": to_list(values=tasks),
                    "blocks": to_list(values=blocks),
                }
            ),
        )

    def update(
        self,
        *,
        case_id: int,
        name: str | None = None,
        team_id: int | None = None,
        description: str | None = None,
        priority: CasePriority | None = None,
        status: CaseStatus | None = None,
        sub_status_id: int | None = None,
        author_email: str | None = None,
        assignee_emails: Sequence[str] | None = None,
        add_assignee_emails: Sequence[str] | None = None,
        remove_assignee_emails: Sequence[str] | None = None,
        add_tag_names: Sequence[str] | None = None,
        remove_tag_names: Sequence[str] | None = None,
        opened_at: datetime | str | None = None,
        resolved_at: datetime | str | None = None,
        closure_conditions: Sequence[ClosureCondition] | None = None,
    ) -> Response:
        """Update a case. ``PATCH /api/v2/cases/{case_id}``

        The Tines documentation shows this operation as ``PUT``. The OpenAPI document lists the
        same operation under ``PUT`` and ``PATCH``, and tapi uses ``PATCH``.

        Args:
            case_id: The ID of the case.
            name: A new name.
            team_id: The ID of the team to move the case to.
            description: A new description, as Markdown. To add to it, use ``append_description``.
            priority: A new priority: ``CRITICAL``, ``HIGH``, ``MEDIUM``, ``LOW`` or ``INFO``, in
                any case.
            status: A new status: ``OPEN`` or ``CLOSED``, in any case. Closing a case sets
                ``resolved_at`` and ``resolved_by``, and opening it again clears ``resolved_at``.
            sub_status_id: The ID of a case status of the team.
            author_email: The email address of the user making the change.
            assignee_emails: The email addresses of the users to assign. Only the Tines docs list
                it, and it replaces the assignees.
            add_assignee_emails: The email addresses of users to add as assignees. An address that
                is not a user of the tenant was ignored.
            remove_assignee_emails: The email addresses of users to remove as assignees.
            add_tag_names: The names of tags to add.
            remove_tag_names: The names of tags to remove.
            opened_at: When the case was opened: a ``datetime`` or an ISO 8601 string.
            resolved_at: When the case was resolved: a ``datetime`` or an ISO 8601 string.
            closure_conditions: The conditions that must be true to close the case, each an
                object with a ``name`` and a ``formula``.

        Returns:
            A ``Response`` whose ``data`` is the updated case. A call that sends nothing is a
            200. The reply is a 422 naming the field when a value is not valid, such as a
            ``priority`` that does not exist, and a 422 with ``Cannot close case as all case
            requirements have not been met`` when ``status`` is ``CLOSED`` while a closure
            condition is not true.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v2/cases/{case_id}",
            json=omit_none(
                values={
                    "name": name,
                    "team_id": team_id,
                    "description": description,
                    "priority": priority,
                    "status": status,
                    "sub_status_id": sub_status_id,
                    "author_email": author_email,
                    "assignee_emails": to_list(values=assignee_emails),
                    "add_assignee_emails": to_list(values=add_assignee_emails),
                    "remove_assignee_emails": to_list(values=remove_assignee_emails),
                    "add_tag_names": to_list(values=add_tag_names),
                    "remove_tag_names": to_list(values=remove_tag_names),
                    "opened_at": to_iso(value=opened_at),
                    "resolved_at": to_iso(value=resolved_at),
                    "closure_conditions": to_list(values=closure_conditions),
                }
            ),
        )

    def delete(self, *, case_id: int) -> Response:
        """Delete a case. ``DELETE /api/v2/cases/{case_id}``

        Args:
            case_id: The ID of the case.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(method="DELETE", path=f"/api/v2/cases/{case_id}")

    def append_description(self, *, case_id: int, description: str) -> Response:
        """Add text to the description of a case. ``POST /api/v2/cases/{case_id}/description``

        Args:
            case_id: The ID of the case.
            description: The text to add, as Markdown.

        Returns:
            A ``Response`` whose ``data`` is the updated case. The reply is a 400 when the
            description is missing or empty.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v2/cases/{case_id}/description",
            json={"description": description},
        )

    def search(
        self,
        *,
        filter: SearchNode | None = None,
        sort: Sequence[SearchSort] | None = None,
        page: SearchPage | None = None,
        include_total: bool | None = None,
        timezone: str | None = None,
    ) -> Response:
        """Search cases. ``POST /api/v3/cases/search``

        This is the endpoint that Tines recommends over ``list``. It is available on Tines Cloud
        only, and the OpenAPI document does not list it. The index is not updated at once: a case
        created or deleted a moment ago may take a few seconds to appear in or leave the results,
        and ``list`` shows the change immediately.

        Args:
            filter: What to match. A condition is an object with a ``field`` (see
                ``tapi.cases.types.SearchField``), an ``operator`` (see
                ``tapi.cases.types.SearchOperator``) and, depending on the operator, a ``value``
                and a ``key``. A group is ``{"op": "AND", "nodes": [...]}``, with ``OR`` and
                ``NOT`` too (``NOT`` takes one node, and a group needs at least one). A nested
                filter on the comments, notes, records or tasks of a case is ``{"op": "NESTED",
                "path": "task", "filter": {"field": "text", ...}}``, and inside it the fields
                have no ``task.`` prefix: a task has ``text``, ``completed`` and ``assignee``.
                Left out, every case you can see matches. Operators are not case-sensitive, and
                neither are the values of ``status`` and ``priority``. Each field supports only
                some of the operators, and the 400 for a field that does not support one lists
                those it does.
            sort: Up to three objects with a ``field`` (``created_at``, ``name``, ``opened_at``,
                ``priority``, ``resolved_at`` or ``updated_at``) and a ``direction`` (``ASC`` or
                ``DESC``, in any case), in order of importance. A fourth key is a 400. Cases are
                sorted by ID if none is given.
            page: An object with a ``size`` (1 to 50, 20 by default) and a ``token``, the
                ``next_page_token`` of the previous reply. The filter and the sort must be the
                same.
            include_total: When true, the reply holds the number of cases that match.
            timezone: An IANA time zone name such as ``Europe/Dublin``, used by relative dates
                and times of day. Tines defaults to UTC.

        Returns:
            A ``Response`` whose ``data`` is an object with ``cases``, the cases of the page,
            ``total`` when ``include_total`` is true, and ``next_page_token`` when there are more
            pages. The reply is a 400 whose ``data`` is ``{"error": {"type", "message", "field",
            "hint"}}`` for an invalid request, such as an unknown field, an operator the field
            does not support or a time zone that does not exist, and a 403 when your tenant has
            no access to Cases.
        """
        return self._transport.request(
            method="POST",
            path="/api/v3/cases/search",
            json=omit_none(
                values={
                    "filter": filter,
                    "sort": to_list(values=sort),
                    "page": page,
                    "include_total": include_total,
                    "timezone": timezone,
                }
            ),
        )

    def bulk_update_fields(
        self,
        *,
        case_ids: Sequence[int],
        fields: Sequence[BulkFieldUpdate],
    ) -> Response:
        """Set field values on several cases. ``POST /api/v2/cases/bulk/fields``

        Args:
            case_ids: The IDs of the cases to update.
            fields: The values to set, each an object with the ``input_id`` of the field, the
                ``value`` and, optionally, ``upsert``. By default only the cases that already
                have the field are updated, and ``upsert`` set to true adds the field to the
                others. A field that allows several values takes them as one string separated by
                ``|``. The OpenAPI document shows an object with ``case_id`` in each item, and
                the Tines docs show ``case_ids`` apart, which tapi follows.

        Returns:
            A ``Response`` whose ``data`` is an object with ``cases``, a list with the ``case_id``
            and the ``fields`` of each updated case. The reply is a 400 when ``case_ids`` or
            ``fields`` is missing or empty, and a 404 with ``TeamCaseInput not found`` for a field
            that does not exist or ``One or more cases not found``.
        """
        return self._transport.request(
            method="POST",
            path="/api/v2/cases/bulk/fields",
            json={"case_ids": to_list(values=case_ids), "fields": to_list(values=fields)},
        )

    def get_pdf(self, *, case_id: int) -> Response:
        """Export a case as a PDF. ``GET /api/v2/cases/{case_id}/pdf``

        Args:
            case_id: The ID of the case.

        Returns:
            A ``Response`` whose ``data`` is the PDF, as ``bytes``, with the content type
            ``application/pdf``. The Tines docs show a JSON object with the file Base64 encoded,
            which is what Tines returns to an HTTP action, not what the API returns.
        """
        return self._transport.request(method="GET", path=f"/api/v2/cases/{case_id}/pdf")
