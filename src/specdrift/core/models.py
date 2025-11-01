from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from specdrift.drift.taxonomy import DriftCategory, DriftSeverity

class DriftEventDefinition(BaseModel):
    drift_id: str
    type: DriftCategory
    trigger_condition: str  # e.g., "step: 5", "tool: write_file"
    message: str
    affected_components: List[str]
    expected_agent_response: str
    severity: DriftSeverity
    authoritative_source: str

class TaskDefinition(BaseModel):
    task_id: str
    title: str
    initial_description: str
    initial_requirements: List[str]
    constraints: List[str]
    setup_command: str
    test_command: str
    drift_events: List[DriftEventDefinition]
    expected_behavior: str
    grading_rubric: str
    difficulty: str
    category: str

class AgentTraceStep(BaseModel):
    timestamp: float
    action_id: str
    action_type: str  # e.g. "tool_call", "message"
    command: Optional[str] = None
    arguments: Optional[Dict[str, Any]] = None
    output: Optional[str] = None
    files_changed: List[str] = Field(default_factory=list)
    tests_executed: bool = False
    errors: Optional[str] = None
    visible_drift_events: List[str] = Field(default_factory=list)

class RunMetadata(BaseModel):
    run_id: str
    task_id: str
    agent_name: str
    timestamp: float
    benchmark_version: str

class RunTrace(BaseModel):
    metadata: RunMetadata
    steps: List[AgentTraceStep]

class EvaluationScore(BaseModel):
    initial_success: float
    drift_detection_rate: float
    adaptation_success: float
    final_success: float
    regression_rate: float
    constraint_violation_rate: float
    recovery_cost: float
    verification_rate: float
    drs: float  # Drift Recovery Score
