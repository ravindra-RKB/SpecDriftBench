import subprocess
import os
import uuid
import time
from typing import Dict, Any

class DockerExecutor:
    def __init__(self, image: str = "specdrift-sandbox"):
        self.image = image
        self.container_id = None
        self.workspace_dir = None
        
    def start(self, workspace_dir: str):
        self.workspace_dir = os.path.abspath(workspace_dir)
        container_name = f"specdrift_{uuid.uuid4().hex[:8]}"
        
        # Build image if it doesn't exist? (Skipping build step here for simplicity, assuming pre-built or built in setup)
        # docker run -d --rm --name {name} -v {workspace}:/workspace -u agentuser --memory=512m --cpus=1 {image} tail -f /dev/null
        cmd = [
            "docker", "run", "-d", "--rm",
            "--name", container_name,
            "-v", f"{self.workspace_dir}:/workspace",
            "--memory=512m",
            "--cpus=1",
            "--network=none",
            self.image
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.container_id = result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to start Docker container: {e.stderr}")
            
    def execute_command(self, command: str, timeout: int = 10) -> Dict[str, Any]:
        if not self.container_id:
            raise RuntimeError("Container not running")
            
        start_time = time.time()
        # docker exec -w /workspace {container} sh -c {command}
        cmd = [
            "docker", "exec", "-w", "/workspace",
            self.container_id, "sh", "-c", command
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            duration = time.time() - start_time
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode,
                "duration": duration,
                "error": None
            }
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return {
                "stdout": "",
                "stderr": "",
                "exit_code": -1,
                "duration": duration,
                "error": "TimeoutExpired"
            }
            
    def stop(self):
        if self.container_id:
            subprocess.run(["docker", "stop", "-t", "1", self.container_id], capture_output=True)
            self.container_id = None
