# Real Agent Experiment 001

## Research Question
Can a genuine LLM agent seamlessly handle the entire SpecDriftBench execution pipeline (initial task, sandboxed tools, dynamic drift event, validation) successfully under realistic constraints?

## Model
Unconfigured (SPECDRIFT_OPENAI_MODEL was strictly required but unavailable).

## Task
`task_001_auth_drift`

## Execution mode
`docker`

## Docker image
`specdrift-sandbox` (Dockerfile provided)

## Initial Requirements
Build a simple REST endpoint that accepts username/password.

## Drift Event
REQUIREMENT UPDATE: The /login endpoint must now also support OAuth2 tokens via Authorization header, while preserving backward compatibility for username/password.

## Environment
Local host attempting to bridge to Docker containers, but without OpenAI SDK credentials or Docker daemon running.

## Agent Trace Summary
*No trace generated due to missing credentials.*

## Code Changes
*No changes made.*

## Test Results
*Before drift:* N/A
*After drift:* N/A

## Regression
N/A

## Final score
N/A

## Recovery Cost
N/A

## Failure Analysis
The framework accurately rejected the real execution attempt because:
1. `SPECDRIFT_OPENAI_API_KEY` was missing.
2. `SPECDRIFT_OPENAI_MODEL` was not explicitly configured (fallback behavior disabled per Phase 6 instructions).
3. If credentials were provided, the runner would have immediately thrown `RuntimeError: Docker is unavailable but execution-mode is set to docker. Stopping.`

This correctly prevents invalid, fabricated, or unsafe execution on un-containerized hosts.

## Limitations
Because this pipeline aborted securely at initialization, the semantic reliability of the OpenAI ChatCompletion output handling against the tool schemas could not be measured.
