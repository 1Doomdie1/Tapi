from collections.abc import Mapping

from tapi.core import Response, Transport
from tapi.core.params import omit_none


class Skills:
    """Skills of AI agents, available as ``tines.skills``.

    A skill is a set of instructions that AI agents can load. Agents are shown only the ``name``
    and the ``description`` of a skill and match a task against them to decide whether to load it.
    The ``body`` is loaded only after that. A skill belongs to a team, and its name is unique
    within the team, so a skill is found by its name and the ID of its team.

    A skill, as listed by ``list`` and returned by the other methods, has ``name``,
    ``description``, ``body``, ``license`` and ``compatibility`` (both ``null`` when not set),
    ``metadata`` (a flat object of strings, empty when none is set), ``team_id``, ``created_at``
    and ``updated_at``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        team_id: int | None = None,
        search: str | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List skills. ``GET /api/v1/skills``

        Lists the skills that the API key has access to.

        Args:
            team_id: Only skills owned by this team.
            search: Only skills whose name contains this text, in any case.
            per_page: The number of results per page.
            page: The page to return, starting at 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``skills``, the skills of the page, and
            ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/skills",
            params=omit_none(
                values={
                    "team_id": team_id,
                    "search": search,
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )

    def get(self, *, skill_name: str, team_id: int) -> Response:
        """Get a skill. ``GET /api/v1/skills/{skill_name}``

        Args:
            skill_name: The name of the skill. Names are unique only within a team.
            team_id: The ID of the team that owns the skill.

        Returns:
            A ``Response`` whose ``data`` is the skill. The reply is a 404 with ``Skill not
            found`` for a name that no skill has in the team, or a team that does not exist, and
            a 400 when ``team_id`` is missing.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/skills/{skill_name}",
            params={"team_id": team_id},
        )

    def create(
        self,
        *,
        team_id: int,
        name: str,
        description: str,
        body: str,
        license: str | None = None,
        compatibility: str | None = None,
        metadata: Mapping[str, str] | None = None,
    ) -> Response:
        """Create a skill. ``POST /api/v1/skills``

        Args:
            team_id: The ID of the team that gets the skill.
            name: The name of the skill: lowercase letters and digits with hyphens, such as
                ``triage-alerts``, at most 64 characters, with no double hyphen and no hyphen at the
                end. It is unique within the team.
            description: What the skill does and when to use it. AI agents match a task against it
                to decide whether to load the skill. It cannot be empty.
            body: The full instructions of the skill, as Markdown. Agents load it only after the
                description matches the task. It cannot be empty.
            license: The license that the skill is distributed under, such as ``Apache-2.0``.
            compatibility: A free-text note on what the skill is compatible with.
            metadata: A flat object of string keys and string values.

        Returns:
            A ``Response`` whose ``data`` is the created skill, with a 201 status. A skill that was
            created without a ``license`` or ``compatibility`` has ``null`` for them.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/skills",
            json=omit_none(
                values={
                    "team_id": team_id,
                    "name": name,
                    "description": description,
                    "body": body,
                    "license": license,
                    "compatibility": compatibility,
                    "metadata": metadata,
                }
            ),
        )

    def update(
        self,
        *,
        skill_name: str,
        team_id: int,
        name: str | None = None,
        description: str | None = None,
        body: str | None = None,
        license: str | None = None,
        compatibility: str | None = None,
        metadata: Mapping[str, str] | None = None,
    ) -> Response:
        """Change a skill. ``PATCH /api/v1/skills/{skill_name}``

        Only what is sent changes, and what is left out keeps its value. The skill has to exist: use
        ``create`` to add one.

        Args:
            skill_name: The current name of the skill.
            team_id: The ID of the team that owns the skill. It is sent in the body.
            name: A new name. Tines also rewrites the name in every AI action that references the
                skill.
            description: A new description.
            body: New instructions, as Markdown.
            license: A new license. An empty string is accepted and stored as it is, not as
                ``null``.
            compatibility: A new compatibility note.
            metadata: New metadata, which replaces the whole object, so include every key that
                should stay. An empty object clears it.

        Returns:
            A ``Response`` whose ``data`` is the updated skill, with ``updated_at`` moved and
            ``created_at`` kept.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v1/skills/{skill_name}",
            json=omit_none(
                values={
                    "team_id": team_id,
                    "name": name,
                    "description": description,
                    "body": body,
                    "license": license,
                    "compatibility": compatibility,
                    "metadata": metadata,
                }
            ),
        )

    def delete(self, *, skill_name: str, team_id: int) -> Response:
        """Delete a skill. ``DELETE /api/v1/skills/{skill_name}``

        Args:
            skill_name: The name of the skill.
            team_id: The ID of the team that owns the skill.

        Returns:
            A ``Response`` with a 204 status and no data. The reply is a 404 with ``Skill not
            found`` for a name that no skill has in the team, which includes a skill that was
            deleted, and a 400 when ``team_id`` is missing.
        """
        return self._transport.request(
            method="DELETE",
            path=f"/api/v1/skills/{skill_name}",
            params={"team_id": team_id},
        )
