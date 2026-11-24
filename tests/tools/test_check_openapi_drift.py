import httpx
import pytest

from tools import check_openapi_drift as drift


def report_for(*, spec, tapi, known=None):
    return drift.compare(spec=spec, tapi=tapi, known=known or drift.Known(), unparsed=[])


def test_the_names_of_placeholders_and_a_trailing_slash_do_not_matter():
    assert drift.normalize(path="/api/v1/stories/{story_id}/") == "/api/v1/stories/{}"
    assert drift.normalize(path="/api/v1/stories/{id}") == "/api/v1/stories/{}"
    assert drift.parse_route(text="get /api/v1/tags/{tag_id}") == ("GET", "/api/v1/tags/{}")


def test_only_the_http_verbs_of_a_path_are_operations():
    spec = {
        "paths": {
            "/api/v1/tags": {"get": {}, "post": {}, "parameters": [], "summary": "Tags"},
            "/api/v1/tags/{id}": {"put": {}, "delete": {}},
        }
    }

    assert drift.spec_routes(spec=spec) == {
        ("GET", "/api/v1/tags"),
        ("POST", "/api/v1/tags"),
        ("PUT", "/api/v1/tags/{}"),
        ("DELETE", "/api/v1/tags/{}"),
    }


def test_only_the_operations_marked_deprecated_are_deprecated():
    spec = {
        "paths": {
            "/api/v1/tags": {"get": {"deprecated": True}, "post": {"deprecated": False}},
            "/api/v1/tags/{id}": {"put": {}, "delete": {"deprecated": True}, "parameters": []},
        }
    }

    assert drift.deprecated_routes(spec=spec) == {
        ("GET", "/api/v1/tags"),
        ("DELETE", "/api/v1/tags/{}"),
    }


def test_a_route_that_tapi_offers_and_the_documents_deprecate_makes_the_report_unclean():
    spec = {("GET", "/a"), ("GET", "/old"), ("PUT", "/old/{}"), ("GET", "/fine")}
    tapi = {("GET", "/a"), ("GET", "/old"), ("PATCH", "/old/{}"), ("GET", "/fine")}

    report = drift.compare(
        spec=spec,
        tapi=tapi,
        known=drift.Known(),
        unparsed=[],
        deprecated={("GET", "/old"), ("PUT", "/old/{}")},
    )

    assert report.deprecated == [("GET", "/old"), ("PATCH", "/old/{}")]
    assert not report.clean


@pytest.mark.parametrize(
    ("spec", "tapi", "expected"),
    [
        pytest.param({("PUT", "/x/{}")}, {("PATCH", "/x/{}")}, {("PATCH", "/x/{}")}, id="patch"),
        pytest.param({("PUT", "/x/{}")}, {("PUT", "/x/{}")}, {("PUT", "/x/{}")}, id="put kept"),
        pytest.param(
            {("PUT", "/x/{}"), ("PATCH", "/x/{}")},
            {("PATCH", "/x/{}")},
            {("PATCH", "/x/{}")},
            id="twin dropped",
        ),
        pytest.param({("PUT", "/x/{}")}, set(), {("PUT", "/x/{}")}, id="not built"),
    ],
)
def test_a_put_of_the_documents_is_matched_by_the_patch_that_tapi_sends(spec, tapi, expected):
    assert drift.align_updates(spec=spec, tapi=tapi) == expected


def test_routes_missing_on_either_side_are_reported_unless_they_are_known():
    spec = {("GET", "/a"), ("GET", "/old/1"), ("GET", "/later/1"), ("GET", "/later/2")}
    tapi = {("GET", "/a"), ("GET", "/only-tapi"), ("GET", "/odd/1")}
    known = drift.Known(
        not_offered=(drift.Entry(prefix="/old", reason="a copy"),),
        not_built=(drift.Entry(prefix="/later", reason="not built"),),
        not_in_spec=(drift.Entry(prefix="/odd", reason="documented elsewhere"),),
    )

    report = report_for(spec=spec, tapi=tapi, known=known)

    assert report.matched_count == 1
    assert report.missing == []
    assert report.extra == [("GET", "/only-tapi")]
    assert report.not_offered == {"/old/...": 1}
    assert report.not_built == {"/later/...": 2}
    assert not report.clean


