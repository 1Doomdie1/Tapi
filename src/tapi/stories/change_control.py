from tapi.core import Response, Transport
from tapi.core.params import omit_none


class ChangeControl:
    """The change requests of a story, available as ``tines.stories.change_control``.

    These are the change request operations that Tines groups under a story. The change request
    endpoints at ``/api/v1/change_requests`` belong to ``tines.change_requests``.

    A reply of ``create``, ``view``, ``approve``, ``cancel`` and ``reject`` has ``id`` (the ID of
    the live story), ``draft_id`` and ``draft_name`` (the draft that holds the change request) and
    ``change_request``: an object with ``id`` and ``status``. ``create`` and ``view`` add ``name``,
    ``description``, ``participants`` (a list of user IDs), ``live_story_export`` and
    ``draft_export`` (the stories as JSON strings), and ``approve``, ``cancel`` and ``reject`` add
    ``participants`` or a ``comment``.

    Args:
        transport: The transport used to send requests.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport

    def create(
        self,
        *,
        story_id: int,
        title: str | None = None,
        description: str | None = None,
        draft_id: int | None = None,
    ) -> Response:
        """Create a change request. ``POST /api/v1/stories/{story_id}/change_request``

        Args:
            story_id: The ID of the story.
            title: The name of the change request. The Tines docs call it the change request name
                in the reply.
            description: A description of the change request. To mention a user, write
                ``<@user-2435>`` with the ID of the user.
            draft_id: The ID of the draft.

        Returns:
            A ``Response`` whose ``data`` is the created change request. Its ``status`` is
            ``PENDING`` or ``APPROVED``.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/stories/{story_id}/change_request",
            json=omit_none(
                values={"title": title, "description": description, "draft_id": draft_id}
            ),
        )

    def view(self, *, story_id: int, draft_id: int | None = None) -> Response:
        """View a change request. ``GET /api/v1/stories/{story_id}/change_request/view``

        Shows the current change request of a story.

        Args:
            story_id: The ID of the story.
            draft_id: The ID of the draft.

        Returns:
            A ``Response`` whose ``data`` is the current change request. ``change_request`` is
            ``null`` when no change request has been submitted. The reply is a 404 with the
            message ``Story not found`` for a story without change control.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/stories/{story_id}/change_request/view",
            params=omit_none(values={"draft_id": draft_id}),
        )

    def generate_description(self, *, story_id: int, draft_id: int) -> Response:
        """Generate a description. ``GET /api/v1/stories/{story_id}/change_request/ai_description``

        Tines writes a description of the changes of a change request. AI features must be enabled
        for it to succeed.

        Args:
            story_id: The ID of the story.
            draft_id: The ID of the draft.

        Returns:
            A ``Response`` whose ``data`` is an object with ``change_request_ai_description``, the
            generated text. The reply is a 404 with the message ``Draft not found`` when the draft
            does not exist.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/stories/{story_id}/change_request/ai_description",
            params={"draft_id": draft_id},
        )

    def approve(self, *, story_id: int, change_request_id: int) -> Response:
        """Approve a change request. ``POST /api/v1/stories/{story_id}/change_request/approve``

        Args:
            story_id: The ID of the story.
            change_request_id: The ID of the change request.

        Returns:
            A ``Response`` whose ``data`` is the status of the change request, ``APPROVED``. The
            reply is a 401 when your key may not approve it, for example because it lacks the
            change control permissions, or because it belongs to the author of a change request on
            a tenant that requires approval. A tenant that does not require it let the author
            approve. The reply is a 404 with the message ``StoryChangeRequest not found`` when no
            change request has that ID.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/stories/{story_id}/change_request/approve",
            json={"change_request_id": change_request_id},
        )

    def cancel(
        self,
        *,
        story_id: int,
        change_request_id: int,
        comment: str | None = None,
    ) -> Response:
        """Cancel a change request. ``POST /api/v1/stories/{story_id}/change_request/cancel``

        Cancels your own change request. If you are not the author, Tines rejects it instead.

        Args:
            story_id: The ID of the story.
            change_request_id: The ID of the change request.
            comment: Feedback for the author, up to 1,000 characters. Only when you are not the
                author: a comment on your own change request is answered with a 400.

        Returns:
            A ``Response`` whose ``data`` has the ``change_request`` with its new ``status``
            (``IN_PROGRESS`` when the author cancels it, ``REJECTED`` otherwise) and ``comment``, an
            object with ``id``, ``message`` and ``created_at``, or ``null``. A change request that
            was pending or approved can be canceled.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/stories/{story_id}/change_request/cancel",
            json=omit_none(values={"change_request_id": change_request_id, "comment": comment}),
        )

    def reject(
        self,
        *,
        story_id: int,
        change_request_id: int,
        comment: str | None = None,
    ) -> Response:
        """Reject a change request. ``POST /api/v1/stories/{story_id}/change_request/reject``

        Rejects a change request. If you are its author, Tines cancels it instead.

        Args:
            story_id: The ID of the story.
            change_request_id: The ID of the change request.
            comment: Feedback for the author, up to 1,000 characters. Not accepted when you are the
                author: Tines answers with a 400 and leaves the change request unchanged.

        Returns:
            A ``Response`` whose ``data`` has the ``change_request`` with its new ``status``
            (``REJECTED``, or ``IN_PROGRESS`` when the author cancels it) and ``comment``, an object
            with ``id``, ``message`` and ``created_at``, or ``null``.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/stories/{story_id}/change_request/reject",
            json=omit_none(values={"change_request_id": change_request_id, "comment": comment}),
        )

    def promote(
        self,
        *,
        story_id: int,
        change_request_id: int,
        bypass_approval: bool | None = None,
        bypass_approval_reason: str | None = None,
        delete_draft: bool | None = None,
    ) -> Response:
        """Promote a change request. ``POST /api/v1/stories/{story_id}/change_request/promote``

        Promotes the changes of a change request to the live story. Bypassing the approval needs the
        permission to manage the story on its team, is recorded in the audit trail and sends a
        notification.

        Args:
            story_id: The ID of the story.
            change_request_id: The ID of the change request.
            bypass_approval: Whether to promote a change request that is still pending, skipping its
                approval.
            bypass_approval_reason: The reason recorded in the audit trail. Tines records ``Approval
                bypassed via API`` when the approval is bypassed without one.
            delete_draft: Whether to delete the draft after promoting it.

        Returns:
            A ``Response`` whose ``data`` is the updated live story.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/stories/{story_id}/change_request/promote",
            json=omit_none(
                values={
                    "change_request_id": change_request_id,
                    "bypass_approval": bypass_approval,
                    "bypass_approval_reason": bypass_approval_reason,
                    "delete_draft": delete_draft,
                }
            ),
        )
