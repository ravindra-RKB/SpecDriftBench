FROM python:3.11-slim

# Create a non-root user
RUN useradd -m -s /bin/bash agentuser

# Set up working directory
WORKDIR /workspace
RUN chown agentuser:agentuser /workspace

# Install common testing tools (e.g. pytest)
RUN pip install --no-cache-dir pytest

# Switch to non-root user
USER agentuser

# Start an idle process to keep container alive if needed, or rely on execution commands
CMD ["tail", "-f", "/dev/null"]
