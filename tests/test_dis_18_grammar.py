"""Tests for DIS 1.8 grammar extensions and fixes for flaws G1-G6:
- G1: Triplet mode and bound function endpoint mutates consistency
- G2: writesEntity required on mutating functions and targetEntity alignment
- G3: Binding status on triplets
- G4: Multi-transport endpoints (MQTT, RTSP, ESPNOW, WebRTC, SSE, etc.) and networkScope
- G5: Function-scoped access gates (allowedFunction)
"""
import pytest
from rdflib import Literal

from conftest import DIS, D, add_triplet, add_node

ROLE = D["retail-support-agent"]
ENTITY = D.product
MODE = DIS.READ


def _ep(g, iri, **overrides):
    props = dict(
        name=Literal("ep"),
        description=Literal("desc"),
        hostedBy=D["retail-catalog-api"],
        httpMethod=DIS.GET,
        urlPath=Literal("/thing"),
        mutates=Literal(False),
    )
    props.update(overrides)
    return add_node(g, iri, DIS.Endpoint, **props)


def _fn(g, iri, **overrides):
    props = dict(
        name=Literal("fn"),
        description=Literal("desc"),
        callsEndpoint=D["get-product-attribute"],
        readsEntity=D.product,
        inputFields=Literal("a"),
        outputFields=Literal("b"),
    )
    props.update(overrides)
    return add_node(g, iri, DIS.FunctionCatalogEntry, **props)


# ---------- G1: Mode vs Mutates Consistency ----------


def test_g1_read_triplet_with_mutating_endpoint_rejected(dossier, validate):
    g = dossier("retail")
    ep_mutating = _ep(g, D.ep_mut, httpMethod=DIS.POST, mutates=Literal(True))
    fn_mutating = _fn(g, D.fn_mut, callsEndpoint=ep_mutating, writesEntity=D.product)
    t = D.t_bad_read
    add_triplet(g, t, ROLE, ENTITY, DIS.READ, boundFunction=fn_mutating)

    report = validate(g, inference="none")
    assert not report.conforms
    assert any(
        r.shape == "TripletModeMutationConsistencyShape" and r.focus == "t_bad_read"
        for r in report.violations()
    )


def test_g1_update_triplet_with_non_mutating_endpoint_rejected(dossier, validate):
    g = dossier("retail")
    # Add matrix grant for UPDATE on product so matrix shapes don't fire
    add_node(
        g,
        D.gate_update,
        DIS.AccessGateMatrix,
        matrixRole=ROLE,
        matrixEntity=ENTITY,
        allowedMode=DIS.UPDATE,
        name=Literal("update gate"),
        description=Literal("desc"),
    )
    # Target entity must also support UPDATE
    g.add((D["emm-product"], DIS.supportedMode, DIS.UPDATE))

    ep_read = _ep(g, D.ep_ro, httpMethod=DIS.GET, mutates=Literal(False))
    fn_read = _fn(g, D.fn_ro, callsEndpoint=ep_read, readsEntity=D.product)
    t = D.t_bad_update
    add_triplet(g, t, ROLE, ENTITY, DIS.UPDATE, boundFunction=fn_read)

    report = validate(g, inference="none")
    assert not report.conforms
    assert any(
        r.shape == "TripletModeMutationConsistencyShape" and r.focus == "t_bad_update"
        for r in report.violations()
    )


# ---------- G2: writesEntity & Target Alignment ----------


def test_g2_function_calling_mutating_endpoint_without_writesentity_rejected(dossier, validate):
    g = dossier("retail")
    ep_mut = _ep(g, D.ep_mut2, httpMethod=DIS.POST, mutates=Literal(True))
    _fn(g, D.fn_no_writes, callsEndpoint=ep_mut, readsEntity=D.product)

    report = validate(g, inference="none")
    assert not report.conforms
    assert any(
        r.shape == "FunctionMutatesNeedsWritesEntityShape" and r.focus == "fn_no_writes"
        for r in report.violations()
    )


def test_g2_mutating_triplet_target_mismatch_with_writesentity_rejected(dossier, validate):
    g = dossier("retail")
    g.add((D["emm-product"], DIS.supportedMode, DIS.UPDATE))
    add_node(
        g,
        D.gate_update2,
        DIS.AccessGateMatrix,
        matrixRole=ROLE,
        matrixEntity=D.product,
        allowedMode=DIS.UPDATE,
        name=Literal("update gate"),
        description=Literal("desc"),
    )

    ep_mut = _ep(g, D.ep_mut3, httpMethod=DIS.POST, mutates=Literal(True))
    # fn writes order, but triplet targets product
    fn_order = _fn(g, D.fn_order, callsEndpoint=ep_mut, writesEntity=D.order)
    t = D.t_mismatch
    add_triplet(g, t, ROLE, D.product, DIS.UPDATE, boundFunction=fn_order)

    report = validate(g, inference="none")
    assert not report.conforms
    assert any(
        r.shape == "TripletTargetEntityConsistencyShape" and r.focus == "t_mismatch"
        for r in report.violations()
    )


