#!/usr/bin/env python
import os
import sys

if not sys.prefix.endswith('.venv'):
    venv_path = os.path.join(os.path.dirname(__file__), '..', '.venv')
    if os.path.exists(venv_path):
        activate_this = os.path.join(venv_path, 'bin', 'activate_this.py')
        if os.path.exists(activate_this):
            with open(activate_this) as f:
                code = compile(f.read(), activate_this, 'exec')
                exec(code, {'__file__': activate_this})


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.base")
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
    main()