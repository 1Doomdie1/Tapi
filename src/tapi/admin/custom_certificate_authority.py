from tapi.core import Response, Transport
from tapi.core.params import omit_none


class CustomCertificateAuthority:
    """The custom certificate authority, available as ``tines.admin.custom_certificate_authority``.

    The authority is used by all the IMAP and HTTP Request actions of the tenant. The Tines docs and
    the OpenAPI document have a single operation for it, ``set``, and no route to read or remove an
    authority.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def set(self, *, certificate: str, name: str | None = None) -> Response:
        """Set the authority. ``PATCH /api/v1/admin/custom_certificate_authority``

        The Tines documentation shows this operation as ``PUT``. The OpenAPI document lists the
        same operation under ``PUT`` and ``PATCH``, and tapi uses ``PATCH``.

        Args:
            certificate: The PEM encoded X.509 public certificate, or certificate chain, of the
                certificate authority.
            name: The name of the authority. Tines defaults to ``default``.

        Returns:
            A ``Response`` with a 200 status and no data. The Tines docs say that the reply is a
            422 for a request that fails.
        """
        return self._transport.request(
            method="PATCH",
            path="/api/v1/admin/custom_certificate_authority",
            json=omit_none(values={"certificate": certificate, "name": name}),
        )
