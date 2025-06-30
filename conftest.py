import pytest
import os
import sys
import django

@pytest.fixture(scope='session', autouse=True)
def setup_django():
    project_root = os.getcwd()
    sys.path.insert(0, project_root)
    sys.path.insert(0, os.path.join(project_root, 'code'))
    sys.path.insert(0, os.path.join(project_root, 'code', 'src'))
    sys.path.insert(0, os.path.join(project_root, 'code', 'task_manager'))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
    django.setup()