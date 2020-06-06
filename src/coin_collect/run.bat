set script_dir=%~dp0
set VENV_PYTHON_INTERPRETER=..\..\venv\Scripts\python.exe
start /min %VENV_PYTHON_INTERPRETER% coin_collect.py
