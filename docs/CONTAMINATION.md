# Benchmark Contamination

Contamination is a major threat to validity in coding agent benchmarks. If an agent's training data contains the tasks or the solutions to the drift events, its performance will be artificially inflated.

## Threat Model
1. **Public Task Exposure**: Tasks hosted in this public repository will inevitably be scraped into pre-training corpora (e.g., GitHub scrapes, Common Crawl).
2. **Hidden Drift Events**: If the prompt and final solution are correlated during RLHF, the agent might jump to the final solution without observing the drift.

## Mitigation Strategies (Phase 2 & Beyond)
- **Parameterized Tasks**: Instead of hard-coding the scenario, the framework supports dynamically generated variants of the base tasks.
- **Held-out Tasks**: A private evaluation set containing 50 additional, unreleased tasks will be maintained separately from the public MVP tasks.
- **Benchmark Refresh Strategy**: The public benchmark tasks will be rotated periodically, and performance discrepancies between the public and private sets will be monitored to detect contamination.

*Note: We do not claim this public MVP is currently contamination-resistant. Future formal evaluations must use the private held-out set.*
