#!/usr/bin/env python
import os
import sys
from pathlib import Path


VENV_PATH = Path('/project/.venv/bin/activate_this.py')
if VENV_PATH.exists():
    with open(VENV_PATH, 'r') as f:
        code = compile(f.read(), VENV_PATH, 'exec')
        exec(code, {'__file__': str(VENV_PATH)})

SRC_MANAGE = Path(__file__).parent / 'src' / 'manage.py'
if not SRC_MANAGE.exists():
    sys.exit(f"Error: Main manage.py not found at {SRC_MANAGE}")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
sys.argv.insert(0, str(SRC_MANAGE))
exec(open(SRC_MANAGE).read(), {'__name__': '__main__', '__file__': SRC_MANAGE})
