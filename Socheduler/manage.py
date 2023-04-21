#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
from pathlib import Path
import os
import sys


def load_env_vars():
    env_file_path = Path(__file__).parent.parent / ".env"
    with open(env_file_path, "r") as f:
        [os.environ.setdefault(line.split("=")[0], line.split("=")[1]) for line in f]


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Socheduler.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    load_env_vars()
    main()
