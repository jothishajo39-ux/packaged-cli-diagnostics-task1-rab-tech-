import os
import shutil
import subprocess
import sys


def get_system_info():
    total, used, free = shutil.disk_usage(os.getcwd())

    return {
        "python_version": sys.version.split()[0],
        "python_executable": sys.executable,
        "platform": sys.platform,
        "disk_space": {
            "total_gb": round(total / (1024 ** 3), 2),
            "used_gb": round(used / (1024 ** 3), 2),
            "free_gb": round(free / (1024 ** 3), 2),
        },
        "environment": {
            "PATH_configured": bool(os.environ.get("PATH")),
            "VIRTUAL_ENV": os.environ.get("VIRTUAL_ENV"),
        },
        "developer_tools": detect_tools(),
    }


def detect_tools():
    tools = {}
    for name, command in {
        "git": ["git", "--version"],
        "pip": [sys.executable, "-m", "pip", "--version"],
        "pytest": [sys.executable, "-m", "pytest", "--version"],
    }.items():
        try:
            result = subprocess.run(
                command, capture_output=True, text=True, timeout=5
            )
            tools[name] = {
                "installed": result.returncode == 0,
                "version": result.stdout.strip() or result.stderr.strip(),
            }
        except (OSError, subprocess.SubprocessError):
            tools[name] = {"installed": False, "version": None}
    return tools