def test_g2_read_triplet_target_mismatch_with_readsentity_rejected(dossier, validate):
    g = dossier("retail")
    ep_ro = _ep(g, D.ep_ro2, httpMethod=DIS.GET, mutates=Literal(False))
    # fn reads order, but triplet targets product
    fn_order = _fn(g, D.fn_ro_order, callsEndpoint=ep_ro, readsEntity=D.order)
    t = D.t_ro_mismatch
    add_triplet(g, t, ROLE, D.product, DIS.READ, boundFunction=fn_order)

    report = validate(g, inference="none")
    assert not report.conforms
    assert any(
        r.shape == "TripletTargetEntityConsistencyShape" and r.focus == "t_ro_mismatch"
        for r in report.violations()
    )


# ---------- G4: Multi-Transport Endpoints & Network Scope ----------


@pytest.mark.parametrize(
    "transport,prop,val",
    [
        (DIS.TRANSPORT_MQTT, DIS.topic, Literal("frigate/owl1/enabled/set")),
        (DIS.TRANSPORT_RTSP, DIS.streamUri, Literal("rtsp://gateway.local:8554/owl1")),
        (DIS.TRANSPORT_ESPNOW, DIS.peerAddress, Literal("AA:BB:CC:DD:EE:FF")),
        (DIS.TRANSPORT_NATS, DIS.subject, Literal("norns.events.camera.dark")),
        (DIS.TRANSPORT_UNIX_SOCKET, DIS.socketPath, Literal("/var/run/argus.sock")),
    ],
)
def test_g4_multi_transport_endpoints_without_http_fields_accepted(dossier, validate, transport, prop, val):
    g = dossier("retail")
    ep_props = {
        "name": Literal("trans_ep"),
        "description": Literal("desc"),
        "hostedBy": D["retail-catalog-api"],
        "transport": transport,
        "mutates": Literal(False),
        _local(prop): val,
    }
    add_node(g, D.ep_trans, DIS.Endpoint, **ep_props)
    report = validate(g, inference="none")
    assert report.conforms, report.results


def test_g4_internal_network_scope_allows_plain_http_baseurl(dossier, validate):
    g = dossier("retail")
    add_node(
        g,
        D.app_internal,
        DIS.Application,
        name=Literal("Internal LAN app"),
        description=Literal("desc"),
        applicationType=DIS.SYSTEM_OF_RECORD,
        networkScope=DIS.SCOPE_INTERNAL,
        baseUrl=Literal("http://10.20.10.155:5000"),
    )
    report = validate(g, inference="none")
    assert report.conforms, report.results


# ---------- G5: Function-Scoped Access Gates ----------


def test_g5_allowed_function_permits_matching_bound_function(dossier, validate):
    g = dossier("retail")
    g.add((D["emm-product"], DIS.supportedMode, DIS.UPDATE))
    ep_mut = _ep(g, D.ep_mut_g5, httpMethod=DIS.POST, mutates=Literal(True))
    fn_allowed = _fn(g, D.fn_allowed, callsEndpoint=ep_mut, writesEntity=D.product)

    add_node(
        g,
        D.gate_scoped,
        DIS.AccessGateMatrix,
        matrixRole=ROLE,
        matrixEntity=D.product,
        allowedMode=DIS.UPDATE,
        allowedFunction=fn_allowed,
        name=Literal("scoped gate"),
        description=Literal("desc"),
    )
    t = D.t_scoped_ok
    add_triplet(g, t, ROLE, D.product, DIS.UPDATE, boundFunction=fn_allowed)

    report = validate(g, inference="none")
    assert report.conforms, report.results


def test_g5_allowed_function_rejects_unlisted_bound_function(dossier, validate):
    g = dossier("retail")
    g.add((D["emm-product"], DIS.supportedMode, DIS.UPDATE))
    ep_mut = _ep(g, D.ep_mut_g5_2, httpMethod=DIS.POST, mutates=Literal(True))
    fn_allowed = _fn(g, D.fn_allowed2, callsEndpoint=ep_mut, writesEntity=D.product)
    fn_unlisted = _fn(g, D.fn_unlisted, callsEndpoint=ep_mut, writesEntity=D.product)

    add_node(
        g,
        D.gate_scoped2,
        DIS.AccessGateMatrix,
        matrixRole=ROLE,
        matrixEntity=D.product,
        allowedMode=DIS.UPDATE,
        allowedFunction=fn_allowed,
        name=Literal("scoped gate"),
        description=Literal("desc"),
    )
    t = D.t_scoped_bad
    add_triplet(g, t, ROLE, D.product, DIS.UPDATE, boundFunction=fn_unlisted)

    report = validate(g, inference="none")
    assert not report.conforms
    assert any(
        r.shape == "TripletWithinAllowedFunctionGateShape" and r.focus == "t_scoped_bad"
        for r in report.violations()
    )


# ---------- G3: BindingStatus on Triplet ----------


def test_g3_binding_status_accepted_on_triplet(dossier, validate):
    g = dossier("retail")
    t = D.t_manual
    add_triplet(
        g,
        t,
        ROLE,
        ENTITY,
        DIS.READ,
        bindingStatus=DIS.MANUAL_PROCEDURE,
        unboundReason=Literal("Executed by manual visual check"),
    )
    report = validate(g, inference="none")
    assert report.conforms, report.results


def _local(prop):
    s = str(prop)
    return s.rsplit("/", 1)[-1] if "/" in s else s.rsplit("#", 1)[-1]
