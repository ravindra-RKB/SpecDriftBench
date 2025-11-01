from abc import ABC, abstractmethod
from typing import List
from specdrift.core.models import TaskDefinition, AgentTraceStep, RunTrace, RunMetadata
import time

class AgentAdapter(ABC):
    def __init__(self, name: str):
        self.name = name
        self.trace_steps: List[AgentTraceStep] = []

    @abstractmethod
    def start_task(self, task: TaskDefinition, workspace_dir: str):
        pass

    @abstractmethod
    def step(self, drift_message: str = None) -> bool:
        """Executes one step of the agent. Returns False if finished."""
        pass

    def get_trace(self, run_id: str, task_id: str, version: str) -> RunTrace:
        return RunTrace(
            metadata=RunMetadata(
                run_id=run_id,
                task_id=task_id,
                agent_name=self.name,
                timestamp=time.time(),
                benchmark_version=version
            ),
            steps=self.trace_steps
        )
