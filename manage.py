#!/usr/bin/env python
import os
import sys


base_dir = os.path.dirname(os.path.abspath(__file__))
venv_path = os.path.join(base_dir, '..', '.venv')

if os.path.exists(venv_path):
    site_packages = os.path.join(venv_path, 'lib', f'python{sys.version_info.major}.{sys.version_info.minor}', 'site-packages')
    if os.path.exists(site_packages):
        sys.path.insert(0, site_packages)
        
    bin_path = os.path.join(venv_path, 'bin')
    if os.path.exists(bin_path):
        os.environ['PATH'] = bin_path + os.pathsep + os.environ.get('PATH', '')

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.base")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()