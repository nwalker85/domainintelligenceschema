"""§3 the Systems layer (Application/Endpoint/FunctionCatalogEntry) + §7.4/7.5.

Gap 3 (xfail): the spec text (§3.2/3.3/3.4) says several of these fields are
required, but the shapes only declare them sh:maxCount (optional). Do not
"fix" the shapes to match — that is Nate's call, not this suite's.
"""
import pytest
from rdflib import Literal

from conftest import DIS, D, add_node

APP_OK = dict(
    name=Literal("app"),
    description=Literal("desc"),
    applicationType=DIS.MOCK,
    baseUrl=Literal("https://example.test"),
)


def _app(g, iri, **overrides):
    props = dict(APP_OK)
    props.update(overrides)
    return add_node(g, iri, DIS.Application, **props)


ENDPOINT_OK = dict(
    name=Literal("ep"),
    description=Literal("desc"),
    hostedBy=D["kronos-product-api"],
    httpMethod=DIS.POST,
    urlPath=Literal("/thing"),
    mutates=Literal(False),
)


def _endpoint(g, iri, **overrides):
    props = dict(ENDPOINT_OK)
    props.update(overrides)
    return add_node(g, iri, DIS.Endpoint, **props)


FCE_OK = dict(
    name=Literal("fn"),
    description=Literal("desc"),
    callsEndpoint=D["get-product-attribute"],
    readsEntity=D.product,
    inputFields=Literal("a"),
    outputFields=Literal("b"),
)


def _fce(g, iri, **overrides):
    props = dict(FCE_OK)
    props.update(overrides)
    return add_node(g, iri, DIS.FunctionCatalogEntry, **props)


# ---------- Application ----------


def test_application_baseurl_http_rejected(dossier, validate):
    g = dossier("kronos-candies")
    _app(g, D.appx, baseUrl=Literal("http://example.test"))
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "appx" and r.path == "baseUrl" for r in report.violations())


def test_application_baseurl_https_accepted(dossier, validate):
    g = dossier("kronos-candies")
    _app(g, D.appx)
    report = validate(g, inference="none")
    assert report.conforms, report.results


def test_application_missing_applicationtype_rejected(dossier, validate):
    g = dossier("kronos-candies")
    _app(g, D.appx, applicationType=None)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "appx" and r.path == "applicationType" for r in report.violations())


def test_mock_and_system_of_record_together_rejected(dossier, validate):
    g = dossier("kronos-candies")
    _app(g, D.appx, applicationType=[DIS.MOCK, DIS.SYSTEM_OF_RECORD])
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "appx" and r.shape == "MockHonestyShape" for r in report.violations())


# ---------- Endpoint ----------


def test_endpoint_missing_hostedby_rejected(dossier, validate):
    g = dossier("kronos-candies")
    _endpoint(g, D.epx, hostedBy=None)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "epx" and r.path == "hostedBy" for r in report.violations())


def test_endpoint_hostedby_pointing_at_entity_rejected(dossier, validate):
    g = dossier("kronos-candies")
    _endpoint(g, D.epx, hostedBy=D.product)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "epx" and r.path == "hostedBy" for r in report.violations())


def test_endpoint_urlpath_without_leading_slash_rejected(dossier, validate):
    g = dossier("kronos-candies")
    _endpoint(g, D.epx, urlPath=Literal("product"))
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "epx" and r.path == "urlPath" for r in report.violations())


def test_endpoint_urlpath_with_leading_slash_accepted(dossier, validate):
    g = dossier("kronos-candies")
    _endpoint(g, D.epx, urlPath=Literal("/product"))
    report = validate(g, inference="none")
    assert report.conforms, report.results


def test_endpoint_httpmethod_delete_rejected_not_in_closed_set(dossier, validate):
    g = dossier("kronos-candies")
    _endpoint(g, D.epx, httpMethod=DIS.DELETE)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "epx" and r.path == "httpMethod" for r in report.violations())


def test_endpoint_httpmethod_http_delete_accepted(dossier, validate):
    g = dossier("kronos-candies")
    _endpoint(g, D.epx, httpMethod=DIS.HTTP_DELETE)
    report = validate(g, inference="none")
    assert report.conforms, report.results


