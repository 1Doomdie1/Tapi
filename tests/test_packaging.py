import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
SDIST_PATHS = {
    "/src",
    "/tests",
    "/tools",
    "/docs",
    "/CHANGELOG.md",
    "/LICENSE",
    "/README.md",
    "/requirements.txt",
    "/pyproject.toml",
}


def test_sdist_holds_exactly_the_allowed_paths() -> None:
    include = PROJECT["tool"]["hatch"]["build"]["targets"]["sdist"]["include"]

    assert set(include) == SDIST_PATHS
    for entry in include:
        assert (ROOT / entry.lstrip("/")).exists(), entry


def test_changelog_has_a_heading_for_the_version() -> None:
    version = PROJECT["project"]["version"]
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    assert f"## [{version}] - " in changelog
