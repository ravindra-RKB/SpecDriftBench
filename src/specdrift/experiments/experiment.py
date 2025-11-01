import yaml
import os
from typing import List, Dict, Any
from pydantic import BaseModel

class ExperimentConfig(BaseModel):
    tasks: List[str]
    agents: List[str]
    repetitions: int = 1
    timeout: int = 300
    seed: int = 42

class ExperimentRunner:
    def __init__(self, config_path: str):
        with open(config_path, "r") as f:
            self.config = ExperimentConfig.model_validate(yaml.safe_load(f))
            
    def run_all(self):
        from specdrift.cli import run as cli_run
        
        tasks_to_run = self.config.tasks
        if "all" in tasks_to_run:
            tasks_to_run = [d for d in os.listdir("tasks") if os.path.isdir(os.path.join("tasks", d))]
            
        print(f"Running experiment with {len(self.config.agents)} agents on {len(tasks_to_run)} tasks.")
        print(f"Repetitions: {self.config.repetitions}")
        
        for agent in self.config.agents:
            for task in tasks_to_run:
                for rep in range(self.config.repetitions):
                    task_path = os.path.join("tasks", task)
                    try:
                        cli_run(task_dir=task_path, agent=agent)
                    except Exception as e:
                        print(f"Failed to run {agent} on {task}: {e}")
