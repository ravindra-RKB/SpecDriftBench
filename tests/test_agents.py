import pytest
from specdrift.agents.mock_agent import MockAgent
from specdrift.core.models import TaskDefinition

@pytest.fixture
def dummy_task():
    return TaskDefinition.model_validate({
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
        "drift_events": []
    })

def test_mock_agent_initialization():
    agent = MockAgent("mock-perfect")
    assert agent.name == "mock-perfect"

def test_mock_agent_step(dummy_task, tmp_path):
    agent = MockAgent("mock-perfect")
    agent.start_task(dummy_task, str(tmp_path))
    
    assert agent.current_step == 0
    active = agent.step()
    assert active is True
    assert agent.current_step == 1
    assert len(agent.trace_steps) == 1

def test_mock_agent_finish(dummy_task, tmp_path):
    agent = MockAgent("mock-perfect", steps_to_finish=1)
    agent.start_task(dummy_task, str(tmp_path))
    agent.step()
    assert agent.step() is False

def test_mock_agent_drift_recording(dummy_task, tmp_path):
    agent = MockAgent("mock-perfect")
    agent.start_task(dummy_task, str(tmp_path))
    agent.step(drift_message="test drift")
    assert "test drift" in agent.drift_messages
    assert "test drift" in agent.trace_steps[-1].visible_drift_events
