#!/usr/bin/env python
import os
import sys

def setup_venv():
    # Получаем базовый путь
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)
    venv_path = os.path.join(project_root, '.venv')
    
    # Проверяем существование виртуального окружения
    if not os.path.exists(venv_path):
        print(f"Virtual environment not found at {venv_path}")
        return
    
    # Добавляем site-packages в sys.path
    site_packages = os.path.join(
        venv_path, 
        'lib', 
        f'python{sys.version_info.major}.{sys.version_info.minor}',
        'site-packages'
    )
    
    if os.path.exists(site_packages):
        sys.path.insert(0, site_packages)
        print(f"Added site-packages to sys.path: {site_packages}")
    else:
        print(f"Site packages not found at {site_packages}")
    
    # Добавляем bin в PATH
    bin_path = os.path.join(venv_path, 'bin')
    if os.path.exists(bin_path):
        os.environ['PATH'] = bin_path + os.pathsep + os.environ.get('PATH', '')
        print(f"Added bin to PATH: {bin_path}")

def main():
    setup_venv()
    
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