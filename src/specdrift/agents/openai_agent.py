import os
import time
import uuid
import subprocess
from typing import List, Dict, Any, Optional

from specdrift.agents.base import AgentAdapter
from specdrift.core.models import TaskDefinition, AgentTraceStep

class OpenAIAgent(AgentAdapter):
    def __init__(self, name: str = "openai"):
        super().__init__(name)
        self.api_key = os.environ.get("SPECDRIFT_OPENAI_API_KEY")
        self.model = os.environ.get("SPECDRIFT_OPENAI_MODEL")
        
        if not self.api_key:
            print("Real model execution could not be validated because credentials were unavailable.")
            raise ValueError("SPECDRIFT_OPENAI_API_KEY environment variable is missing.")
            
        if not self.model:
            print("Real model execution could not be validated because model is not configured.")
            raise ValueError("SPECDRIFT_OPENAI_MODEL environment variable is missing. Explicit model selection is required.")
            
        print("API key: configured")
        print("Model: configured")
            
        self.task: Optional[TaskDefinition] = None
        self.workspace_dir: Optional[str] = None
        self.drift_messages: List[str] = []
        self.is_finished = False

    def start_task(self, task: TaskDefinition, workspace_dir: str):
        self.task = task
        self.workspace_dir = workspace_dir
        self.drift_messages = []
        self.is_finished = False
        self.trace_steps = []
        self.messages = [{"role": "system", "content": "You are an autonomous AI coding agent."}]
        
        # In a real implementation, we would send the initial system prompt 
        # and task description to the OpenAI API here.

    def step(self, drift_message: str = None) -> bool:
        if self.is_finished:
            return False

        if drift_message:
            self.drift_messages.append(drift_message)
            self.messages.append({"role": "user", "content": f"DRIFT ALERT: {drift_message}"})

        # Try to import openai, if fails, we abort
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
        except ImportError:
            print("Real model execution could not be validated because credentials were unavailable.")
            self.is_finished = True
            return False

        # Real API request
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=self._get_tools_schema(),
                tool_choice="auto"
            )
            
            msg = response.choices[0].message
            self.messages.append(msg)
            
            if msg.tool_calls:
                for tool_call in msg.tool_calls:
                    import json
                    args = json.loads(tool_call.function.arguments)
                    result = self.execute_tool(tool_call.function.name, args)
                    
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })
                    
                    self.trace_steps.append(
                        AgentTraceStep(
                            timestamp=time.time(),
                            action_id=tool_call.id,
                            action_type="tool_call",
                            command=tool_call.function.name,
                            arguments=args,
                            files_changed=[],
                            visible_drift_events=list(self.drift_messages)
                        )
                    )
            else:
                self.is_finished = True
                
        except Exception as e:
            print(f"API Error: {e}")
            self.is_finished = True

        return not self.is_finished

    def _get_tools_schema(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read file contents",
                    "parameters": {
                        "type": "object",
                        "properties": {"path": {"type": "string"}},
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Write to a file",
                    "parameters": {
                        "type": "object",
                        "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
                        "required": ["path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_files",
                    "description": "List directory contents",
                    "parameters": {
                        "type": "object",
                        "properties": {"path": {"type": "string"}},
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "run_command",
                    "description": "Run a shell command",
                    "parameters": {
                        "type": "object",
                        "properties": {"command": {"type": "string"}},
                        "required": ["command"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "run_tests",
                    "description": "Run test suite",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
        ]

    def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> str:
        """Restricted tool set execution inside the workspace"""
        safe_path = lambda p: os.path.abspath(os.path.join(self.workspace_dir, p))
        
        if tool_name == "read_file":
            p = safe_path(args["path"])
            if not p.startswith(os.path.abspath(self.workspace_dir)): return "Error: access denied"
            try:
                with open(p, "r") as f: return f.read()
            except Exception as e: return str(e)
            
        elif tool_name == "write_file":
            p = safe_path(args["path"])
            if not p.startswith(os.path.abspath(self.workspace_dir)): return "Error: access denied"
            try:
                with open(p, "w") as f: f.write(args["content"])
                return "Success"
            except Exception as e: return str(e)
            
        elif tool_name == "list_files":
            p = safe_path(args.get("path", "."))
            if not p.startswith(os.path.abspath(self.workspace_dir)): return "Error: access denied"
            try:
                return "\n".join(os.listdir(p))
            except Exception as e: return str(e)
            
        elif tool_name == "run_command":
            cmd = args["command"]
            try:
                result = subprocess.run(cmd, shell=True, cwd=self.workspace_dir, capture_output=True, text=True, timeout=10)
                return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            except subprocess.TimeoutExpired:
                return "Error: timeout"
            except Exception as e:
                return str(e)
                
        elif tool_name == "run_tests":
            return self.execute_tool("run_command", {"command": self.task.test_command})
            
        elif tool_name == "inspect_diff":
            # Just a placeholder for diff
            return "Diff output..."
            
        return "Error: Unknown tool"
