from collections.abc import Mapping, Sequence

from tapi.cases.types import CaseActionInput, CaseActionType
from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_list


class Actions:
    """The actions of a case, available as ``tines.cases.actions``.

    A case action is a button on the case that opens a page or calls a webhook. These are not
    the actions of a story, which are ``tines.stories.actions``. A case action, as returned by
    ``get``, ``create`` and ``update`` and listed by ``list``, has ``id``, ``case_id``, ``url``,
    ``label``, ``action_type``, ``action_text`` (the text of the button, ``Run`` for a webhook
    that has none), ``query_params`` (``null`` if none), ``story_name``, ``story_emoji``,
    ``page_emoji``, ``created_at`` and ``updated_at``, and the fields ``query_param_key``,
    ``query_param_value`` and ``three_b_reference``.

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
        """List the actions of a case. ``GET /api/v2/cases/{case_id}/actions``

        The endpoint is paginated and one call returns one page.

        Args:
            case_id: The ID of the case.
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id``, ``actions``, the actions
            of the page, and ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v2/cases/{case_id}/actions",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )

    def get(self, *, case_id: int, action_id: int) -> Response:
        """Get an action of a case. ``GET /api/v2/cases/{case_id}/actions/{action_id}``

        Args:
            case_id: The ID of the case.
            action_id: The ID of the action.

        Returns:
            A ``Response`` whose ``data`` is the action.
        """
        return self._transport.request(
            method="GET", path=f"/api/v2/cases/{case_id}/actions/{action_id}"
        )

    def create(
        self,
        *,
        case_id: int,
        url: str,
        label: str,
        action_type: CaseActionType,
        action_text: str | None = None,
        query_params: Mapping[str, str] | None = None,
    ) -> Response:
        """Add an action to a case. ``POST /api/v2/cases/{case_id}/actions``

        Args:
            case_id: The ID of the case.
            url: The address that the action opens or calls. An address that is not a URL is a
                422.
            label: The name that identifies the action. The server refuses an action without
                one, as the Tines docs say and the OpenAPI document does not.
            action_type: ``webhook`` or ``page``, as the Tines docs say. The server also lists
                ``chat``, ``story`` and ``app``, which were not tried. It refuses an action
                without a type, as the Tines docs say and the OpenAPI document does not.
            action_text: The text of the button.
            query_params: Key-value pairs that are added to the address as a query string.

        Returns:
            A ``Response`` whose ``data`` is the created action, with a 201 status. The reply is
            a 422 naming the field for a value that is missing or not valid, and a 400 when
            ``query_params`` is not an object.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v2/cases/{case_id}/actions",
            json=omit_none(
                values={
                    "url": url,
                    "label": label,
                    "action_type": action_type,
                    "action_text": action_text,
                    "query_params": query_params,
                }
            ),
        )

    def update(
        self,
        *,
        case_id: int,
        action_id: int,
        url: str | None = None,
        label: str | None = None,
        action_type: CaseActionType | None = None,
        action_text: str | None = None,
        query_params: Mapping[str, str] | None = None,
    ) -> Response:
        """Change an action of a case. ``PATCH /api/v2/cases/{case_id}/actions/{action_id}``

        The Tines documentation shows this operation as ``PUT``. The OpenAPI document lists the
        same operation under ``PUT`` and ``PATCH``, and tapi uses ``PATCH``.

        Args:
            case_id: The ID of the case.
            action_id: The ID of the action.
            url: A new address.
            label: A new name.
            action_type: A new type: ``webhook`` or ``page``.
            action_text: New text for the button.
            query_params: New key-value pairs for the query string.

        Returns:
            A ``Response`` whose ``data`` is the updated action. A call that sends nothing is a
            200. The reply is a 400 when ``query_params`` is not an object, and a 404 with
            ``Action not found`` for an action that does not exist.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v2/cases/{case_id}/actions/{action_id}",
            json=omit_none(
                values={
                    "url": url,
                    "label": label,
                    "action_type": action_type,
                    "action_text": action_text,
                    "query_params": query_params,
                }
            ),
        )

    def delete(self, *, case_id: int, action_id: int) -> Response:
        """Delete an action of a case. ``DELETE /api/v2/cases/{case_id}/actions/{action_id}``

        Args:
            case_id: The ID of the case.
            action_id: The ID of the action.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(
            method="DELETE", path=f"/api/v2/cases/{case_id}/actions/{action_id}"
        )

    def batch_update(self, *, case_id: int, actions: Sequence[CaseActionInput]) -> Response:
        """Replace the actions of a case. ``PUT /api/v2/cases/{case_id}/actions/batch``

        The actions that are sent replace the ones the case has, and an empty list removes them
        all.

        Args:
            case_id: The ID of the case.
            actions: The new actions, each an object with a ``url``, a ``label``, an
                ``action_type`` and optionally ``action_text`` and ``query_params``. See
                ``tapi.cases.CaseActionInput``.

        Returns:
            A ``Response`` whose ``data`` is an object with ``case_id`` and ``actions``. The
            reply is a 422 with ``Validation failed: Label can't be blank`` for an action
            without a label, and a 400 when the ``query_params`` of an action is not an object.
        """
        return self._transport.request(
            method="PUT",
            path=f"/api/v2/cases/{case_id}/actions/batch",
            json={"actions": to_list(values=actions)},
        )
