"""Compare the routes of tapi with the routes of the Tines OpenAPI documents.

The OpenAPI document is downloaded into memory each time the tool runs. It is never written to disk.
Run it from the project root with the virtual environment active:

    python tools/check_openapi_drift.py

The exit code is 0 when tapi and the document agree, apart from the differences listed in
``tools/openapi_known_differences.toml``, 1 when they do not, and 2 when the document could not be
read.
"""

import argparse
import inspect
import json
import re
import sys
import tomllib
from collections import Counter
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import httpx

from tapi import Tines

DEFAULT_SPECS = (
    "https://www.tines.com/stories/docs/api/openapi.json",
    "https://www.tines.com/cases/docs/api/openapi.json",
)
DEFAULT_KNOWN = Path(__file__).with_name("openapi_known_differences.toml")
HTTP_VERBS = ("get", "post", "put", "patch", "delete")
DOCUMENTED_ROUTE = re.compile(r"``(GET|POST|PUT|PATCH|DELETE) (/\S+)``")

Route = tuple[str, str]


@dataclass(frozen=True, kw_only=True)
class Entry:
    """One difference that is known and accepted."""

    route: Route | None = None
    prefix: str | None = None
    reason: str


@dataclass(frozen=True, kw_only=True)
class Known:
    """The accepted differences between tapi and the OpenAPI documents."""

    not_offered: tuple[Entry, ...] = ()
    not_built: tuple[Entry, ...] = ()
    not_in_spec: tuple[Entry, ...] = ()


@dataclass(frozen=True, kw_only=True)
class Report:
    """The result of comparing tapi with the OpenAPI documents."""

    spec_count: int
    tapi_count: int
    matched_count: int
    missing: list[Route] = field(default_factory=list)
    extra: list[Route] = field(default_factory=list)
    not_offered: Counter[str] = field(default_factory=Counter)
    not_built: Counter[str] = field(default_factory=Counter)
    stale: list[str] = field(default_factory=list)
    unparsed: list[str] = field(default_factory=list)

    @property
    def clean(self) -> bool:
        return not (self.missing or self.extra or self.stale or self.unparsed)


def normalize(*, path: str) -> str:
    """Make a route independent of the names of its placeholders.

    Args:
        path: A route such as ``/api/v1/stories/{story_id}/``.

    Returns:
        The route with every placeholder written as ``{}`` and without a trailing slash.
    """
    return re.sub(r"\{[^/]+\}", "{}", path).rstrip("/") or "/"


def parse_route(*, text: str) -> Route:
    """Split a route written as ``GET /api/v1/tags`` into its verb and its normalized path.

    Args:
        text: The verb and the path, separated by a space.

    Returns:
        The upper-case verb and the normalized path.
    """
    verb, path = text.split(" ", 1)
    return verb.upper(), normalize(path=path.strip())


def spec_routes(*, spec: dict[str, Any]) -> set[Route]:
    """List the operations of an OpenAPI document.

    Args:
        spec: The parsed OpenAPI document.

    Returns:
        The verb and the normalized path of every operation.
    """
    return {
        (verb.upper(), normalize(path=path))
        for path, operations in spec["paths"].items()
        for verb in HTTP_VERBS
        if verb in operations
    }


def is_area(*, member: object) -> bool:
    module = type(member).__module__
    return module.startswith("tapi.") and not module.startswith("tapi.core")


def methods_of(*, obj: object, prefix: str) -> dict[str, Callable[..., Any]]:
    found: dict[str, Callable[..., Any]] = {}
    for name, member in inspect.getmembers(obj):
        if name.startswith("_"):
            continue
        if inspect.ismethod(member):
            found[f"{prefix}{name}"] = member
        elif is_area(member=member):
            found.update(methods_of(obj=member, prefix=f"{prefix}{name}."))
    return found


