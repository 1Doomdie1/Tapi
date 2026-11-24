from tapi.core import Response, Transport
from tapi.core.params import omit_none


class IpAccessControlRules:
    """The IP access control rules, available as ``tines.admin.ip_access_control_rules``.

    A rule names an IP address or a range of addresses that may access the tenant. Tines applies
    the rules only if IP access control is enabled for the tenant, which cannot be done here. Be
    careful: a rule that is wrong can keep you out of your own tenant. A rule, as listed by
    ``list`` and returned by the other methods, has ``id``, ``ip`` (an address or a CIDR range),
    ``description`` (or ``null``), ``created_at`` and ``updated_at``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        matching_ip: str | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List IP access control rules. ``GET /api/v1/admin/ip_access_control_rules``

        The endpoint is paginated and one call returns one page. Read ``data["meta"]`` to decide
        whether to ask for the next page.

        Args:
            matching_ip: An address or a CIDR range: only the rules that match it are returned.
                Tines answers 500 for a value that is not an address.
            per_page: The number of results per page. Tines defaults to 20 and caps it at 500.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``admin/ip_access_control_rules``,
            the rules of the page, and ``meta``, the pagination details: ``current_page``,
            ``previous_page`` and ``next_page`` (links), ``next_page_number``, ``per_page``,
            ``pages`` (the number of pages) and ``count``.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/admin/ip_access_control_rules",
            params=omit_none(
                values={"matching_ip": matching_ip, "per_page": per_page, "page": page}
            ),
        )

    def get(self, *, rule_id: int) -> Response:
        """Get an IP access control rule. ``GET /api/v1/admin/ip_access_control_rules/{rule_id}``

        Args:
            rule_id: The ID of the rule.

        Returns:
            A ``Response`` whose ``data`` is the rule. The reply is a 404 with ``Rule not found``
            for a rule that does not exist.
        """
        return self._transport.request(
            method="GET", path=f"/api/v1/admin/ip_access_control_rules/{rule_id}"
        )

    def create(self, *, ip: str, description: str | None = None) -> Response:
        """Create an IP access control rule. ``POST /api/v1/admin/ip_access_control_rules``

        Args:
            ip: An IP address or a CIDR range, such as ``192.168.1.1`` or ``10.0.0.0/8``.
            description: A description of the rule.

        Returns:
            A ``Response`` whose ``data`` is the created rule, with a 201 status.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/admin/ip_access_control_rules",
            json=omit_none(values={"ip": ip, "description": description}),
        )

    def update(
        self,
        *,
        rule_id: int,
        ip: str | None = None,
        description: str | None = None,
    ) -> Response:
        """Change a rule. ``PATCH /api/v1/admin/ip_access_control_rules/{rule_id}``

        The Tines documentation shows this operation as ``PUT``. The OpenAPI document lists the
        same operation under ``PUT`` and ``PATCH``, and tapi uses ``PATCH``.

        Args:
            rule_id: The ID of the rule.
            ip: A new IP address or CIDR range.
            description: A new description.

        Returns:
            A ``Response`` whose ``data`` is the updated rule.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v1/admin/ip_access_control_rules/{rule_id}",
            json=omit_none(values={"ip": ip, "description": description}),
        )

    def delete(self, *, rule_id: int) -> Response:
        """Delete a rule. ``DELETE /api/v1/admin/ip_access_control_rules/{rule_id}``

        Args:
            rule_id: The ID of the rule.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(
            method="DELETE", path=f"/api/v1/admin/ip_access_control_rules/{rule_id}"
        )
