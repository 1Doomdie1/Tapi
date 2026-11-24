from collections.abc import Sequence

from tapi.cases.types import TaskInput
from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_list


class Tasks:
    """The tasks of a case, available as ``tines.cases.tasks``.

    A task, as returned by ``get``, ``create`` and ``update`` and listed by ``list``, has ``id``,
    ``description``, ``completed``, ``assignees`` (a list of objects with ``id``, ``email``,
    ``first_name`` and ``last_name``), ``created_at`` and ``updated_at``.

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
        """List the tasks of a case. ``GET /api/v2/cases/{case_id}/tasks``

        The endpoint is paginated and one call returns one page.

        Args:
            case_id: The ID of the case.
            per_page: The number of results per page. Tines defaults to 20, and its docs give a
                maximum of 50, which the server did not enforce.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``tasks``, the tasks of the page, and
            ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v2/cases/{case_id}/tasks",
            params=omit_none(values={"per_page": per_page, "page": page}),
        )

    def get(self, *, case_id: int, task_id: int) -> Response:
        """Get a task. ``GET /api/v2/cases/{case_id}/tasks/{task_id}``

        Args:
            case_id: The ID of the case.
            task_id: The ID of the task.

        Returns:
            A ``Response`` whose ``data`` is an object with ``task``.
        """
        return self._transport.request(
            method="GET", path=f"/api/v2/cases/{case_id}/tasks/{task_id}"
        )

    def create(
        self,
        *,
        case_id: int,
        description: str,
        assignee_emails: Sequence[str] | None = None,
    ) -> Response:
        """Add a task to a case. ``POST /api/v2/cases/{case_id}/tasks``

        Args:
            case_id: The ID of the case.
            description: The description of the task.
            assignee_emails: The email addresses of the users to assign.

        Returns:
            A ``Response`` whose ``data`` is an object with ``task``, with a 201 status. The reply
            is a 400 with ``Users <email> not found`` for an assignee that is not a user, and a
            422 with ``Description cannot be blank`` for a blank description.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v2/cases/{case_id}/tasks",
            json=omit_none(
                values={
                    "description": description,
                    "assignee_emails": to_list(values=assignee_emails),
                }
            ),
        )

    def batch_create(self, *, case_id: int, tasks: Sequence[TaskInput]) -> Response:
        """Add several tasks to a case. ``POST /api/v2/cases/{case_id}/tasks/batch``

        Args:
            case_id: The ID of the case.
            tasks: The tasks to add, at most 25, each an object with a ``description`` and
                optionally ``assignee_emails``.

        Returns:
            A ``Response`` whose ``data`` is an object with ``tasks``, the created tasks, with a
            201 status. The reply is a 400 when ``tasks`` is empty (``tasks must be a non-empty
            array``), has more than 25 tasks (``Cannot create more than 25 tasks at once``) or
            names an assignee that is not a user.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v2/cases/{case_id}/tasks/batch",
            json={"tasks": to_list(values=tasks)},
        )

    def update(
        self,
        *,
        case_id: int,
        task_id: int,
        description: str | None = None,
        completed: bool | None = None,
        assignee_emails: Sequence[str] | None = None,
    ) -> Response:
        """Change a task. ``PATCH /api/v2/cases/{case_id}/tasks/{task_id}``

        Args:
            case_id: The ID of the case.
            task_id: The ID of the task.
            description: A new description.
            completed: Whether the task is completed.
            assignee_emails: The email addresses of the users to assign. They replace the assignees
                of the task.

        Returns:
            A ``Response`` whose ``data`` is an object with ``task``.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v2/cases/{case_id}/tasks/{task_id}",
            json=omit_none(
                values={
                    "description": description,
                    "completed": completed,
                    "assignee_emails": to_list(values=assignee_emails),
                }
            ),
        )

    def delete(self, *, case_id: int, task_id: int) -> Response:
        """Delete a task. ``DELETE /api/v2/cases/{case_id}/tasks/{task_id}``

        Args:
            case_id: The ID of the case.
            task_id: The ID of the task.

        Returns:
            A ``Response`` with a 204 status and no data, as the OpenAPI document says. The Tines
            docs show a JSON object with ``destroyed_id``, which the server does not return.
        """
        return self._transport.request(
            method="DELETE", path=f"/api/v2/cases/{case_id}/tasks/{task_id}"
        )
