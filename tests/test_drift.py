import pytest
from specdrift.drift.taxonomy import DriftCategory, DriftSeverity
from specdrift.core.models import DriftEventDefinition

def test_drift_category_enum():
    assert DriftCategory.REQUIREMENT_DRIFT == "REQUIREMENT_DRIFT"

def test_drift_severity_enum():
    assert DriftSeverity.CRITICAL == "CRITICAL"

def test_drift_event_creation():
    event = DriftEventDefinition(
        drift_id="d1",
        type=DriftCategory.API_DRIFT,
        trigger_condition="step: 1",
        message="API updated",
        affected_components=["api"],
        expected_agent_response="Update endpoint",
        severity=DriftSeverity.MEDIUM,
        authoritative_source="Docs"
    )
    assert event.drift_id == "d1"
