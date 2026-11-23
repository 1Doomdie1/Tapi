from datetime import datetime

from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_iso
from tapi.workbench.types import ConversationType


class Workbench:
    """Workbench conversations, available as ``tines.workbench``.

    A conversation is a chat with Tines AI. These methods read conversations across every surface
    that has them: Workbench itself, AI agents and story authoring. They cannot start a
    conversation or send a message.

    A conversation, as listed by ``list``, has ``guid`` (its identifier), ``title``, ``source``
    (where it came from, such as ``tines`` or ``slack``), ``conversation_type``, ``source_type``
    and ``source_id`` (the resource it is linked to, such as a ``Story``, or ``null``),
    ``favorited``, ``creator_id`` and ``creator_type`` (``User`` or ``Agent``), ``created_at``,
    ``updated_at``, ``tool_uses_count``, ``credits_used`` and ``billed_cost`` (an object with
    ``currency`` and ``amount``, a string with two decimals). ``get`` returns the same fields and
    also ``status``, ``usage`` and ``steps``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def list(
        self,
        *,
        search: str | None = None,
        favorited: bool | None = None,
        creator_id: int | None = None,
        conversation_type: ConversationType | None = None,
        created_after: datetime | str | None = None,
        created_before: datetime | str | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List conversations. ``GET /api/v1/workbench``

        Lists AI conversations across all surfaces, including Workbench, AI agents and story
        authoring.

        The endpoint is paginated and one call returns one page. Read ``data["meta"]`` to decide
        whether to ask for the next page.

        Args:
            search: Only conversations whose title matches this text.
            favorited: Only conversations that are favorited (``True``) or that are not
                (``False``). Every conversation is returned when this is left out.
            creator_id: Only conversations created by the user with this ID.
            conversation_type: Only conversations of this type: ``workbench``, ``task_agent``,
                ``chat_agent`` or ``workbench_storyboard``.
            created_after: Only conversations created at or after this time, as a ``datetime`` or
                an ISO 8601 string with a time, such as ``2026-11-01T00:00:00Z``. A datetime
                without a timezone is treated as UTC. Tines refuses a date without a time.
            created_before: Only conversations created at or before this time, in the same
                formats. It must be later than ``created_after`` when both are given.
            per_page: The number of results per page. Tines defaults to 20 and caps it at 500.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``conversations``, the conversations
            of the page, and ``meta``, the pagination details: ``current_page``,
            ``previous_page`` and ``next_page`` (links), ``next_page_number``, ``per_page``,
            ``pages`` (the number of pages) and ``count``. The reply is a 400 for a
            ``conversation_type`` that is not supported (``conversation_type is not a valid
            value``), a timestamp that is not valid (``created_after must be an ISO8601
            timestamp``), a ``created_after`` that is not before ``created_before``, and a
            ``per_page`` or ``page`` that is not a positive integer.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/workbench",
            params=omit_none(
                values={
                    "search": search,
                    "favorited": favorited,
                    "creator_id": creator_id,
                    "conversation_type": conversation_type,
                    "created_after": to_iso(value=created_after),
                    "created_before": to_iso(value=created_before),
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )

    def get(self, *, conversation_id: str) -> Response:
        """Get a conversation. ``GET /api/v1/workbench/{conversation_id}``

        Retrieves a conversation, with its metadata, its aggregate AI usage and its full
        transcript.

        Args:
            conversation_id: The GUID of the conversation, which is the ``guid`` of a conversation
                that ``list`` returns.

        Returns:
            A ``Response`` whose ``data`` is the conversation, with the fields that ``list``
            returns and also:

            - ``status``: ``in_progress``, ``complete``, ``cancelled`` or ``failed``.
            - ``usage``: the aggregate model token usage, an object with ``input_tokens``,
              ``output_tokens``, ``cached_read_input_tokens``, ``cached_write_input_tokens`` and
              ``model_ids`` (a list of strings).
            - ``steps``: the messages of the conversation. A message has a ``role`` of ``user``,
              ``assistant`` or ``tool``. A user or assistant message has ``contents``, a list of
              objects with a ``type``: ``text`` (with ``text``), ``reasoning`` for the assistant
              (with ``text``, ``started_at`` and ``completed_at``) or ``message_context`` for the
              user (with ``message_context``, an object with ``url``). A tool message has
              ``name``, ``inputs`` and ``output``, an object whose keys depend on the tool. The
              Tines docs show ``body``, ``meta``, ``status`` and ``headers`` for it, which the
              tools seen live did not return.

            The reply is a 404 with ``Conversation not found`` for a GUID that does not exist.
        """
        return self._transport.request(method="GET", path=f"/api/v1/workbench/{conversation_id}")
