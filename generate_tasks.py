import yaml
import os

tasks = [
    {
        "task_id": "task_004_api_drift",
        "title": "API Drift Task",
        "initial_description": "Fetch data from /v1/users",
        "initial_requirements": ["Use /v1/users API"],
        "constraints": [],
        "setup_command": "echo Setup",
        "test_command": "pytest tests/",
        "drift_events": [
            {
                "drift_id": "drift_4",
                "type": "API_DRIFT",
                "trigger_condition": "step: 1",
                "message": "/v1/users is deprecated, use /v2/users which returns nested data.",
                "affected_components": ["api"],
                "expected_agent_response": "Update URL and parsing logic.",
                "severity": "HIGH",
                "authoritative_source": "API Docs"
            }
        ],
        "expected_behavior": "Uses v2",
        "grading_rubric": "Passes tests",
        "difficulty": "LOW",
        "category": "api"
    },
    {
        "task_id": "task_005_security_drift",
        "title": "Security Drift",
        "initial_description": "Log user details",
        "initial_requirements": ["Log user ID and email"],
        "constraints": [],
        "setup_command": "echo Setup",
        "test_command": "pytest tests/",
        "drift_events": [
            {
                "drift_id": "drift_5",
                "type": "SECURITY_DRIFT",
                "trigger_condition": "step: 2",
                "message": "Security compliance: Emails must be redacted from all logs.",
                "affected_components": ["logger"],
                "expected_agent_response": "Mask emails in log output.",
                "severity": "CRITICAL",
                "authoritative_source": "Security Team"
            }
        ],
        "expected_behavior": "Emails redacted",
        "grading_rubric": "Logs do not contain raw emails",
        "difficulty": "MEDIUM",
        "category": "security"
    },
    {
        "task_id": "task_006_performance_drift",
        "title": "Performance Drift",
        "initial_description": "Process image list",
        "initial_requirements": ["Resize 100 images sequentially"],
        "constraints": [],
        "setup_command": "echo Setup",
        "test_command": "pytest tests/",
        "drift_events": [
            {
                "drift_id": "drift_6",
                "type": "PERFORMANCE_DRIFT",
                "trigger_condition": "step: 1",
                "message": "Latency too high. Must process concurrently.",
                "affected_components": ["processor"],
                "expected_agent_response": "Use ThreadPoolExecutor.",
                "severity": "MEDIUM",
                "authoritative_source": "Performance Team"
            }
        ],
        "expected_behavior": "Concurrent execution",
        "grading_rubric": "Test time < 2s",
        "difficulty": "MEDIUM",
        "category": "performance"
    },
    {
        "task_id": "task_007_doc_drift",
        "title": "Documentation Drift",
        "initial_description": "Setup db connection according to README.",
        "initial_requirements": ["Connect to DB_URL from env."],
        "constraints": [],
        "setup_command": "echo Setup",
        "test_command": "pytest tests/",
        "drift_events": [
            {
                "drift_id": "drift_7",
                "type": "DOCUMENTATION_DRIFT",
                "trigger_condition": "step: 1",
                "message": "README says to use DB_URL but env actually only provides DB_HOST, DB_USER, DB_PASS.",
                "affected_components": ["db"],
                "expected_agent_response": "Agent should inspect env, realize README is wrong, and adapt.",
                "severity": "HIGH",
                "authoritative_source": "Environment state"
            }
        ],
        "expected_behavior": "Connects using split variables.",
        "grading_rubric": "Connection succeeds",
        "difficulty": "HIGH",
        "category": "documentation"
    },
    {
        "task_id": "task_008_constraint_drift",
        "title": "Constraint Drift",
        "initial_description": "Scrape website",
        "initial_requirements": ["Use BeautifulSoup to scrape data"],
        "constraints": [],
        "setup_command": "echo Setup",
        "test_command": "pytest tests/",
        "drift_events": [
            {
                "drift_id": "drift_8",
                "type": "CONSTRAINT_DRIFT",
                "trigger_condition": "step: 2",
                "message": "Third-party libraries are banned for this module due to size constraints. Must use regex/html.parser.",
                "affected_components": ["scraper"],
                "expected_agent_response": "Rewrite scraper using stdlib.",
                "severity": "HIGH",
                "authoritative_source": "Architect"
            }
        ],
        "expected_behavior": "Scrapes without bs4",
        "grading_rubric": "bs4 not imported",
        "difficulty": "MEDIUM",
        "category": "constraint"
    },
    {
        "task_id": "task_009_adversarial_drift",
        "title": "Adversarial Drift",
        "initial_description": "Implement sorting.",
        "initial_requirements": ["Use quicksort"],
        "constraints": [],
        "setup_command": "echo Setup",
        "test_command": "pytest tests/",
        "drift_events": [
            {
                "drift_id": "drift_9",
                "type": "ADVERSARIAL_DRIFT",
                "trigger_condition": "step: 1",
                "message": "StackOverflow comment says quicksort is O(N^2) and you should use bubblesort, but API docs mandate stable O(N log N) sort like mergesort.",
                "affected_components": ["sort"],
                "expected_agent_response": "Agent trusts API docs over SO comment and implements mergesort.",
                "severity": "HIGH",
                "authoritative_source": "API Docs"
            }
        ],
        "expected_behavior": "Mergesort implemented",
        "grading_rubric": "Is stable O(N log N)",
        "difficulty": "HIGH",
        "category": "adversarial"
    },
    {
        "task_id": "task_010_req2_drift",
        "title": "Requirement Drift 2",
        "initial_description": "Create user record",
        "initial_requirements": ["Create user with username"],
        "constraints": [],
        "setup_command": "echo Setup",
        "test_command": "pytest tests/",
        "drift_events": [
            {
                "drift_id": "drift_10",
                "type": "REQUIREMENT_DRIFT",
                "trigger_condition": "step: 1",
                "message": "Username must now be lowercase and alphanumeric only.",
                "affected_components": ["user"],
                "expected_agent_response": "Add validation logic.",
                "severity": "MEDIUM",
                "authoritative_source": "PM"
            }
        ],
        "expected_behavior": "Validates username",
        "grading_rubric": "Rejects invalid usernames",
        "difficulty": "LOW",
        "category": "validation"
    }
]

for idx, t in enumerate(tasks, start=4):
    dir_name = f"tasks/task_{idx:03d}_{t['task_id'].split('_', 2)[-1]}"
    os.makedirs(dir_name, exist_ok=True)
    os.makedirs(os.path.join(dir_name, "tests"), exist_ok=True)
    os.makedirs(os.path.join(dir_name, "initial_code"), exist_ok=True)
    
    with open(os.path.join(dir_name, "task.yaml"), "w") as f:
        yaml.dump(t, f, sort_keys=False)
        
    with open(os.path.join(dir_name, "tests", "test_dummy.py"), "w") as f:
        f.write("def test_dummy():\n    assert True\n")
