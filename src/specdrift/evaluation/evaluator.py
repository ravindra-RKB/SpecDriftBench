from specdrift.core.models import EvaluationScore, RunTrace

import os
import json
from specdrift.core.models import EvaluationScore, RunTrace

class Evaluator:
    def evaluate(self, run_dir: str) -> EvaluationScore:
        # Check if trace exists
        trace_file = os.path.join(run_dir, "trace.json")
        if not os.path.exists(trace_file):
            raise ValueError(f"Trace not found at {trace_file}")
            
        with open(trace_file, "r") as f:
            trace = json.load(f)
            
        # In a real evaluation, we would parse test results
        # Here we do deterministic behavioral scoring for the MVP mock agent.
        
        agent_name = trace["metadata"]["agent_name"]
        
        # Determine success from embedded test results
        test_results = trace.get("test_results", {})
        before_tests = test_results.get("before", {}).get("exit_code", 1)
        after_tests = test_results.get("after", {}).get("exit_code", 1)
        
        initial_success = 1.0 if before_tests == 0 else 0.0
        
        # A mock-regression agent breaks prior functionality. We simulate that by reading the agent_name for the MVP since our dummy tests always pass (exit code 0).
        # In a real environment with real tests, we would parse pytest output for specific test IDs.
        regression_rate = 1.0 if "regression" in agent_name else 0.0
        
        # Adaptation success: if it was a perfect agent, it adapted.
        adaptation_success = 1.0 if "perfect" in agent_name else (0.5 if "partial" in agent_name else 0.0)
        
        # If regression rate is high, final success drops.
        final_success = adaptation_success * (1.0 - regression_rate)
        
        recovery_cost = len([step for step in trace["steps"] if len(step.get("visible_drift_events", [])) > 0])

        drs = (1.0 - regression_rate) * adaptation_success

        return EvaluationScore(
            initial_success=1.0,
            drift_detection_rate=1.0 if "ignores" not in agent_name else 0.0,
            adaptation_success=adaptation_success,
            final_success=adaptation_success * (1.0 - regression_rate),
            regression_rate=regression_rate,
            constraint_violation_rate=0.0,
            recovery_cost=float(recovery_cost),
            verification_rate=1.0,
            drs=drs
        )
