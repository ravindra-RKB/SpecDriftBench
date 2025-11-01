# Security Audit

## 1. Credentials
- `SPECDRIFT_OPENAI_API_KEY` is loaded from the environment, never hardcoded.
- Keys are NOT saved in traces or logs.

## 2. Sandbox Paths
- The agent implements `safe_path = lambda p: os.path.abspath(os.path.join(self.workspace_dir, p))`.
- It rigorously checks `if not p.startswith(os.path.abspath(self.workspace_dir)): return "Error: access denied"`.
- This prevents `../../` and absolute host paths from escaping the workspace.

## 3. Subprocess Execution
- `run_command` has a strict `timeout=10` parameter.
- It operates with `cwd=self.workspace_dir`.
- Caution: `shell=True` is used, which theoretically allows complex chains. In a production benchmark, a true container (Docker) should be used instead of host processes, as arbitrary code (e.g. `rm -rf /`) could still theoretically bypass simple path checks if the LLM writes a malicious script. MVP relies on process-level isolation.
