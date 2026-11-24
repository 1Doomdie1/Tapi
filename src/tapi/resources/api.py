from collections.abc import Sequence
from typing import Any, Literal

from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_list

ResourceValue = str | int | float | bool | dict[str, Any] | list[Any]
ReadAccess = Literal["TEAM", "GLOBAL", "SPECIFIC_TEAMS"]
ResourceFilter = Literal["UNUSED_IN_ACTIONS"]


class Resources:
    """Resources, available as ``tines.resources``.

    A resource, as returned by ``get``, ``create`` and ``update`` and listed by ``list``, has
    ``id``, ``name``, ``value``, ``team_id``, ``folder_id``, ``user_id``, ``read_access``,
    ``shared_team_slugs``, ``slug``, ``created_at``, ``updated_at``, ``description``,
    ``test_resource_enabled``, ``test_resource`` and ``referencing_action_ids``. ``value`` is a
    string unless ``typed_value`` is true, and for a file resource it holds ``name``,
    ``contents`` and ``type``.

    A value, as taken by ``create``, ``update``, ``append``, ``remove`` and ``replace``, is a
    string, a number, a boolean, a JSON object (a ``dict``) or a JSON array (a ``list``).

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        team_id: int | None = None,
        folder_id: int | None = None,
        filter: ResourceFilter | None = None,
        include_referencing_action_ids: bool | None = None,
        include_value: bool | None = None,
        typed_value: bool | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List resources. ``GET /api/v1/global_resources``

        Args:
            team_id: Only resources of this team.
            folder_id: Only resources in this folder.
            filter: ``UNUSED_IN_ACTIONS`` keeps only the resources that no action uses.
            include_referencing_action_ids: Whether each resource has ``referencing_action_ids``.
            include_value: Whether each resource has ``value`` and ``test_resource.value``.
            typed_value: When true, ``value`` is a boolean, a number, an array or an object where it
                holds one, instead of a string.
            per_page: The number of results per page.
            page: The page to return, starting at 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``global_resources``, the resources of
            the page, and ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/global_resources",
            params=omit_none(
                values={
                    "team_id": team_id,
                    "folder_id": folder_id,
                    "filter": filter,
                    "include_referencing_action_ids": include_referencing_action_ids,
                    "include_value": include_value,
                    "typed_value": typed_value,
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )

    def get(
        self,
        *,
        resource_id: int,
        include_referencing_action_ids: bool | None = None,
        typed_value: bool | None = None,
    ) -> Response:
        """Get a resource. ``GET /api/v1/global_resources/{resource_id}``

        Args:
            resource_id: The ID of the live resource to retrieve.
            include_referencing_action_ids: Whether the resource has ``referencing_action_ids``.
                Tines defaults to true.
            typed_value: When true, ``value`` is a boolean, a number, an array or an object where
                it holds one, instead of a string. Tines defaults to false.

        Returns:
            A ``Response`` whose ``data`` is the resource.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/global_resources/{resource_id}",
            params=omit_none(
                values={
                    "include_referencing_action_ids": include_referencing_action_ids,
                    "typed_value": typed_value,
                }
            ),
        )

    def create(
        self,
        *,
        name: str,
        value: ResourceValue,
        team_id: int,
        folder_id: int | None = None,
        read_access: ReadAccess | None = None,
        shared_team_slugs: Sequence[str] | None = None,
        description: str | None = None,
        live_resource_id: int | None = None,
        include_referencing_action_ids: bool | None = None,
        typed_value: bool | None = None,
    ) -> Response:
        """Create a resource. ``POST /api/v1/global_resources``

        Args:
            name: The name of the resource.
            value: The contents of the resource. A string that is not JSON is stored as text. A
                ``dict`` or a ``list`` creates a JSON resource. A file resource takes a ``dict``
                with ``name`` (the file name), ``contents`` (the Base64-encoded contents) and
                optionally ``type`` (the MIME type).
            team_id: The ID of the team the resource is created in.
            folder_id: The ID of the folder to put the resource in.
            read_access: Where the resource can be used: ``TEAM`` (the default), ``GLOBAL`` or
                ``SPECIFIC_TEAMS``, which is a premium feature.
            shared_team_slugs: The slugs of the teams that can use the resource. Needed to set
                ``read_access`` to ``SPECIFIC_TEAMS``.
            description: A description of the resource.
            live_resource_id: For a test resource used in the TEST mode of change control, the ID of
                the live resource it corresponds to. The other optional values then default to those
                of the live resource.
            include_referencing_action_ids: Whether the reply has ``referencing_action_ids``.
            typed_value: When true, ``value`` in the reply is a boolean, a number, an array or an
                object where it holds one, instead of a string.

        Returns:
            A ``Response`` whose ``data`` is the created resource, with a 201 status.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/global_resources",
            json=omit_none(
                values={
                    "name": name,
                    "value": value,
                    "team_id": team_id,
                    "folder_id": folder_id,
                    "read_access": read_access,
                    "shared_team_slugs": to_list(values=shared_team_slugs),
                    "description": description,
                    "live_resource_id": live_resource_id,
                    "include_referencing_action_ids": include_referencing_action_ids,
                    "typed_value": typed_value,
                }
            ),
        )

    def update(
        self,
        *,
        resource_id: int,
        value: ResourceValue,
        name: str | None = None,
        folder_id: int | None = None,
        read_access: ReadAccess | None = None,
        shared_team_slugs: Sequence[str] | None = None,
        description: str | None = None,
        test_resource_enabled: bool | None = None,
        is_test: bool | None = None,
        include_referencing_action_ids: bool | None = None,
        typed_value: bool | None = None,
    ) -> Response:
        """Update a resource. ``PATCH /api/v1/global_resources/{resource_id}``

        ``value`` is needed on every update, even to rename a resource: without it Tines answers a
        422 with the message ``Value may not be null``. The other parameters are sent only when you
        give them. A parameter left as ``None`` is not sent, so tapi cannot set a field to ``null``,
        and cannot move a resource to the root folder, which Tines does with an empty value.

        Args:
            resource_id: The ID of the live resource to update.
            value: The contents of the resource. To keep them, pass the current value. For a file
                resource, a ``dict`` with ``name``, ``contents`` (Base64-encoded) and optionally
                ``type``.
            name: The new name of the resource.
            folder_id: The ID of the folder to move the resource to.
            read_access: Where the resource can be used: ``TEAM``, ``GLOBAL`` or ``SPECIFIC_TEAMS``,
                which is a premium feature.
            shared_team_slugs: The slugs of the teams that can use the resource. Needed to set
                ``read_access`` to ``SPECIFIC_TEAMS``.
            description: The new description of the resource.
            test_resource_enabled: Whether the resource is enabled for using a test resource.
            is_test: Whether the test resource is the one to update. It requires
                ``test_resource_enabled`` to be true and a test resource to exist.
            include_referencing_action_ids: Whether the reply has ``referencing_action_ids``.
            typed_value: When true, ``value`` in the reply is a boolean, a number, an array or an
                object where it holds one, instead of a string.

        Returns:
            A ``Response`` whose ``data`` is the updated resource.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v1/global_resources/{resource_id}",
            json=omit_none(
                values={
                    "value": value,
                    "name": name,
                    "folder_id": folder_id,
                    "read_access": read_access,
                    "shared_team_slugs": to_list(values=shared_team_slugs),
                    "description": description,
                    "test_resource_enabled": test_resource_enabled,
                    "is_test": is_test,
                    "include_referencing_action_ids": include_referencing_action_ids,
                    "typed_value": typed_value,
                }
            ),
        )

    def delete(self, *, resource_id: int) -> Response:
        """Delete a resource. ``DELETE /api/v1/global_resources/{resource_id}``

        A locked resource can be deleted. Tines does not document whether a resource that actions
        reference can be deleted.

        Args:
            resource_id: The ID of the live resource to delete.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(
            method="DELETE",
            path=f"/api/v1/global_resources/{resource_id}",
        )

    def append(
        self,
        *,
        resource_id: int,
        value: ResourceValue,
        is_test: bool | None = None,
    ) -> Response:
        """Append to a resource. ``POST /api/v1/global_resources/{resource_id}/append``

        On a text resource the string is added to the end of the text. On an array resource a
        string is added as a new element, and an array adds its elements. An object resource is
        refused with a 422. A locked resource is refused with a 422 as well.

        Args:
            resource_id: The ID of the live resource.
            value: The string or array to append.
            is_test: Whether the test resource is the one to modify.

        Returns:
            A ``Response`` whose ``data`` is the updated value of the resource.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/global_resources/{resource_id}/append",
            json=omit_none(values={"value": value, "is_test": is_test}),
        )

    def remove(
        self,
        *,
        resource_id: int,
        key: str | None = None,
        index: int | None = None,
        if_value: ResourceValue | None = None,
        is_test: bool | None = None,
    ) -> Response:
        """Remove an element from a resource. ``POST /api/v1/global_resources/{resource_id}/remove``

        Removes a top-level element from an array resource, or a key from an object resource.

        Args:
            resource_id: The ID of the live resource.
            key: The key to remove, for an object resource.
            index: The index of the element to remove, for an array resource, counting from 0. When
                omitted, the last element is removed.
            if_value: Only remove the element if its current value matches this. If it does not,
                Tines answers with a 422 whose ``data`` holds the current value.
            is_test: Whether the test resource is the one to modify.

        Returns:
            A ``Response`` whose ``data`` is the removed item, or ``None`` when there was nothing to
            remove, such as a key that does not exist.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/global_resources/{resource_id}/remove",
            json=omit_none(
                values={"key": key, "index": index, "if_value": if_value, "is_test": is_test}
            ),
        )

    def replace(
        self,
        *,
        resource_id: int,
        value: ResourceValue,
        key: str | None = None,
        index: int | None = None,
        if_value: ResourceValue | None = None,
        is_test: bool | None = None,
    ) -> Response:
        """Replace an element of a resource. ``POST /api/v1/global_resources/{resource_id}/replace``

        Replaces a top-level element of an array resource, or a key of an object resource.

        Args:
            resource_id: The ID of the live resource.
            value: The new value of the element.
            key: The key to replace, for an object resource.
            index: The index of the element to replace, for an array resource, counting from 0.
            if_value: Only replace the element if its current value matches this. If it does not,
                Tines answers with a 422 whose ``data`` holds the current value, and the resource is
                unchanged.
            is_test: Whether the test resource is the one to modify.

        Returns:
            A ``Response`` whose ``data`` is the updated value of the resource. Replacing a key that
            does not exist adds it.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/global_resources/{resource_id}/replace",
            json=omit_none(
                values={
                    "key": key,
                    "index": index,
                    "value": value,
                    "if_value": if_value,
                    "is_test": is_test,
                }
            ),
        )

    def set_locked(self, *, resource_id: int, locked: bool) -> Response:
        """Lock or unlock a resource. ``PUT /api/v1/global_resources/{resource_id}/locked``

        A locked resource cannot have its value modified: ``update``, ``append``, ``remove`` and
        ``replace`` are refused with a 422, but it can still be deleted. This needs the
        ``RESOURCE_MANAGE`` permission. Unlocking through the API is permanent, and locking or
        unlocking also applies to the test resource of the resource. Locking a locked resource is
        not an error.

        Args:
            resource_id: The ID of the resource.
            locked: True to lock the resource, false to unlock it.

        Returns:
            A ``Response`` whose ``data`` is an object with the ``id`` of the resource and its
            ``locked`` status.
        """
        return self._transport.request(
            method="PUT",
            path=f"/api/v1/global_resources/{resource_id}/locked",
            json={"locked": locked},
        )
