$env:SPECDRIFT_OPENAI_API_KEY = "dummy_key_for_environment_check"
$env:SPECDRIFT_OPENAI_MODEL = "gpt-4-turbo"
$env:PYTHONPATH="src"
.\venv\Scripts\python src\specdrift\cli.py doctor
.\venv\Scripts\python src\specdrift\cli.py preflight --agent openai --execution-mode docker
