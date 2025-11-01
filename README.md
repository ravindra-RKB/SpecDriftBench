# SpecDriftBench

Evaluating Coding-Agent Reliability Under Changing Requirements

SpecDriftBench is a benchmark for evaluating the reliability of coding agents under changing software-engineering requirements, testing their ability to detect, adapt, and preserve valid work across a variety of drift events.

## Motivation

Most coding benchmarks are static: an agent receives a prompt and writes code. Real-world software engineering is dynamic. Requirements change, dependencies get deprecated, and environments break. SpecDriftBench measures whether agents can handle these realities.

## Research Question

Do state-of-the-art coding agents remain reliable when requirements, dependencies, APIs, infrastructure, security constraints, or authoritative documentation change during execution?

## What Existing Coding Benchmarks Miss

Benchmarks like HumanEval or SWE-bench evaluate an agent's ability to solve a fixed issue. They do not evaluate:
- Recognition of changing constraints.
- Preservation of prior valid work (avoiding regressions).
- Redundant work introduced during adaptation.

## Drift Taxonomy

1. **REQUIREMENT_DRIFT**: Business logic changes.
2. **DEPENDENCY_DRIFT**: Library versions or APIs change.
3. **API_DRIFT**: External schema changes.
4. **INFRASTRUCTURE_DRIFT**: Database or service unavailability.
5. **SECURITY_DRIFT**: New compliance constraints.
6. **PERFORMANCE_DRIFT**: Latency or scale requirements.
7. **DOCUMENTATION_DRIFT**: Misalignment between docs and reality.
8. **CONSTRAINT_DRIFT**: Restrictions on tools or libraries.
9. **ADVERSARIAL_DRIFT**: Conflicting sources of truth.

## Benchmark Architecture

- **Agent Interface**: Provider-agnostic API.
- **Drift Engine**: Deterministic injection of drift events.
- **Evaluation Engine**: Independent metrics for adaptation and regression.

## Metrics

- **Drift Recovery Score (DRS)**: Experimental metric combining final correctness, drift detection, adaptation quality, and regression avoidance.
- **Initial Success**: Correctness before drift.
- **Regression Rate**: Prior requirements broken after drift.
- **Recovery Cost**: Actions required to adapt.

## Quick Start

```bash
pip install -e .[dev]
specdrift run tasks/task_001_auth_drift --agent mock-perfect
specdrift evaluate runs/<RUN_ID>
```

## Running the Mock Benchmark

The repository includes a deterministic `MockAgent` for testing the framework without API calls.

## Results

*(Placeholder for future experimental results. No claims of statistical significance are made at this time.)*

## Limitations

- Synthetic nature of drift events.
- Difficulty in perfectly isolating adaptation cost.
- Potential benchmark contamination.

## Research Ethics

No fabricated results. All trace data and evaluation scripts are open source to ensure reproducibility.
