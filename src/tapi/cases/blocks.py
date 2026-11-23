from collections.abc import Sequence

from tapi.cases.types import BlockColor, BlockType, FileElement, NoteElement
from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_list


class Blocks:
    """The blocks of a case, available as ``tines.cases.blocks``.

    A block is a section of the case page. A block, as returned by ``get``, ``create`` and
    ``update`` and listed by ``list``, has ``id``, ``slug`` (such as ``blk_...``), ``title``,
    ``block_type``, ``color``, ``position``, ``hidden``, ``default_collapsed``,
    ``block_group_id`` (the block group that holds it, or ``null``), ``elements``, ``created_at``
    and ``updated_at``. An element, as returned by ``get_element`` and ``update_element``, has
    ``id``, ``element_id``, ``element_type``, ``content``, ``note_type``, ``color``,
    ``sensitive``, ``file``, ``annotation`` (for a file), ``author``, ``created_at`` and
    ``updated_at``. The methods for elements take the ``element_id`` of the element, which is
    not its ``id``.

    The methods for blocks take a ``block_id`` that can be the numeric ID or the slug of the
    block. The methods for elements need the numeric ID: a slug was a 404.

    A new case has one block already, the metadata block, and a second one is refused.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        case_id: int,
        block_type: BlockType | None = None,
        block_group_id: int | str | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List the blocks of a case. ``GET /api/v2/cases/{case_id}/blocks``

        The endpoint is paginated and one call returns one page.

        Args:
            case_id: The ID of the case.
            block_type: Only blocks of this type: ``note``, ``file``, ``linked_cases``,
                ``metadata``, ``closure_conditions``, ``case_action``, ``block_group`` or
                ``html``. The OpenAPI document names only four of them.
            block_group_id: Only blocks inside this block group, by ID or slug.
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``blocks``, the blocks of the page,
            and ``meta``. The reply is a 422 that lists the valid values for a ``block_type``
            that does not exist.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v2/cases/{case_id}/blocks",
            params=omit_none(
                values={
                    "block_type": block_type,
                    "block_group_id": block_group_id,
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )

    def get(self, *, case_id: int, block_id: int | str) -> Response:
        """Get a block. ``GET /api/v2/cases/{case_id}/blocks/{block_id}``

        Args:
            case_id: The ID of the case.
            block_id: The ID or the slug of the block.

        Returns:
            A ``Response`` whose ``data`` is an object with ``block``.
        """
        return self._transport.request(
            method="GET", path=f"/api/v2/cases/{case_id}/blocks/{block_id}"
        )

    def create(
        self,
        *,
        case_id: int,
        title: str,
        block_type: BlockType,
        color: BlockColor | None = None,
        elements: Sequence[NoteElement | FileElement] | None = None,
        position: int | None = None,
        hidden: bool | None = None,
        default_collapsed: bool | None = None,
        block_group_id: int | str | None = None,
        author_email: str | None = None,
    ) -> Response:
        """Add a block to a case. ``POST /api/v2/cases/{case_id}/blocks``

        Args:
            case_id: The ID of the case.
            title: The title of the block. The server refuses a block without one, as the Tines
                docs say and the OpenAPI document does not.
            block_type: The type: ``note``, ``file``, ``linked_cases``, ``metadata``,
                ``closure_conditions``, ``case_action``, ``block_group`` or ``html``. A case has a
                metadata block already, and a second is a 422.
            color: The color: ``primary``, ``white``, ``gold``, ``magenta``, ``green``,
                ``blue``, ``red``, ``mint`` or ``indigo``. Only note, file, block group and HTML
                blocks have a color. ``primary`` is the same as ``white``, which is what a block
                shows. A new block is white.
            elements: The elements to put in the block, each a note element with a ``content``
                and a ``note_type``, or a file element with a ``filename`` and its
                ``file_contents``. See ``tapi.cases.NoteElement`` and ``tapi.cases.FileElement``.
                A note block needs a note element and an HTML block an HTML element, and a block
                without one is a 422.
            position: The zero-based position of the block in the case, a non-negative integer.
                A number past the end puts the block last. The OpenAPI document also names
                ``top`` and ``bottom``, which were a 400.
            hidden: Whether the block is hidden.
            default_collapsed: Whether the block is collapsed by default. Tines defaults to
                false.
            block_group_id: The ID or the slug of the block group that holds the block.
            author_email: The email address of the author of the block. An address that is not a
                user was accepted.

        Returns:
            A ``Response`` whose ``data`` is an object with ``block``, with a 201 status.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v2/cases/{case_id}/blocks",
            json=omit_none(
                values={
                    "title": title,
                    "block_type": block_type,
                    "color": color,
                    "elements": to_list(values=elements),
                    "position": position,
                    "hidden": hidden,
                    "default_collapsed": default_collapsed,
                    "block_group_id": block_group_id,
                    "author_email": author_email,
                }
            ),
        )

    def update(
        self,
        *,
        case_id: int,
        block_id: int | str,
        title: str | None = None,
        color: BlockColor | None = None,
        position: int | None = None,
        hidden: bool | None = None,
        default_collapsed: bool | None = None,
        block_group_id: int | str | None = None,
    ) -> Response:
        """Change a block. ``PATCH /api/v2/cases/{case_id}/blocks/{block_id}``

        The Tines documentation shows this operation as ``PUT``. The OpenAPI document lists the
        same operation under ``PUT`` and ``PATCH``, and tapi uses ``PATCH``.

        Args:
            case_id: The ID of the case.
            block_id: The ID or the slug of the block.
            title: A new title.
            color: A new color: ``primary``, ``white``, ``gold``, ``magenta``, ``green``,
                ``blue``, ``red``, ``mint`` or ``indigo``.
            position: A new zero-based position in the case.
            hidden: Whether the block is hidden.
            default_collapsed: Whether the block is collapsed by default.
            block_group_id: The ID or the slug of the block group to move the block into. The
                Tines docs take ``null`` to remove the block from its group, which tapi cannot
                send.

        Returns:
            A ``Response`` whose ``data`` is an object with ``block``.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v2/cases/{case_id}/blocks/{block_id}",
            json=omit_none(
                values={
                    "title": title,
                    "color": color,
                    "position": position,
                    "hidden": hidden,
                    "default_collapsed": default_collapsed,
                    "block_group_id": block_group_id,
                }
            ),
        )

    def delete(
        self,
        *,
        case_id: int,
        block_id: int | str,
        include_children: bool | None = None,
    ) -> Response:
        """Delete a block. ``DELETE /api/v2/cases/{case_id}/blocks/{block_id}``

        Args:
            case_id: The ID of the case.
            block_id: The ID or the slug of the block.
            include_children: For a block group, whether to delete the blocks inside it too.
                Without it, the blocks stay and are no longer in a group.

        Returns:
            A ``Response`` with a 204 status and no data.
        """
        return self._transport.request(
            method="DELETE",
            path=f"/api/v2/cases/{case_id}/blocks/{block_id}",
            params=omit_none(values={"include_children": include_children}),
        )

    def get_element(self, *, case_id: int, block_id: int, element_id: int) -> Response:
        """Get an element. ``GET /api/v2/cases/{case_id}/blocks/{block_id}/elements/{element_id}``

        An element is one part of a block, such as a note or a file.

        Args:
            case_id: The ID of the case.
            block_id: The ID of the block. A slug was a 404.
            element_id: The ``element_id`` of the element. Its ``id`` was a 404.

        Returns:
            A ``Response`` whose ``data`` is the element. The reply is a 404 with
            ``TeamCaseBlockElement not found`` for an element that does not exist.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v2/cases/{case_id}/blocks/{block_id}/elements/{element_id}",
        )

    def update_element(
        self,
        *,
        case_id: int,
        block_id: int,
        element_id: int,
        content: str | None = None,
        color: BlockColor | None = None,
        sensitive: bool | None = None,
        author_email: str | None = None,
        annotation: str | None = None,
    ) -> Response:
        """Edit element. ``PATCH /api/v2/cases/{case_id}/blocks/{block_id}/elements/{element_id}``

        The Tines documentation shows this operation as ``PUT``. The OpenAPI document lists the
        same operation under ``PUT`` and ``PATCH``, and tapi uses ``PATCH``.

        Args:
            case_id: The ID of the case.
            block_id: The ID of the block. A slug was a 404.
            element_id: The ``element_id`` of the element, not its ``id``.
            content: New content for a note element, as Markdown.
            color: A new color for a note element. The Tines docs deprecate it: set the color of
                the block instead.
            sensitive: Whether the element is sensitive. Only the OpenAPI document lists it, and
                the server answered 200 and left the element as it was.
            author_email: The email address of the author of a note element. Only the Tines docs
                list it.
            annotation: A new annotation for a file element. Only the Tines docs list it.

        Returns:
            A ``Response`` whose ``data`` is the updated element. A call that sends nothing is a
            200.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v2/cases/{case_id}/blocks/{block_id}/elements/{element_id}",
            json=omit_none(
                values={
                    "content": content,
                    "color": color,
                    "sensitive": sensitive,
                    "author_email": author_email,
                    "annotation": annotation,
                }
            ),
        )

    def append_element_content(
        self,
        *,
        case_id: int,
        block_id: int,
        element_id: int,
        content: str,
        author_email: str | None = None,
    ) -> Response:
        """Append. ``POST /api/v2/cases/{case_id}/blocks/{block_id}/elements/{element_id}/content``

        This adds text to the end of a note element. Only note elements can be added to.

        Args:
            case_id: The ID of the case.
            block_id: The ID of the block. A slug was a 404.
            element_id: The ``element_id`` of the element, not its ``id``.
            content: The text to add, as Markdown.
            author_email: The email address of the author of the note.

        Returns:
            A ``Response`` whose ``data`` is the updated element. The reply is a 422 with
            ``Element type does not support append`` for a file element.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v2/cases/{case_id}/blocks/{block_id}/elements/{element_id}/content",
            json=omit_none(values={"content": content, "author_email": author_email}),
        )
