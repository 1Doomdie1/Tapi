from collections.abc import Sequence
from datetime import datetime

from tapi.admin.types import UserFilter, UserInclude
from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_iso, to_list


class Users:
    """The users of the tenant, available as ``tines.admin.users``.

    A user, as listed by ``list`` and returned by the other methods, has ``id``, ``scim_uid``
    (``null`` unless the user came from SCIM), ``email``, ``first_name``, ``last_name``, ``admin``
    (whether the user is a tenant owner), ``is_active``, ``tenant_permissions`` (a list of
    permission names), ``last_seen`` (``null`` if the user was never seen), ``created_at`` and
    ``updated_at``. With ``include="team_memberships"`` it also has ``team_memberships``: a list
    of objects with ``team_id``, ``team_name`` and ``role``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        filter: UserFilter | None = None,
        search: str | None = None,
        include: UserInclude | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List users. ``GET /api/v1/admin/users``

        The endpoint is paginated and one call returns one page. Read ``data["meta"]`` to decide
        whether to ask for the next page.

        Args:
            filter: Which users to list: ``ALL``, ``ADMIN`` (the tenant owners), ``ACTIVE`` or
                ``INACTIVE``. The Tines docs give only ``TENANT_OWNER``, which Tines accepts and
                treats as ``ADMIN``. The values are case-sensitive.
            search: Only users whose name or email contains this text, in any case.
            include: ``team_memberships`` to add the teams of each user. Another value is ignored.
            per_page: The number of results per page. Tines defaults to 20 and caps it at 500.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``admin/users``, the users of the
            page, and ``meta``, the pagination details: ``current_page``, ``previous_page`` and
            ``next_page`` (links), ``next_page_number``, ``per_page``, ``pages`` (the number of
            pages) and ``count``. The reply is a 422 that lists the valid values for a ``filter``
            that is not valid, and a 400 for a ``per_page`` or ``page`` that is not a positive
            integer.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/admin/users",
            params=omit_none(
                values={
                    "filter": filter,
                    "search": search,
                    "include": include,
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )

    def get(self, *, user_id: int | str, include: UserInclude | None = None) -> Response:
        """Get a user. ``GET /api/v1/admin/users/{user_id}``

        Args:
            user_id: The ID of the user, or the email address of the user.
            include: ``team_memberships`` to add the teams of the user.

        Returns:
            A ``Response`` whose ``data`` is the user. The reply is a 404 with ``User not found``
            for an ID or an email address that no user has.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/admin/users/{user_id}",
            params=omit_none(values={"include": include}),
        )

    def create(
        self,
        *,
        email: str,
        first_name: str | None = None,
        last_name: str | None = None,
        admin: bool | None = None,
        tenant_permissions: Sequence[str] | None = None,
        is_active: bool | None = None,
        team_id: int | None = None,
    ) -> Response:
        """Create a user. ``POST /api/v1/admin/users``

        Creating a user with an email address that a user already has does not fail: Tines
        answers 201 with the ID of that user and overwrites the fields that were sent, such as
        the first name. The match ignores the case of the address. Do not call this with the
        address of a user that must stay as it is.

        Every new user also gets a personal team, with a story called ``Your first story``.
        ``delete`` does not remove them. Delete the story with ``tines.stories.delete`` first,
        then the team with ``tines.teams.delete``, which Tines refuses until the story is gone.

        Args:
            email: The email address of the user.
            first_name: The first name.
            last_name: The last name.
            admin: Whether the user is a tenant owner. Tines defaults to ``False``.
            tenant_permissions: The tenant permissions to grant, such as ``AUDIT_LOG_READ``. The
                Tines docs link a list of them.
            is_active: Whether the user is active. Tines defaults to ``True``.
            team_id: The ID of a shared team to add the user to. The OpenAPI document has it, and
                the Tines docs do not.

        Returns:
            A ``Response`` whose ``data`` is the created user, with a 201 status. The reply is a
            422 for an email address that is missing or not valid and for a permission that does
            not exist (``Tenant permissions contains invalid permissions``), and a 404 with
            ``Team not found`` for a ``team_id`` that does not exist. A call that is refused for
            an invalid permission or an unknown team can still leave the user behind, so check
            the list after one.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/admin/users",
            json=omit_none(
                values={
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "admin": admin,
                    "tenant_permissions": to_list(values=tenant_permissions),
                    "is_active": is_active,
                    "team_id": team_id,
                }
            ),
        )

    def update(
        self,
        *,
        user_id: int,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        admin: bool | None = None,
        tenant_permissions: Sequence[str] | None = None,
        is_active: bool | None = None,
    ) -> Response:
        """Change a user. ``PATCH /api/v1/admin/users/{user_id}``

        The Tines documentation shows this operation as ``PUT``. The OpenAPI document lists the
        same operation under ``PUT`` and ``PATCH``, and tapi uses ``PATCH``.

        Args:
            user_id: The ID of the user.
            email: A new email address.
            first_name: A new first name.
            last_name: A new last name.
            admin: Whether the user is a tenant owner.
            tenant_permissions: The tenant permissions, which replace the old ones.
            is_active: Whether the user is active.

        Returns:
            A ``Response`` whose ``data`` is the updated user. A call that sends nothing is a 200.
            ``tenant_permissions`` is an empty list when none is granted. The reply is a 404 with
            ``User not found`` for a user that does not exist.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v1/admin/users/{user_id}",
            json=omit_none(
                values={
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "admin": admin,
                    "tenant_permissions": to_list(values=tenant_permissions),
                    "is_active": is_active,
                }
            ),
        )

    def delete(self, *, user_id: int) -> Response:
        """Delete a user. ``DELETE /api/v1/admin/users/{user_id}``

        Args:
            user_id: The ID of the user.

        Returns:
            A ``Response`` with a 204 status and no data. The user is still listed for about half
            a minute afterwards, and is then gone. The personal team of the user stays, empty.
            The reply is a 404 with ``User not found`` for a user that does not exist.
        """
        return self._transport.request(method="DELETE", path=f"/api/v1/admin/users/{user_id}")

    def list_signin_activities(
        self,
        *,
        user_id: int,
        before: datetime | str | None = None,
        after: datetime | str | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List the sign-ins of a user. ``GET /api/v1/admin/users/{user_id}/signin_activities``

        The endpoint is paginated and one call returns one page. It returns a subset of the data
        of the audit logs.

        Args:
            user_id: The ID of the user.
            before: Only sign-ins before this time, as a ``datetime`` or an ISO 8601 string. A
                datetime without a timezone is treated as UTC.
            after: Only sign-ins after this time, in the same formats.
            per_page: The number of results per page. Tines defaults to 20 and caps it at 500.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``admin/login_activities``, the
            sign-ins of the page, and ``meta``, the pagination details. A sign-in has ``id``,
            ``user_id``, ``ip``, ``user_agent`` and ``created_at``. The list is empty for a
            ``user_id`` that no user has, not a 404. The reply is a 422 for a time that cannot be
            read, and a 400 for a ``per_page`` or ``page`` that is not a positive integer.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/admin/users/{user_id}/signin_activities",
            params=omit_none(
                values={
                    "before": to_iso(value=before),
                    "after": to_iso(value=after),
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )

    def resend_invitation(self, *, user_id: int) -> Response:
        """Resend an invitation. ``POST /api/v1/admin/users/{user_id}/resend_invitation``

        Resends the invitation to the platform to a user.

        Args:
            user_id: The ID of the user.

        Returns:
            A ``Response`` with a 200 status. ``data`` is an empty object, or an object with
            ``message`` when the user already accepted the invitation. The reply is a 404 with
            ``User not found`` for a user that does not exist.
        """
        return self._transport.request(
            method="POST", path=f"/api/v1/admin/users/{user_id}/resend_invitation"
        )

    def expire_session(self, *, user_id: int) -> Response:
        """Expire a session. ``POST /api/v1/admin/users/{user_id}/expire_session``

        Signs the user out of the tenant on all devices. The Tines docs give ``DELETE`` in the
        request section of the page and ``POST`` in its example, and the OpenAPI document gives
        ``POST``. Only ``POST`` works: ``DELETE`` is a 404.

        Args:
            user_id: The ID of the user.

        Returns:
            A ``Response`` with a 200 status and no data, where the Tines docs and the OpenAPI
            document say 204. The reply is a 422 with ``User with ID ... not found.`` for a user
            that does not exist, not a 404.
        """
        return self._transport.request(
            method="POST", path=f"/api/v1/admin/users/{user_id}/expire_session"
        )
