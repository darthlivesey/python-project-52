#!/usr/bin/env python
import os
import sys
import subprocess
from pathlib import Path


main_manage = Path(__file__).resolve().parent / 'src' / 'manage.py'

if not main_manage.exists():
    sys.stderr.write(f"Error: Main manage.py not found at {main_manage}\n")
    sys.exit(1)

try:
    cmd = [sys.executable, str(main_manage)] + sys.argv[1:]
    subprocess.run(cmd, check=True)
except subprocess.CalledProcessError as e:
    sys.exit(e.returncode)
