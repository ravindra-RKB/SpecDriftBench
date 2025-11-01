import pytest
from specdrift.core.models import TaskDefinition, DriftCategory, DriftSeverity
from specdrift.drift.manager import DriftManager

def test_task_schema():
    data = {
        "task_id": "test_1",
        "title": "Test",
        "initial_description": "Desc",
        "initial_requirements": ["Req 1"],
        "constraints": [],
        "setup_command": "echo",
        "test_command": "pytest",
        "expected_behavior": "Works",
        "grading_rubric": "Passes",
        "difficulty": "LOW",
        "category": "test",
        "drift_events": [
            {
                "drift_id": "d1",
                "type": "REQUIREMENT_DRIFT",
                "trigger_condition": "step: 2",
                "message": "Change",
                "affected_components": ["comp"],
                "expected_agent_response": "Adapts",
                "severity": "LOW",
                "authoritative_source": "Me"
            }
        ]
    }
    task = TaskDefinition.model_validate(data)
    assert task.task_id == "test_1"
    assert len(task.drift_events) == 1

def test_drift_manager():
    data = {
        "task_id": "test_1",
        "title": "Test",
        "initial_description": "Desc",
        "initial_requirements": ["Req 1"],
        "constraints": [],
        "setup_command": "echo",
        "test_command": "pytest",
        "expected_behavior": "Works",
        "grading_rubric": "Passes",
        "difficulty": "LOW",
        "category": "test",
        "drift_events": [
            {
                "drift_id": "d1",
                "type": "REQUIREMENT_DRIFT",
                "trigger_condition": "step: 2",
                "message": "Change",
                "affected_components": ["comp"],
                "expected_agent_response": "Adapts",
                "severity": "LOW",
                "authoritative_source": "Me"
            }
        ]
    }
    task = TaskDefinition.model_validate(data)
    manager = DriftManager(task.drift_events)
    
    assert manager.step() is None
    assert manager.step() is not None # Step 2
    assert manager.step() is None
    assert len(manager.get_visible_events()) == 1
