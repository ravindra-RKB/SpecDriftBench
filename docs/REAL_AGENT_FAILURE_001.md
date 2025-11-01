# Real Agent Failure 001

## Status
EXPERIMENT BLOCKED

## Reason
The preflight diagnostic correctly intercepted execution before the agent could run. The pipeline is structurally secure and blocks execution when mandatory environment constraints are missing.

## Doctor Output
```
SpecDriftBench Environment

Python               OK
OpenAI SDK           MISSING
API Key              MISSING
Model                MISSING
Docker CLI           MISSING
Docker daemon        UNAVAILABLE
Docker image         MISSING
Required task dependencies OK

REAL EXPERIMENT: BLOCKED
```

## Trace Validation
No trace generated.

## Next Steps
To run the genuine benchmark, the host environment must provide:
1. Docker daemon running locally (`docker info` must pass).
2. The `specdrift-sandbox` image must be built.
3. Python `openai` SDK installed.
4. `SPECDRIFT_OPENAI_API_KEY` set.
5. `SPECDRIFT_OPENAI_MODEL` explicitly defined.
