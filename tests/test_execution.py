import pytest
from specdrift.core.models import RunTrace, RunMetadata, AgentTraceStep
import time

def test_trace_serialization():
    step = AgentTraceStep(
        timestamp=time.time(),
        action_id="123",
        action_type="mock",
        command="write",
        files_changed=["a.py"],
        visible_drift_events=["drift1"]
    )
    
    trace = RunTrace(
        metadata=RunMetadata(
            run_id="run1",
            task_id="task1",
            agent_name="mock",
            timestamp=time.time(),
            benchmark_version="0.1.0"
        ),
        steps=[step]
    )
    
    data = trace.model_dump()
    assert data["metadata"]["run_id"] == "run1"
    assert len(data["steps"]) == 1
    assert data["steps"][0]["action_id"] == "123"
