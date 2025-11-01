# Research Notes

## Experimental Design
- We must establish a baseline using identical tasks *without* drift to measure the true cost of adaptation.
- LLM judges should be heavily restricted. Deterministic tests are preferred.

## Contamination Mitigation
- Task prompts and drift conditions should be parameterized to prevent exact string matching in training data.
- The evaluation engine should support "hidden" drift events not present in the public repository.

## Future Work
- Implement a human-in-the-loop review interface for agent traces.
- Add more complex adversarial drift scenarios (e.g., outdated StackOverflow answers embedded in issues).
