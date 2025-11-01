# OpenAI Agent Audit

## IMPLEMENTED
- Interface `AgentAdapter` inheritance.
- Initialization via `SPECDRIFT_OPENAI_API_KEY` (currently throws ValueError if missing).
- Tool definitions mapping to sandbox functions (read, write, command, tests).
- Iterative loop logic integrated via `step()` called by `TaskRunner`.

## SCAFFOLDED / MOCKED
- The actual call to the `openai.ChatCompletion` API. Currently it simulates an API turn by just appending a fake "list_files" tool call and incrementing a trace step counter.
- The `messages` context array is updated with system prompt and drift alerts, but never submitted to the API.
- Token tracking, latency, and cost calculations are simulated or skipped.

## UNTESTED
- True network-layer interaction.
- Handling of API timeouts, RateLimits, or context window overflows.
- Efficacy of the LLM in understanding the sandbox boundaries.
