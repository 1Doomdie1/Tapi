from tapi.core import Response, Transport


class Providers:
    """AI providers and their models, available as ``tines.ai.providers``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(self) -> Response:
        """List the AI providers and models available to you. ``GET /api/v1/ai_providers``

        Not paginated. Administrators get every provider of the tenant, other users those of
        their teams.

        Returns:
            A ``Response`` whose ``data`` has ``ai_providers``. A provider has ``guid``,
            ``enabled``, ``name``, ``provider_type``, ``provisioning_type`` and ``models``. A
            model has ``display_name``, ``api_model_id``, ``description``, ``cost_tier`` and
            ``legacy``.
        """
        return self._transport.request(method="GET", path="/api/v1/ai_providers")
