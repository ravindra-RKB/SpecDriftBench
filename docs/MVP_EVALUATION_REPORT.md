# SpecDriftBench MVP Evaluation

## Research Question
Do state-of-the-art coding agents remain reliable when requirements, dependencies, APIs, infrastructure, security constraints, or authoritative documentation change during execution?

## Benchmark Design
SpecDriftBench evaluates agents by dynamically injecting deterministic drift events into their context during task execution, rather than presenting a static initial prompt.

## Experimental Setup
The MVP framework was validated using a local subprocess runner and a deterministic `MockAgent` capable of perfect adaptation, ignoring drift, and introducing regressions.

## Tasks
10 public tasks spanning 9 drift categories (Requirement, Dependency, API, Infrastructure, Security, Performance, Documentation, Constraint, Adversarial).

## Metrics
- **Initial Success**: Task correctness before drift.
- **Drift Detection Rate**: Both declared (in trace) and behavioral (actions taken).
- **Adaptation Success**: Meeting the new requirements.
- **Regression Rate**: Breaking prior valid functionality.
- **Recovery Cost**: The number of tool calls or files modified.

## Mock-Agent Validation
The framework successfully distinguishes between `mock-perfect` (handles drift without regression) and `mock-regression` (breaks original functionality). The experimental Drift Recovery Score (DRS) correctly reflects these differences.

## Real-Agent Experiments
*No real-model experimental results are included at this time. The OpenAI integration (`OpenAIAgent`) has been implemented as a stub for the MVP Phase 2.*

## Failure Analysis
Expected automated failure categories include: `DRIFT_NOT_DETECTED`, `PARTIAL_ADAPTATION`, and `REGRESSION`. (Automated failure classification is not yet a source of ground truth).

## Limitations
- Evaluator currently relies on stubbed test outcomes for the mock benchmark.
- Publicly available tasks are subject to data contamination.
- AST analysis is currently limited to Python.

## Threats to Validity
- The deterministic injection mechanism (based on step count) may not perfectly map to an asynchronous agent's internal state.
- Automated tests may fail to capture subtle semantic regressions.

## Future Work
- Execute full evaluation with GPT-4, Claude 3, and Gemini 1.5.
- Integrate true sandboxing (Docker).