def test_a_route_that_is_missing_without_being_known_makes_the_report_unclean():
    report = report_for(spec={("GET", "/a"), ("GET", "/b")}, tapi={("GET", "/a")})

    assert report.missing == [("GET", "/b")]
    assert not report.clean


def test_everything_matching_is_a_clean_report():
    assert report_for(spec={("GET", "/a")}, tapi={("GET", "/a")}).clean


def test_known_entries_that_no_longer_apply_are_reported():
    spec = {("GET", "/a"), ("GET", "/built/1"), ("GET", "/offered/1")}
    tapi = {("GET", "/a"), ("GET", "/built/1"), ("GET", "/offered/1"), ("GET", "/now-listed")}
    known = drift.Known(
        not_offered=(
            drift.Entry(prefix="/offered", reason="x"),
            drift.Entry(prefix="/gone", reason="x"),
        ),
        not_built=(drift.Entry(prefix="/built", reason="x"),),
        not_in_spec=(
            drift.Entry(route=("GET", "/now-listed"), reason="x"),
            drift.Entry(route=("GET", "/removed"), reason="x"),
        ),
    )

    stale = report_for(spec=spec | {("GET", "/now-listed")}, tapi=tapi, known=known).stale

    assert len(stale) == 5
    assert any("tapi offers it now" in line and "/offered" in line for line in stale)
    assert any("no longer list it" in line and "/gone" in line for line in stale)
    assert any("covers all of it now" in line and "/built" in line for line in stale)
    assert any("list it now" in line and "/now-listed" in line for line in stale)
    assert any("no longer has it" in line and "/removed" in line for line in stale)


def test_the_file_of_known_differences_is_read(tmp_path):
    path = tmp_path / "known.toml"
    path.write_text(
        '[[not_offered]]\nprefix = "/api/v1/agents/"\nreason = "a copy"\n\n'
        '[[not_in_spec]]\nroute = "post /api/v1/x/{name}"\nreason = "elsewhere"\n',
        encoding="utf-8",
    )

    known = drift.load_known(path=path)

    assert known.not_offered == (drift.Entry(prefix="/api/v1/agents", reason="a copy"),)
    assert known.not_in_spec == (drift.Entry(route=("POST", "/api/v1/x/{}"), reason="elsewhere"),)
    assert drift.load_known(path=tmp_path / "missing.toml") == drift.Known()


def test_every_method_of_tapi_states_the_route_it_calls():
    routes, unparsed = drift.tapi_routes()

    assert unparsed == []
    assert ("GET", "/api/v1/tags/{}") in routes


@pytest.mark.parametrize(
    ("tapi", "code"),
    [
        pytest.param({("GET", "/a")}, 0, id="clean"),
        pytest.param({("GET", "/a"), ("GET", "/b")}, 1, id="difference"),
    ],
)
def test_the_exit_code_tells_whether_tapi_and_the_documents_agree(
    monkeypatch, tmp_path, capsys, tapi, code
):
    monkeypatch.setattr(drift, "fetch_spec", lambda *, url: {"paths": {"/a": {"get": {}}}})
    monkeypatch.setattr(drift, "tapi_routes", lambda: (tapi, []))

    result = drift.main(arguments=["--known", str(tmp_path / "none.toml")])

    assert result == code
    assert ("No unexpected differences." in capsys.readouterr().out) == (code == 0)


def test_a_document_that_cannot_be_read_gives_exit_code_2(monkeypatch, tmp_path, capsys):
    def refuse(*, url):
        raise httpx.ConnectError("refused")

    monkeypatch.setattr(drift, "fetch_spec", refuse)

    result = drift.main(arguments=["--known", str(tmp_path / "none.toml")])

    assert result == 2
    assert "Could not read" in capsys.readouterr().err
