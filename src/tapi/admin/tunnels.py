from tapi.core import Response, Transport


class Tunnels:
    """The tunnels of the tenant, available as ``tines.admin.tunnels``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def health(self, *, tunnel_name: str) -> Response:
        """Get the health of a tunnel. ``GET /api/v1/admin/tunnel/{tunnel_name}/health``

        The route has ``tunnel`` in the singular. The Tines docs say that a tenant-level API key is
        needed.

        Args:
            tunnel_name: The name of the tunnel.

        Returns:
            A ``Response`` whose ``data`` is an object with ``health``: ``Down``, ``Healthy``,
            ``Inactive`` or ``Degraded``. The reply is a 404 for a tunnel that does not exist, and
            ``data`` is then an object with ``error`` (``Tunnel named ... not found``), not a
            list of messages.
        """
        return self._transport.request(
            method="GET", path=f"/api/v1/admin/tunnel/{tunnel_name}/health"
        )
