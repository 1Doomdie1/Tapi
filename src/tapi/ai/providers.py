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

        Administrators get every AI provider configured for the tenant. Other users get the
        providers that belong to one of their teams, are shared with one of their teams or are
        available to the whole tenant. Enabled and disabled providers are both included. The
        endpoint is not paginated.

        Returns:
            A ``Response`` whose ``data`` is an object with an ``ai_providers`` list. Each
            provider has:

            - ``guid``: the unique identifier of the provider.
            - ``enabled``: whether the provider is enabled.
            - ``name``: the configured name, or the default name of the provider.
            - ``provider_type``: ``ANTHROPIC``, ``OPEN_AI``, ``AWS_BEDROCK``, ``ORACLE_COHERE``,
              ``MISTRAL`` or ``GOOGLE_VERTEX``.
            - ``provisioning_type``: ``customer_provisioned`` or ``tines_provisioned``.
            - ``models``: the models available through the provider. Each has ``display_name``,
              ``api_model_id`` (the identifier to use when configuring Tines AI features through
              the API), ``description`` (``null`` if there is none), ``cost_tier`` (``LOW``,
              ``MEDIUM``, ``HIGH`` or ``null``) and ``legacy`` (whether the model is a legacy
              model).
        """
        return self._transport.request(method="GET", path="/api/v1/ai_providers")
