import yaml
import os

tasks = [
    {
        "task_id": "task_001_auth_drift",
        "title": "REST Authentication Service",
        "initial_description": "Build a simple REST endpoint that accepts username/password.",
        "initial_requirements": ["Endpoint /login accepts JSON POST with username/password.", "Returns 200 OK for valid users."],
        "constraints": ["Use Python stdlib or basic Flask."],
        "setup_command": "echo 'Setup'",
        "test_command": "pytest tests/",
        "drift_events": [
            {
                "drift_id": "drift_auth_oauth",
                "type": "REQUIREMENT_DRIFT",
                "trigger_condition": "step: 2",
                "message": "REQUIREMENT UPDATE: The /login endpoint must now also support OAuth2 tokens via Authorization header, while preserving backward compatibility for username/password.",
                "affected_components": ["auth"],
                "expected_agent_response": "Agent should check for Authorization header before falling back to JSON payload.",
                "severity": "HIGH",
                "authoritative_source": "Product Manager"
            }
        ],
        "expected_behavior": "Both basic and OAuth auth succeed.",
        "grading_rubric": "Initial success: passes basic test. Final success: passes both. Regression: basic test fails after adaptation.",
        "difficulty": "MEDIUM",
        "category": "auth"
    },
    {
        "task_id": "task_002_dependency_drift",
        "title": "Data Parsing Service",
        "initial_description": "Parse CSV data using pandas.",
        "initial_requirements": ["Read CSV file.", "Return JSON list of dicts."],
        "constraints": ["Use pandas 1.x."],
        "setup_command": "echo 'Setup'",
        "test_command": "pytest tests/",
        "drift_events": [
            {
                "drift_id": "drift_dep_pandas",
                "type": "DEPENDENCY_DRIFT",
                "trigger_condition": "step: 3",
                "message": "DEPENDENCY UPDATE: The project is being upgraded to pandas 2.0. The append() method on DataFrame has been removed. You must use pd.concat() instead.",
                "affected_components": ["parser"],
                "expected_agent_response": "Agent should replace append with pd.concat.",
                "severity": "MEDIUM",
                "authoritative_source": "Engineering Manager"
            }
        ],
        "expected_behavior": "Code parses data without using append.",
        "grading_rubric": "Avoids append error",
        "difficulty": "LOW",
        "category": "data"
    },
    {
        "task_id": "task_003_infrastructure_drift",
        "title": "Caching Layer",
        "initial_description": "Implement a caching function using Redis.",
        "initial_requirements": ["Cache results of compute_heavy_function."],
        "constraints": ["Use redis-py."],
        "setup_command": "echo 'Setup'",
        "test_command": "pytest tests/",
        "drift_events": [
            {
                "drift_id": "drift_infra_redis",
                "type": "INFRASTRUCTURE_DRIFT",
                "trigger_condition": "step: 1",
                "message": "INFRASTRUCTURE UPDATE: Redis cluster is down for maintenance. Fall back to in-memory dictionary caching if Redis is unavailable.",
                "affected_components": ["cache"],
                "expected_agent_response": "Agent wraps Redis calls in try-except and falls back to dict.",
                "severity": "HIGH",
                "authoritative_source": "DevOps"
            }
        ],
        "expected_behavior": "Code falls back to dict when Redis fails.",
        "grading_rubric": "Dict fallback used",
        "difficulty": "MEDIUM",
        "category": "caching"
    }
]

for t in tasks:
    dir_name = f"tasks/{t['task_id']}"
    os.makedirs(dir_name, exist_ok=True)
    os.makedirs(os.path.join(dir_name, "tests"), exist_ok=True)
    os.makedirs(os.path.join(dir_name, "initial_code"), exist_ok=True)
    
    with open(os.path.join(dir_name, "task.yaml"), "w") as f:
        yaml.dump(t, f, sort_keys=False)
        
    with open(os.path.join(dir_name, "tests", "test_dummy.py"), "w") as f:
        f.write("def test_dummy():\n    assert True\n")
