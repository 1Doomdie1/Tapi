from tapi.core import Response, Transport


class Info:
    """Information about your Tines tenant, available as ``tines.info``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def get(self) -> Response:
        """Get basic information about your tenant's stack. ``GET /api/v1/info``

        Returns:
            A ``Response`` whose ``data`` is an object with one key, ``stack``. It holds ``name``
            (the name assigned to the stack), ``type`` (whether the stack is dedicated or shared),
            ``region`` (the AWS region the stack is hosted in) and ``egress_ips`` (the origin IPs
            used for any request that originates from your tenant).
        """
        return self._transport.request(method="GET", path="/api/v1/info")

    def web_stats(self) -> Response:
        """Get operational information about your web server. ``GET /api/v1/info/web_stats``

        Tines documents this endpoint as accessible only to self-hosted customers. If you run
        several ``tines-web`` containers, the statistics only reflect the container that handled
        the request.

        Returns:
            A ``Response`` whose ``data`` is the status of the Puma web server, for example
            ``started_at``, ``backlog``, ``running``, ``pool_capacity``, ``busy_threads``,
            ``max_threads``, ``requests_count`` and ``versions``. See
            https://puma.io/puma/file.stats.html for what the Puma fields mean.
        """
        return self._transport.request(method="GET", path="/api/v1/info/web_stats")

    def worker_stats(self) -> Response:
        """Get essential information about worker statistics. ``GET /api/v1/info/worker_stats``

        Tines documents this endpoint as accessible only to self-hosted customers and customers
        on dedicated cloud stacks.

        Returns:
            A ``Response`` whose ``data`` holds ``current_workers`` (the number of active workers),
            ``max_workers`` (the maximum number of workers allowed), ``queue_count`` (the number of
            items in the queue) and ``queue_latency`` (the latency of the default queue).
        """
        return self._transport.request(method="GET", path="/api/v1/info/worker_stats")
