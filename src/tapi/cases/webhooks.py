from collections.abc import Sequence

from tapi.cases.types import WebhookNotification
from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_list


class Webhooks:
    """The case webhooks of a team, available as ``tines.cases.webhooks``.

    A case webhook sends a request to an address when something happens to a case of the team. A
    webhook, as returned by ``get``, ``create`` and ``update`` and listed by ``list``, has ``id``,
    ``name`` (``null`` when none was given), ``url``, ``version_number`` (the version of the
    payload), ``notifications`` (the events that trigger it) and ``team``. The Tines docs say that
    a team can have at most five webhooks.

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
        """List the case webhooks. ``GET /api/v1/case_webhooks``

        The endpoint is paginated and one call returns one page.

        Args:
            team_id: Only webhooks of this team.
            per_page: The number of results per page. Tines defaults to 20, and its docs give a
                maximum of 50, though a ``per_page`` of 51 was accepted.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``webhooks``, the webhooks of the
            page, and ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/case_webhooks",
            params=omit_none(values={"team_id": team_id, "per_page": per_page, "page": page}),
        )

    def get(self, *, webhook_id: int) -> Response:
        """Get a case webhook. ``GET /api/v1/case_webhooks/{webhook_id}``

        Args:
            webhook_id: The ID of the webhook.

        Returns:
            A ``Response`` whose ``data`` is an object with ``webhook``. The reply is a 404 with
            ``TeamCaseWebhook not found`` for a webhook that does not exist.
        """
        return self._transport.request(method="GET", path=f"/api/v1/case_webhooks/{webhook_id}")

    def create(
        self,
        *,
        team_id: int,
        url: str,
        name: str | None = None,
        notifications: Sequence[WebhookNotification] | None = None,
    ) -> Response:
        """Create a case webhook. ``POST /api/v1/case_webhooks``

        Args:
            team_id: The ID of the team that gets the webhook.
            url: The address that Tines sends the requests to.
            name: A name to show for the webhook.
            notifications: The events that trigger the webhook: ``ALL``, or any of the values of
                ``tapi.cases.types.WebhookNotification`` such as ``CREATED`` and ``COMMENTED``.
                Tines defaults to ``["ALL"]``.

        Returns:
            A ``Response`` whose ``data`` is an object with ``webhook``, with a 201 status. The
            reply is a 422 for a ``url`` that is not valid (``Url is not a valid URL``) and for a
            notification that is not valid, where the message lists the valid ones.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/case_webhooks",
            json=omit_none(
                values={
                    "team_id": team_id,
                    "url": url,
                    "name": name,
                    "notifications": to_list(values=notifications),
                }
            ),
        )

    def update(
        self,
        *,
        webhook_id: int,
        url: str | None = None,
        name: str | None = None,
        notifications: Sequence[WebhookNotification] | None = None,
    ) -> Response:
        """Change a case webhook. ``PATCH /api/v1/case_webhooks/{webhook_id}``

        Args:
            webhook_id: The ID of the webhook.
            url: A new address.
            name: A new name. An empty string is accepted.
            notifications: The events that trigger the webhook, which replace the old ones.

        Returns:
            A ``Response`` whose ``data`` is an object with ``webhook``.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v1/case_webhooks/{webhook_id}",
            json=omit_none(
                values={
                    "url": url,
                    "name": name,
                    "notifications": to_list(values=notifications),
                }
            ),
        )

    def delete(self, *, webhook_id: int) -> Response:
        """Delete a case webhook. ``DELETE /api/v1/case_webhooks/{webhook_id}``

        Args:
            webhook_id: The ID of the webhook.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(method="DELETE", path=f"/api/v1/case_webhooks/{webhook_id}")
