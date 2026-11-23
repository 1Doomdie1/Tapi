from tapi.ai.providers import Providers
from tapi.ai.usage import Usage
from tapi.core import Transport


class AI:
    """The AI endpoints, available as ``tines.ai``.

    Args:
        transport: The transport used to send requests.

    Attributes:
        providers: AI providers and their models. See ``tapi.ai.Providers``.
        usage: Aggregated AI usage. See ``tapi.ai.Usage``.
    """

    def __init__(self, *, transport: Transport) -> None:
        self.providers = Providers(transport=transport)
        self.usage = Usage(transport=transport)
