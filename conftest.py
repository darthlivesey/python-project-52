import os
import sys
import django


print("="*80)
print("BEFORE SETUP:")
print(f"Current directory: {os.getcwd()}")
print(f"Files: {os.listdir('.')}")
print(f"Python path: {sys.path}")
print(f"task_manager exists: {os.path.exists('task_manager')}")
print("="*80)


TASK_MANAGER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'task_manager')
if TASK_MANAGER_PATH not in sys.path:
    sys.path.insert(0, TASK_MANAGER_PATH)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
django.setup()


print("="*80)
print("AFTER SETUP:")
print(f"Python path: {sys.path}")
try:
    import task_manager
    print("SUCCESS: task_manager imported successfully!")
except ImportError as e:
    print(f"ERROR importing task_manager: {e}")
print("="*80)
