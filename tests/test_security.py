import pytest
import os
from specdrift.agents.openai_agent import OpenAIAgent
from specdrift.core.models import TaskDefinition

def test_path_traversal_prevention(tmp_path):
    # Mock environment variable to bypass missing API key for instantiation
    os.environ["SPECDRIFT_OPENAI_API_KEY"] = "dummy"
    os.environ["SPECDRIFT_OPENAI_MODEL"] = "gpt-4-turbo"
    agent = OpenAIAgent("openai")
    
    # Mock workspace setup
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    
    # Setup dummy task just to satisfy init requirements if needed
    task = TaskDefinition(
        task_id="t1", title="title", initial_description="desc",
        initial_requirements=[], constraints=[], setup_command="echo", test_command="pytest",
        expected_behavior="", grading_rubric="", difficulty="LOW", category="test", drift_events=[]
    )
    
    agent.start_task(task, str(workspace))
    
    # Test safe_path traversal
    res = agent.execute_tool("read_file", {"path": "../outside.txt"})
    assert "access denied" in res
    
    res = agent.execute_tool("write_file", {"path": "/etc/passwd", "content": "hack"})
    assert "access denied" in res
    
    res = agent.execute_tool("list_files", {"path": "../../"})
    assert "access denied" in res
