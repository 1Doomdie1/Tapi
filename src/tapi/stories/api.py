from collections.abc import Mapping, Sequence
from typing import Any

from tapi.core import Response, Transport
from tapi.core.params import omit_none, to_list
from tapi.stories.actions import Actions
from tapi.stories.change_control import ChangeControl
from tapi.stories.drafts import Drafts
from tapi.stories.events import Events
from tapi.stories.groups import Groups
from tapi.stories.links import Links
from tapi.stories.notes import Notes
from tapi.stories.owners import Owners
from tapi.stories.recipients import Recipients
from tapi.stories.runs import Runs
from tapi.stories.types import (
    DiagramContent,
    DiagramFormat,
    ImportMode,
    KeepEventsFor,
    SendToStoryAccess,
    SendToStoryAccessSource,
    StoryFilter,
    StoryMode,
    StoryOrder,
)
from tapi.stories.versions import Versions


class Stories:
    """Stories, available as ``tines.stories``.

    A story, as returned by ``get``, ``create``, ``update`` and ``import_`` and listed by ``list``,
    has ``id``, ``guid``, ``slug``, ``name``, ``description`` (``null`` if there is none),
    ``user_id`` (the creator), ``team_id``, ``folder_id`` (``null`` at the root level), ``tags``
    (a list of tag names), ``owners`` (a list of user IDs), ``recipients`` (a list of objects with
    an ``address``), ``keep_events_for`` (seconds), ``disabled``, ``priority``, ``published``,
    ``locked``, ``change_control_enabled``, ``monitor_failures``, ``actions_with_monitoring`` (a
    list of action IDs), ``entry_agent_id`` and ``exit_agents`` (the entry and exit actions),
    ``mode`` (``LIVE`` or ``TEST``), ``created_at``, ``updated_at``, ``edited_at`` (ISO 8601
    timestamps; ``edited_at`` tracks changes to the story itself), the Send to Story fields
    ``send_to_story_enabled``, ``send_to_story_access_source``, ``send_to_story_access``,
    ``shared_team_slugs``, ``send_to_story_timeout_enabled``,
    ``send_to_story_timeout_duration_seconds`` and
    ``send_to_story_skill_use_requires_confirmation``, and the API fields ``api_enabled``,
    ``api_entry_actions``, ``api_exit_actions`` and ``api_name``. A tenant can add more fields,
    such as ``change_control_require_owner_approval``.

    Args:
        transport: The transport used to send requests.

    Attributes:
        actions: The actions of stories, with their events, logs and memory. See
            ``tapi.stories.Actions``.
        events: The events of the tenant. See ``tapi.stories.Events``.
        links: The links between actions. See ``tapi.stories.Links``.
        notes: The notes on the storyboard. See ``tapi.stories.Notes``.
        drafts: The drafts of a story. See ``tapi.stories.Drafts``.
        owners: The owners of a story. See ``tapi.stories.Owners``.
        recipients: The monitoring recipients of a story. See ``tapi.stories.Recipients``.
        runs: Story runs. See ``tapi.stories.Runs``.
        groups: Group runs. See ``tapi.stories.Groups``.
        versions: Story versions. See ``tapi.stories.Versions``.
        change_control: Change requests of a story. See ``tapi.stories.ChangeControl``.
    """

    def __init__(self, *, transport: Transport) -> None:
        self._transport = transport
        self.actions = Actions(transport=transport)
        self.events = Events(transport=transport)
        self.links = Links(transport=transport)
        self.notes = Notes(transport=transport)
        self.drafts = Drafts(transport=transport)
        self.owners = Owners(transport=transport)
        self.recipients = Recipients(transport=transport)
        self.runs = Runs(transport=transport)
        self.groups = Groups(transport=transport)
        self.versions = Versions(transport=transport)
        self.change_control = ChangeControl(transport=transport)

    def list(
        self,
        *,
        team_id: int | None = None,
        folder_id: int | None = None,
        tags: Sequence[str] | None = None,
        search: str | None = None,
        filter: StoryFilter | None = None,
        order: StoryOrder | None = None,
        include_live_activity: bool | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List stories. ``GET /api/v1/stories``

        The endpoint is paginated and one call returns one page. Only live stories are listed.

        Args:
            team_id: Only stories of this team.
            folder_id: Only stories in this folder.
            tags: Only stories with these tag names. Sent as ``tags[]``, once per name.
            search: Only stories whose name matches this text.
            filter: Only stories that match one condition: ``SEND_TO_STORY_ENABLED``,
                ``HIGH_PRIORITY``, ``API_ENABLED``, ``FAVORITE``, ``CHANGE_CONTROL_ENABLED``,
                ``CHANGE_CONTROL_DISABLED``, ``ENABLED``, ``DISABLED`` or ``LOCKED``. The server
                also accepts ``ALL_STORIES``, ``WORKBENCH_ENABLED`` and ``TUNNELS_ENABLED``, which
                neither the Tines docs nor its OpenAPI document list. The deprecated ``PUBLISHED``
                is not offered.
            order: How to sort the stories: ``NAME``, ``NAME_DESC``, ``RECENTLY_EDITED``,
                ``LEAST_RECENTLY_EDITED``, ``ACTION_COUNT_ASC``, ``ACTION_COUNT_DESC``,
                ``CONCURRENT_RUNS_COUNT_DESC``, ``PENDING_ACTION_RUNS_COUNT_DESC`` or
                ``NOT_WORKING_ACTIONS_COUNT_DESC``. On one tenant ``ACTION_COUNT_ASC`` and
                ``ACTION_COUNT_DESC`` were answered with a 500 after about 35 seconds, which is
                longer than the default timeout of ``Tines``.
            include_live_activity: Add ``pending_action_runs_count``, ``concurrent_runs_count``,
                ``tokens_used_percentage`` and ``not_working_actions_count`` to each story. Tines
                defaults to ``False``.
            per_page: The number of results per page. Tines defaults to 20 and caps it at 500.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``stories``, the stories of the page,
            and ``meta``, the pagination details.
        """
        return self._transport.request(
            method="GET",
            path="/api/v1/stories",
            params=omit_none(
                values={
                    "team_id": team_id,
                    "folder_id": folder_id,
                    "tags[]": to_list(values=tags),
                    "search": search,
                    "filter": filter,
                    "order": order,
                    "include_live_activity": include_live_activity,
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )

    def get(
        self,
        *,
        story_id: int,
        story_mode: StoryMode | None = None,
        draft_id: int | None = None,
        include_live_activity: bool | None = None,
    ) -> Response:
        """Get a story. ``GET /api/v1/stories/{story_id}``

        Args:
            story_id: The ID of the story to retrieve.
            story_mode: The mode of the story to retrieve: ``TEST`` or ``LIVE``.
            draft_id: The ID of the draft to retrieve.
            include_live_activity: Add ``pending_action_runs_count``, ``concurrent_runs_count``
                and ``tokens_used_percentage`` to the story. Tines defaults to ``False``.

        Returns:
            A ``Response`` whose ``data`` is the story. The reply is a 404 with the message
            ``Story not found`` when no story with that ID is visible to your key, and a 400 when
            ``story_mode`` is ``TEST`` for a story without change control.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/stories/{story_id}",
            params=omit_none(
                values={
                    "story_mode": story_mode,
                    "draft_id": draft_id,
                    "include_live_activity": include_live_activity,
                }
            ),
        )

    def create(
        self,
        *,
        team_id: int,
        name: str | None = None,
        description: str | None = None,
        keep_events_for: KeepEventsFor | None = None,
        folder_id: int | None = None,
        tags: Sequence[str] | None = None,
        disabled: bool | None = None,
        priority: bool | None = None,
    ) -> Response:
        """Create a story. ``POST /api/v1/stories``

        Args:
            team_id: The ID of the team the story is added to.
            name: The name of the story.
            description: A description of the story.
            keep_events_for: How long events are kept, in seconds: ``3600``, ``21600``, ``86400``,
                ``259200``, ``604800``, ``1209600``, ``2592000``, ``5184000``, ``7776000``,
                ``15552000`` or ``31536000``.
            folder_id: The ID of the folder the story is added to.
            tags: Tag names used to classify the story. The Tines docs say that Tines creates the
                tags, but a request with ``tags`` was answered with a 500 and created nothing,
                even for tags that exist. Create the story without them and add the tags with
                ``update`` and ``add_tag_names``.
            disabled: Whether the story is disabled. Tines defaults to ``False``.
            priority: Whether the story is high priority. Tines defaults to ``False``. A tenant
                without priority processing refuses ``True`` with a 422.

        Returns:
            A ``Response`` whose ``data`` is the created story, with a 201 status. A new story has
            no owners and one recipient that Tines adds.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/stories",
            json=omit_none(
                values={
                    "team_id": team_id,
                    "name": name,
                    "description": description,
                    "keep_events_for": keep_events_for,
                    "folder_id": folder_id,
                    "tags": to_list(values=tags),
                    "disabled": disabled,
                    "priority": priority,
                }
            ),
        )

    def update(
        self,
        *,
        story_id: int,
        name: str | None = None,
        description: str | None = None,
        add_tag_names: Sequence[str] | None = None,
        remove_tag_names: Sequence[str] | None = None,
        keep_events_for: KeepEventsFor | None = None,
        disabled: bool | None = None,
        locked: bool | None = None,
        priority: bool | None = None,
        webhook_api_enabled: bool | None = None,
        api_entry_action_id: int | None = None,
        api_exit_action_ids: Sequence[int] | None = None,
        send_to_story_access_source: SendToStoryAccessSource | None = None,
        entry_action_id: int | None = None,
        exit_action_ids: Sequence[int] | None = None,
        send_to_story_access: SendToStoryAccess | None = None,
        shared_team_slugs: Sequence[str] | None = None,
        send_to_story_skill_use_requires_confirmation: bool | None = None,
        team_id: int | None = None,
        folder_id: int | None = None,
        change_control_enabled: bool | None = None,
        draft_id: int | None = None,
        monitor_failures: bool | None = None,
    ) -> Response:
        """Update a story. ``PATCH /api/v1/stories/{story_id}``

        If change control is enabled on the story and no ``draft_id`` is given, Tines updates a
        draft called ``test`` and leaves the live story as it is. The reply then describes the
        draft, with ``draft_id`` and ``draft_name``. A field left as ``None`` is not sent, and the
        story keeps its value. The Tines documentation shows this operation as ``PUT``. The
        OpenAPI document lists the same operation under ``PUT`` and ``PATCH``, and tapi uses
        ``PATCH``.

        Args:
            story_id: The ID of the story to update.
            name: The new name of the story.
            description: The new description of the story.
            add_tag_names: Tag names to add to the story. The tags must exist on the team of the
                story, or Tines answers with a 422.
            remove_tag_names: Tag names to remove from the story.
            keep_events_for: How long events are kept, in seconds: ``3600``, ``21600``, ``86400``,
                ``259200``, ``604800``, ``1209600``, ``2592000``, ``5184000``, ``7776000``,
                ``15552000`` or ``31536000``.
            disabled: Whether the story is disabled from running.
            locked: Whether the story is locked, which prevents edits. An update of a locked
                story was accepted on the tested tenant.
            priority: Whether the story runs with high priority. A tenant without priority
                processing refuses ``True`` with a 422.
            webhook_api_enabled: Whether the story can be run through its webhook API. Enabling it
                also needs ``api_entry_action_id`` and ``api_exit_action_ids``, and ``draft_id``
                if the story is not live.
            api_entry_action_id: The ID of the entry action of an API-enabled story. It must be a
                webhook action.
            api_exit_action_ids: The IDs of the exit actions of an API-enabled story.
            send_to_story_access_source: Where Send to Story can be used: ``STS``,
                ``STS_AND_WORKBENCH``, ``WORKBENCH`` or ``OFF``. Enabling it also needs
                ``entry_action_id`` and ``exit_action_ids``.
            entry_action_id: The ID of the entry action of a Send to Story story. It must be a
                webhook action.
            exit_action_ids: The IDs of the exit actions of a Send to Story story.
            send_to_story_access: Who may send to the story: ``TEAM``, ``GLOBAL`` or
                ``SPECIFIC_TEAMS``. Tines defaults to ``TEAM``. ``SPECIFIC_TEAMS`` also needs
                ``shared_team_slugs``.
            shared_team_slugs: The slugs of the teams that may send to the story.
            send_to_story_skill_use_requires_confirmation: Whether Workbench asks for confirmation
                before it runs the story.
            team_id: The ID of the team to move the story to.
            folder_id: The ID of the folder to move the story to. Tines moves a story to the root
                folder when this is empty. A parameter left as ``None`` is not sent, so tapi cannot
                do that yet.
            change_control_enabled: Whether change control is enabled on the story.
            draft_id: The ID of the draft to update.
            monitor_failures: Whether failures are monitored in the story.

        Returns:
            A ``Response`` whose ``data`` is the updated story.
        """
        return self._transport.request(
            method="PATCH",
            path=f"/api/v1/stories/{story_id}",
            json=omit_none(
                values={
                    "name": name,
                    "description": description,
                    "add_tag_names": to_list(values=add_tag_names),
                    "remove_tag_names": to_list(values=remove_tag_names),
                    "keep_events_for": keep_events_for,
                    "disabled": disabled,
                    "locked": locked,
                    "priority": priority,
                    "webhook_api_enabled": webhook_api_enabled,
                    "api_entry_action_id": api_entry_action_id,
                    "api_exit_action_ids": to_list(values=api_exit_action_ids),
                    "send_to_story_access_source": send_to_story_access_source,
                    "entry_action_id": entry_action_id,
                    "exit_action_ids": to_list(values=exit_action_ids),
                    "send_to_story_access": send_to_story_access,
                    "shared_team_slugs": to_list(values=shared_team_slugs),
                    "send_to_story_skill_use_requires_confirmation": (
                        send_to_story_skill_use_requires_confirmation
                    ),
                    "team_id": team_id,
                    "folder_id": folder_id,
                    "change_control_enabled": change_control_enabled,
                    "draft_id": draft_id,
                    "monitor_failures": monitor_failures,
                }
            ),
        )

    def delete(self, *, story_id: int) -> Response:
        """Delete a story. ``DELETE /api/v1/stories/{story_id}``

        Args:
            story_id: The ID of the story to delete.

        Returns:
            A ``Response`` with a 204 status and no data. The story can still be retrieved for a
            moment afterwards.
        """
        return self._transport.request(method="DELETE", path=f"/api/v1/stories/{story_id}")

    def batch_delete(self, *, ids: Sequence[int]) -> Response:
        """Delete many stories. ``DELETE /api/v1/stories/batch``

        Tines skips stories that are sync sources and live read-only sync destinations, and does
        not say which it skipped.

        Args:
            ids: The IDs of the stories to delete.

        Returns:
            A ``Response`` with a 204 status and no data. A list of one ID that does not exist is
            answered with a 404 and ``StoryContainer not found``. The stories can still be
            retrieved for a moment afterwards.
        """
        return self._transport.request(
            method="DELETE",
            path="/api/v1/stories/batch",
            json={"ids": to_list(values=ids)},
        )

    def export(
        self,
        *,
        story_id: int,
        randomize_urls: bool | None = None,
        clear_recipients: bool | None = None,
        draft_id: int | None = None,
    ) -> Response:
        """Export a story. ``GET /api/v1/stories/{story_id}/export``

        Args:
            story_id: The ID of the story to export.
            randomize_urls: Whether the page and webhook URLs of the story are randomized.
            clear_recipients: Whether the monitoring and email recipient fields of the story are
                cleared.
            draft_id: The ID of the draft to export.

        Returns:
            A ``Response`` whose ``data`` is the story in exported form, a JSON object that
            ``import_`` takes as ``data``. Its ``tags`` are objects with a ``name``. To get an image
            of the story instead, use ``diagram``.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/stories/{story_id}/export",
            params=omit_none(
                values={
                    "randomize_urls": randomize_urls,
                    "clear_recipients": clear_recipients,
                    "draft_id": draft_id,
                }
            ),
        )

    def import_(
        self,
        *,
        new_name: str,
        data: Mapping[str, Any],
        team_id: int,
        folder_id: int | None = None,
        mode: ImportMode | None = None,
        draft_name: str | None = None,
    ) -> Response:
        """Import a story. ``POST /api/v1/stories/import``

        Embedded substories in the story data are not imported.

        Args:
            new_name: The name of the imported story.
            data: The story in exported form, as ``export`` returns it.
            team_id: The ID of the team the story is added to.
            folder_id: The ID of the folder the story is added to.
            mode: ``new`` to create a new story, or ``versionReplace`` to update an existing one
                by name. Tines defaults to ``new``.
            draft_name: The name of the draft when change control is enabled. Tines defaults to
                ``Imported story``.

        Returns:
            A ``Response`` whose ``data`` is the imported story. The status is 200, although the
            OpenAPI document says 201. The tags of the exported story are kept.
        """
        return self._transport.request(
            method="POST",
            path="/api/v1/stories/import",
            json=omit_none(
                values={
                    "new_name": new_name,
                    "data": data,
                    "team_id": team_id,
                    "folder_id": folder_id,
                    "mode": mode,
                    "draft_name": draft_name,
                }
            ),
        )

    def diagram(
        self,
        *,
        story_id: int,
        format: DiagramFormat | None = None,
        content: DiagramContent | None = None,
        draft_id: int | None = None,
    ) -> Response:
        """Get an image of a story. ``GET /api/v1/stories/{story_id}/diagram``

        The diagram keeps the layout of the storyboard. Tines renders up to 1,000 items and 2,000
        links, and scales a PNG to fit within 2,000 by 2,000 pixels.

        Args:
            story_id: The ID of the story to draw.
            format: The image format: ``png`` or ``svg``. Tines defaults to ``png``.
            content: ``full`` for actions, links, notes and sections, or ``actions`` for actions
                and links only. Tines defaults to ``full``.
            draft_id: The ID of the draft to draw. Tines draws the live story without it.

        Returns:
            A ``Response`` whose ``data`` is the image: the raw ``bytes`` of a PNG
            (``image/png``), or the text, a ``str``, of an SVG (``image/svg+xml``). The reply is a
            422 when the format or the content is not supported or the story is over the limits,
            and a 503 when the diagram could not be rendered.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/stories/{story_id}/diagram",
            params=omit_none(values={"format": format, "content": content, "draft_id": draft_id}),
        )

    def disable(self, *, story_id: int, disabled: bool) -> Response:
        """Set the disabled state of a story. ``POST /api/v1/stories/{story_id}/disable``

        This works on a story with change control enabled and bypasses its approval process.

        Args:
            story_id: The ID of the story to update.
            disabled: The new disabled state: ``True`` disables the story and ``False`` enables
                it.

        Returns:
            A ``Response`` whose ``data`` is an object with ``disabled``, the new state. On a
            story with change control it changes the live story at once.
        """
        return self._transport.request(
            method="POST",
            path=f"/api/v1/stories/{story_id}/disable",
            json={"disabled": disabled},
        )

    def list_pending_actions(
        self,
        *,
        story_id: int,
        search: str | None = None,
        story_mode: StoryMode | None = None,
        draft_id: int | None = None,
        per_page: int | None = None,
        page: int | None = None,
    ) -> Response:
        """List pending actions. ``GET /api/v1/stories/{story_id}/pending_actions``

        Lists the actions of a story that have pending action runs, the one with the most first.
        The endpoint is paginated and one call returns one page.

        Args:
            story_id: The ID of the story.
            search: Only actions whose name matches this text.
            story_mode: The mode of the story: ``TEST`` or ``LIVE``. Tines defaults to ``LIVE``.
            draft_id: Only actions of this draft.
            per_page: The number of results per page. Tines defaults to 20.
            page: The page to return, starting at 1. Tines defaults to 1.

        Returns:
            A ``Response`` whose ``data`` is an object with ``pending_actions``, a list of objects
            with ``id``, ``name``, ``type`` and ``pending_action_runs_count``, and ``meta``, the
            pagination details.
        """
        return self._transport.request(
            method="GET",
            path=f"/api/v1/stories/{story_id}/pending_actions",
            params=omit_none(
                values={
                    "search": search,
                    "story_mode": story_mode,
                    "draft_id": draft_id,
                    "per_page": per_page,
                    "page": page,
                }
            ),
        )
