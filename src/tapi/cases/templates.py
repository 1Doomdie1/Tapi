from collections.abc import Mapping
from typing import Any

from tapi.cases.types import TemplateOptions
from tapi.core import Response, Transport
from tapi.core.params import omit_none


class Templates:
    """The case templates of a team, available as ``tines.cases.templates``.

    A template fills in the values of a case when a case is created from it, with
    ``template_id`` of ``tines.cases.create``. A template, as returned by ``get``, ``create`` and
    ``update`` and listed by ``list``, has ``id``, ``name``, ``emoji``, ``team``, ``created_at``
    and ``updated_at``. Its options are not part of that reply: read them with ``export``, which
    names some of them differently from ``create`` (``case_name``, ``case_description`` and
    ``team_case_tasks`` for ``name``, ``description`` and ``tasks``).

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        team_id: int,
        search: str | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List the case templates of a team. ``GET /api/v1/case_templates``

        Args:
            team_id: The ID of the team.
            search: Only templates whose name matches this text.
            per_page: The number of results per page.
            page: The page to return, starting at 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_templates``, the templates of the
            page, and ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/case_templates",
            params=omit_none(
                values={
                    "team_id": team_id,
                    "search": search,
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )

    def get(self, *, template_id: int) -> Response:
        """Get a case template. ``GET /api/v1/case_templates/{template_id}``

        Args:
            template_id: The ID of the template.

        Returns:
            A ``Response`` whose ``data`` is the template. The reply is a 404 with ``Case template
            not found`` for a template that does not exist.
        """
        return self._transport.request(method="GET", path=f"/api/v1/case_templates/{template_id}")

    def create(
        self,
        *,
        team_id: int,
        name: str,
        emoji: str | None = None,
        options: TemplateOptions | None = None,
    ) -> Response:
        """Create a case template. ``POST /api/v1/case_templates``

        Args:
            team_id: The ID of the team that gets the template.
            name: The name of the template. It is unique within the team.
            emoji: The emoji of the template, as a shortcode such as ``:mag:``.
            options: What a case created from the template gets, an object with any of the keys of
                ``tapi.cases.TemplateOptions``. A name and a description can hold formulas and field
                mentions, which Tines evaluates when a case is created. ``status`` and ``priority``
                are taken in upper and lower case.

        Returns:
            A ``Response`` whose ``data`` is the created template, with a 201 status.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/case_templates",
            json=omit_none(
                values={"team_id": team_id, "name": name, "emoji": emoji, "options": options}
            ),
        )

    def update(
        self,
        *,
        template_id: int,
        name: str | None = None,
        emoji: str | None = None,
        options: TemplateOptions | None = None,
    ) -> Response:
        """Change a case template. ``PATCH /api/v1/case_templates/{template_id}``

        Args:
            template_id: The ID of the template.
            name: A new name.
            emoji: A new emoji, as a shortcode.
            options: New options. An option that is left out keeps its value, and an option that is
                sent replaces the old value as a whole.

        Returns:
            A ``Response`` whose ``data`` is the updated template. Cases that were created from the
            template before are not changed.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v1/case_templates/{template_id}",
            json=omit_none(values={"name": name, "emoji": emoji, "options": options}),
        )

    def delete(self, *, template_id: int) -> Response:
        """Delete a case template. ``DELETE /api/v1/case_templates/{template_id}``

        Args:
            template_id: The ID of the template.

        Returns:
            A ``Response`` with a 204 status and no data. Cases created from the template are not
            changed.
        """
        return self._transport.request(
            method="DELETE", path=f"/api/v1/case_templates/{template_id}"
        )

    def export(self, *, template_id: int) -> Response:
        """Export a case template. ``GET /api/v1/case_templates/{template_id}/export``

        Args:
            template_id: The ID of the template.

        Returns:
            A ``Response`` whose ``data`` is the template in a form that ``import_`` takes, to
            copy it to another team or tenant: an object with ``schema_version``,
            ``exported_at`` and ``templates``, each with ``name``, ``emoji``, ``options``,
            ``input_values`` and ``field_definitions``. The ``options`` have ``case_name``,
            ``case_description``, ``team_case_tasks``, ``team_case_buttons``, ``sub_status``,
            ``tag_names``, ``assignee_emails``, ``blocks``, ``closure_conditions``, ``metadata``,
            ``priority`` and ``status``, the last two in lower case.
        """
        return self._transport.request(
            method="GET", path=f"/api/v1/case_templates/{template_id}/export"
        )

    def import_(self, *, team_id: int, data: Mapping[str, Any]) -> Response:
        """Import case templates. ``POST /api/v1/case_templates/import``

        Args:
            team_id: The ID of the team that gets the templates.
            data: What ``export`` returned.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_templates``, the templates that
            were created, with a 201 status. Importing what was exported from the same team
            creates a copy under a changed name. The reply is a 422 with ``Missing or invalid
            templates array`` for ``data`` that has no templates array, and an empty array creates
            nothing.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/case_templates/import",
            json={"team_id": team_id, "data": data},
        )

    def preview(self, *, template_id: int) -> Response:
        """Preview a case template. ``GET /api/v1/case_templates/{template_id}/preview``

        Args:
            template_id: The ID of the template.

        Returns:
            A ``Response`` whose ``data`` is the case that the template would create, with
            ``name``, ``description``, ``status``, ``priority``, ``sub_status``, ``assignees``,
            ``tags``, ``fields``, ``actions``, ``blocks``, ``tasks``, ``closure_conditions`` and
            ``metadata``. Formulas and field mentions are not evaluated.
        """
        return self._transport.request(
            method="GET", path=f"/api/v1/case_templates/{template_id}/preview"
        )
