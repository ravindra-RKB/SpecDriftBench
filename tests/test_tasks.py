import pytest
import os
import yaml
from specdrift.core.models import TaskDefinition

def test_all_tasks_loadable():
    tasks_dir = "tasks"
    if not os.path.exists(tasks_dir):
        return
        
    for task_dir in os.listdir(tasks_dir):
        task_path = os.path.join(tasks_dir, task_dir, "task.yaml")
        if os.path.exists(task_path):
            with open(task_path, "r") as f:
                data = yaml.safe_load(f)
            task = TaskDefinition.model_validate(data)
            assert task.task_id.startswith("task_")
            assert len(task.title) > 0
            assert len(task.drift_events) > 0
            
def test_task_directories_exist():
    tasks_dir = "tasks"
    if not os.path.exists(tasks_dir):
        return
        
    for task_dir in os.listdir(tasks_dir):
        if os.path.isdir(os.path.join(tasks_dir, task_dir)):
            assert os.path.exists(os.path.join(tasks_dir, task_dir, "tests"))
            assert os.path.exists(os.path.join(tasks_dir, task_dir, "initial_code"))
