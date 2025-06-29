import os
import sys
import django


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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
