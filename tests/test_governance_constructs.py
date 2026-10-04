"""RAV-1947 gap 5 / gap 6 / gap 7 closure: the eight governance and value
constructs ported from 1.6, the APPROVED-needs-approver and
comparison-of-a-dossier-with-itself SPARQL shapes, dossier metadata, the two
new views, dis:AccessGate's removal, and dis:roleType/dis:entityType's
declaration.

One positive + one negative case per new shape: a complete node conforms; a
node missing its one sh:minCount 1 field is rejected by that specific shape.
"""
from decimal import Decimal

from rdflib import RDF, OWL, Literal, XSD

from conftest import DIS, D, add_node


# ---------- TagDefinition ----------


def test_tagdefinition_complete_conforms(dossier, validate):
    g = dossier("retail")
    add_node(
        g, D.tag_channel, DIS.TagDefinition,
        name=Literal("Channel"), description=Literal("How the inquiry arrived."),
        allowedValue=[Literal("voice"), Literal("chat")],
        multiSelect=Literal(False),
    )
    report = validate(g, inference="none")
    assert report.conforms, report.results


def test_tagdefinition_missing_allowedvalue_rejected(dossier, validate):
    g = dossier("retail")
    add_node(
        g, D.tag_channel, DIS.TagDefinition,
        name=Literal("Channel"), description=Literal("How the inquiry arrived."),
        multiSelect=Literal(False),
    )
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "tag_channel" and r.path == "allowedValue" for r in report.violations())


# ---------- PrivacyManifest ----------

PRIVACY_OK = dict(
    name=Literal("Product PII manifest"),
    description=Literal("Governs product-level personal data."),
    governsAttribute=Literal("/product/owner"),
    dataCategory=DIS.PII,
    processingPurpose=DIS.OPERATIONS,
    storagePolicy=DIS.ENCRYPTED_AT_REST,
)


def test_privacymanifest_complete_conforms(dossier, validate):
    g = dossier("retail")
    add_node(g, D.privacy_product, DIS.PrivacyManifest, **PRIVACY_OK)
    report = validate(g, inference="none")
    assert report.conforms, report.results


def test_privacymanifest_missing_datacategory_rejected(dossier, validate):
    g = dossier("retail")
    props = dict(PRIVACY_OK)
    props["dataCategory"] = None
    add_node(g, D.privacy_product, DIS.PrivacyManifest, **props)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "privacy_product" and r.path == "dataCategory" for r in report.violations())


def test_privacymanifest_governsattribute_without_leading_slash_rejected(dossier, validate):
    g = dossier("retail")
    props = dict(PRIVACY_OK)
    props["governsAttribute"] = Literal("product/owner")
    add_node(g, D.privacy_product, DIS.PrivacyManifest, **props)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "privacy_product" and r.path == "governsAttribute" for r in report.violations())


# ---------- TelemetryConfiguration ----------


def test_telemetryconfiguration_complete_conforms(dossier, validate):
    g = dossier("retail")
    add_node(
        g, D.telemetry_default, DIS.TelemetryConfiguration,
        name=Literal("Default telemetry"), description=Literal("Baseline observability."),
        logLevel=DIS.LOG_ERROR,
    )
    report = validate(g, inference="none")
    assert report.conforms, report.results


def test_telemetryconfiguration_missing_name_rejected(dossier, validate):
    g = dossier("retail")
    add_node(
        g, D.telemetry_default, DIS.TelemetryConfiguration,
        description=Literal("Baseline observability."),
        logLevel=DIS.LOG_ERROR,
    )
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "telemetry_default" and r.path == "name" for r in report.violations())


# ---------- MarketplaceEntry ----------

MARKETPLACE_OK = dict(
    name=Literal("Retail Support listing"),
    description=Literal("Publishes the retail support dossier."),
    listsDossier=D[""],
    publisherName=Literal("Ravenhelm"),
    pricingModel=DIS.FREE,
    marketplaceCategory=DIS.RETAIL,
)


def test_marketplaceentry_complete_conforms(dossier, validate):
    g = dossier("retail")
    add_node(g, D.listing, DIS.MarketplaceEntry, **MARKETPLACE_OK)
    report = validate(g, inference="none")
    assert report.conforms, report.results


def test_marketplaceentry_missing_pricingmodel_rejected(dossier, validate):
    g = dossier("retail")
    props = dict(MARKETPLACE_OK)
    props["pricingModel"] = None
    add_node(g, D.listing, DIS.MarketplaceEntry, **props)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "listing" and r.path == "pricingModel" for r in report.violations())


def test_marketplaceentry_documentationurl_http_rejected(dossier, validate):
    g = dossier("retail")
    props = dict(MARKETPLACE_OK)
    props["documentationUrl"] = Literal("http://example.test/docs")
    add_node(g, D.listing, DIS.MarketplaceEntry, **props)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "listing" and r.path == "documentationUrl" for r in report.violations())


# ---------- ChangeManagementRecord ----------

CHANGE_OK = dict(
    name=Literal("Bump to 1.1.0"),
    description=Literal("Adds the loyalty-program entity."),
    recordsChangeTo=D[""],
    toVersion=Literal("1.1.0"),
    changeStatus=DIS.PENDING_REVIEW,
    submittedBy=Literal("nate"),
)


def test_changemanagementrecord_complete_conforms(dossier, validate):
    g = dossier("retail")
    add_node(g, D.change_1, DIS.ChangeManagementRecord, **CHANGE_OK)
    report = validate(g, inference="none")
    assert report.conforms, report.results


