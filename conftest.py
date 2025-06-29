import os
import sys
import django


TASK_MANAGER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'task_manager')
if TASK_MANAGER_PATH not in sys.path:
    sys.path.insert(0, TASK_MANAGER_PATH)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
django.setup()


print("="*80)
print(f"Current directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")
print(f"Python path: {sys.path}")
print(f"task_manager exists: {os.path.exists('task_manager')}")
print(f"src exists: {os.path.exists('src')}")
print("="*80)
