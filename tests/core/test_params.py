from datetime import UTC, datetime, timedelta, timezone

import pytest

from tapi.core.params import omit_none, to_iso, to_list, to_object_or_list


def test_omit_none_drops_none_and_keeps_other_falsy_values():
    values = {"count": 0, "enabled": False, "name": "", "tags": []}

    assert omit_none(values={**values, "page": None}) == values


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(
            datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC), "2026-01-02T03:04:05+00:00", id="utc"
        ),
        pytest.param(datetime(2026, 1, 2, 3, 4, 5), "2026-01-02T03:04:05+00:00", id="naive is utc"),
        pytest.param(
            datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone(timedelta(hours=2))),
            "2026-01-02T03:04:05+02:00",
            id="offset kept",
        ),
        pytest.param("2026-01-02T03:04:05Z", "2026-01-02T03:04:05Z", id="string unchanged"),
        pytest.param(None, None, id="none unchanged"),
    ],
)
def test_to_iso(value, expected):
    assert to_iso(value=value) == expected


def test_to_list_turns_any_sequence_into_a_list_and_keeps_none_apart_from_empty():
    assert to_list(values=(1, 2)) == [1, 2]
    assert to_list(values=range(1, 3)) == [1, 2]
    assert to_list(values=[]) == []
    assert to_list(values=None) is None


@pytest.mark.parametrize("value", ["abc", b"abc", {"path": "App.tsx"}])
def test_to_list_rejects_a_single_string_or_mapping(value):
    with pytest.raises(TypeError):
        to_list(values=value)


def test_to_object_or_list_keeps_an_object_and_listifies_a_sequence():
    assert to_object_or_list(value={"cron": "0 0 * * *"}) == {"cron": "0 0 * * *"}
    assert to_object_or_list(value=({"cron": "0 0 * * *"},)) == [{"cron": "0 0 * * *"}]
    assert to_object_or_list(value=None) is None
    with pytest.raises(TypeError):
        to_object_or_list(value="0 0 * * *")
