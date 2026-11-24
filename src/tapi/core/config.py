import os
from urllib.parse import urlsplit

from tapi.core.exceptions import TinesConfigurationError

TENANT_DOMAIN_ENV_VAR = "TINES_TENANT_DOMAIN"
API_KEY_ENV_VAR = "TINES_API_KEY"


def resolve_base_url(*, tenant_domain: str | None) -> str:
    """Build the root URL of a tenant from its domain.

    Args:
        tenant_domain: The tenant domain, such as ``acme.tines.com``. A scheme is accepted
            (``https`` or ``http``) and any path is ignored. Without a scheme ``https`` is used.
            When empty, the ``TINES_TENANT_DOMAIN`` environment variable is used.

    Returns:
        The tenant root URL, for example ``https://acme.tines.com``.

    Raises:
        TinesConfigurationError: If no domain is available, or it is not a valid http(s) address.
    """
    value = (tenant_domain or os.environ.get(TENANT_DOMAIN_ENV_VAR) or "").strip()
    if not value:
        raise TinesConfigurationError(
            f"No tenant domain configured. Pass tenant_domain or set {TENANT_DOMAIN_ENV_VAR}."
        )
    parts = urlsplit(value if "://" in value else f"https://{value}")
    if parts.scheme not in {"http", "https"} or not parts.netloc:
        raise TinesConfigurationError(f"{value!r} is not a valid tenant domain.")
    return f"{parts.scheme}://{parts.netloc}"


def resolve_api_key(*, api_key: str | None) -> str:
    """Return the API key to use.

    Args:
        api_key: The API key. When empty, the ``TINES_API_KEY`` environment variable is used.

    Returns:
        The API key, without surrounding whitespace.

    Raises:
        TinesConfigurationError: If no API key is available.
    """
    value = (api_key or os.environ.get(API_KEY_ENV_VAR) or "").strip()
    if not value:
        raise TinesConfigurationError(
            f"No API key configured. Pass api_key or set {API_KEY_ENV_VAR}."
        )
    return value