def tapi_routes() -> tuple[set[Route], list[str]]:
    """Read the route that every public method of tapi documents in its docstring.

    Returns:
        The verb and the normalized path of every method, and the names of the methods whose
        docstring does not state a route.
    """
    routes: set[Route] = set()
    unparsed: list[str] = []
    with Tines(tenant_domain="example.invalid", api_key="unused") as tines:
        methods: dict[str, Callable[..., Any]] = {}
        for name, member in vars(tines).items():
            if is_area(member=member):
                methods.update(methods_of(obj=member, prefix=f"{name}."))
    for name, method in sorted(methods.items()):
        first_line = (inspect.getdoc(method) or "").splitlines()[:1]
        found = DOCUMENTED_ROUTE.search(first_line[0]) if first_line else None
        if found is None:
            unparsed.append(name)
        else:
            routes.add((found.group(1), normalize(path=found.group(2))))
    return routes, unparsed


def align_updates(*, spec: set[Route], tapi: set[Route]) -> set[Route]:
    """Treat ``PUT`` in the document as ``PATCH`` where tapi updates with ``PATCH``.

    Args:
        spec: The operations of the OpenAPI documents.
        tapi: The operations of tapi.

    Returns:
        The operations of the documents, with a ``PUT`` that tapi sends as ``PATCH`` rewritten as
        that ``PATCH``, and a ``PUT`` dropped when the document lists a ``PATCH`` at the same path.
    """
    aligned: set[Route] = set()
    for verb, path in spec:
        if verb == "PUT" and ("PATCH", path) in spec:
            continue
        if verb == "PUT" and ("PATCH", path) in tapi and ("PUT", path) not in tapi:
            aligned.add(("PATCH", path))
        else:
            aligned.add((verb, path))
    return aligned


def covers(*, entry: Entry, route: Route) -> bool:
    """Tell whether a known difference names a route, by the route itself or by a prefix."""
    if entry.route is not None:
        return entry.route == route
    prefix = entry.prefix or ""
    return route[1] == prefix or route[1].startswith(f"{prefix}/")


def label(*, entry: Entry) -> str:
    return " ".join(entry.route) if entry.route is not None else f"{entry.prefix}/..."


def compare(*, spec: set[Route], tapi: set[Route], known: Known, unparsed: Sequence[str]) -> Report:
    """Compare the routes of the OpenAPI documents with the routes of tapi.

    Args:
        spec: The operations of the OpenAPI documents.
        tapi: The operations of tapi.
        known: The differences that are known and accepted.
        unparsed: The methods of tapi whose docstring states no route.

    Returns:
        The report: the routes that are missing from tapi or from the documents without being
        known, the known differences counted by entry, and the known entries that no longer apply.
    """
    expected = align_updates(spec=spec, tapi=tapi)
    missing: list[Route] = []
    not_offered: Counter[str] = Counter()
    not_built: Counter[str] = Counter()
    for route in sorted(expected - tapi):
        offered = next((e for e in known.not_offered if covers(entry=e, route=route)), None)
        built = next((e for e in known.not_built if covers(entry=e, route=route)), None)
        if offered is not None:
            not_offered[label(entry=offered)] += 1
        elif built is not None:
            not_built[label(entry=built)] += 1
        else:
            missing.append(route)
    absent = sorted(tapi - expected)
    extra = [r for r in absent if not any(covers(entry=e, route=r) for e in known.not_in_spec)]

    stale: list[str] = []
    for entry in known.not_offered:
        if not any(covers(entry=entry, route=r) for r in expected):
            stale.append(f"not offered, but the documents no longer list it: {label(entry=entry)}")
        elif any(covers(entry=entry, route=r) for r in tapi):
            stale.append(f"not offered, but tapi offers it now: {label(entry=entry)}")
    for entry in known.not_built:
        listed = [r for r in expected if covers(entry=entry, route=r)]
        if not listed:
            stale.append(f"not built, but the documents no longer list it: {label(entry=entry)}")
        elif all(r in tapi for r in listed):
            stale.append(f"not built, but tapi covers all of it now: {label(entry=entry)}")
    for entry in known.not_in_spec:
        if not any(covers(entry=entry, route=r) for r in tapi):
            stale.append(f"not in the documents, but tapi no longer has it: {label(entry=entry)}")
        elif any(covers(entry=entry, route=r) for r in expected):
            stale.append(f"not in the documents, but they list it now: {label(entry=entry)}")

    return Report(
        spec_count=len(expected),
        tapi_count=len(tapi),
        matched_count=len(expected & tapi),
        missing=missing,
        extra=extra,
        not_offered=not_offered,
        not_built=not_built,
        stale=stale,
        unparsed=list(unparsed),
    )


