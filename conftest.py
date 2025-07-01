import os
import sys
import pytest
import django


@pytest.fixture(scope='session', autouse=True)
def setup_django():
    project_root = os.getcwd()


    paths_to_add = [
        project_root,
        os.path.join(project_root, 'code'),
        os.path.join(project_root, 'code', 'src'),
        os.path.join(project_root, 'code', 'task_manager'),
        os.path.join(project_root, 'src'),
        os.path.join(project_root, 'task_manager')
    ]

    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)

    print(f"Current working directory: {project_root}")
    print(f"sys.path: {sys.path}")
    print(f"Files in project root: {os.listdir(project_root)}")

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
    django.setup()
