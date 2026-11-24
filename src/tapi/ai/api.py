from tapi.ai.providers import Providers
from tapi.ai.usage import Usage
from tapi.core import Transport


class AI:
    """The AI endpoints, available as ``tines.ai``.

    Args:
        transport: The transport used to send requests.

    The areas are attributes of the module:

    - ``providers``: AI providers and their models.
    - ``usage``: Aggregated AI usage.
    """

    def __init__(self, *, transport: Transport) -> None:
        self.providers = Providers(transport=transport)
        self.usage = Usage(transport=transport)
