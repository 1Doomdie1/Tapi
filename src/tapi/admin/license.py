from tapi.core import Response, Transport


class License:
    """The license of a self-hosted tenant, available as ``tines.admin.license``.

    The routes exist only on self-hosted tenants. A license, as returned by every method, has
    ``customer_name``, ``unique_identifier``, ``environment``, ``created_at``, ``expires_at`` (or
    ``null``), ``pricing_model``, the limits ``users``, ``builders``, ``teams``, ``stories``,
    ``story_units``, ``actions``, ``tunnels``, ``daily_story_events`` and ``daily_tenant_events``
    (integers), and ``features``, a list of names such as ``AUDIT_LOGS`` or ``SSO``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def get(self) -> Response:
        """Get the license. ``GET /api/v1/admin/license``

        Returns:
            A ``Response`` whose ``data`` is the license. The reply is a 404 for a tenant that has
            no license, and a 403 for a tenant that is not self-hosted, with ``data`` an object
            whose ``error`` is ``This endpoint is only available on self-hosted installations``.
            A 403 can also come from the IP access control rules or the domain enforcement of the
            tenant.
        """
        return self._transport.request(method="GET", path="/api/v1/admin/license")

    def create(self, *, license: str) -> Response:
        """Apply the first license. ``POST /api/v1/admin/license``

        A license must not exist yet: use ``update`` to replace one.

        Args:
            license: The signed license string, such as ``TINES-company_name-ENV::LICENSE_DATA``.

        Returns:
            A ``Response`` with a 201 status whose ``data`` is the applied license. The reply is a
            409 when the tenant already has a license, and a 422 when the string is not a valid
            signed license.
        """
        return self._transport.request(
            method="POST", path="/api/v1/admin/license", json={"license": license}
        )

    def update(self, *, license: str) -> Response:
        """Replace the license. ``PATCH /api/v1/admin/license``

        A license must exist already: use ``create`` to apply the first one.

        Args:
            license: The signed license string, such as ``TINES-company_name-ENV::LICENSE_DATA``.

        Returns:
            A ``Response`` whose ``data`` is the applied license. The reply is a 404 when the tenant
            has no license, and a 422 when the string is not a valid signed license.
        """
        return self._transport.request(
            method="PATCH", path="/api/v1/admin/license", json={"license": license}
        )
