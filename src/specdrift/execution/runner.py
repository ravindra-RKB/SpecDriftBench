import os
import shutil
import subprocess
import uuid
import yaml
import json
from pydantic import parse_obj_as
from specdrift.core.models import TaskDefinition
from specdrift.drift.manager import DriftManager
from specdrift.agents.base import AgentAdapter

class TaskRunner:
    def __init__(self, task_dir: str, agent: AgentAdapter, runs_dir: str = "runs", execution_mode: str = "docker"):
        self.task_dir = task_dir
        self.agent = agent
        self.runs_dir = runs_dir
        self.execution_mode = execution_mode
        self.run_id = f"run_{uuid.uuid4().hex[:8]}"

    def load_task(self) -> TaskDefinition:
        with open(os.path.join(self.task_dir, "task.yaml"), "r") as f:
            data = yaml.safe_load(f)
        return TaskDefinition.model_validate(data)

    def run(self) -> str:
        task = self.load_task()
        run_path = os.path.join(self.runs_dir, self.run_id)
        workspace = os.path.join(run_path, "workspace")
        os.makedirs(workspace, exist_ok=True)
        
        # Copy task files to workspace
        if os.path.exists(os.path.join(self.task_dir, "initial_code")):
            shutil.copytree(os.path.join(self.task_dir, "initial_code"), workspace, dirs_exist_ok=True)
        if os.path.exists(os.path.join(self.task_dir, "tests")):
            shutil.copytree(os.path.join(self.task_dir, "tests"), os.path.join(workspace, "tests"), dirs_exist_ok=True)

        drift_manager = DriftManager(task.drift_events)
        
        from specdrift.execution.docker_runner import DockerExecutor
        executor = None
        
        if self.execution_mode == "docker":
            executor = DockerExecutor()
            try:
                executor.start(workspace)
            except Exception as e:
                print(f"Docker execution failed: {e}")
                raise RuntimeError("Docker is unavailable but execution-mode is set to docker. Stopping.")
        else:
            print("SECURITY WARNING: Running in local execution mode. This is unsafe for untrusted models.")

        print(f"Starting run {self.run_id} for task {task.task_id}")
        
        test_cmd = task.test_command
        if test_cmd.startswith("pytest") and executor is None:
            import sys
            test_cmd = f"{sys.executable} -m {test_cmd}"

        # Run Baseline tests before drift
        print("Running tests BEFORE drift...")
        if executor:
            result_before = executor.execute_command(task.test_command)
        else:
            res = subprocess.run(test_cmd, shell=True, cwd=workspace, capture_output=True, text=True)
            result_before = {"exit_code": res.returncode, "stdout": res.stdout, "stderr": res.stderr}
            
        self.agent.start_task(task, workspace)
        
        active = True
        while active:
            event = drift_manager.step()
            drift_msg = event.message if event else None
            if drift_msg:
                print(f"[DRIFT INJECTED]: {drift_msg}")
                
            active = self.agent.step(drift_message=drift_msg)

        # Run tests AFTER drift
        print("Running tests AFTER drift...")
        if executor:
            result_after = executor.execute_command(task.test_command)
            executor.stop()
        else:
            res = subprocess.run(test_cmd, shell=True, cwd=workspace, capture_output=True, text=True)
            result_after = {"exit_code": res.returncode, "stdout": res.stdout, "stderr": res.stderr}

        # Save trace
        trace = self.agent.get_trace(self.run_id, task.task_id, "0.1.0")
        
        # Embed test results in the trace directly
        trace_dict = trace.model_dump()
        trace_dict["test_results"] = {
            "before": {
                "exit_code": result_before["exit_code"],
                "stdout": result_before["stdout"]
            },
            "after": {
                "exit_code": result_after["exit_code"],
                "stdout": result_after["stdout"]
            }
        }
        
        with open(os.path.join(run_path, "trace.json"), "w") as f:
            json.dump(trace_dict, f, indent=2)
            
        print(f"Run {self.run_id} completed.")
        return self.run_id
