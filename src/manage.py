#!/project/.venv/bin/python
import os
import sys


def activate_virtual_environment():
    """Activate the virtual environment explicitly"""
    venv_path = '/project/.venv'
    if os.path.exists(venv_path):
        activate_script = os.path.join(venv_path, 'bin', 'activate_this.py')
        if os.path.exists(activate_script):
            with open(activate_script) as f:
                exec(f.read(), {'__file__': activate_script})


activate_virtual_environment()


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