def test_changemanagementrecord_missing_toversion_rejected(dossier, validate):
    g = dossier("retail")
    props = dict(CHANGE_OK)
    props["toVersion"] = None
    add_node(g, D.change_1, DIS.ChangeManagementRecord, **props)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "change_1" and r.path == "toVersion" for r in report.violations())


def test_approved_change_without_approver_rejected(dossier, validate):
    g = dossier("retail")
    props = dict(CHANGE_OK)
    props["changeStatus"] = DIS.APPROVED
    add_node(g, D.change_1, DIS.ChangeManagementRecord, **props)
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "change_1" and r.shape == "ApprovedChangeNamesApproverShape" for r in report.violations())


def test_approved_change_with_approver_accepted(dossier, validate):
    g = dossier("retail")
    props = dict(CHANGE_OK)
    props["changeStatus"] = DIS.APPROVED
    props["approver"] = Literal("qa-regulatory")
    add_node(g, D.change_1, DIS.ChangeManagementRecord, **props)
    report = validate(g, inference="none")
    assert report.conforms, report.results


# ---------- ValueEngineeringProfile ----------


def test_valueengineeringprofile_complete_conforms(dossier, validate):
    g = dossier("retail")
    add_node(
        g, D.vep_baseline, DIS.ValueEngineeringProfile,
        name=Literal("AS-IS baseline"), description=Literal("Current manual handling cost."),
        currency=DIS.USD, avgLaborRatePerHour=Literal(Decimal("35.0"), datatype=XSD.decimal),
    )
    report = validate(g, inference="none")
    assert report.conforms, report.results


def test_valueengineeringprofile_missing_description_rejected(dossier, validate):
    g = dossier("retail")
    add_node(
        g, D.vep_baseline, DIS.ValueEngineeringProfile,
        name=Literal("AS-IS baseline"),
        currency=DIS.USD,
    )
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "vep_baseline" and r.path == "description" for r in report.violations())


# ---------- DossierComparison ----------


def test_dossiercomparison_complete_conforms(dossier, validate):
    g = dossier("retail")
    add_node(
        g, D.comparison_1, DIS.DossierComparison,
        name=Literal("Discovery vs Design"), description=Literal("What the redesign changes."),
        comparesDiscovery=D["discovery/"], comparesDesign=D[""],
    )
    report = validate(g, inference="none")
    assert report.conforms, report.results


def test_dossiercomparison_missing_comparesdesign_rejected(dossier, validate):
    g = dossier("retail")
    add_node(
        g, D.comparison_1, DIS.DossierComparison,
        name=Literal("Discovery vs Design"), description=Literal("What the redesign changes."),
        comparesDiscovery=D["discovery/"],
    )
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "comparison_1" and r.path == "comparesDesign" for r in report.violations())


def test_dossiercomparison_with_itself_rejected(dossier, validate):
    g = dossier("retail")
    add_node(
        g, D.comparison_self, DIS.DossierComparison,
        name=Literal("Self comparison"), description=Literal("A modelling mistake."),
        comparesDiscovery=D[""], comparesDesign=D[""],
    )
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(
        r.focus == "comparison_self" and r.shape == "ComparisonIsBetweenTwoDossiersShape"
        for r in report.violations()
    )


# ---------- KnowledgeDocument ----------


def test_knowledgedocument_complete_conforms(dossier, validate):
    g = dossier("retail")
    add_node(
        g, D.doc_faq, DIS.KnowledgeDocument,
        name=Literal("Allergen FAQ"), description=Literal("Reference document for support agents."),
    )
    report = validate(g, inference="none")
    assert report.conforms, report.results


def test_knowledgedocument_missing_name_rejected(dossier, validate):
    g = dossier("retail")
    add_node(g, D.doc_faq, DIS.KnowledgeDocument, description=Literal("Reference document."))
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.focus == "doc_faq" and r.path == "name" for r in report.violations())


# ---------- dossier metadata ----------


def test_dossier_metadata_on_retail_conforms(dossier, validate):
    g = dossier("retail")
    report = validate(g, inference="none")
    assert report.conforms, report.results


def test_dossier_metadata_bad_dossiertype_rejected(dossier, validate):
    g = dossier("retail")
    root = D[""]
    g.remove((root, DIS.dossierType, None))
    g.add((root, DIS.dossierType, DIS.NOT_A_REAL_TYPE))
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.path == "dossierType" for r in report.violations())


def test_dossier_metadata_bad_dossierstatus_rejected(dossier, validate):
    g = dossier("retail")
    root = D[""]
    g.remove((root, DIS.dossierStatus, None))
    g.add((root, DIS.dossierStatus, DIS.NOT_A_REAL_STATUS))
    report = validate(g, inference="none")
    assert not report.conforms
    assert any(r.path == "dossierStatus" for r in report.violations())


# ---------- gap 5: dis:AccessGate is gone ----------


def test_accessgate_class_removed_from_vocab(vocab):
    assert (DIS.AccessGate, RDF.type, OWL.Class) not in vocab
    assert list(vocab.subjects(RDF.type, DIS.AccessGate)) == []


# ---------- gap 4: roleType / entityType are declared properties ----------


def test_roletype_and_entitytype_are_declared_properties(vocab):
    prop_types = {OWL.ObjectProperty, OWL.DatatypeProperty, RDF.Property}
    assert set(vocab.objects(DIS.roleType, RDF.type)) & prop_types
    assert set(vocab.objects(DIS.entityType, RDF.type)) & prop_types
