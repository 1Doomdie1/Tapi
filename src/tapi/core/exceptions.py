class TinesError(Exception):
    """Base class for every exception raised by tapi."""


class TinesConfigurationError(TinesError):
    """The client has missing or invalid configuration, such as the tenant domain or API key."""


class TinesConnectionError(TinesError):
    """No HTTP response was received because the connection was refused, failed or timed out.

    The exception that caused it is available as ``__cause__``.
    """