def test_endpoint_httpmethod_options_rejected(dossier, validate):
    g = dossier("kronos-candies")
    _endpoint(g, D.epx, httpMethod=DIS.OPTIONS)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "epx" and r.path == "httpMethod" for r in report.violations())


def test_endpoint_mutates_string_rejected(dossier, validate):
    g = dossier("kronos-candies")
    _endpoint(g, D.epx, mutates=Literal("yes"))
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "epx" and r.path == "mutates" for r in report.violations())


def test_post_with_mutates_false_accepted_declared_never_inferred(dossier, validate):
    g = dossier("kronos-candies")
    _endpoint(g, D.epx, httpMethod=DIS.POST, mutates=Literal(False))
    report = validate(g, inference="none")
    assert report.conforms, report.results


def test_get_with_mutates_true_accepted_declared_never_inferred(dossier, validate):
    g = dossier("kronos-candies")
    _endpoint(g, D.epx, httpMethod=DIS.GET, mutates=Literal(True))
    report = validate(g, inference="none")
    assert report.conforms, report.results


# ---------- FunctionCatalogEntry ----------


def test_fce_missing_callsendpoint_rejected(dossier, validate):
    g = dossier("kronos-candies")
    _fce(g, D.fcex, callsEndpoint=None)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "fcex" and r.path == "callsEndpoint" for r in report.violations())


def test_fce_callsendpoint_pointing_at_application_rejected(dossier, validate):
    g = dossier("kronos-candies")
    _fce(g, D.fcex, callsEndpoint=D["kronos-product-api"])
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "fcex" and r.path == "callsEndpoint" for r in report.violations())


def test_fce_readsentity_pointing_at_role_rejected(dossier, validate):
    g = dossier("kronos-candies")
    _fce(g, D.fcex, readsEntity=D["kronos-support-agent"])
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "fcex" and r.path == "readsEntity" for r in report.violations())


# ---------- gap 3: spec says required, shapes say optional (xfail) ----------


@pytest.mark.xfail(
    strict=True,
    reason="RAV-1947 gap 3: spec §3.2 says Application.baseUrl is required, "
    "ApplicationShape only declares sh:maxCount (optional)",
)
def test_gap3_application_missing_baseurl_is_rejected(dossier, validate):
    g = dossier("kronos-candies")
    _app(g, D.appx, baseUrl=None)
    report = validate(g, inference="none")
    assert not report.conforms


@pytest.mark.xfail(
    strict=True,
    reason="RAV-1947 gap 3: spec §3.3 says Endpoint.mutates is required, "
    "EndpointShape only declares sh:maxCount (optional)",
)
def test_gap3_endpoint_missing_mutates_is_rejected(dossier, validate):
    g = dossier("kronos-candies")
    _endpoint(g, D.epx, mutates=None)
    report = validate(g, inference="none")
    assert not report.conforms


@pytest.mark.xfail(
    strict=True,
    reason="RAV-1947 gap 3: spec §3.4 says FunctionCatalogEntry.readsEntity "
    "is required, FunctionCatalogEntryShape only declares sh:maxCount",
)
def test_gap3_fce_missing_readsentity_is_rejected(dossier, validate):
    g = dossier("kronos-candies")
    _fce(g, D.fcex, readsEntity=None)
    report = validate(g, inference="none")
    assert not report.conforms


@pytest.mark.xfail(
    strict=True,
    reason="RAV-1947 gap 3: spec §3.4 says FunctionCatalogEntry.inputFields "
    "is required, FunctionCatalogEntryShape only declares sh:maxCount",
)
def test_gap3_fce_missing_inputfields_is_rejected(dossier, validate):
    g = dossier("kronos-candies")
    _fce(g, D.fcex, inputFields=None)
    report = validate(g, inference="none")
    assert not report.conforms


@pytest.mark.xfail(
    strict=True,
    reason="RAV-1947 gap 3: spec §3.4 says FunctionCatalogEntry.outputFields "
    "is required, FunctionCatalogEntryShape only declares sh:maxCount",
)
def test_gap3_fce_missing_outputfields_is_rejected(dossier, validate):
    g = dossier("kronos-candies")
    _fce(g, D.fcex, outputFields=None)
    report = validate(g, inference="none")
    assert not report.conforms
