from tapi.core import Response, Transport
from tapi.core.params import omit_none


class Files:
    """The files attached to a case, available as ``tines.cases.files``.

    A file is attached to a case by an activity. ``get``, ``create`` and the items of ``list``
    are that activity: ``id`` (which is the ``file_id`` of the other methods), ``activity_type``
    (``FILE_ATTACHED`` or ``FILE_ATTACHED_AND_COMMENTED``), ``value`` (the comment sent with the
    file), ``created_at``, ``file`` (an object with the ``filename`` and a ``url``) and ``user``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        case_id: int,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List the files of a case. ``GET /api/v2/cases/{case_id}/files``

        The endpoint is paginated and one call returns one page.

        Args:
            case_id: The ID of the case.
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``files``, the files of the page,
            and ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v2/cases/{case_id}/files",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )

    def get(self, *, case_id: int, file_id: int) -> Response:
        """Get a file of a case. ``GET /api/v2/cases/{case_id}/files/{file_id}``

        This returns the activity that attached the file. To get the file itself, use
        ``download``, and for its metadata alone, ``info``.

        Args:
            case_id: The ID of the case.
            file_id: The ID of the file, the ``id`` of the activity.

        Returns:
            A ``Response`` whose ``data`` is the activity, with ``case_id`` added.
        """
        return self._transport.request(
            method="GET", path=f"/api/v2/cases/{case_id}/files/{file_id}"
        )

    def create(
        self,
        *,
        case_id: int,
        filename: str,
        file_contents: str,
        value: str | None = None,
        author_email: str | None = None,
        team_case_block_id: int | None = None,
    ) -> Response:
        """Attach a file to a case. ``POST /api/v2/cases/{case_id}/files``

        The file is sent as Base64 text in a JSON body, and not as a multipart upload.

        Args:
            case_id: The ID of the case.
            filename: The name of the file.
            file_contents: The contents of the file, Base64 encoded. To encode bytes, use
                ``base64.b64encode(data).decode()``.
            value: A comment to add with the file, as Markdown. User mentions are written
                ``<@user-2435>``.
            author_email: The email address of the user who attaches the file.
            team_case_block_id: The ID of the file block to attach the file to. The reply then
                has a ``block_id``.

        Returns:
            A ``Response`` whose ``data`` is the activity that attached the file, with a 201
            status. The server accepted text that is not Base64 and an empty filename. The reply
            is a 422 when ``file_contents`` is missing, and a 404 with ``TeamCaseBlock not
            found`` for a block that does not exist.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v2/cases/{case_id}/files",
            json=omit_none(
                values={
                    "filename": filename,
                    "file_contents": file_contents,
                    "value": value,
                    "author_email": author_email,
                    "team_case_block_id": team_case_block_id,
                }
            ),
        )

    def delete(self, *, case_id: int, file_id: int) -> Response:
        """Delete a file of a case. ``DELETE /api/v2/cases/{case_id}/files/{file_id}``

        The Tines docs say that only the user who attached the file or an admin can delete it.

        Args:
            case_id: The ID of the case.
            file_id: The ID of the file.

        Returns:
            A ``Response`` with a 204 status and no data. Deleting it again is a 422 with ``You
            must provide a valid file attachment``.
        """
        return self._transport.request(
            method="DELETE", path=f"/api/v2/cases/{case_id}/files/{file_id}"
        )

    def download(self, *, case_id: int, file_id: int) -> Response:
        """Download a file of a case. ``GET /api/v2/cases/{case_id}/files/{file_id}/download``

        Args:
            case_id: The ID of the case.
            file_id: The ID of the file.

        Returns:
            A ``Response`` whose ``data`` is the file, decoded by its content type: text is a
            ``str`` and a binary file is ``bytes``. The ``Content-Disposition`` header is an
            attachment, except for images, which the Tines docs say are shown inline. The reply
            is a 404 with ``File not found`` for a file that does not exist.
        """
        return self._transport.request(
            method="GET", path=f"/api/v2/cases/{case_id}/files/{file_id}/download"
        )

    def info(self, *, case_id: int, file_id: int) -> Response:
        """Get the details of a file. ``GET /api/v2/cases/{case_id}/files/{file_id}/info``

        Args:
            case_id: The ID of the case.
            file_id: The ID of the file.

        Returns:
            A ``Response`` whose ``data`` is an object with ``filename``, ``content_type``,
            ``guid``, ``md5``, ``sha256``, ``sizeinbytes`` and ``base64encodedcontents``, the
            last of which only the OpenAPI document lists. The reply is a 404 with
            ``TeamCaseAction not found`` when there is no such file.
        """
        return self._transport.request(
            method="GET", path=f"/api/v2/cases/{case_id}/files/{file_id}/info"
        )
