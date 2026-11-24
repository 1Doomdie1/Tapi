import inspect
import json
import re
import types
import typing
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

import httpx
import respx

from tapi import Response, Tines

DOCUMENTED_ROUTE = re.compile(r"``(GET|POST|PUT|PATCH|DELETE) (/\S+)``")


@dataclass(frozen=True, kw_only=True)
class Case:
    target: str
    arguments: Mapping[str, Any]
    route: str
    params: Mapping[str, Any] = field(default_factory=dict)
    body: Any = None
    name: str | None = None


def wire(*, arguments: Mapping[str, Any], drop: Sequence[str] = ()) -> dict[str, Any]:
    return {
        key: list(value) if isinstance(value, tuple | range) else value
        for key, value in arguments.items()
        if key not in drop
    }


def case_id(case: Case) -> str:
    if case.name is not None:
        return f"{case.target}: {case.name}"
    names = ", ".join(case.arguments)
    return f"{case.target}({names})" if len(names) <= 40 else f"{case.target}(...)"


def resolve(*, tines: Tines, target: str) -> Callable[..., Response]:
    obj: Any = tines
    for name in target.split("."):
        obj = getattr(obj, name)
    return obj


def _is_area(*, member: object) -> bool:
    module = type(member).__module__
    return module.startswith("tapi.") and not module.startswith("tapi.core")


def public_methods(*, tines: Tines, area: str | None = None) -> dict[str, Callable[..., Response]]:
    found: dict[str, Callable[..., Response]] = {}

    def visit(*, obj: object, path: str) -> None:
        for name, member in inspect.getmembers(obj):
            if name.startswith("_"):
                continue
            if inspect.ismethod(member):
                found[f"{path}.{name}"] = member
            elif _is_area(member=member):
                visit(obj=member, path=f"{path}.{name}")

    roots = (
        [area]
        if area
        else [name for name, member in vars(tines).items() if _is_area(member=member)]
    )
    for root in roots:
        visit(obj=getattr(tines, root), path=root)
    return found


def _query_items(*, params: Mapping[str, Any]) -> list[tuple[str, str]]:
    def text(*, value: Any) -> str:
        if value is True:
            return "true"
        if value is False:
            return "false"
        return str(value)

    return sorted(
        (key, text(value=item))
        for key, value in params.items()
        for item in (value if isinstance(value, list) else [value])
    )


def _documented_route(*, method: Callable[..., Response]) -> tuple[str, str]:
    first_line = (inspect.getdoc(method) or "").splitlines()[0]
    found = DOCUMENTED_ROUTE.search(first_line)
    assert found, f"{method.__qualname__} does not state its route on the first docstring line"
    return found.group(1), found.group(2)


def assert_sent(*, tines: Tines, router: respx.MockRouter, case: Case) -> None:
    verb, path = case.route.split(" ", 1)
    route = router.request(verb, path).mock(return_value=httpx.Response(200, json={}))
    method = resolve(tines=tines, target=case.target)

    reply = method(**case.arguments)

    assert isinstance(reply, Response)
    assert (reply.status_code, reply.data) == (200, {})
    assert route.call_count == 1
    request = route.calls.last.request
    assert sorted(request.url.params.multi_items()) == _query_items(params=case.params)
    assert (json.loads(request.content) if request.content else None) == case.body
    documented_verb, template = _documented_route(method=method)
    pattern = "[^/]+".join(re.escape(part) for part in re.split(r"\{[^/]+\}", template))
    assert documented_verb == verb
    assert re.fullmatch(pattern, path), f"{case.target} documents {template}, but sends {path}"


def assert_covers(*, tines: Tines, area: str, cases: Sequence[Case]) -> None:
    names = [(case.target, case.name) for case in cases if case.name is not None]
    assert all(name.strip() for _, name in names), "a case has an empty name"
    assert len(names) == len(set(names)), (
        f"names used twice: {sorted({item for item in names if names.count(item) > 1})}"
    )
    used: dict[str, set[str]] = {}
    for case in cases:
        used.setdefault(case.target, set()).update(case.arguments)
    methods = public_methods(tines=tines, area=area)
    assert set(used) == set(methods), (
        f"without a case: {sorted(set(methods) - set(used))}; "
        f"not a method: {sorted(set(used) - set(methods))}"
    )
    for target, method in methods.items():
        parameters = set(inspect.signature(method).parameters)
        assert used[target] == parameters, (
            f"{target}: parameters without a case {sorted(parameters - used[target])}"
        )


def is_sequence(*, hint: Any) -> bool:
    if typing.get_origin(hint) in (types.UnionType, typing.Union):
        return any(is_sequence(hint=part) for part in typing.get_args(hint))
    return typing.get_origin(hint) is Sequence or hint is Sequence
