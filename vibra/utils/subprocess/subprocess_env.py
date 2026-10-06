import platform
import subprocess
from pathlib import Path

PYTHON_VERSION = "3.14t"
VENV_NAME = ".venv-freethreaded-314"
VENV_HASH_FILE = "venv_hash.txt"
REQUIREMENTS_FILE = "requirements.txt"


def project_root() -> Path:
    return Path(__file__).resolve().parents[3]

def folder_path() -> Path:
    return Path(__file__).resolve().parents[0]

def freethreaded_python() -> Path:
    return project_root() / freethreaded_python_without_root()

def freethreaded_python_without_root() -> Path:
    python_target = Path("Scripts/python.exe")
    if platform.system() != "Windows":
        python_target = Path("bin/python")

    return Path(VENV_NAME / python_target)

def get_requirements_file() -> Path:
    return Path(folder_path()/REQUIREMENTS_FILE)

def ensure_freethreaded_env() -> Path:
    generate_freethreaded_env()

def generate_freethreaded_env():
    subprocess.run(["uv", "venv", "--python", f"{PYTHON_VERSION}", f"{VENV_NAME}"], check=False)
    subprocess.run(["uv", "pip", "install", "--python", f"{freethreaded_python_without_root()!s}", "-r", f"{get_requirements_file()!s}"], check=False)
