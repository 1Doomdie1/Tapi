from tapi.admin.types import SmtpAuthType, SmtpEncryptionMode
from tapi.core import Response, Transport
from tapi.core.params import omit_none


class Smtp:
    """The SMTP configuration of a self-hosted tenant, available as ``tines.admin.smtp``.

    The routes exist only on self-hosted tenants, and the Tines docs say that a Tines cloud tenant
    answers 403. A tenant that has no configuration saved through the API uses the SMTP settings
    of its environment.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def get(self) -> Response:
        """Get the SMTP configuration. ``GET /api/v1/admin/smtp``

        Returns:
            A ``Response`` whose ``data`` is an object with ``address``, ``port``, ``domain`` (or
            ``null``), ``user_name`` (or ``null``), ``auth_type`` (or ``null``),
            ``encryption_mode``, ``verify_ssl_certificate``, ``ca_path`` (or ``null``), ``ca_file``
            (or ``null``), ``open_timeout`` and ``read_timeout`` (seconds), ``source`` (``database``
            for the configuration saved through the API, ``environment`` for the settings of the
            tenant environment) and ``password_set`` (whether a password is saved: the password is
            never returned). ``warnings``, an object keyed by field, is returned when the saved
            configuration has warnings. A tenant that is not self-hosted gets a 403, with ``data``
            an object whose ``error`` is ``This endpoint is only available on self-hosted
            installations``.
        """
        return self._transport.request(method="GET", path="/api/v1/admin/smtp")

    def update(
        self,
        *,
        address: str,
        port: int,
        encryption_mode: SmtpEncryptionMode,
        verify_ssl_certificate: bool,
        domain: str | None = None,
        user_name: str | None = None,
        password: str | None = None,
        auth_type: SmtpAuthType | None = None,
        ca_path: str | None = None,
        ca_file: str | None = None,
        open_timeout: int | None = None,
        read_timeout: int | None = None,
    ) -> Response:
        """Replace the SMTP configuration. ``PATCH /api/v1/admin/smtp``

        Creates the configuration, or replaces all of it: a field that is left out is cleared,
        except the two timeouts, which Tines sets to 30 seconds.

        Args:
            address: The address of the SMTP server, at most 255 characters.
            port: The port of the SMTP server, from 1 to 65535.
            encryption_mode: ``none``, ``tls``, ``starttls_auto`` or ``starttls_strict``.
            verify_ssl_certificate: Whether Tines verifies the certificate of the server.
            domain: The domain sent in the SMTP greeting, at most 255 characters.
            user_name: The user name for the server, at most 255 characters. It is required when
                ``auth_type`` is set.
            password: The password for the server, at most 1024 characters. It is required when
                ``auth_type`` is set. Tines never returns it and does not keep the old one, so send
                it every time.
            auth_type: ``plain``, ``login`` or ``cram_md5``. When it is left out, Tines does not
                authenticate to the server.
            ca_path: The path of a directory of CA certificates, or of a PEM file, on the
                installation, at most 4096 characters. ``ca_file`` takes precedence over it.
            ca_file: The path of a CA certificate file on the installation, at most 4096 characters.
            open_timeout: The seconds to wait for the connection to open, from 1 to 120.
            read_timeout: The seconds to wait for a read, from 1 to 120.

        Returns:
            A ``Response`` with a 200 status. ``data`` is ``None``, or an object with ``warnings``
            when the saved configuration has warnings.
        """
        return self._transport.request(
            method="PATCH",
            path="/api/v1/admin/smtp",
            json=omit_none(
                values={
                    "address": address,
                    "port": port,
                    "encryption_mode": encryption_mode,
                    "verify_ssl_certificate": verify_ssl_certificate,
                    "domain": domain,
                    "user_name": user_name,
                    "password": password,
                    "auth_type": auth_type,
                    "ca_path": ca_path,
                    "ca_file": ca_file,
                    "open_timeout": open_timeout,
                    "read_timeout": read_timeout,
                }
            ),
        )

    def delete(self) -> Response:
        """Delete the SMTP configuration. ``DELETE /api/v1/admin/smtp``

        Removes only the configuration saved through the API. The tenant then uses the SMTP
        settings of its environment, which are not changed.

        Returns:
            A ``Response`` with a 204 status and no data. The reply is the same when there was no
            configuration to delete. The Tines docs say that a Tines cloud tenant answers 403.
        """
        return self._transport.request(method="DELETE", path="/api/v1/admin/smtp")