def render(*, report: Report) -> str:
    """Write a report as text.

    Args:
        report: The result of ``compare``.

    Returns:
        The lines to print.
    """
    lines = [
        f"Routes in the OpenAPI documents: {report.spec_count}",
        f"Routes in tapi: {report.tapi_count}",
        f"Matched: {report.matched_count}",
    ]
    if report.not_offered:
        total = sum(report.not_offered.values())
        lines.append(f"Known, not offered by tapi on purpose: {total}")
    if report.not_built:
        lines.append("Known, not built yet:")
        lines += [f"  {name}: {count}" for name, count in sorted(report.not_built.items())]
    sections = (
        ("In the OpenAPI documents, missing from tapi", [" ".join(r) for r in report.missing]),
        ("In tapi, missing from the OpenAPI documents", [" ".join(r) for r in report.extra]),
        ("Known differences that no longer apply", report.stale),
        ("Methods of tapi whose docstring states no route", report.unparsed),
    )
    for title, items in sections:
        if items:
            lines += ["", f"{title}: {len(items)}"] + [f"  {item}" for item in items]
    lines += ["", "No unexpected differences." if report.clean else "Unexpected differences found."]
    return "\n".join(lines)


def load_known(*, path: Path) -> Known:
    """Read the file of known differences.

    Args:
        path: The TOML file.

    Returns:
        The known differences. A missing file means that none are known.
    """
    if not path.exists():
        return Known()
    data = tomllib.loads(path.read_text(encoding="utf-8-sig"))

    def entries(*, table: str) -> tuple[Entry, ...]:
        return tuple(
            Entry(
                route=parse_route(text=item["route"]) if "route" in item else None,
                prefix=normalize(path=item["prefix"]) if "prefix" in item else None,
                reason=item["reason"],
            )
            for item in data.get(table, [])
        )

    return Known(
        not_offered=entries(table="not_offered"),
        not_built=entries(table="not_built"),
        not_in_spec=entries(table="not_in_spec"),
    )


def fetch_spec(*, url: str) -> dict[str, Any]:
    """Download an OpenAPI document into memory.

    Args:
        url: The address of the document.

    Returns:
        The parsed document.
    """
    reply = httpx.get(url, timeout=60, follow_redirects=True)
    reply.raise_for_status()
    spec: dict[str, Any] = json.loads(reply.content)
    if not isinstance(spec.get("paths"), dict):
        raise ValueError("the document has no paths")
    return spec


def main(*, arguments: Sequence[str] | None = None) -> int:
    """Run the comparison and print the report.

    Args:
        arguments: The command line arguments. Defaults to the ones of the process.

    Returns:
        The exit code of the tool.
    """
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0] if __doc__ else None)
    parser.add_argument(
        "--spec",
        action="append",
        metavar="URL",
        help="An OpenAPI document to read. Repeat it for several. Defaults to Stories and Cases.",
    )
    parser.add_argument(
        "--known",
        type=Path,
        default=DEFAULT_KNOWN,
        help="The TOML file of known differences.",
    )
    parsed = parser.parse_args(arguments)

    spec: set[Route] = set()
    for url in parsed.spec or DEFAULT_SPECS:
        try:
            spec |= spec_routes(spec=fetch_spec(url=url))
        except (httpx.HTTPError, ValueError, KeyError) as error:
            print(f"Could not read {url}: {type(error).__name__}", file=sys.stderr)
            return 2
    tapi, unparsed = tapi_routes()
    report = compare(spec=spec, tapi=tapi, known=load_known(path=parsed.known), unparsed=unparsed)
    print(render(report=report))
    return 0 if report.clean else 1


if __name__ == "__main__":
    raise SystemExit(main())
