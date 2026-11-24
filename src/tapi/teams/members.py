from tapi.core import Response, Transport
from tapi.core.params import omit_none


class Members:
    """The members of a team, available as ``tines.teams.members``.

    A member, as listed by ``list`` and returned by ``invite``, has ``id`` (the ID of the user),
    ``first_name``, ``last_name``, ``email``, ``is_admin``, ``created_at`` (when the user was
    created, an ISO 8601 timestamp), ``last_seen`` (an ISO 8601 timestamp, or ``null`` if the user
    has not been seen), ``invitation_accepted`` (whether the user accepted the invitation to the
    team) and ``role`` (the role of the user on the team, such as ``TEAM_ADMIN`` or ``VIEWER``).

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        team_id: int,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List the members of a team. ``GET /api/v1/teams/{team_id}/members``

        The endpoint is paginated and one call returns one page.

        Args:
            team_id: The ID of the team.
            per_page: The number of results per page. Tines defaults to 20 and caps it at 500.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``members``, the members of the page,
            and ``meta``, the pagination details. The reply is a 404 with the message
            ``Team not found`` when no team with that ID is visible to your key.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/teams/{team_id}/members",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )

    def invite(
        self,
        *,
        team_id: int,
        email: str | None = None,
        user_id: int | None = None,
        role: str | None = None,
    ) -> Response:
        """Invite a user to a team. ``POST /api/v1/teams/{team_id}/invite_member``

        Give either ``email`` or ``user_id``, but not both. Tines enforces this, and tapi sends
        whatever it is given.

        Args:
            team_id: The ID of the team.
            email: The email address of the user to invite.
            user_id: The ID of an existing user in the tenant.
            role: The role the user gets on the team. Tines accepts default and custom roles, such
                as ``TEAM_ADMIN`` or ``VIEWER``, and does not list the allowed values.

        Returns:
            A ``Response`` whose ``data`` is the invited member.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/teams/{team_id}/invite_member",
            json=omit_none(values={"email": email, "user_id": user_id, "role": role}),
        )

    def resend_invitation(self, *, team_id: int, user_id: int) -> Response:
        """Resend the invitation to a team. ``POST /api/v1/teams/{team_id}/resend_invitation``

        Args:
            team_id: The ID of the team.
            user_id: The ID of the user to invite again.

        Returns:
            A ``Response`` whose ``data`` is the invited user, with the fields of a member except
            ``role``. The reply is a 404 with the message ``User not found`` when no user has that
            ID.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/teams/{team_id}/resend_invitation",
            json={"user_id": user_id},
        )

    def remove(self, *, team_id: int, user_id: int) -> Response:
        """Remove a user from a team. ``POST /api/v1/teams/{team_id}/remove_member``

        Args:
            team_id: The ID of the team.
            user_id: The ID of the user to remove.

        Returns:
            A ``Response`` with a 200 status whose ``data`` is an object with ``deleted_id``, the
            ID of the removed membership. The reply is a 404 with the message ``User not found``
            when no user has that ID.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/teams/{team_id}/remove_member",
            json={"user_id": user_id},
        )
