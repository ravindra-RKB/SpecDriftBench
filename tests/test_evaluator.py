import pytest
import os
import json
from specdrift.evaluation.evaluator import Evaluator

def test_evaluator_missing_trace():
    evaluator = Evaluator()
    with pytest.raises(ValueError):
        evaluator.evaluate("nonexistent_run_dir")

def test_evaluator_perfect_agent(tmp_path):
    run_dir = tmp_path / "run_mock"
    run_dir.mkdir()
    
    trace_data = {
        "metadata": {"agent_name": "mock-perfect"},
        "steps": [
            {"visible_drift_events": ["drift1"]}
        ]
    }
    
    (run_dir / "trace.json").write_text(json.dumps(trace_data))
    
    evaluator = Evaluator()
    score = evaluator.evaluate(str(run_dir))
    
    assert score.adaptation_success == 1.0
    assert score.regression_rate == 0.0
    assert score.drs == 1.0
    assert score.drift_detection_rate == 1.0

def test_evaluator_ignores_agent(tmp_path):
    run_dir = tmp_path / "run_mock"
    run_dir.mkdir()
    
    trace_data = {
        "metadata": {"agent_name": "mock-ignores"},
        "steps": [
            {"visible_drift_events": ["drift1"]}
        ]
    }
    
    (run_dir / "trace.json").write_text(json.dumps(trace_data))
    
    evaluator = Evaluator()
    score = evaluator.evaluate(str(run_dir))
    
    assert score.drift_detection_rate == 0.0
    assert score.adaptation_success == 0.0
    assert score.drs == 0.0

def test_evaluator_regression_agent(tmp_path):
    run_dir = tmp_path / "run_mock"
    run_dir.mkdir()
    
    trace_data = {
        "metadata": {"agent_name": "mock-regression"},
        "steps": [
            {"visible_drift_events": ["drift1"]}
        ]
    }
    
    (run_dir / "trace.json").write_text(json.dumps(trace_data))
    
    evaluator = Evaluator()
    score = evaluator.evaluate(str(run_dir))
    
    assert score.regression_rate == 1.0
    assert score.drs == 0.0
