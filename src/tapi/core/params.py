from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from typing import Any, TypeVar

T = TypeVar("T")


def omit_none(*, values: Mapping[str, Any]) -> dict[str, Any]:
    """Drop the entries of ``values`` that are ``None``.

    Args:
        values: Query parameters or body fields.

    Returns:
        A new dictionary without the ``None`` entries. Other falsy values, such as ``0``,
        ``False`` and ``""``, are kept.
    """
    return {name: value for name, value in values.items() if value is not None}


def to_iso(*, value: datetime | str | None) -> str | None:
    """Format a datetime as an ISO 8601 string.

    Args:
        value: A ``datetime``, an ISO 8601 string or ``None``. A datetime without a timezone is
            treated as UTC.

    Returns:
        The ISO 8601 string. A string or ``None`` is returned unchanged.
    """
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value.isoformat()
    return value


def to_object_or_list(
    *, value: Mapping[str, Any] | Sequence[Mapping[str, Any]] | None
) -> dict[str, Any] | list[Mapping[str, Any]] | None:
    """Keep an object as an object and turn a sequence of objects into a list.

    Args:
        value: An object, a sequence of objects, or ``None``.

    Returns:
        A new dictionary for an object, a new list for a sequence, or ``None``.

    Raises:
        TypeError: If ``value`` is a single string, which would be split into characters.
    """
    if value is None:
        return None
    if isinstance(value, Mapping):
        return dict(value)
    return to_list(values=value)


def to_list(*, values: Sequence[T] | None) -> list[T] | None:
    """Turn a sequence into the list that repeats a query parameter once per value.

    Args:
        values: A sequence of values, or ``None``.

    Returns:
        A new list, or ``None`` if ``values`` is ``None``.

    Raises:
        TypeError: If ``values`` is a single string, which would be split into characters, or a
            single mapping, which would be reduced to its keys.
    """
    if values is None:
        return None
    if isinstance(values, str | bytes | Mapping):
        raise TypeError("Expected a sequence of values, not a single string or mapping.")
    return list(values)
