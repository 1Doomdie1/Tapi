from collections.abc import Sequence

from tapi.admin.types import EgressActionType
from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_list


class ActionEgressControlRules:
    """The action egress control rules, available as ``tines.admin.action_egress_control_rules``.

    A rule restricts the outbound traffic of actions: it names an IP address, a range or a domain
    name, and the types of action that may send traffic to it. Tines applies the rules only if
    action egress control is enabled for the tenant, which cannot be done here. Be careful: once it
    is enabled, a rule that is wrong can stop the actions of your stories. A rule, as listed by
    ``list`` and returned by the other methods, has ``id``, ``ip`` and ``fqdn`` (a rule has one of
    them and the other is ``null``), ``description``, ``allowed_action_types`` (a list with
    ``http-request``, ``send-email`` or both), ``created_at`` and ``updated_at``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List action egress control rules. ``GET /api/v1/admin/action_egress_control_rules``

        The endpoint is paginated and one call returns one page. Read ``data["meta"]`` to decide
        whether to ask for the next page.

        Args:
            per_page: The number of results per page. Tines defaults to 20 and caps it at 500.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``admin/action_egress_control_rules``,
            the rules of the page, and ``meta``, the pagination details: ``current_page``,
            ``previous_page`` and ``next_page`` (links), ``next_page_number``, ``per_page``,
            ``pages`` (the number of pages) and ``count``.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/admin/action_egress_control_rules",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )

    def get(self, *, rule_id: int) -> Response:
        """Get a rule. ``GET /api/v1/admin/action_egress_control_rules/{rule_id}``

        Args:
            rule_id: The ID of the rule.

        Returns:
            A ``Response`` whose ``data`` is the rule. The reply is a 404 with ``Rule not found``
            for a rule that does not exist.
        """
        return self._transport.request(
            method="GET", path=f"/api/v1/admin/action_egress_control_rules/{rule_id}"
        )

    def create(
        self,
        *,
        description: str,
        allowed_action_types: Sequence[EgressActionType],
        ip: str | None = None,
        fqdn: str | None = None,
    ) -> Response:
        """Create an action egress control rule. ``POST /api/v1/admin/action_egress_control_rules``

        Send ``ip`` or ``fqdn``, not both.

        Args:
            description: A description of the rule.
            allowed_action_types: The types of action that may send traffic to the address or the
                domain name: ``http-request``, ``send-email`` or both. ``send-email`` is for a
                domain name only. Tines refuses any other value.
            ip: An IP address or a CIDR range.
            fqdn: A fully qualified domain name.

        Returns:
            A ``Response`` whose ``data`` is the created rule, with a 201 status.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/admin/action_egress_control_rules",
            json=omit_none(
                values={
                    "description": description,
                    "allowed_action_types": to_list(values=allowed_action_types),
                    "ip": ip,
                    "fqdn": fqdn,
                }
            ),
        )

    def update(
        self,
        *,
        rule_id: int,
        description: str,
        allowed_action_types: Sequence[EgressActionType],
        ip: str | None = None,
        fqdn: str | None = None,
    ) -> Response:
        """Change a rule. ``PATCH /api/v1/admin/action_egress_control_rules/{rule_id}``

        Replaces the whole rule: send the description, the types and the ``ip`` or ``fqdn`` every
        time.

        Args:
            rule_id: The ID of the rule.
            description: A description of the rule.
            allowed_action_types: ``http-request``, ``send-email`` or both. ``send-email`` is for a
                domain name only.
            ip: An IP address or a CIDR range. Send ``ip`` or ``fqdn``, not both.
            fqdn: A fully qualified domain name.

        Returns:
            A ``Response`` whose ``data`` is the updated rule.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v1/admin/action_egress_control_rules/{rule_id}",
            json=omit_none(
                values={
                    "description": description,
                    "allowed_action_types": to_list(values=allowed_action_types),
                    "ip": ip,
                    "fqdn": fqdn,
                }
            ),
        )

    def delete(self, *, rule_id: int) -> Response:
        """Delete a rule. ``DELETE /api/v1/admin/action_egress_control_rules/{rule_id}``

        Args:
            rule_id: The ID of the rule.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(
            method="DELETE", path=f"/api/v1/admin/action_egress_control_rules/{rule_id}"
        )
