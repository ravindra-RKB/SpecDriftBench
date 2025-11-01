import pytest
from specdrift.experiments.experiment import ExperimentConfig

def test_experiment_config_parsing():
    data = {
        "tasks": ["task_001"],
        "agents": ["mock-perfect"],
        "repetitions": 5,
        "timeout": 100,
        "seed": 42
    }
    config = ExperimentConfig.model_validate(data)
    assert config.repetitions == 5
    assert "task_001" in config.tasks
    assert "mock-perfect" in config.agents
    
def test_experiment_config_defaults():
    data = {
        "tasks": ["all"],
        "agents": ["mock-ignores"]
    }
    config = ExperimentConfig.model_validate(data)
    assert config.repetitions == 1
    assert config.timeout == 300
    assert config.seed == 42
