import os
import subprocess
import time
from specdrift.agents.base import AgentAdapter
from specdrift.core.models import TaskDefinition, AgentTraceStep
import uuid

class MockAgent(AgentAdapter):
    def __init__(self, name: str = "mock-perfect", steps_to_finish: int = 5):
        super().__init__(name)
        self.steps_to_finish = steps_to_finish
        self.current_step = 0
        self.task = None
        self.workspace_dir = None
        self.drift_messages = []

    def start_task(self, task: TaskDefinition, workspace_dir: str):
        self.task = task
        self.workspace_dir = workspace_dir
        self.current_step = 0
        # Mock initial implementation
        with open(os.path.join(workspace_dir, "solution.py"), "w") as f:
            f.write("# Initial mock solution\ndef run():\n    return 'initial'\n")

    def step(self, drift_message: str = None) -> bool:
        if self.current_step >= self.steps_to_finish:
            return False
            
        if drift_message:
            self.drift_messages.append(drift_message)
            # Perfect mock adapts to drift immediately
            if "perfect" in self.name:
                with open(os.path.join(self.workspace_dir, "solution.py"), "a") as f:
                    f.write(f"\n# Adapted to: {drift_message}\n")
            elif "regression" in self.name:
                with open(os.path.join(self.workspace_dir, "solution.py"), "w") as f:
                    f.write(f"\n# Completely broke previous behavior\ndef run():\n    return 'broken'\n")
            elif "ignores" in self.name:
                pass # Doesn't do anything

        # Record action
        self.trace_steps.append(
            AgentTraceStep(
                timestamp=time.time(),
                action_id=str(uuid.uuid4()),
                action_type="mock_step",
                command="write_code",
                files_changed=["solution.py"] if not "ignores" in self.name else [],
                visible_drift_events=list(self.drift_messages)
            )
        )
        self.current_step += 1
        return True
